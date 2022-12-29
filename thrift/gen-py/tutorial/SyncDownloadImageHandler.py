from DownloadImageService import *
import requests


def download(session, url):
    with session.get(url) as response:
        return response.content


class LinkedList:

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self.prev_node = None
        self.next_node = None

    def remove(self):
        if self.prev_node and self.next_node:
            prev_node = self.prev_node
            prev_node.next_node = self.next_node
            next_node = self.next_node
            next_node.prev_node = self.prev_node
        elif self.next_node is None and self.prev_node:
            prev_node = self.prev_node
            prev_node.next_node = None
        self.prev_node = None
        self.next_node = None

    def __del__(self):
        self.remove()


class LRUCache:

    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = dict()
        self.head_node = None
        self.tail_node = None

    def _insert_head(self, node):
        if self.head_node is None:
            self.head_node = node
            self.tail_node = node
            return
        old_head_node = self.head_node
        old_head_node.prev_node = node
        self.head_node = node
        node.next_node = old_head_node

    def _remove_tail(self):
        tail_node = self.tail_node
        self.tail_node = tail_node.prev_node
        self.cache.pop(tail_node.key)
        tail_node.remove()

    def _is_in_cache(self, key):
        return key in self.cache

    def _read_from_cache(self, key):
        return self.cache[key]

    def _write_to_cache(self, key, value):
        if len(self.cache) == self.capacity:
            self._remove_tail()
        node = LinkedList(key, value)
        self._insert_head(node)
        self.cache[key] = node

    def _sort_cache(self, key):
        if key == self.head_node.key:
            return
        node = self.cache[key]
        if key == self.tail_node.key:
            self.tail_node = self.tail_node.prev_node
        node.remove()
        self._insert_head(node)

    def _handle_cache(self, key, value):
        if self._is_in_cache(key):
            print('Sort')
            self._sort_cache(key)
        else:
            print('Write')
            self._write_to_cache(key, value)

    def download_image(self, session, url):
        # thread_name = threading.current_thread().name
        # print(thread_name)
        value = None
        if self._is_in_cache(url):
            value = self._read_from_cache(url).value

        if not value:
            value = download(session, url)

        self._handle_cache(url, value)
        
        return value


class DownloadImageHandler(Iface):
    def __init__(self) -> None:
        self.cache = LRUCache(100)
        self.session = requests.Session()
    
    def download_image(self, url):      
        print(f'Server has received a download image request from url: {url}')
        image = self.cache.download_image(self.session, url)
        return image