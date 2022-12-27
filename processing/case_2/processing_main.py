import threading

import requests
import concurrent.futures
import multiprocessing
import time
import string
import random

from processing_lru_cache import LRUCache
from read_file import read_all_image_urls_from_file

cache = None
thread_local = None
RequestDownloadMutex = None
WriteMutex = None
ReadMutex = None
Writer = None
Reader = None

CPU = 12
Threads = 16


def set_global_variables(urls):
    global cache
    global thread_local
    global RequestDownloadMutex
    global WriteMutex
    global ReadMutex
    global Writer
    global Reader

    process = multiprocessing.current_process()
    # print(f'Setup global variables - {process.name}')

    if not thread_local:
        thread_local = threading.local()
    if not cache:
        name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        cache = LRUCache(int(len(urls)/CPU*10), name)
    if not RequestDownloadMutex:
        RequestDownloadMutex = threading.Lock()
    if not WriteMutex:
        WriteMutex = threading.Lock()
    if not ReadMutex:
        ReadMutex = threading.Lock()
    if not Writer:
        Writer = 0
    if not Reader:
        Reader = 0
    if not cache.lock:
        cache.lock = threading.Lock()


def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def download(url):
    # print(f'Download URL: {url}')
    session = get_session()
    with session.get(url) as response:
        return response.content


def write_cache(key, value=None, sort=False):
    global Writer

    process = multiprocessing.current_process()

    # print(f'Lock WriteMutex - {process.name}')
    WriteMutex.acquire()
    Writer += 1
    # print(f'Writer = {Writer} - {process.name}')
    if Writer == 1:
        # print(f'Lock RequestDownloadMutex - {process.name}')
        RequestDownloadMutex.acquire()
    # print(f'Unlock WriteMutex - {process.name}')
    WriteMutex.release()

    # print(f'Lock EditCache - {process.name}')
    cache.lock.acquire()
    if sort or bool(cache.get(key)):
        # print(f'Sort to cache - {cache.name} in {multiprocessing.current_process().name}')
        cache.sort_cache(key)
    else:
        # print(f'Write to cache - {cache.name} in {multiprocessing.current_process().name}')
        cache.put(key, value)
    # print(f'Unlock EditCache - {process.name}')
    cache.lock.release()

    # print(f'Lock WriteMutex - {process.name}')
    WriteMutex.acquire()
    Writer -= 1
    # print(f'Writer = {Writer} - {process.name}')
    if Writer == 0:
        # print(f'Unlock RequestDownloadMutex - {process.name}')
        RequestDownloadMutex.release()
    # print(f'Unlock WriteMutex - {process.name}')
    WriteMutex.release()


def request_download(url):
    process = multiprocessing.current_process()
    # print(f'Process - {process.name} and Cache - {cache.name}')

    global Reader

    # print(f'Lock RequestDownload - {process.name}')
    RequestDownloadMutex.acquire()
    # print(f'Lock ReadMutex - {process.name}')
    ReadMutex.acquire()
    Reader += 1
    # print(f'Reader = {Reader} - {process.name}')
    if Reader == 1:
        # print(f'Lock ReadMutex - {process.name}')
        cache.lock.acquire()
    # print(f'Unlock ReadMutex - {process.name}')
    ReadMutex.release()
    # print(f'Unlock RequestDownloadMutex - {process.name}')
    RequestDownloadMutex.release()

    check_contains_key = cache.get(url)  # return node

    # print(f'Lock ReadMutex - {process.name}')
    ReadMutex.acquire()
    Reader -= 1
    # print(f'Reader = {Reader} - {process.name}')
    if Reader == 0:
        # print(f'Unlock EditCache - {process.name}')
        cache.lock.release()
    # print(f'Unlock ReadMutex - {process.name}')
    ReadMutex.release()

    value = None

    if not check_contains_key:
        # print(f'Download url - {process.name}')
        value = download(url)

    write_cache(url, value, bool(check_contains_key))


def request_download_many_images(urls):
    with concurrent.futures.ThreadPoolExecutor(max_workers=Threads) as executor:
        executor.map(request_download, urls)


def download_all_images():
    TH1_path = '../../data2/TH1.txt'
    TH2_path = '../../data2/TH2.txt'
    TH3_path = '../../data2/TH3.txt'
    TH4_path = '../../data2/TH4.txt'
    TH5_path = '../../data2/TH5.txt'
    debug = '../../debug.txt'
    urls = read_all_image_urls_from_file(TH5_path)
    tmp_urls = urls
    list_urls = []
    unit = int(len(urls)/(CPU-1))
    while True:
        list_urls.append(urls[:unit])
        urls = urls[unit:]
        if len(urls) <= unit:
            list_urls.append(urls)
            break

    with multiprocessing.Pool(CPU, initializer=set_global_variables, initargs=(tmp_urls,)) as pool:
        pool.map(request_download_many_images, list_urls)


if __name__ == '__main__':
    start_time = time.time()
    download_all_images()
    duration = time.time() - start_time
    print(f'Downloaded images in {duration} seconds')

# Multiprocessing Case 1:

# TH1: All URLs difference - Runtime: 64.86879992485046 seconds

# TH2: First 100 URLs difference (store in cache),
#   Remain 900 URLs are duplicated from 100 URLs first
#       90% hit in cache
#       Runtime: 61.541645526885986 seconds

# TH3: First 100 URLS difference (store in cache),
#   400 URLs behind are duplicated from first 100 URLs,
#   500 URLS remain are difference.
#       40% hit in cache
#       Runtime: 62.9975152015686 seconds

# TH4: 22.748013019561768 seconds

# TH5: 34.97758340835571 seconds
