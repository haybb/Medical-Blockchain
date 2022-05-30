"""
Here are defined all the functions and classes used to work with network
"""


import files

import socket, pickle, logging, tqdm
from threading import Thread
import os.path as path
from os import makedirs


log = logging.getLogger(__name__)



class ClientSocket(Thread):
    """
    Represents a client-side socket.
    For the parameters, check the socket.socket parameters.
    """
    def __init__(self,
                 socketFamily=socket.AF_INET,
                 socketType=socket.SOCK_STREAM,
                 socketProto=0,
                 socketfileno=None,
                 threadGroup=None,
                 threadTarget=None,
                 threadName=None,
                 threadArgs=list(),
                 threadKwargs=dict(),
                 threadDaemon=None):
        super().__init__(group=threadGroup, target=threadTarget, name=threadName, daemon=threadDaemon)
        self._args = threadArgs
        self._kwargs = threadKwargs
        self._socketInfos = (socketFamily, socketType, socketProto, socketfileno)
        self._socket = socket.socket(*self._socketInfos)
        self._connected = False
    

    def _connect(self, address: tuple[str, int]) -> None:
        """
        Connects to an address

        :param address: the address to connect to, first ipv4, second port
        :type address: tuple[str, int]
        """
        log.info("Connecting client to %s:%i...", address[0], address[1])
        self._socket.connect(address)
        self._connected = True
        log.info("Client connected")
    

    def _close(self) -> None:
        """
        Closes the socket
        """
        log.info("Closing connexion...")
        # self._socket.sendall(b"*CLOSING*")
        self._socket.close()
        self._connected = False
        self._socket = socket.socket(*self._socketInfos)
        log.info("Client connexion closed")
    

    def run(self) -> None:
        filePath = self._kwargs["filePath"]
        address = self._kwargs["address"]
        bufferSize = self._kwargs["bufferSize"]
        
        fileInBytes = files.loadFile(filePath, False, inBytes=True)

        self._connect(address)

        fileName, fileExtension = path.split(filePath)[1].split(".")
        toSend = f"{fileName}*SEPARATOR*{fileExtension}"
        log.debug(f"sending : {toSend}")
        self._socket.sendall(toSend.encode())
        log.debug("sent")
        log.debug("sending stop")
        self._socket.sendall(b'*STOP*')
        log.debug("sent")

        log.debug("waiting for confirmation")
        received = b''
        while received.lower() != b"file ok":
            received = self._socket.recv(bufferSize)
        log.debug(f"received : {received.decode()}")

        progressBar = tqdm.tqdm(range(len(fileInBytes)), f"Sending {fileName} to {address[0]}:{address[1]}", unit="b", unit_scale=True, unit_divisor=1024)

        log.debug("sending file")
        i=0
        while (i+1)*bufferSize < len(fileInBytes):
            self._socket.sendall(fileInBytes[i*bufferSize : (i+1)*bufferSize])
            i += 1
            progressBar.update(bufferSize)
        self._socket.sendall(fileInBytes[i*bufferSize : ])
        progressBar.update(len(fileInBytes) - i*bufferSize)
        log.debug("file sent")

        self._close()


    def sendFile(self, filePath: str, address: tuple[str, int], bufferSize=2048) -> None:
        """
        Send a file to a specific address

        :param str filePath: the path to the file to send
        :param address: the address to send the file to
        :type address: tuple[str, int]
        :param int bufferSize: the size of the buffer, default 2048
        """
        if self._connected: raise socket.error("the socket is already connected to an address")
        self._kwargs |= {
            "filePath" : filePath,
            "address" : address,
            "bufferSize" : bufferSize
        }
        self.start()



class ServerSocket(Thread):
    """
    Represents a client-side socket.
    For the parameters not mentionned here, check the socket.socket parameters.
    
    :param address: the address of the socket, first the ipv4, second the port
    :type address: tuple[str, int]
    """
    def __init__(self,
                 address: tuple[str, int],
                 socketFamily=socket.AF_INET,
                 socketType=socket.SOCK_STREAM,
                 socketProto=0,
                 socketfileno=None,
                 threadGroup=None,
                 threadTarget=None,
                 threadName=None,
                 threadArgs=list(),
                 threadKwargs=dict(),
                 threadDaemon=None):
        super().__init__(group=threadGroup, target=threadTarget, name=threadName, daemon=threadDaemon)
        self._address = address
        self._args = threadArgs
        self._kwargs = threadKwargs
        self._socketInfos = (socketFamily, socketType, socketProto, socketfileno)
        self._socket = socket.socket(*self._socketInfos)
        self._connected = False
    

    def _open(self) -> None:
        """
        Opens the connexion of the socket on the address given in the initialization
        """
        log.info("Opening the server connexion...")
        self._socket.bind(self._address)
        self._socket.listen(1)
        self._connected = True
        log.info("Server connexion opened. Listening on %s:%i", self._address[0], self._address[1])


    def _close(self) -> None:
        """
        Closes the socket
        """
        log.info("Closing connexion...")
        self._socket.close()
        self._connected = False
        self._socket = socket.socket(*self._socketInfos)
        log.info("Server connexion closed")
    
    
    def _accept(self) -> None:
        """
        Accepts a connexion
        """
        conn, addr = self._socket.accept()
        self._connectedSocket = (conn, addr)
        log.info("Accepted connexion from %s:%i", {addr[0]}, {addr[1]})


    def _receiveData(self) -> bytes:
        newData = self._connectedSocket[0].recv(self._kwargs["bufferSize"])
        allData = newData
        while newData != b'' and allData[-6:] != b'*STOP*':
            newData = self._connectedSocket[0].recv(self._kwargs["bufferSize"])
            allData += newData
        if allData[-6:] == b"*STOP*": return allData[:-6]
        else: return allData


    def run(self) -> None:
        self._open()
        self._accept()

        receivedFileData = self._receiveData().decode()
        fileName, fileExtension = receivedFileData.split("*SEPARATOR*")
        log.info("File received (data) : %s.%s", fileName, fileExtension)

        log.debug("sending : file ok")
        self._connectedSocket[0].sendall(b"file ok")
        log.debug("sent")

        log.debug("receiving file")
        receivedFile = self._receiveData()
        log.debug("file received")
        self._close()

        filePath = path.join(self._kwargs["downloadsPath"], "%s.%s" % (fileName, fileExtension))
        files.saveFile(receivedFile, filePath, binary=True)

        self._close()
        
    

    def receiveFile(self, downloadsPath=None, bufferSize=2048) -> None:
        """
        Receives a file

        :param str downloadsPath: the path to where the file has to be saved
        :param int bufferSize: the size of the buffer, default 2048
        """
        if self._connected: raise socket.error("the socket is already listening an address")
        if not downloadsPath:
            downloadsPath = "downloads"
        if not path.isdir(downloadsPath):
            makedirs(downloadsPath)
        self._kwargs |= {
            "downloadsPath": downloadsPath,
            "bufferSize": bufferSize
        }
        self.start()







# =======================================================================
# =======================================================================
#           THIS PART OF THE CODE SHOULD ONLY BE USED FOR TESTS
# =======================================================================
# =======================================================================
BUFFER_SIZE = 2048
host, port = ("192.168.1.71", 8088)

def server():
    serverSocket = ServerSocket((host, port))
    serverSocket.open()

    serverSocket.accept()
    dataReceived = serverSocket.recv(BUFFER_SIZE)
    log.info(f"Server received \"{dataReceived}\"")
    serverSocket.close()



def client(data):
    clientSocket = ClientSocket()
    clientSocket.connect((host, port))
    print(f"Sending \"{data}\"")
    clientSocket.sendall(data)
    print("Message sent")
    clientSocket.close()



if __name__ == "__main__":
    from data_manager import initializeLogger
    initializeLogger()

    add = ("192.168.1.71", 8088)
    fp = "C:\\Users\\aubin\\Documents\\foo.png"

    if socket.gethostname() == "LAPTOP-AUBIN":
        serverSocket = ServerSocket(add)
        serverSocket.receiveFile()
    else:
        clientSocket = ClientSocket()
        clientSocket.sendFile(fp, add)

    # clientSocket = ClientSocket()
    # clientSocket.sendFile(filePath, address)
