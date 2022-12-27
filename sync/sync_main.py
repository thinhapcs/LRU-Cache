import requests
import time

from sync_lru_cache import LRUCache
from read_file import read_all_image_urls_from_file

N = 0
cache = None


def download(url, session):
    with session.get(url) as response:
        # print(f"Read {len(response.content)} from {url}")
        return response.content


def write_cache(key, value=None, sort=False):
    if sort:
        cache.sort_cache(key)
    else:
        cache.put(key, value)


def request_download(url, session):
    check_contains_key = cache.get(url)     # return node
    # if check_contains_key:
        # print(f'Get image with: {check_contains_key.key}')

    value = None

    if not check_contains_key:
        value = download(url, session)
        # print(f'Download image of url: {url}')

    write_cache(url, value, bool(check_contains_key))


def download_all_images():
    global N
    global cache

    TH1_path = '../data2/TH1.txt'
    TH2_path = '../data2/TH2.txt'
    TH3_path = '../data2/TH3.txt'
    TH4_path = '../data2/TH4.txt'
    TH5_path = '../data2/TH5.txt'
    urls = read_all_image_urls_from_file(TH4_path)

    if urls:
        N = len(urls)
        cache = LRUCache(int(N/10))

    with requests.Session() as session:
        for url in urls:
            request_download(url, session)


if __name__ == '__main__':
    start_time = time.time()
    download_all_images()
    duration = time.time() - start_time
    print(f'Downloaded {N} images in {duration} seconds')

# Single Thread

# Runtime TH1: 57.78139901161194 seconds - 72.24757146835327 seconds
# Runtime TH2: 6.764083385467529 seconds
# Runtime TH3: 39.71559929847717 seconds
# Runtime TH4: 0.36130475997924805 seconds
# Runtime TH5: 33.7780179977417 seconds

# Runtime of 1000 images difference: 974.2457575798035 seconds
# Runtime of 200 images difference: 135.48971462249756 seconds
# Runtime of 200 images - 20 in cache and 180 duplicated: 12.38429307937622 seconds
# Runtime of 200 images - 20 in cache and 80 duplicated, 100 difference: 88.40535521507263 seconds
