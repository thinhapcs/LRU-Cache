import requests
import multiprocessing
import time

from processing_lru_cache import LRUCache
from read_file import read_all_image_urls_from_file

session = None
RequestDownloadMutex = multiprocessing.Lock()
WriteMutex = multiprocessing.Lock()
ReadMutex = multiprocessing.Lock()
Writer = multiprocessing.Value
Reader = 0
EditCache = multiprocessing.Lock()

N = None
cache = None

from multiprocessing import Manager


def set_global_session():
    global session

    if not session:
        session = requests.Session()


def download(url):
    # print(f'Download URL: {url}')
    with session.get(url) as response:
        return response.content


def write_cache(key, value=None, sort=False):
    global Writer

    # print(f'Lock WriteMutex - {key}')
    WriteMutex.acquire()
    Writer += 1
    # print(f'Writer = {Writer} - {key}')
    if Writer == 1:
        # print(f'Lock RequestDownloadMutex - {key}')
        RequestDownloadMutex.acquire()
    # print(f'Unlock WriteMutex - {key}')
    WriteMutex.release()

    # print(f'Lock EditCache - {key}')
    EditCache.acquire()
    if sort or bool(cache.get(key)):
        # print(f'SortCache - {key}')
        cache.sort_cache(key)
    else:
        # print(f'Write Cache - {key}')
        cache.put(key, value)
    # print(f'Unlock EditCache - {key}')
    EditCache.release()

    # print(f'Lock WriteMutex - {key}')
    WriteMutex.acquire()
    Writer -= 1
    # print(f'Writer = {Writer} - {key}')
    if Writer == 0:
        # print(f'Unlock RequestDownloadMutex - {key}')
        RequestDownloadMutex.release()
    # print(f'Unlock WriteMutex - {key}')
    WriteMutex.release()


def request_download(url):
    global Reader

    # print(f'Lock RequestDownloadMutex - {url}')
    RequestDownloadMutex.acquire()
    # print(f'Lock ReadMutex - {url}')
    ReadMutex.acquire()
    Reader += 1
    # print(f'Reader = {Reader} - {url}')
    if Reader == 1:
        # print(f'Lock EditCache - {url}')
        EditCache.acquire()
    # print(f'Unlock ReadMutex - {url}')
    ReadMutex.release()
    # print(f'Unlock RequestDownloadMutex - {url}')
    RequestDownloadMutex.release()

    check_contains_key = cache.get(url)     # return node

    # print(f'Lock ReadMutex - {url}')
    ReadMutex.acquire()
    Reader -= 1
    # print(f'Reader = {Reader} - {url}')
    if Reader == 0:
        # print(f'Unlock EditCache - {url}')
        EditCache.release()
    # print(f'Unlock ReadMutex - {url}')
    ReadMutex.release()

    value = None

    if check_contains_key is None:
        value = download(url)

    write_cache(url, value, bool(check_contains_key))


def download_all_images():
    global N
    global cache

    TH1_path = '../../data2/TH1.txt'
    TH2_path = '../../data2/TH2.txt'
    TH3_path = '../../data2/TH3.txt'
    TH4_path = '../../data2/TH4.txt'
    TH5_path = '../../data2/TH5.txt'
    debug = 'debug.txt'
    urls = read_all_image_urls_from_file(TH3_path)

    if urls:
        N = len(urls)
        cache = LRUCache(int(N/10))

    with multiprocessing.Pool(12, initializer=set_global_session) as pool:
        pool.map(request_download, urls)


if __name__ == '__main__':
    start_time = time.time()
    download_all_images()
    duration = time.time() - start_time
    print(f'Downloaded {N} images in {duration} seconds')

# Multithread xài threading:

# TH1: All URLs difference - Runtime: 50.6492338180542 seconds

# TH2: First 100 URLs difference (store in cache),
#   Remain 900 URLs are duplicated from 100 URLs first
#       90% hit in cache
#       Runtime: 30.89967179298401 seconds

# TH3: First 100 URLS difference (store in cache),
#   400 URLs behind are duplicated from first 100 URLs,
#   500 URLS remain are difference.
#       40% hit in cache
#       Runtime: 41.30361223220825 seconds
