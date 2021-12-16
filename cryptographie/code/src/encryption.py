"""
Here are defined all the functions and classes related to the encryption part
"""

from Crypto.Hash import SHA256
import pickle




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



def minstd(lastNumber: int) -> int:
    """
    Generates a pseudo-random number based on lastNumber, using the MINSTD linear congruential generator.
    2 147 483 645 different numbers are available.

    :param int lastNumber: the last number obtained with minstd
    :return: a new pseudo-random number
    :rtype: int
    """
    return (0xbc8f * lastNumber) % 0x7fffffff # 48271 for the first, 2147483647=2**31-1 for the second, according to
                                              # the new "minimum standard" recommended by Park, Miller and Stockmeyer


if __name__ == "__main__":
    from tqdm import tqdm
    import files, os

    filePath = os.path.join(os.path.split(__file__)[0], "minstd")
    first = 36226479
    last = first
    for i in tqdm(range(2**32)):
        last = minstd(last)
        if last == first:
            value = [
                f"there was an issue at step {i}",
                {
                    "nb (int)": last,
                    "nb (hex)": hex(last)
                }
            ]
            files.saveJson(value, filePath)
            raise ValueError(i)
    files.saveJson(["no issue"], filePath)
