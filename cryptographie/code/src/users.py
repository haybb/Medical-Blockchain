"""
Here are defined all classes used to represent a user
"""


from Crypto.PublicKey import RSA

from pprint import PrettyPrinter
prettyPrinter = PrettyPrinter(indent=2)


userTypes = [
    "patient",
    "doctor",
    "nurse",
    "pharmacist",
    "research"
]



class User:
    """
    Represent a person or an organization
    """
    def __init__(self, uniqueID: int, userType: str, **kwinfos) -> None:
        r"""
        :param int uniqueID: the ID of the user. Has to be unique
        :param str userType: the type of user
        :param \**kwinfos: additionnal infos about the user
        """
        self._id = uniqueID
        self._type = userType
        self._publicKey = None # type RSA.RsaKey
        self._infos = kwinfos
    

    def getID(self) -> int:
        """ Returns the ID of the user """
        return int(self._id)
    

    def modifyInfos(self, **kwinfos) -> None:
        r"""
        Modify the infos of the user with the given one

        :param \**kwinfos: additionnal infos about the user
        """
        self._infos = dict(self._infos, **kwinfos)
    

    def getInfo(self, key: str) -> object:
        """
        Get some info about the user

        :param str key: the key of the info
        :return: the info requested
        :rtype: object
        """
        try:
            return self._infos[key]
        except KeyError:
            raise KeyError("This info does not exist")
    
    
    def __repr__(self) -> str:
        return f"User of type {self._type}, id: {self.getID()}, infos: {prettyPrinter.pformat(self._infos)}"


    def __eq__(self, __o: object) -> bool:
        if not type(__o) == User:
            return False
        return self._id == __o._id and self._type == __o._type and self._publicKey == __o._publicKey and self._infos == __o._infos


    # @staticmethod
    # def importUser(uniqueID: int, userType: str, publicKey: RSA.RsaKey, infos: dict):
    #     """
    #     Creates a new User with the given paramaters

    #     :param int uniqueID: the ID of the user
    #     :param str userType: the type of user
    #     :param RSA.RsaKey publicKey: the public key of the user
    #     :param dict infos: all additionnal infos
    #     :return: a new User object with the parameters
    #     :rtype: User
    #     """
    #     newUser = User(uniqueID, userType)
    #     newUser._publicKey = publicKey
    #     newUser._infos = infos
    #     return newUser



    



if __name__ == "__main__":
    from data_manager import initializeLogger
    initializeLogger()
    print(User(1, name="john", age=31))