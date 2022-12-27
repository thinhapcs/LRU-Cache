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

    def __init__(self, capacity, name):
        self.capacity = capacity
        self.cache = dict()
        self.head_node = None
        self.tail_node = None
        self.name = name

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

    def get(self, key):
        if self._is_in_cache(key):
            return self.cache[key]
        return None

    def put(self, key, value):
        if len(self.cache) == self.capacity:
            self._remove_tail()
        node = LinkedList(key, value)
        self._insert_head(node)
        self.cache[key] = node

    def sort_cache(self, key):
        if key == self.head_node.key:
            return
        node = self.cache[key]
        if key == self.tail_node.key:
            self.tail_node = self.tail_node.prev_node
        node.remove()
        self._insert_head(node)
