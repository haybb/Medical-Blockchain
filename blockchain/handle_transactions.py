import python_blockchain
from cryptographie.code.src.encryption import *


def request_info(minstd: int, requestObject: str, ipp: int, rpps: int, ip: str,
                 recipientPublicKey: object, senderPrivateKey: object) -> dict:
    """
    Gives a dictionary with minstd and encrypted message.

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
    Decrypts the given message.

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
    Sends a transaction through the blockchain with given parameters.

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
    Reads new transaction between stored and new blockchains given

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
            print(block)
            for tx in block.data:
                if tx['recipient'] == address:
                    L.append(tx)

    else:  # another transaction in the same block
        print('checking last block')
        block = new_blockchain.chain[-1]
        for tx in block.data:
            if tx['recipient'] == address:
                L.append(tx)

    return (new_blockchain, L)


def last_minstd(blockchain: object) -> int:
    """
    Finds last minstd stored in the given blockchain.

    :param blockchain: blockchain where minstd is to find
    :return: last minstd stored in the given blockchain
    """
    for i in range(1, len(blockchain.chain) + 1):
        for j in range(1, len(blockchain.chain[-i].data) + 1):
            mess = blockchain.chain[-i].data[-j]['message']
            if type(mess) == dict:
                return mess['minstd']


if __name__ == '__main__':

    """Exemple : un patient se rend chez son médecin et veut ses résultats d'analyse,
    celle ci s'étant déroulé chez son spécialiste"""

    # création paires de clés pour médecin et spécialiste
    doctorPublicKey, doctorPrivateKey = newKeyPair()
    specialistPublicKey, specialistPrivateKey = newKeyPair()

    # simulation de 2 blockchains différentes sur les 2 pc
    blockchain_doctor = python_blockchain.Blockchain()
    blockchain_specialist = python_blockchain.Blockchain()

    # rpps = minstd(-1)
    # ipp = minstd(rpps)    # name 'loadFromBlockchain' is not defined ... ajout manuel des valeurs
    rpps = 48271
    ipp = 2147483647


    # création des 2 portefeuilles, des clés d'encryptage en réalité
    doctor_wallet = "doctor_wallet"
    specialist_wallet = "specialist_wallet"

    # état des lieux
    print('ETAT INITIAL \n')
    print('Blockchain du médecin:', blockchain_doctor.chain, '\n')
    print('Blockchain du spécialiste:', blockchain_specialist.chain, '\n\n')


    # A) demande de l'analyse par médecin au spécialiste
    analysis_demand = request_info(ipp, 'Analyses du 31/05', ipp, rpps, '127.0.0.1',
                                   specialistPublicKey, doctorPrivateKey)
    send_transaction(blockchain_doctor, doctor_wallet, specialist_wallet, 1, analysis_demand)


    # B) message reçu par spécialiste
    blockchain_specialist, L = read_transaction(blockchain_specialist, blockchain_doctor, specialist_wallet)

    print('MESSAGE DECRYPTE PAR LE SPECIALISTE:',
          decrypt_info(L[-1]['message']['data'], doctorPublicKey, specialistPrivateKey), '\n\n')

    print('UNE TRANSACTION PLUS TARD \n')
    print('Blockchain du médecin:', blockchain_doctor.chain)
    print('Blockchain du spécialiste:', blockchain_specialist.chain, '\n\n')


    # C) spécialiste envoie clé symétrique au médecin
    sym_key = send_symmetric_key(last_minstd(blockchain_specialist), 'this is a symmetric key',
                           b'tag', b'nonce', doctorPublicKey, specialistPrivateKey)
    send_transaction(blockchain_specialist, specialist_wallet, doctor_wallet, 1, sym_key)
    # PROBLEME : ici blockchain_doctor et blockchain_specialist sont les 2 modifiés
    # lors de l'ajout de cette transaction
    # or seul blockchain_specialist devrait être modifié
    # d'où l'ajout de la condition else dans read_transaction()

    print('CLÉ SYMÉTRIQUE ENVOYÉE \n')
    print('Blockchain du médecin:', blockchain_doctor.chain, '\n')
    print('Blockchain du spécialiste:', blockchain_specialist.chain, '\n\n')


    # D) médecin reçoit clé symétrique du spécialiste et la déchiffre
    blockchain_doctor, M = read_transaction(blockchain_doctor, blockchain_specialist, doctor_wallet)
    print('MESSAGE DECRYPTE PAR LE MEDECIN:',
          decrypt_info(M[-1]['message']['data'], specialistPublicKey, doctorPrivateKey), '\n\n')

    print('ETAT FINAL \n')
    print('Blockchain du médecin:', blockchain_doctor.chain)
    print('Blockchain du spécialiste:', blockchain_specialist.chain)
