"""
Here is defined the Tree class and its components
"""



import logging
from typing import Union

log = logging.getLogger(__name__)
ASCII_CHAR = "!\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"


def isASCII(string: str) -> Union[bool,str]:
    """
    Tests if all characters in a string are ASCII characters.
    If the string is empty, returns True

    :param str string: the string to test
    :return: True if all characters are ASCII cahracters or if the string is empty, and the first character which is not ASCII if there is at least one
    :rtype: bool or str
    """
    if len(string) == 0: return True
    if len(string) == 1: 
        if string in ASCII_CHAR: return True
        else: return string
    else:
        for char in string:
            if not char in ASCII_CHAR: return char
        return True




class ASCIITree:
    def __init__(self) -> None:
        self._children = dict() # Stores all children (Tree type) in a dict
                                # The key represents the value of the node
                                # The value represents another Tree
    

    def append(self, string: str, *infos, **kwinfos) -> None:
        r"""
        Adds a string to the tree

        :param str string: the string to add to the tree
        :param \*infos: additionnal infos about the string
        :param \**kwinfos: additionnal infos about the string
        """
        c = isASCII(string)
        if c != True:
            raise ValueError("All characters of the string have to be ASCII characters (character '%c')" % c)
        if len(string) == 0:
            self._children = {"info": (infos, kwinfos)}
        else:
            try:
                self._children[string[0]]
            except KeyError:
                self._children[string[0]] = ASCIITree()
            finally:
                self._children[string[0]].append(string[1:], *infos, **kwinfos)
    

    def remove(self, string: str) -> None:
        """
        Removes the string from the tree

        :param str string: the string to remove
        """
        try:
            self._children["info"]
        except KeyError:
            try:
                self._children[string[0]]
            except KeyError:
                raise KeyError("This string is not in the tree")
            else:
                self._children[string[0]].remove(string[1:])
                if len(self._children[string[0]]._children) == 0:
                    self._children.pop(string[0])
        else:
            self._children = dict()
        

    def getInfos(self, string: str) -> tuple:
        """
        Returns the infos stored with the string

        :param str string: the string of which you want to get the infos
        :return: the infos stored with the key
        :rtype: tuple
        """
        if len(string) == 0:
            if len(self._children) == 0: return dict()
            else:
                try:
                    return self._children["info"]
                except KeyError:
                    raise KeyError("The string is not in the tree")
        else:
            try:
                return self._children[string[0]].getInfos(string[1:])
            except KeyError as e:
                raise KeyError("The string is not in the tree")
    

    def _allStrings(self) -> list:
        """
        Enumerates all the strings inside the tree
        
        :return: all the strings inside the tree
        :rtype: list of str
        """
        # if len(self._children) == 0:
        #     return [("", )]
        # else:
        try:
            self._children["info"]
        except KeyError:
            l = list()
            for k, v in self._children.items():
                children = v._allStrings()
                for child in children:
                    l.append((k + child[0], child[1]))
            return l
        else:
            return [("", self._children["info"])]


    def __contains__(self, string: str) -> bool:
        """
        Tests if a string is in the tree

        :param str string: the string to test
        :return: returns True if the string is in the tree
        :rtype: bool
        """
        if len(string) == 0:
            if len(self._children) == 0: return True
            else:
                try:
                    self._children["info"]
                except KeyError:
                    raise ValueError("The string is not of the good length")
                else:
                    return True
        else:
            try:
                return string[1:] in self._children[string[0]]
            except KeyError as e:
                return False

    
    def __repr__(self) -> str:
        log.warning("Enumerating all strings from the tree, may take time. Try to avoid __repr__ of an ASCIITree")
        return self._allStrings().__repr__()







if __name__ == "__main__":
    from data_manager import initializeLogger
    initializeLogger()

    try: # Tests
        import files
        config = files.loadJson("Git\\TIPE-Blockchain\\cryptographie\\code\\data\\config.json")

        keys = list()
        keySize = 3
        keyNbr = 2
        rep = ASCIITree()
        key = "abc"
        rep.append("abcd", "foo")
        print(rep.getInfos(key))
    except Exception as e:
        log.exception(e)


