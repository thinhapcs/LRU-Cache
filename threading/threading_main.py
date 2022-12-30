import concurrent.futures
import requests
import threading
import time

from threading_lru_cache import LRUCache
from read_file import read_all_image_urls_from_file


thread_local = threading.local()

N = 0
cache = None


def get_session():
    if not hasattr(thread_local, 'session'):
        thread_local.session = requests.Session()
    return thread_local.session


def request_download(url):
    session = get_session()
    cache.download_image(session, url)


def download_all_images():
    global N
    global cache

    th1_path = '../data2/TH1.txt'
    th2_path = '../data2/TH2.txt'
    th3_path = '../data2/TH3.txt'
    debug = '../debug.txt'
    urls = read_all_image_urls_from_file(th1_path)

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

'''
TH1:
    Worker = 16 - 38.628791093826294 seconds
    Worker = 50 - 46.8055784702301 seconds
    Worker = 200 - 29.11229705810547 seconds
    Worker = 500 - 100.8307113647461 seconds
    Worker = 1000 - 131.70369815826416 seconds
    
TH2:
    Worker = 16 - 5.296700716018677 seconds
    Worker = 50 - 10.160197257995605 seconds
    Worker = 200 - 61.19453048706055 seconds
    Worker = 500 - 131.2691867351532 seconds
    Worker = 1000 - 132.1524956226349 seconds
'''

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
