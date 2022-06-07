import python_blockchain
from cryptographie.code.src.encryption import *


def request_info(minstd: int, requestObject: str, ipp: int, rpps: int, ip: str,
                 recipientPublicKey: object, senderPrivateKey: object) -> dict:
    """
    Give a dictionary with minstd and encrypted message.

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

    data = f'{requestObject}*DEL*{ipp}*DEL*{rpps}*DEL*{ip}'
    signature = RSASignature(data, senderPrivateKey)
    message = asymmetricRSAEncryption(data.encode(), recipientPublicKey) + b"*SEP*" + signature

    return {'minstd': minstd, 'data': message}


def decrypt_info(data: bytes, senderPublicKey: object, recipientPrivateKey: object) -> list:
    """
    Decrypt the given message.

    :param data: given message
    :param senderPublicKey: public key of the sender
    :param recipientPrivateKey: private key of the recipient
    :return: decrypted message if valid signature, else value error
    :rtype: list
    :raise: error if RSA signature isn't valid
    """
    dataReceived, signatureReceived = data.split(b"*SEP*")
    dataReceived = asymmetricRSADecryption(dataReceived, recipientPrivateKey)
    dataReceived = dataReceived.decode()

    try:
        verifyRSASignature(dataReceived, signatureReceived, senderPublicKey)
        return dataReceived.split("*DEL*")

    except Exception as e:
        print(e)
        return [e]


def send_symmetric_key(minstd: int, symmetricKey: object, tag: bytes, nonce: bytes,
                       recipientPublicKey: object, senderPrivateKey: object) -> dict:
    """
    Message format to send symmetric key of the file, asymmetrically encrypted.

    :param minstd: minstd
    :param symmetricKey: symmetric key to send
    :param tag: tag needed for decryption
    :param nonce: nonce needed for decryption
    :param recipientPublicKey: public key of the recipient
    :param senderPrivateKey: private key of the sender
    :return: dictionary which serves as message through the blockchain transaction
    :rtype: dictionary
    """
    data = f'retour*DEL*{symmetricKey}*DEL*{tag}*DEL*{nonce}'
    signature = RSASignature(data, senderPrivateKey)
    message = asymmetricRSAEncryption(data.encode(), recipientPublicKey) + b"*SEP*" + signature

    return {'minstd': minstd, 'data': message}


def send_transaction(blockchain: object, sender: str, recipient: str, quantity: float, data: object) -> None:
    """
    Send a transaction through the blockchain with given parameters.

    :param blockchain: blockchain where we have to have the transaction
    :param sender: wallet of the sender
    :param recipient: wallet of the recipient
    :param quantity: quantity to send
    :param data: data to send
    """
    blockchain.new_data(
        sender=sender,
        recipient=recipient,
        quantity=quantity,
        message=data)

    blockchain.block_mining(sender)


def read_transaction(stored_blockchain: object, new_blockchain:object, address: str) -> (object, list):
    """
    Read new transaction between stored and new blockchains given

    :param stored_blockchain: old blockchain stored locally
    :param new_blockchain: new blockchain, which may have changed if a new transaction was added
    :param address: wallet of the transaction sender
    :return: new blockchain and list of new transactions
    """
    diff = len(new_blockchain.chain) - len(stored_blockchain.chain)
    L = []

    if diff != 0:
        for i in range(1, diff + 1):
            block = new_blockchain.chain[-i]
            for tx in block.data:
                if tx['recipient'] == address:
                    L.append(tx)

    else:  # another transaction in the same block
        block = new_blockchain.chain[-1]
        for tx in block.data:
            if tx['recipient'] == address:
                L.append(tx)

    return (new_blockchain, L)


def last_minstd(blockchain: object) -> int:
    """
    Find last minstd stored in the given blockchain.

    :param blockchain: blockchain where minstd is to find
    :return: last minstd stored in the given blockchain
    """
    for i in range(1, len(blockchain.chain) + 1):
        for j in range(1, len(blockchain.chain[-i].data) + 1):
            mess = blockchain.chain[-i].data[-j]['message']
            if type(mess) == dict:
                return mess['minstd']


if __name__ == '__main__':

    """Example : a patient visits his doctor and wants analysis results carried out at the laboratory."""

    # Creation of keypairs for doctor & specialist
    doctorPublicKey, doctorPrivateKey = newKeyPair()
    specialistPublicKey, specialistPrivateKey = newKeyPair()

    # Simulation of 2 differents blockchains on the 2 laptops
    blockchain_doctor = python_blockchain.Blockchain()
    blockchain_specialist = python_blockchain.Blockchain()

    # rpps = minstd(-1)
    # ipp = minstd(rpps)
    rpps = 48271
    ipp = 2147483647


    # Creation of 2 wallets
    doctor_wallet = "doctor_wallet"
    specialist_wallet = "specialist_wallet"

    # Inventory
    print('ETAT INITIAL \n')
    print('Blockchain du médecin:', blockchain_doctor.chain, '\n')
    print('Blockchain du spécialiste:', blockchain_specialist.chain, '\n\n')


    # A) Request of  the analysis by the authorized doctor to the specialist
    analysis_demand = request_info(ipp, 'Demande analyse sanguine de M.Dupont', ipp, rpps, '127.0.0.1',
                                   specialistPublicKey, doctorPrivateKey)
    send_transaction(blockchain_doctor, doctor_wallet, specialist_wallet, 1, analysis_demand)


    # B) Message received by the specialist
    blockchain_specialist, L = read_transaction(blockchain_specialist, blockchain_doctor, specialist_wallet)

    print('UNE TRANSACTION PLUS TARD \n')
    print('Blockchain du médecin:', blockchain_doctor.chain)
    print('Blockchain du spécialiste:', blockchain_specialist.chain, '\n\n')

    print('MESSAGE DECRYPTE PAR LE SPECIALISTE:',
          decrypt_info(L[-1]['message']['data'], doctorPublicKey, specialistPrivateKey), '\n\n')

    baseKey = b"abcdefghijklmnop"
    encrypted, key, tag, nonce = symmetricAESEncryption("test", baseKey)


    # C) The specialist sends the symmetric key to the doctor
    sym_key = send_symmetric_key(last_minstd(blockchain_specialist), encrypted,
                          tag, nonce, doctorPublicKey, specialistPrivateKey)
    send_transaction(blockchain_specialist, specialist_wallet, doctor_wallet, 1, sym_key)

    print('CLÉ SYMÉTRIQUE ENVOYÉE \n')
    print('Blockchain du médecin:', blockchain_doctor.chain, '\n')
    print('Blockchain du spécialiste:', blockchain_specialist.chain, '\n\n')


    # D) The doctor receives the symmetrical key from the specialist and decrypts it
    blockchain_doctor, M = read_transaction(blockchain_doctor, blockchain_specialist, doctor_wallet)
    print('MESSAGE DECRYPTE PAR LE MEDECIN:',
          decrypt_info(M[-1]['message']['data'], specialistPublicKey, doctorPrivateKey), '\n\n')

    print('ETAT FINAL \n')
    print('Blockchain du médecin:', blockchain_doctor.chain)
    print('Blockchain du spécialiste:', blockchain_specialist.chain)
