"""
The program that will be started by the server.

By running this program, you run the entire one.
You can give as arguments the paths to the data directory
"""



from data_manager import DataManager, initializeLogger, getDirectories

import os.path as path
import logging

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
        log.info("Server started")
    

    def _sendToBlockchain(self, *argv, **kwargs) -> None:
        """
        Send data to the blockchain
        This function still have to be written - waiting for Hugo
        """
        log.debug("This data has to be sent to the blockchain:\n    - %s\n    - %s", argv, kwargs)

    
    def _getFromBlockchain(self, *argv, **kwargs):
        """
        Get data from the blockchain
        This function still have to be written - waiting for Hugo
        """
        log.debug("This data has to be got from the blockchain:\n    - %s\n    - %s", argv, kwargs)






if __name__ == "__main__":
    ###### DO NOT MODIFY THESE LINES ######
    import sys
    allDirs = getDirectories(sys.argv)
    dataPath = allDirs[0] if len(allDirs)>=1 else ""
    initializeLogger(dataPath)
    ###### DO NOT MODIFY THESE LINES ######

    # You can modify the next ones
    try:
        mainServer = Server(dataPath)
    except Exception as e:
        log.error(e)
        raise e
