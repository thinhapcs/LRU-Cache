import logging
import grpc
import path
import sys
import time

# directory reach
directory = path.Path(__file__).abspath()

# setting path
sys.path.append(directory.parent.parent)
sys.path.append(directory.parent.parent.parent.parent)

import lrucache_pb2
import lrucache_pb2_grpc
from read_file import read_all_image_urls_from_file


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    
    th1_path = 'TH1.txt'
    th2_path = 'TH2.txt'
    th3_path = 'TH3.txt'
    debug = 'debug.txt'
    
    urls = read_all_image_urls_from_file(th2_path)
    
    port = 9001
    print(f'Trying to connect to server with port {port} ...')
    
    
    with grpc.insecure_channel(f'localhost:{port}') as channel:
        start_time = time.time()
        
        stub = lrucache_pb2_grpc.DownloadImageStub(channel)
        for url in urls:
            # print(f'Client send a download image request to Server - {url}')
            response = stub.RequestDownloadImage(lrucache_pb2.ImageRequest(url=url))
            print(f'Greeter client received: {len(response.image)}')
    
        duration = time.time() - start_time
        print(f'Downloaded {len(urls)} images in {duration} seconds')

if __name__ == '__main__':
    logging.basicConfig()
    run()
