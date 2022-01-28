"""
Here are defined all functions and classes used to work with files
"""



import json, pickle, logging, sys
from typing import Union
from os.path import splitext

log = logging.getLogger(__name__)





def saveFile(data: object, filePath: str, overwrite=True, binary=False) -> None:
    """
    Saves the data in a file

    :param object data: the object to be stored
    :param str filePath: the path to the file with extension
    :param bool overwrite: if True, overwrite the file
    :param bool binary: True if the file is binary
    """
    openMode = 'w' if overwrite else 'a'
    if binary:
        openMode += 'b'
        if (type(data) == bytes):
            toSave = data
        else:
            while True: # If the data si to big, pickle raises a RecursionError exception.
                        # It can be avoided by raising the recursion limit, but at a certain point,
                        # it has to be raised because it can causes to crash the program.
                try:
                    toSave = pickle.dumps(data)
                    break
                except RecursionError as e:
                    recursionLimit = sys.getrecursionlimit()
                    if recursionLimit <= 10000:
                        sys.setrecursionlimit(recursionLimit + 100)
                    else:
                        log.critical("Could not save the file at \"%s\": may cause critical issues. It is recommended to restart the server.", filePath)
                        return
                    
    else:
        if type(data) != str:
            openMode += 'b'
            while True: # See above
                try:
                    toSave = pickle.dumps(data)
                    break
                except RecursionError as e:
                    recursionLimit = sys.getrecursionlimit()
                    if recursionLimit <= 1000:
                        sys.setrecursionlimit(recursionLimit + 100)
                    else:
                        log.critical("Could not save the file at \"%s\": may cause critical issues. It is recommended to restart the server", filePath)
                        break
        else:
            toSave = data
    with open(filePath, openMode) as f:
        f.write(toSave)



def loadFile(filePath: str, binary: bool) -> object:
    """
    Returns the data from a file

    :param str filePath: the path of the file
    :param bool binary: True if the file is binary
    :return: the data stored in the file
    :rtype: object
    """
    openMode = "rb" if binary else 'r'
    file = bytes() if binary else str()
    with open(filePath, openMode) as f:
        data = f.read(2048)
        while data:
            file += data
            data = f.read(2048)
    if binary:
        return pickle.loads(file)
    else:
        return file



def saveJson(data: Union[dict, list], filePath: str, sortKeys=False) -> None:
    """
    Saves the data in a JSON file by overwriting it
    
    :param data: the object to be converted to JSON and written in the file
    :type data: dict or list
    :param str filePath: the path where the JSON object will be written, withour extension
    """
    if type(data) not in (dict, list):
        raise TypeError("Data type has to be dict or list, not", type(data))
    else:
        saveFile(json.dumps(data, indent=4, sort_keys=sortKeys), splitext(filePath)[0] + ".json", True, False)



def loadJson(filePath: str) -> Union[dict, list]:
    """
    Returns the dict or list of a JSON file

    :param str filePath: The path of the JSON file
    :return: the JSON as a python object
    :rtype: dict or list
    """
    file = ""
    with open(splitext(filePath)[0] + ".json", 'r') as f:
        data = f.read(2048)
        while data:
            file += data
            data = f.read(2048)
    return json.loads(file)

    



if __name__ == "__main__":
    from data_manager import initializeLogger
    initializeLogger()

    # loginfo("current working directory: %s", os.getcwd())