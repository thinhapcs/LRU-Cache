import requests
import multiprocessing
import time
import string
import random

from processing_lru_cache import LRUCache
from read_file import read_all_image_urls_from_file

session = None
cache = None

CPU = 12


def set_global_variables(urls):
    global session
    global cache

    if not session:
        session = requests.Session()
    if not cache:
        name = ''.join(random.choice(string.ascii_letters) for _ in range(5))
        cache = LRUCache(int(len(urls)/CPU*10), name)


def download(url):
    # print(f'Download URL: {url}')
    with session.get(url) as response:
        return response.content


def write_cache(key, value=None, sort=False):
    if sort:
        # print(f'Sort to cache - {cache.name} in {multiprocessing.current_process().name}')
        cache.sort_cache(key)
    else:
        # print(f'Write to cache - {cache.name} in {multiprocessing.current_process().name}')
        cache.put(key, value)


def request_download(url):
    # process = multiprocessing.current_process()
    # print(process.name)
    # print(cache.name)

    check_contains_key = cache.get(url)  # return node

    value = None

    if not check_contains_key:
        value = download(url)

    write_cache(url, value, bool(check_contains_key))


def download_all_images():
    TH1_path = '../../data2/TH1.txt'
    TH2_path = '../../data2/TH2.txt'
    TH3_path = '../../data2/TH3.txt'
    TH4_path = '../../data2/TH4.txt'
    TH5_path = '../../data2/TH5.txt'
    debug = '../../debug.txt'
    urls = read_all_image_urls_from_file(TH5_path)

    with multiprocessing.Pool(CPU, initializer=set_global_variables, initargs=(urls,)) as pool:
        pool.map(request_download, urls)


if __name__ == '__main__':
    start_time = time.time()
    download_all_images()
    duration = time.time() - start_time
    print(f'Downloaded images in {duration} seconds')

# Multiprocessing Case 1:

# TH1: All URLs difference - Runtime: 40.20072674751282 seconds

# TH2: First 100 URLs difference (store in cache),
#   Remain 900 URLs are duplicated from 100 URLs first
#       90% hit in cache
#       Runtime: 26.841148853302002 seconds

# TH3: First 100 URLS difference (store in cache),
#   400 URLs behind are duplicated from first 100 URLs,
#   500 URLS remain are difference.
#       40% hit in cache
#       Runtime: 36.88100552558899 seconds

# TH4: Runtime: 4.748173475265503 seconds

# TH5: Runtime: 21.432844161987305 seconds
