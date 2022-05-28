"""
Here are defined all functions and classes used by the server to work with the data
"""


import files, encryption
from users import User, userTypes
from tree import ASCIITree

import logging, pickle

import os.path as path
from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

import sqlite3


log = logging.getLogger(__name__)


DEFAULT_CONFIG = {
    "key-chars": "!#$%&()*+-/0123456789<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz~",
    "max-key-number-of-attempts": 10,
    "symmetric-key-number-of-bytes": 16
}





def initializeLogger(dataPath="") -> None:
    """
    Initializes the log. Should be called only 1 time\n
    The terminal-side logger's logs level is set to DEBUG, the file's one to INFO

    :param str dataPath: the path to the directory where data will be stored
    """
    from datetime import datetime

    if dataPath != "":
        if path.isabs(dataPath):
            if path.isdir(dataPath):
                dataPath = path.join(dataPath, "logs", datetime.now().strftime("%Y-%m-%d") + ".txt")
            else:
                raise ValueError("The path has to point to a directory")
        else:
            raise ValueError("The path has to be absolute")
    else:
        dataPath = path.join(path.split(path.split(__file__)[0])[0], "data", "logs", datetime.now().strftime("%Y-%m-%d") + ".txt")
    
    defaultFormatter = logging.Formatter("%(asctime)s %(levelname)s (%(module)s): %(message)s", "[%Y-%m-%d %H:%M:%S]")

    try:
        fileHandler = logging.FileHandler(dataPath)
    except FileNotFoundError:
        from os import makedirs
        makedirs(path.split(dataPath)[0], exist_ok=True)
        fileHandler = logging.FileHandler(dataPath)
    fileHandler.setLevel(logging.INFO)
    
    streamHandler = logging.StreamHandler()
    streamHandler.setLevel(logging.DEBUG)

    fileHandler.setFormatter(defaultFormatter)
    streamHandler.setFormatter(defaultFormatter)

    logging.root.setLevel(logging.DEBUG)
    logging.root.addHandler(fileHandler)
    logging.root.addHandler(streamHandler)



def getDirectories(data: list, isAbsolute=False) -> list[str]:
    """
    Gets all the elements representing a directory from the given list. They have to exist to be detected.

    :param list data: a list of all the elements to check if they represent a path
    :return: a list of all the strings representing a directory. Empty if no one is found
    :rtype: list of str
    """
    allDirs = list()
    for dirToTest in data:
        if type(dirToTest) == str and path.isdir(dirToTest):
            if isAbsolute:
                if path.isabs(dirToTest):
                    allDirs.append(dirToTest)
            else:
                allDirs.append(dirToTest)
    return allDirs







class DataManager:
    """
    Deals with the data stored in the server.
    Main class used to deal with data, it is the only object that should be able to do this.
    """
    def __init__(self, dataPath="") -> None:
        """
        :param dataPath: the absolute path to the file where data is stored. If no path is given (None), the path to the data will be .\\data
        :type dataPath: str
        """

        log.debug("Starting the data manager...")

        # All the files used by the data manager
        self._dataFiles = {
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
            },
            "database": { # Contains a database which references every specialists
                "path": "database",
                "extension": "db",
                "binary": True
            },
        }

        # Various checks about the data path
        if dataPath != "":
            if path.isabs(dataPath): # Check if the path is absolute
                if path.isdir(dataPath): # Check if the path points to a directory
                    self._dataPath = Path(dataPath)
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

        log.info("Data will be stored at \"%s\"", self._dataPath)

        # Creating the necessary files if they do not exist
        try:
            self._dataPath.mkdir()
        except FileExistsError:
            pass
        if not path.isfile(path.join(self._dataPath, self._dataFiles["config"]["path"] + "." + self._dataFiles["config"]["extension"])):
            log.debug("Creating \"config\" file at path \"%s\"", self._dataPath)
            self._saveFile(DEFAULT_CONFIG, "config")
        if not path.isfile(path.join(self._dataPath, self._dataFiles["users"]["path"] + "." + self._dataFiles["users"]["extension"])):
            log.debug("Creating \"users\" file at path \"%s\"", self._dataPath)
            self._saveFile(dict(), "users")
        if not path.isfile(path.join(self._dataPath, self._dataFiles["keys"]["path"] + "." + self._dataFiles["keys"]["extension"])):
            log.debug("Creating \"keys\" file at path \"%s\"", self._dataPath)
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
            stringKeyWithEnter = publicKey.export_key().decode().split("-----")[2] # Because RSA.RsaKey.export returns:
            stringKey = "".join(stringKeyWithEnter.split("\n"))                    # -----BEGIN PUBLIC KEY-----\nkey\n-----END PUBLIC KEY-----

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
    

    def symmetricEncryption(self, data: object) -> tuple[bytes]:
        """
        Encryptes some data using the AES symmetric-key algorithm.

        :param object data: the data to encrypt
        :return: a dictionnary containing cipher, key, tag, nonce
        :rtype: tuple[bytes, bytes, bytes, bytes]
        """
        config = self._loadFile("config")
        keySize = config["symmetric-key-number-of-bytes"]
        key = get_random_bytes(keySize)
        return encryption.symmetricAESEncryption(data, key)
    

    def symmetricDecryption(self, encryptedData: bytes, key: bytes, tag: bytes, nonce: bytes) -> object:
        """
        Decryptes some data encrypted with the AES symmetric-key algorithm.

        :param bytes encryptedData: the encrypted data
        :param bytes key: the key used for the encryption
        :param bytes tag: the tag of the encryption
        :param bytes nonce: the nonce of the encryption
        :return: the decrypted data
        :rtype: object
        :raises ValueError: if the key is incorrect or if the data has been corrupted
        """
        return encryption.symmetricAESDecryption(encryptedData, key, tag, nonce)
    

    def asymmetricEncryption(self, data: object, key: RSA.RsaKey) -> bytes:
        """
        Encryptes some data asymmetrically.
        The encryption can be made with both public and private key, while the decryption can only be made with the private key. Therefore, this function can only be used for encryption, not signature.

        :param object data: the data to encrypt
        :param RSA.RsaKey key: the key used for the encryption, can be public or private
        :return: the encrypted data
        :rtype: bytes
        """
        return encryption.asymmetricRSAEncryption(data, key)
    

    def asymmetricRSADecryption(self, encryptedData: bytes, privateKey: RSA.RsaKey) -> object:
        """
        Decryptes some data asymmetrically encrypted.
        The decryption can only be made with the private key.

        :param bytes encryptedData: the encrypted data
        :param RSA.RsaKey privateKey: the key used for decryption, has to be private
        :return: the decrypted data
        :rtype: object
        :raises TypeError: if the key used for the decryption is not private
        :raises ValueError: if the key is incorrect
        """
        return encryption.asymmetricRSADecryption(encryptedData, privateKey)
    

    def sign(self, data: object, privateKey: RSA.RsaKey) -> bytes:
        """
        Signs some data.
        
        :param object data: the data to encrypt
        :param RSA.RsaKey key: the key used to sign, has to be private
        :return: the signature
        :rtype: bytes
        """
        return encryption.RSASignature(data, privateKey)
    

    def verifySignature(self, data: object, signature: bytes, publicKey: RSA.RsaKey) -> None:
        """
        Verifies a signature.

        :param object data: the data to verify its signature
        :param bytes signature: the signature to verify
        :param RSA.RsaKey publicKey: the key used to verify the signature, can be public or private
        :raises TypeError: if the signature is incorrect
        :raises ValueError: if the signature is incorrect
        """
        encryption.verifyRSASignature(data, signature, publicKey)


    def createDataBase(self, dbName: str) -> (object,object):
        """
        Creates a database, or opens it if already existing

        :param str dbName: name of the database
        :return: c the cursor and conn the connection
        :rtype: tuple of cursor and connection sqlite objects
        """
        conn = sqlite3.connect(dbName)
        c = conn.cursor()
        return c, conn


    def createTable(self, c: object, conn: object, tableName: str) -> None:
        """
        Creates a table in given databse, or raise an error
        :param cursor c: cursor of the given database
        :param connection conn: connection of the given databse
        :param str tableName: name of the table
        :raise: Error if table already exists
        """
        try:
            with conn:
                comm = "CREATE TABLE " + tableName + " (cle publique text, nom text, portefeuille text)"
                # this syntax prevents SQL injections
                c.execute(comm)

        except Exception as e:
            print(e)


    def insertValue(self, c: object, conn: object, tableName: str, publicKey: str, personName: str, wallet: str) -> None:
        """
        Inserts value into given table

        :param cursor c: cursor
        :param connection conn: connection
        :param str tableName: name of the table
        :param publicKey: public RSA key of the person
        :param personName: person's name
        :param str wallet: wallet of the person for the given token of blockchain
        """
        with conn:
            comm = "INSERT INTO " + tableName + " VALUES ( '" + publicKey + "', '" + personName + "', '" + wallet + "' )"
            c.execute(comm)


    def showTable(self, c: object, conn: object, tableName: str) -> None:
        """
        Display the given table

        :param object c: cursor
        :param object conn: connection
        :param str tableName: name of the table
        """
        with conn:
            comm = "SELECT * FROM " + tableName
            c.execute(comm)
            print(c.fetchall())


    def deleteRow(self, c: object, conn: object, tableName: str, nameToDelete: str) -> None:
        """
        Delete one row for a given name

        :param object c: cursor
        :param object conn: connection
        :param str tableName: name of the table
        :param str nameToDelete: name to delete
        """
        with conn:
            comm = "DELETE FROM '" + tableName + "' WHERE nom = '" + nameToDelete + "'"
            c.execute(comm)






if __name__ == "__main__":
    initializeLogger()
    
    try:
        manager = DataManager()
        manager.newUser("patient", encryption.newKeyPair()[0])

        # publicKey, privateKey = encryption.newKeyPair()
        # log.debug("publicKey : %s\nprivateKey : %s", publicKey, privateKey)
        # stringKeyWithEnter = publicKey.export_key().decode().split("-----")[2] # Because RSA.RsaKey.export returns:
        # stringKey = "".join(stringKeyWithEnter.split("\n"))   
        # log.debug("stringKey : %s", stringKey)


        #ERROR (data_manager): createDataBase() takes 1 positional argument but 2 were given
        c, conn = manager.createDataBase("ListeSpecialistes.db")
        manager.createTable(c, conn, "Liste")

        manager.insertValue(c, conn, "Liste", "cléPublique1", "Médecin", "Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi")
        manager.insertValue(c, conn, "Liste", "cléPublique2", "Laboratoire", "9xcCpz4Y3BVSFiM7ZWZvS3uT5tUo9xsqpLJadCmEAM7Y")
        manager.insertValue(c, conn, "Liste", "cléPublique3", "Patient", "AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw")
        manager.showTable(c, conn, "Liste")

        manager.deleteRow(c, conn, "Liste", "Patient")
        manager.showTable(c, conn, "Liste")

        conn.close()

        # c.execute("INSERT INTO Liste VALUES(:pubkey, 'Medecin', 'Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi')",
        #           {'pubkey': 'pûbkey'})
        #
        # c.execute("INSERT INTO Liste VALUES(':pubkey','Laboratoire','9xcCpz4Y3BVSFiM7ZWZvS3uT5tUo9xsqpLJadCmEAM7Y')",
        #           {'pubkey': 'pûbkey'})
        #
        # c.execute("INSERT INTO Liste VALUES(':pubkey','Patient','AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw')",
        #           {'pubkey': 'pûbkey'})

        # if __name__ == '__main__':
        #
        #     insertValue()
        #     c.execute("SELECT * FROM Liste")
        #     print(c.fetchall())
        #
        #     conn.commit()
        #     conn.close()


    except Exception as e:
        log.error(e)
        # raise e

