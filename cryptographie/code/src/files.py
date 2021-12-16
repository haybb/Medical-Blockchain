"""
Here are defined all functions and classes used to work with files
"""


from typing import Union
from os.path import splitext, join
import json





def saveFile(data: object, filePath: str, overwrite=False, binary=False) -> None:
    """
    Save the data in the file

    :param object data: the object to be stored
    :param str filePath: the path to the file with extension
    :param bool overwrite: if True, overwrite the file
    :param bool binary: True if the file is binary
    """
    openMode = 'w' if overwrite else 'a'
    if binary: openMode += 'b'
    with open(filePath, openMode) as f:
        f.write(data)



def loadJson(filePath: str) -> Union[dict, list]:
    """
    Returns the dict or list of a json

    :param str filePath: The path of the JSON file, relative to the file 'data'
    :return: the JSON as a python object
    :rtype: dict or list
    """
    file = ""
    with open(splitext(filePath)[0] + ".json", 'r') as f:
        data = f.read(2048)
        while data:
            file += data
            data = f.read()
    return json.loads(file)



def saveJson(data: Union[dict, list], filePath: str, sortKeys=False) -> None:
    """
    Overwrite the file with the data
    
    :param data: the object to be converted to JSON and written int he file
    :type data: dict or list
    :param str filePath: the path where the JSON object will be written, withour extension
    """
    if type(data) not in (dict, list):
        raise TypeError("Data type has to be dict or list, not", type(data))
    else:
        saveFile(json.dumps(data, indent=4, sort_keys=sortKeys), splitext(filePath)[0] + ".json", True, False)



if __name__ == "__main__":
    pass