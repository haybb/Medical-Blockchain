"""
Here are defined all functions and classes used by the server to wrok with the data
"""


from tkinter.tix import ASCII
from weakref import KeyedRef
from pydantic import EnumError
import files, encryption
from users import User, userTypes
from tree import ASCIITree
import logging, pickle
import os.path as path
from pathlib import Path
from Crypto.PublicKey import RSA

log = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    "key-chars": "!#$%&()*+-/0123456789<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz~",
    "max-key-number-of-attempts": 10
}





def initializeLogger() -> None:
    """
    Initializes the log Should be called only 1 time\n
    The terminal-side logger's logs level is set to DEBUG, the file's one to INFO
    """
    from datetime import datetime
    logsPath = path.join(path.split(path.split(__file__)[0])[0], "data", "logs", datetime.now().strftime("%Y-%m-%d") + ".txt")
    
    defaultFormatter = logging.Formatter("%(asctime)s %(levelname)s (%(module)s): %(message)s", "[%Y-%m-%d %H:%M:%S]")

    try:
        fileHandler = logging.FileHandler(logsPath)
    except FileNotFoundError:
        from os import makedirs
        makedirs(path.split(logsPath)[0], exist_ok=True)
        fileHandler = logging.FileHandler(logsPath)
    fileHandler.setLevel(logging.INFO)
    
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)

    fileHandler.setFormatter(defaultFormatter)
    streamHandler.setFormatter(defaultFormatter)

    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(fileHandler)
    logging.root.addHandler(streamHandler)







class DataManager:
    """
    Deals with the data stored in the server.
    Main class used to deal with data, it is the only object that should be able to do this.
    """
    def __init__(self, dataPath=None) -> None:
        """
        :param dataPath: the absolute path to the file where data is stored. If no path is given (None), the path to the data will be .\\data
        :type dataPath: str or None
        """

        log.debug("Starting the data manager...")

        self._dataFiles = { # all the files used
            "config": { # Contains the config of the data manager
                "path": "config",
                "extension": "json",
                "binary": False
            },
            "users": { # Contains the dict of all the users who have access to files. For it's format, check "server.md"
                "path": "users",
                "extension": "dat",
                "binary": True
            },
            "keys": { # Contains the tree of public key from all users
                "path": "keys",
                "extension": "dat",
                "binary": True
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
                # self._dataPath = path.join(fileDirDir, "data")
                self._dataPath = Path(path.join(fileDirDir, "data"))
            else: # Else the data directory is set as the same depth as the working file
                # self._dataPath = path.join(fileDirPath, "data")
                self._dataPath = Path(path.join(fileDirPath, "data"))

        # Creating the necessary files if they do not exist
        try:
            self._dataPath.mkdir()
        except FileExistsError:
            pass
        if not path.isfile(self._dataFiles["config"]["path"] + "." + self._dataFiles["config"]["extension"]):
            log.debug("Creating \"config\" file")
            self._saveFile(DEFAULT_CONFIG, "config")
        if not path.isfile(self._dataFiles["users"]["path"] + "." + self._dataFiles["users"]["extension"]):
            log.debug("Creating \"users\" file")
            self._saveFile(dict(), "users")
        if not path.isfile(self._dataFiles["keys"]["path"] + "." + self._dataFiles["keys"]["extension"]):
            log.debug("Creating \"keys\" file")
            self._saveFile(ASCIITree(), "keys")

        self._config = self._loadFile("config") # Gets the config

        log.debug("Data manager started")


    def _createUser(self, userType: str) -> int:
        """
        Adds a new user who will be able to request files

        :param str userType: the type of the new user
        :return: the unique ID of the user
        :rtype: int
        """
        if not userType in userTypes:
            raise KeyError("This type does not exist")
        uniqueID = encryption.minstd()
        newUser = User(uniqueID, userType)
        allUsers = self._loadFile("users")
        allUsers[uniqueID] = {
            "object": pickle.dumps(newUser)
        }
        self._saveFile(allUsers, "users")
        return uniqueID
    

    def newUser(self, userType: str, publicKey: RSA.RsaKey, **kwinfos) -> int:
        r"""
        Creates a new user based on their public key

        :param str userType: the type of the user
        :param str publicKey: the public key of the user
        :param \**kwinfos: additionnal infos about the user
        :return: the unique ID of the user
        :rtype: int
        """
        newUserID = self._createUser(userType)
        allPublicKeys = self._loadFile("keys")

        for i in range(self._config["max-key-number-of-attempts"]):
            # Creating a new key pair
            # stringKeyWithEnter = publicKey.export_key().decode().split("-----")[2] # Because RSA.RsaKey.export returns:
            # stringKey = "".join(stringKeyWithEnter.split("\n"))                    # -----BEGIN PUBLIC KEY-----\nkey\n-----END PUBLIC KEY-----
            stringKey = "abcdefghijkl"
            # Checking if the key already exist
            if not stringKey in allPublicKeys:
                break
            log.debug("here %i", i)
            if i == self._config["max-key-number-of-attempts"]-1:
                try:
                    self._deleteUser(newUserID)
                except KeyError:
                    pass
                raise TimeoutError("Could not create a new key pair that does not already exist. The user was not created")
        log.debug("appening user %i", newUserID)
        allPublicKeys.append(stringKey, uniqueID=newUserID)

        self._modifyUser(newUserID, publicKey=stringKey, **kwinfos)
        self._saveFile(allPublicKeys, "keys")

        return newUserID
    

    def _getUser(self, userID: int) -> User:
        """
        Gets the user which matches the ID from the registry

        :param int userID: the ID of the user
        :return: the corresponding User object
        :rtype: User
        """
        allUsers = self._loadFile("users")
        try:
            return pickle.loads(allUsers[userID]["object"])
        except KeyError:
            raise KeyError("This ID matchs no registered user")
    

    def _modifyUser(self, userID: int, **kwinfos) -> User:
        r"""
        Modify the corresponding user's infos given in paramaters

        :param int userID: the ID of the user
        :param \**kwinfos: additionnal infos about the string
        :return: the modified user
        :rtype: users.User
        """
        allUsers = self._loadFile("users")
        try:
            user = pickle.loads(allUsers[userID]["object"])
        except KeyError:
            raise KeyError("This ID matchs no registered user")
        user.modifyInfos(**kwinfos)
        allUsers[userID]["object"] = pickle.dumps(user)
        self._saveFile(allUsers, "users")
        return user
    

    def _deleteUser(self, uniqueID: int) -> None:
        """
        Deletes a user

        :param int uniqueID: the unique ID of the user
        """
        allUsers = self._loadFile("users")
        try:
            del allUsers[uniqueID]
        except KeyError:
            raise KeyError("This ID matchs no registered user")
        self._saveFile(allUsers, "users")
    

    def _saveFile(self, data: object, fileName: str, overwrite=True) -> None:
        """
        Saves data in a file

        :param object data: the data to store
        :param str file: the name of the file
        :param bool overwrite: True if the file should be overwritten
        """
        try:
            file = self._dataFiles[fileName]
        except KeyError:
            raise FileNotFoundError("This file does not exist")
        else:
            if file["extension"] == "json":
                files.saveJson(data, self._dataPath.joinpath(file["path"] + '.' + file["extension"]), sortKeys=True)
            else:
                files.saveFile(data, self._dataPath.joinpath(file["path"] + '.' + file["extension"]), overwrite=overwrite, binary=file["binary"])
    

    def _loadFile(self, fileName: str) -> object:
        """
        Loads data from a file

        :param str file: the name of the file
        :return: the object stored in the file
        :rtype: object
        """
        try:
            file = self._dataFiles[fileName]
        except KeyError:
            raise FileNotFoundError("This file does not exist")
        else:
            if file["extension"] == "json":
                return files.loadJson(self._dataPath.joinpath(file["path"] + '.' + file["extension"]))
            else:
                return files.loadFile(self._dataPath.joinpath(file["path"] + '.' + file["extension"]), binary=file["binary"])






if __name__ == "__main__":
    initializeLogger()
    
    try:
        manager = DataManager()
        # manager._saveFile(ASCIITree(), "keys", overwrite=True)
        # manager._saveFile({}, "users", overwrite=True)

        # allKeys = manager._loadFile("keys")
        # log.debug("allKeys : %s", allKeys)
        # for i in range(2):
        #     # publicKey, privateKey = encryption.newKeyPair()
        #     # stringKeyWithEnter = publicKey.export_key().decode().split("-----")[2] # Because RSA.RsaKey.export returns:
        #     # stringKey = "".join(stringKeyWithEnter.split("\n"))
        #     allKeys.append(("%i" % i)*10, ID=i)
        # log.debug("before : %s", allKeys)
        # manager._saveFile(allKeys, "keys")
        # allKeys = manager._loadFile("keys")
        # log.debug("after : %s", allKeys)


        # import tqdm
        # for i in tqdm.tqdm(range(30)):
        #     publicKey, privateKey = encryption.newKeyPair()
        #     manager.newUser("patient", publicKey, number=i)
        
        allUsers = manager._loadFile("users")
        for userID, userDict in allUsers.items():
            print("user ID : %-10i" % userID)
        
        allKeys = manager._loadFile("keys")
        for key in allKeys._allStrings():
            print("user ID / user key (first 20 chars) : %-10i || %s...%s...%s" % (key[1][1]["uniqueID"], key[0][:10], key[0][100:110], key[0][-10:]))

    except Exception as e:
        log.error(e)
        # raise e
    