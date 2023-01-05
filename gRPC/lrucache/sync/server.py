import concurrent.futures
import grpc
import logging
import requests
import path
import sys

# directory reach
directory = path.Path(__file__).abspath()

# setting path
sys.path.append(directory.parent.parent)

from lru_cache import LRUCache
import lrucache_pb2
import lrucache_pb2_grpc


class DownloadImage(lrucache_pb2_grpc.DownloadImageServicer):
    
    def __init__(self) -> None:
        self.cache = LRUCache(100)
        self.session = requests.Session()
    
    def RequestDownloadImage(self, request, context):
        print(f'Server has received a download image request from url: {request.url}')
        image = self.cache.download_image(self.session, request.url)
        return lrucache_pb2.ImageResponse(image=image)


def serve():
    port = 9001
    max_workers = 1
    
    pool = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
    server = grpc.server(pool)
    lrucache_pb2_grpc.add_DownloadImageServicer_to_server(DownloadImage(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f'Server started, listening on {port}')
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()