# server.py
import path
import sys

# directory reach
directory = path.Path(__file__).abspath()

# setting path
sys.path.append(directory.parent.parent)

from DownloadImageHandler import DownloadImageHandler                    
from thrift.transport import TSocket                                        
from thrift.transport import TTransport                                     
from thrift.protocol import TBinaryProtocol                                 
from thrift.server import TServer                                           
from DownloadImageService import *                                         
                                                                            
                                                                            
if __name__ == '__main__':                                                  
    handler = DownloadImageHandler()                                       
    processor =  Processor(handler)                                         
    socket = TSocket.TServerSocket(host='127.0.0.1', port=8000)          
    transport = TTransport.TBufferedTransportFactory()                       
    protocol = TBinaryProtocol.TBinaryProtocolFactory()                     
                                                                            
    server = TServer.TSimpleServer(processor, socket, transport, protocol)
    print("Server has started\nListening...")
    server.serve()
    