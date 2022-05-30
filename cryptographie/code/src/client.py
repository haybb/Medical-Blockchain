"""
The program that will be started by a client
"""

import files, encryption

import socket, logging
import os.path as path
from os import makedirs

from Crypto.PublicKey import RSA

log = logging.getLogger(__name__)


class Client:
    def __init__(self, address: tuple[str, int], bufsize=2048):
        self._address = address
        log.info("opening server")
        self._socket = socket.socket()
        self._socket.bind(self._address)
        if not path.isdir(path.join("data", "downloads")):
            makedirs(path.join("data", "downloads"))


    def _openConnexion(self) -> None:
        self._socket.listen(1)
        log.info(f"server started on {self._address[0]}:{self._address[1]}")
    

    def _closeConnexion(self) -> None:
        self._socket.close()
        log.info("server closed")


    def _receiveData(self, conn) -> bytes:
        newData = conn.recv(2048)
        allData = newData
        while newData != b'' and allData[-6:] != b'*STOP*':
            newData = conn.recv(2048)
            allData += newData
        if allData[-6:] == b"*STOP*": return allData[:-6]
        else: return allData
    

    def _receiveFile(self) -> None:
        self._openConnexion()
        conn, addr = self._socket.accept()
        log.info(f"connected to {addr[0]}:{addr[1]}")
        receivedFileData = self._receiveData(conn).decode()
        log.debug(f"received : {receivedFileData}")
        fileName, fileExtension = receivedFileData.split("*SEPARATOR*")

        log.debug("sending : file ok")
        conn.sendall(b"file ok")
        log.debug("sent")

        log.debug("receiving file")
        receivedFile = self._receiveData(conn)
        log.debug("file received")
        self._closeConnexion()
        log.debug("first 10 characters : %s", receivedFile[:10])
        log.debug("last  10 characters : %s", receivedFile[-10:])

        filePath = path.join("data", "downloads", fileName + "." + fileExtension)
        files.saveFile(receivedFile, filePath, binary=True)







if __name__ == "__main__":
    from data_manager import initializeLogger
    initializeLogger()

    address = ("192.168.1.71", 8088)
    client = Client(address)
    client._receiveFile()

