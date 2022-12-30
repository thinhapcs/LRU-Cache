 # client.py
import time
import path
import sys

# directory reach
directory = path.Path(__file__).abspath()

# setting path
sys.path.append(directory.parent.parent)

import concurrent.futures

from DownloadImageService import *
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from thrift.transport.TTransport import TTransportException
from read_file import read_all_image_urls_from_file

def download_image(url):
    transport = TSocket.TSocket('localhost', 8000)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = Client(protocol)
    
    try:
        transport.open()
    
        image = client.download_image(url)
        print('Received response from Server with data: ', len(image))
        
        transport.close()
    except TTransportException:
        print('Server close connection !!!')

if __name__ == '__main__':
    
    
    th1_path = '../../../../data2/TH1.txt'
    th2_path = '../../../../data2/TH2.txt'
    th3_path = '../../../../data2/TH3.txt'
    
    urls = read_all_image_urls_from_file(th1_path)
    
    # tasks = []
    # for url in urls:
    #     tasks.append(threading.Thread(target=download_image, args=(url,)))        
    
    start_time = time.time()
    
    # for task in tasks:
    #     task.start()
        
    # for task in tasks:
    #     task.join()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        executor.map(download_image, urls)
    
    duration = time.time() - start_time
    print(f'Downloaded {len(urls)} images in {duration} seconds')
    
'''
TH1:    
        Runtime: 50.83654594421387 seconds
        Hit: 0.0%
        Miss: 100.0%
TH2:
        Runtime: 5.425833225250244 seconds
        Hit: 90.0%
        Miss: 10.0%
TH3: 
        Runtime: 28.201115608215332 seconds
        Hit: 39.9%
        Miss: 60.1%
'''
        