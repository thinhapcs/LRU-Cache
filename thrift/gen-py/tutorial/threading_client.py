 # client.py
# from thrift import Thrift
import time
import threading
import concurrent.futures

from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from DownloadImageService import *
from read_file import read_all_image_urls_from_file

def download_images(urls, download_image):
        with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
                executor.map(download_image, urls)

if __name__ == '__main__':
    transport = TSocket.TSocket('localhost', 8000)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Client(protocol)
    
    th1_path = '../../../data2/TH1.txt'
    th2_path = '../../../data2/TH2.txt'
    th3_path = '../../../data2/TH3.txt'
    debug = '../../../debug.txt'
    
    urls = read_all_image_urls_from_file(th3_path)
    
    transport.open()
    start_time = time.time()
    
    download_images(urls, client.download_image)
    
    duration = time.time() - start_time
    print(f'Downloaded {len(urls)} images in {duration} seconds')
    transport.close()
    
'''
TH1: 107.83436155319214 seconds
TH2: 7.318430423736572 seconds
TH3: 66.03992128372192 seconds
'''
        