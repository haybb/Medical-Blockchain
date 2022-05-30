"""
The program that will be started by the server.

By running this program, you run the entire one.
You can give as arguments the paths to the data directory
"""



from data_manager import DataManager, initializeLogger, getDirectories
from network import ClientSocket, ServerSocket
import files, socket

import os.path as path
import logging, tqdm, time

log = logging.getLogger(__name__)



class Server:
    """
    A Server class represents an instance of a server.
    Only one should run at the same time.
    """
    def __init__(self, dataDirPath="") -> None:
        """
        :param str dataDirPath: the path to the directory where the data will be stored
        """
        log.info("Starting the server...")
        self._dataManager = DataManager(dataDirPath)
        # self._serverSocket = ServerSocket(self._dataManager.config["server-address"])
        self._clientSocket = ClientSocket()
        log.info("Server started")
    

    def _sendToBlockchain(self, *argv, **kwargs) -> None:
        """
        Send data to the blockchain
        This function still have to be written - waiting for Hugo
        """
        log.debug("This data has to be sent to the blockchain:\n    - %s\n    - %s", argv, kwargs)
        files.sendToBlockchain(argv, kwargs)

    
    def _getFromBlockchain(self, *argv, **kwargs):
        """
        Get data from the blockchain
        This function still have to be written - waiting for Hugo
        """
        log.debug("This data has to be got from the blockchain:\n    - %s\n    - %s", argv, kwargs)
        files.getFromBlockchain(kwargs)


    def _sendFile(self, filePath: str, address: tuple[str, int]) -> None:
        """
        Send a file to a specific address

        :param str filePath: the path to the file to send
        :param address: the address to send the file to
        :type address: tuple[str, int]
        """
        bufsize = self._dataManager.config["buffer-size"]
        fileInBytes = files.loadFile(filePath, False, inBytes=True)
        n = len(fileInBytes)

        s = socket.socket()
        s.connect(address)
        log.info(f"connected to {address[0]}:{address[1]}")

        fileName, fileExtension = path.split(filePath)[1].split(".")
        toSend = f"{fileName}*SEPARATOR*{fileExtension}"
        log.debug(f"sending : {toSend}")
        s.sendall(toSend.encode())
        log.debug("sent")
        log.debug("sending stop")
        s.sendall(b'*STOP*')
        log.debug("sent")

        log.debug("waiting for confirmation")
        received = b''
        while received.lower() != b"file ok":
            log.debug("-------")
            received += s.recv(bufsize)
        log.debug(f"received : {received.decode()}")

        progressBar = tqdm.tqdm(range(n), f"Sending {fileName} to {address[0]}:{address[1]}", unit="b", unit_scale=True, unit_divisor=1024)

        log.debug("sending file")
        i=0
        while (i+1)*bufsize < n:
            s.sendall(fileInBytes[i*bufsize : (i+1)*bufsize])
            i += 1
            progressBar.update(bufsize)
        s.sendall(fileInBytes[i*bufsize : ])
        progressBar.update(n - i*bufsize)
        log.debug("file sent")


    def _sendFile(self, filePath: str, address: tuple[str, int]) -> None:
        """
        Send a file to a specific address

        :param str filePath: the path to the file to send
        :param address: the address to send the file to
        :type address: tuple[str, int]
        """
        bufferSize = self._dataManager.config["buffer-size"]
        fileInBytes = files.loadFile(filePath, False, inBytes=True)
        self._clientSocket.sendFile(filePath, address)

    



if __name__ == "__main__":
    ###### DO NOT MODIFY THESE LINES ######
    import sys
    allDirs = getDirectories(sys.argv)
    dataPath = allDirs[0] if len(allDirs)>=1 else ""
    initializeLogger(dataPath)
    ###### DO NOT MODIFY THESE LINES ######

    # You can modify the next ones
    address = ("192.168.1.71", 8088)
    filePath = path.join("C:", "Users", "Aubin", "Documents", "foo.png")
    
    server = Server()
    server._sendFile(filePath, address)
