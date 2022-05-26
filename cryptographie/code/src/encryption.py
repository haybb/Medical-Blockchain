"""
Here are defined all the functions and classes related to the encryption part
"""


from .files import *
from .tree import ASCIITree

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Signature import pss as PKCS1_PSS
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



def minstd(lastNumber=-1) -> int:
    """
    Generates a pseudo-random number based on lastNumber, using the MINSTD linear congruential generator.
    2 147 483 645 different numbers are available.

    :param int lastNumber: the last number obtained with minstd
    :return: a new pseudo-random number
    :rtype: int
    """
    # A number is given, so the new one is generated based on the one given. Therefore, the new one is not saved in a file
    if lastNumber == -1:
        return (0xbc8f * lastNumber) % 0x7fffffff # 48271 for the first, 2147483647=2**31-1 for the second, according to
                                                  # the new "minimum standard" recommended by Park, Miller and Stockmeyer
    
    # In the other case
    try:
        lastNumber = files.loadFromBlockchain("last-minstd")
    except FileNotFoundError as e:
        log.error("%s\nCreating the file", e)
        lastNumber = 36226479 # First number to use with this algorithm
        files.saveToBlockchain(lastNumber, "last-minstd")
    except KeyError:
        lastNumber = 36226479 # First number to use with this algorithm
    except Exception as e:
        log.critical(e)
        return
    else:
        lastNumber = (0xbc8f * lastNumber) % 0x7fffffff # 48271 for the first, 2147483647=2**31-1 for the second, according to
                                              # the new "minimum standard" recommended by Park, Miller and Stockmeyer

    if lastNumber == 36226479: # If it matches, it means the minstd has come to the end of the loop
        error = ValueError("The max number made with these parameters of minstd has been reached. You cannot create new unique numbers anymore")
        log.critical(error)
        raise error
    files.saveToBlockchain(lastNumber, "last-minstd")
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
    /!\\ This function DOES NOT check if the key already exists, you have to do it manually /!\\

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
    stringKey = "".join(stringKeyWithEnter.split("\n"))              # -----BEGIN PUBLIC KEY-----\n[key]\n-----END PUBLIC KEY-----
    return stringKey in repertory



def symmetricAESEncryption(data: object, key: bytes) -> tuple[bytes]:
    """
    Encryptes some data using the AES symmetric-key algorithm.

    :param object data: the data to encrypt
    :param bytes key: the key used for the encryption
    :return: a dictionnary containing cipher, key, tag, nonce
    :rtype: tuple[bytes, bytes, bytes, bytes]
    """
    # The functions used to create a new key
    # keyLength = dataManager.getConfig()["symmetric-key-number-of-bits"]
    # key = random.get_random_bytes(keyLength)
    
    dataInBytes = pickle.dumps(data)

    cipherObject = AES.new(key, AES.MODE_EAX) # The EAX mode is used as recommended by the Crypto module, but it may change in the future.
                                              # In fact, EAX allows the receiver to detect any unauthorized modification.
    cipherData, tag = cipherObject.encrypt_and_digest(dataInBytes)

    return (cipherData, key, tag, cipherObject.nonce)



def symmetricAESDecryption(encryptedData: bytes, key: bytes, tag: bytes, nonce: bytes) -> object:
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
    cipherObject = AES.new(key, AES.MODE_EAX, nonce=nonce)
    try:
        decryptedData = cipherObject.decrypt_and_verify(encryptedData, tag)
        return pickle.loads(decryptedData)
    except ValueError:
        raise ValueError("the key might be incorrect or the data has been corrupted")



def asymmetricRSAEncryption(data: object, key: RSA.RsaKey) -> bytes:
    """
    Encryptes some data using the PKCS#1 OAEP asymmetric cipher (because it is the one provided with the Crypto module).
    The encryption can be made with both public and private key, while the decryption can only be made with the private key. Therefore, this function can only be used for encryption, not signature.

    :param object data: the data to encrypt
    :param RSA.RsaKey key: the key used for the encryption, can be public or private
    :return: the encrypted data
    :rtype: bytes
    """
    dataInBytes = pickle.dumps(data)
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(dataInBytes)



def asymmetricRSADecryption(encryptedData: bytes, privateKey: RSA.RsaKey) -> object:
    """
    Decryptes some data encrypted with the PKCS#1 OAEP asymmetric cipher.
    The decryption can only be made with the private key.

    :param bytes encryptedData: the encrypted data
    :param RSA.RsaKey privateKey: the key used for decryption, has to be private
    :return: the decrypted data
    :rtype: object
    :raises TypeError: if the key used for the decryption is not private
    :raises ValueError: if the key is incorrect
    """
    cipher = PKCS1_OAEP.new(privateKey)
    dataInBytes = cipher.decrypt(encryptedData)
    return pickle.loads(dataInBytes)



def RSASignature(data: object, privateKey: RSA.RsaKey) -> bytes:
    """
    Signs some data with the PKCS#1 PSS asymmetric cipher (because it is the one provided with the Crypto module).
    
    :param object data: the data to encrypt
    :param RSA.RsaKey key: the key used to sign, has to be private
    :return: the signature
    :rtype: bytes
    """
    dataHash = SHA256.new(pickle.dumps(data))
    cipher = PKCS1_PSS.new(privateKey)
    signature = cipher.sign(dataHash)
    return signature



def verifyRSASignature(data: object, signature: bytes, publicKey: RSA.RsaKey) -> None:
    """
    Verifies a signature with the PKCS#1 PSS asymmetric cipher.

    :param object data: the data to verify its signature
    :param bytes signature: the signature to verify
    :param RSA.RsaKey publicKey: the key used to verify the signature, can be public or private
    :raises TypeError: if the signature is incorrect
    :raises ValueError: if the signature is incorrect
    """
    dataHash = SHA256.new(pickle.dumps(data))
    verifier = PKCS1_PSS.new(publicKey)
    verifier.verify(dataHash, signature)
    





if __name__ == "__main__":
    from data_manager import initializeLogger
    initializeLogger()

    data = "abc"
    # from Crypto.Random import get_random_bytes
    # data = get_random_bytes(32)
    publicKey, privateKey = newKeyPair()
    signature = RSASignature(data, privateKey)
    verifyRSASignature(data, signature, newKeyPair()[0])