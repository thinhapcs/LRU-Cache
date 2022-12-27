import asyncio
import time
import aiohttp

from sync.sync_lru_cache import LRUCache
from read_file import read_all_image_urls_from_file


RequestDownloadMutex = asyncio.Lock()
WriteMutex = asyncio.Lock()
ReadMutex = asyncio.Lock()
Writer = 0
Reader = 0
EditCache = asyncio.Lock()

N = 0
cache = None


async def write_cache(key, value=None, sort=False):
    global Writer

    print('Write cacheeeeeeeeee')

    await WriteMutex.acquire()
    print(f'Lock WriteMutex - {key}')
    Writer += 1
    if Writer == 1:
        print(f'Lock RequestDownload - {key}')
        await RequestDownloadMutex.acquire()
    print(f'Lock WriteMutex - {key}')
    WriteMutex.release()

    await EditCache.acquire()
    print(f'Lock EditCache - {key}')
    if sort or bool(cache.get(key)):
        cache.sort_cache(key)
    else:
        cache.put(key, value)
    print(f'Unlock EditCache - {key}')
    EditCache.release()

    await WriteMutex.acquire()
    print(f'Lock WriteMutex - {key}')
    Writer -= 1
    if Writer == 0:
        print(f'Unlock RequestDownload - {key}')
        RequestDownloadMutex.release()
    print(f'Unlock WriteMutex - {key}')
    WriteMutex.release()


async def download_site(session, url):
    print(f'Go downloadddd - {url}')
    response = await session.get(url)
    return response.content


async def request_download(url):
    global Reader

    await RequestDownloadMutex.acquire()
    print(f'Lock RequestDownload - {url}')
    await ReadMutex.acquire()
    print(f'Lock ReadMutex - {url}')
    Reader += 1
    if Reader == 1:
        print(f'Lock EditCache - {url}')
        await EditCache.acquire()
    print(f'Unlock ReadMutex - {url}')
    ReadMutex.release()
    print(f'Unlock RequestDownload - {url}')
    RequestDownloadMutex.release()

    check_contains_key = cache.get(url)     # return node

    await ReadMutex.acquire()
    print(f'Lock ReadMutex - {url}')
    Reader -= 1
    if Reader == 0:
        print(f'Unlock EditCache - {url}')
        EditCache.release()
    print(f'Unlock ReadMutex - {url}')
    ReadMutex.release()

    value = None

    if not check_contains_key:
        async with aiohttp.ClientSession() as session:
            value = await download_site(session, url)

    await write_cache(url, value, bool(check_contains_key))


async def download_all_images():
    global N
    global cache

    TH1_path = '../data2/TH1.txt'
    TH2_path = '../data2/TH2.txt'
    TH3_path = '../data2/TH3.txt'
    TH4_path = '../data2/TH4.txt'
    TH5_path = '../data2/TH5.txt'
    debug = 'debug.txt'
    urls = read_all_image_urls_from_file(debug)

    if urls:
        N = len(urls)
        cache = LRUCache(int(N/10))

    tasks = []
    for url in urls:
        task = asyncio.ensure_future(request_download(url))
        tasks.append(task)
    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == '__main__':
    start_time = time.time()
    asyncio.run(download_all_images())
    duration = time.time() - start_time
    print(f'Downloaded {N} images in {duration} seconds')

# Multi-thread xài asyncio:

# TH1: All URLs difference - Runtime:

# TH2: First 100 URLs difference (store in cache),
#   Remain 900 URLs are duplicated from 100 URLs first
#       90% hit in cache
#       Runtime:

# TH3: First 100 URLS difference (store in cache),
#   400 URLs behind are duplicated from first 100 URLs,
#   500 URLS remain are difference.
#       40% hit in cache
#       Runtime:
