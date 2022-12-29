 # client.py
# from thrift import Thrift
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
    th2_path = '../data2/TH2.txt'
    th3_path = '../data2/TH3.txt'
    th4_path = '../data2/TH4.txt'
    th5_path = '../data2/TH5.txt'
    debug = '../debug.txt'
    
    urls = read_all_image_urls_from_file(th1_path)
    
    transport.open()
    for url in urls:
            print(f'Send download image request from {url} to server... ')
            result = client.download_image(url)
            print(f'Server has response. Result is {result}')
    transport.close()
        