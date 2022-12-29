 # client.py

import time

from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from DownloadImageService import *
from read_file import read_all_image_urls_from_file

if __name__ == '__main__':
    transport = TSocket.TSocket('localhost', 8000)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Client(protocol)
    
    th1_path = '../../../data2/TH1.txt'
    th2_path = '../../../data2/TH2.txt'
    th3_path = '../../../data2/TH3.txt'
    
    urls = read_all_image_urls_from_file(th2_path)
    
    transport.open()
    start_time = time.time()
    
    for url in urls:
        # print(f'Client send a download image request to Server - {url}')
        result = client.download_image(url)
        # print(f'Response from Server - {result}')
    
    duration = time.time() - start_time
    print(f'Downloaded {len(urls)} images in {duration} seconds')
    transport.close()
    
'''
TH1: 107.83436155319214 seconds
TH2: 7.318430423736572 seconds
TH3: 66.03992128372192 seconds
'''
        