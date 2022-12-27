import concurrent.futures
import requests
import threading
import time

from threading_lru_cache import LRUCache
from read_file import read_all_image_urls_from_file


thread_local = threading.local()

RequestDownloadMutex = threading.Lock()
WriteMutex = threading.Lock()
ReadMutex = threading.Lock()
Writer = 0
Reader = 0
# EditCache = threading.Lock()

N = 0
cache = None


def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def download(url):
    session = get_session()
    with session.get(url) as response:
        return response.content


def write_cache(key, value=None, sort=False):
    global Writer

    WriteMutex.acquire()
    Writer += 1
    if Writer == 1:
        RequestDownloadMutex.acquire()
    WriteMutex.release()

    cache.lock.acquire()
    # cache.put(key, value)
    if sort or bool(cache.get(key)):
        cache.sort_cache(key)
    else:
        cache.put(key, value)
    cache.lock.release()

    WriteMutex.acquire()
    Writer -= 1
    if Writer == 0:
        RequestDownloadMutex.release()
    WriteMutex.release()


def request_download(url):
    global Reader

    RequestDownloadMutex.acquire()
    ReadMutex.acquire()
    Reader += 1
    if Reader == 1:
        cache.lock.acquire()
    ReadMutex.release()
    RequestDownloadMutex.release()

    check_contains_key = cache.get(url)     # return node

    ReadMutex.acquire()
    Reader -= 1
    if Reader == 0:
        cache.lock.release()
    ReadMutex.release()

    value = None

    if check_contains_key is None:
        value = download(url)

    write_cache(url, value, bool(check_contains_key))


def download_all_images():
    global N
    global cache

    TH1_path = '../data2/TH1.txt'
    TH2_path = '../data2/TH2.txt'
    TH3_path = '../data2/TH3.txt'
    TH4_path = '../data2/TH4.txt'
    TH5_path = '../data2/TH5.txt'
    debug = 'debug.txt'
    urls = read_all_image_urls_from_file(TH5_path)

    if urls:
        N = len(urls)
        cache = LRUCache(int(N/10))
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(request_download, urls)


if __name__ == '__main__':
    start_time = time.time()
    download_all_images()
    duration = time.time() - start_time
    print(f'Downloaded {N} images in {duration} seconds')

# Multithread xài threading:

# TH1: All URLs difference - Runtime: 39.14267134666443 seconds

# TH2: First 100 URLs difference (store in cache),
#   Remain 900 URLs are duplicated from 100 URLs first
#       90% hit in cache
#       Runtime: 3.8917996883392334 seconds

# TH3: First 100 URLS difference (store in cache),
#   400 URLs behind are duplicated from first 100 URLs,
#   500 URLS remain are difference.
#       40% hit in cache
#       Runtime: 24.78499960899353 seconds

# TH4: 1.9528326988220215 seconds

# TH5: 21.153886556625366 seconds
