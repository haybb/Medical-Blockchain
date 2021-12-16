"""
Here are defined all functions and classes used by the server to wrok with the data
"""


import files
import os.path as path
from Crypto.Random.random import sample



class DataManager:
    """
    Deals with the data stored in the server
    """
    def __init__(self, dataPath=None) -> None:
        """
        :param dataPath: the absolute path to the file where data is stored. If no path is given (None), the path to the data will be .\\data
        :type dataPath: str or None
        """
        self.files = { # all the files used
            "config": {
                "path": "config",
                "extension": "dat",
                "binary": False
            },
            "users": {
                "path": "users",
                "extension": "json",
                "binary": False
            }
        }

        if dataPath:
            if path.isabs(dataPath): # Check if the path is absolute
                if path.isdir(dataPath): # Check if the path points to a directory
                    self._dataPath = dataPath
                else:
                    raise ValueError("The path has to point to a directory")
            else:
                raise ValueError("The path has to be absolute")
        else: # Defines the data path relative to the file
            fileDirPath, file = path.split(__file__)
            fileDirDir, fileDirName = path.split(fileDirPath)
            if fileDirName.lower() == "src": # If the working file is in a directory named 'src', the
                                             # data directory will be set at the same depth as src
                self._dataPath = path.join(fileDirDir, "data")
            else: # Else the data directory is set as the same depth as the working file
                self._dataPath = path.join(fileDirPath, "data")
        
        # try: # Check if a file already  exist
        #     files.loadJson(self._dataPath)
        # except FileNotFoundError: # If no one exist, creates one
        #     files.saveJson({}, self._dataPath)


    def createUser(self, type):
        """
        Add a new user who will be able to request files

        
        """
        usersList = files.loadJson(self.dataPath)
        usersIDs = usersList.keys()
    

    def saveFile(self, data: object, fileName: str, overwrite=False) -> None:
        """
        Save data in a file

        :param object data: the data to store
        :param str file: the name of the file
        :param bool overwrite: True if the file should be overwritten
        """
        try:
            file = self.files[fileName]
        except KeyError:
            raise FileNotFoundError("This file does not exist")
        else:
            if file["extension"] == "json":
                files.saveJson(data, path.join(self._dataPath, (file["path"] + '.' + file["extension"])), True)
            else:
                files.saveFile(data, path.join(self._dataPath, (file["path"] + '.' + file["extension"])), overwrite, file["binary"])





if __name__ == "__main__":
    manager = DataManager()
    manager.saveFile("test", "config", True)

    