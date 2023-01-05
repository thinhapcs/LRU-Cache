# server.py
import path
import sys

# directory reach
directory = path.Path(__file__).abspath()

# setting path
sys.path.append(directory.parent.parent)

from DownloadImageService import *

from DownloadImageHandler import DownloadImageHandler                    
from thrift.transport import TSocket                                        
from thrift.server import TNonblockingServer                                      
                                                                            
                                                                            
if __name__ == '__main__':       
    try:                                           
        handler = DownloadImageHandler()                                       
        processor =  Processor(handler)                                         
        socket = TSocket.TServerSocket(host='127.0.0.1', port=8000)          
        
        server = TNonblockingServer.TNonblockingServer(processor, socket, threads=10)
        
        print("Server has started\nListening...")
        server.serve()
    except KeyboardInterrupt:
        print('Server done !!!')
    