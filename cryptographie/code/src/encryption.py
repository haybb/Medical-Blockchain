"""
Here are defined all the functions and classes related to the encryption part
"""


import files
from tree import ASCIITree
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import pickle, logging, os

log = logging.getLogger(__name__)




def hash256(obj: object) -> bytes:
    """
    Takes an object and returns its sha256 hash, the first is printable, the second is not

    :param object obj: the object to be hashed
    :return: the sha256 hash of the object
    :rtype: tuple(bytes, str)
    """
    hashObject = SHA256.new()
    bytesObject = pickle.dumps(obj) # The pickle module is needed to
                                    # convert the object to bytes
    hashObject.update(bytesObject)
    return hashObject.digest(), hashObject.hexdigest()



def areTheSame(obj1: object, obj2: object) -> bool:
    """
    Compares the hash of two objects

    :param object obj1: first object
    :param object obj2: second object
    :return: True if both objects have the same sha256 hash
    :rtype: bool
    """
    return hash256(obj1) == hash256(obj2)



def minstd() -> int:
    """
    Generates a pseudo-random number based on lastNumber, using the MINSTD linear congruential generator.
    2 147 483 645 different numbers are available.

    :param int lastNumber: the last number obtained with minstd
    :return: a new pseudo-random number
    :rtype: int
    """
    try:
        cache = files.loadFile(os.path.join(os.path.split(os.path.split(__file__)[0])[0], "data", "cache"), True)
        lastNumber = cache["last-minstd"]
    except FileNotFoundError as e:
        log.error("%s\nCreating the file", e)
        lastNumber = 36226479 # First number to use with this algorithm
        cache = {"last-minstd": lastNumber}
        files.saveFile(cache, os.path.join(os.path.split(os.path.split(__file__)[0])[0], "data", "cache"), overwrite=True, binary=True)
    except KeyError:
        lastNumber = 36226479 # First number to use with this algorithm
    else:
        lastNumber = (0xbc8f * lastNumber) % 0x7fffffff # 48271 for the first, 2147483647=2**31-1 for the second, according to
                                              # the new "minimum standard" recommended by Park, Miller and Stockmeyer
    cache["last-minstd"] = lastNumber
    files.saveFile(cache, os.path.join(os.path.split(os.path.split(__file__)[0])[0], "data", "cache"), overwrite=True, binary=True)
    return lastNumber



def __resetMinstdCache() -> None:
    """
    Resets the counter used by the minstd function
    """
    log.warning("You are about to reset the minstd count to the default value. Do you really want to proceed ? (y/n)")
    entry = input(" > ")
    if entry.lower() != 'y':
        log.info("The minstd count has NOT been reset.")
        return
    log.warning("Reseting the minstd count...")
    try:
        cache = files.loadFile(os.path.join(os.path.split(os.path.split(__file__)[0])[0], "data", "cache"), True)
        del cache["last-minstd"]
    except FileNotFoundError:
        pass
    except KeyError:
        pass



def newKeyPair() -> tuple[RSA.RsaKey, RSA.RsaKey]:
    """
    Generates a public/private key pair\n
    /!\\ This function DOES NOT check if the key already exist, you have to do it manually /!\\

    :return: the public/private RSA key couple
    :rtype: tuple(RSA.RsaKey, RSA.RsaKey)
    """
    private = RSA.generate(2048) # 2048 is the key size, recommended by the FIPS standard
    public = private.public_key()
    return public, private



def containsKey(repertory: ASCIITree, key: RSA.RsaKey) -> bool:
    """
    Checks if a RSA key is already in a ASCIITree

    :param ASCIITree repertory: the repertory where the key may be stored
    :param RSA.RsaKey key: the key to check
    :return: True if the key is in the repertory
    :rtype: bool 
    """
    if key.has_private(): raise ValueError("You cannot explicit a private key")
    stringKeyWithEnter = key.export_key().decode().split("-----")[2] # Because RSA.RsaKey.export returns:
    stringKey = "".join(stringKeyWithEnter.split("\n"))              # -----BEGIN PUBLIC KEY-----\nkey\n-----END PUBLIC KEY-----
    return stringKey in repertory







if __name__ == "__main__":
    from data_manager import initializeLogger
    initializeLogger()

    try:    
        # keysRep = ASCIITree()
        # public, private = newKeyPair()
        __resetMinstdCache()
    except Exception as e:
        log.error(e)

