# server.py
import path
import sys

# directory reach
directory = path.Path(__file__).abspath()

# setting path
sys.path.append(directory.parent.parent)

from DownloadImageService import *

from ThreadingDownloadImageHandler import DownloadImageHandler                    
from thrift.transport import TSocket                                        
from thrift.transport import TTransport                                     
from thrift.protocol import TBinaryProtocol                                 
from thrift.server import TServer                                           
                                                                            
                                                                            
if __name__ == '__main__':       
    try:                                           
        handler = DownloadImageHandler()                                       
        processor =  Processor(handler)                                         
        socket = TSocket.TServerSocket(host='127.0.0.1', port=8000)          
        transport = TTransport.TBufferedTransportFactory()                       
        protocol = TBinaryProtocol.TBinaryProtocolFactory()
        daemon = False               
        
        # server = TServer.TSimpleServer(processor, socket, transport, protocol)                                                                        
        # server = TServer.TThreadedServer(processor, socket, transport, protocol, daemon=daemon)
        server = TServer.TThreadPoolServer(processor, socket, transport, protocol, daemon=daemon)
        server.threads = 16
        
        print("Server has started\nListening...")
        server.serve()
    except KeyboardInterrupt:
        print('Server done !!!')
    