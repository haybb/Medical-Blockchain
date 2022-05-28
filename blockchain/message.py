from cryptographie.code.src.encryption import *


def request_info(minstd: int, requestObject: str, ipp: int, rpps: int, ip: str,
                 recipientPublicKey: object, senderPrivateKey: object) -> dict:
    """
    Gives a dictionary with minstd and encrypted message

    :param minstd: last minstd number generated
    :param requestObject: object of the request
    :param ipp: unique patient id (=identifiant permanent du patient)
    :param rpps: unique specialist id (= répertoire partagé des professionnels de santé)
    :param ip: ip address of the sender
    :param recipientPublicKey: RSA public key of the recipient
    :param senderPrivateKey: RSA private key of the sender
    :return: dictionary which serves as message through the blockchain transaction
    :rtype: dictionary
    """

    data = f'{requestObject}*DELIMITER*{ipp}*DELIMITER*{rpps}*DELIMITER*{ip}'
    signature = RSASignature(data, senderPrivateKey)
    message = asymmetricRSAEncryption(data.encode(), recipientPublicKey) + b"*SEPARATOR*" + signature

    # NOTES: faire last_minstd() + verif que longueur message ok pour blockchain....

    return {'minstd': minstd, 'message': message}


def decrypt_info(data: bytes, senderPublicKey: object, recipientPrivateKey: object) -> list:
    """
    Decrypts the given message

    :param data: given message
    :param senderPublicKey: public key of the sender of the first transaction
    :param recipientPrivateKey: private key of the recipient of the second transaction
    :return: decrypted message if valid signature, else value error
    :rtype: list
    """
    dataReceived, signatureReceived = data.split(b"*SEPARATOR*")
    dataReceived = asymmetricRSADecryption(dataReceived, recipientPrivateKey)
    dataReceived = dataReceived.decode()
    # L = dataReceived.split("*DELIMITER*")

    try:
        verifyRSASignature(dataReceived, signatureReceived, senderPublicKey)
        # return {'Object': L[0], 'IPP': int(L[1]), 'RPPS': int(L[2]), 'IP': L[3]}
        return dataReceived.split("*DELIMITER*")

    except Exception as e:
        print(e)
        return [e]


def send_symmetric_key(minstd: int, symmetricKey: object, recipientPublicKey: object, senderPrivateKey: object) -> dict:
    """
    Sends symmetric key of the file, asymmetrically encrypted

    :param minstd: minstd
    :param symmetricKey: symmetric key to send
    :param recipientPublicKey: public key of the recipient
    :param senderPrivateKey: private key of the sender
    :return: dictionary which serves as message through the blockchain transaction
    :rtype: dictionary
    """
    data = f'retour*DELIMITER*{symmetricKey}'
    signature = RSASignature(data, senderPrivateKey)
    message = asymmetricRSAEncryption(data.encode(), recipientPublicKey) + b"*SEPARATOR*" + signature

    return {'minstd': minstd, 'message': message}


def last_minstd(lastBlock: object) -> object:
    pass


if __name__ == '__main__':
    doctorPublicKey, doctorPrivateKey = newKeyPair()
    specialistPublicKey, specialistPrivateKey = newKeyPair()


    # ALLER : demande info analyse sanguine médecin vers spécialiste
    aller = request_info(2147483647, "AnalyseSanguine", 2147483647, 48271,
                      "192.168.0.22", specialistPublicKey, doctorPrivateKey)

    print(f'---ALLER---\n\nMessage transaction aller médecin/spécialiste contenant demande info:\n{aller}\n')

    L_aller = decrypt_info(aller['message'], doctorPublicKey, specialistPrivateKey)
    print(f'Message décrypté, reçu par le spécialiste:\n{L_aller}\n')


    # RETOUR : envoi de la clé symétrique associé au fichier, encrypté asymétriquement
    retour = send_symmetric_key(2147483647, 'symKey', doctorPublicKey, specialistPrivateKey)
    print(f'\n---RETOUR---\n\nMessage transaction retour spécialiste/médecin contenant clé symétrique:\n{retour}\n')

    L_retour = decrypt_info(retour['message'], specialistPublicKey, doctorPrivateKey)
    print(f'Message décrypté, reçu par le médecin:\n{L_retour}')