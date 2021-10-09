import hashlib
import time
import requests
from json import dumps
from flask import Flask, request


class Block:

    def __init__(self, index, transactions, timestamp, previous_hash, nonce):
        """
        Initialisation de notre classe Block.

        :param index:           Identifiant unique du block
        :param transactions:    Liste des transactions
        :param timestamp:       Date & heure où le bloc fut créé
        :param previous_hash:       Précédent hachage
        :param nonce:           Nombre de transactions provenant d'un même expéditeur
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def calculate_hash(self):
        """
        Après avoir converti le hachage en un string au format json, retourne le hachage du bloc actuel.
        """
        str_block = dumps(self.__dict__, sort_keys=True)
        # Nous avons besoin de trier les clés pour que les hachages soient cohérents

        return hashlib.sha256(str_block.encode()).hexdigest()
        # Possibilité d'implémenter un hachage pour chaque transaction,
        # puis de les enregistrer pour former un abre de hachage (arbre de Merkle).
        # Les racines de l'arbre représentent le hachage du bloc.

    def __str__(self):
        return str(f'Bloc: {self.index} \n'
                   f'Hachage: {self.calculate_hash()} \n'
                   f'Précédent hachage: {self.previous_hash} \n'
                   f'Temps: {self.timestamp} \n'
                   f'Nonce: {self.nonce} \n'
                   f'Transactions: {self.transactions} \n')


class Blockchain:
    difficulty = 4  # nombre de 0 pour le nonce, utilisé pour l'algorithme de preuve du travail (Proof of Work, PoW)

    def __init__(self):
        """
        Initialisation de la classe Blockchain.
        """
        self.chain = []
        self.create_first_block()
        self.unconfirmed_transactions = []

    def create_first_block(self):
        """
        Création du 1er bloc de la chaine
        """
        first_block = Block(0, [], time.time(), "0", 0)
        first_block.hash = first_block.calculate_hash()
        self.chain.append(first_block)

    @property
    def previous_block(self):
        """
        :return:    dernier bloc de la chaine
        """
        return self.chain[-1]

    def proof_of_work(self, block):
        """
        Recherche de différentes valeurs pour le nonce, pour avoir un hachage satisfaisant la difficulté imposée.

        :param block:   bloc actuel
        :return:        hachage du bloc actuel s'il satisfait la difficulté imposée
        """
        block.nonce = 0
        calculated_hash = block.calculate_hash()

        while not calculated_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            calculated_hash = block.calculate_hash()

        # On voit ici les problèmes écologiques liés à cet algorithme de PoW:
        # utilisation brute du processeur pour chaque mineur,
        # menant à une perte d'électricité conséquente à grande échelle.

        return calculated_hash

    def valid_proof(self, block, block_hash):
        """
        Vérifie si block_hash est un hachage valide du bloc et satisfait la difficulté imposée
        :return:    True si block_hash satisfait les conditions
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and block_hash == block.calculate_hash())

    def new_block(self, block, proof):
        """
        Après vérification de la preuve et que le hachage du bloc précédent corresponde bel et bien à celui indiqué
        dans le bloc, ajoute le nouveau bloc dans la chaine.

        :param block:   bloc actuel
        :param proof:   preuve du bloc actuel
        :return:        True si le nouveau bloc est ajouté sinon False
        """
        last_hash = self.previous_block().hash

        if last_hash != block.last_hash:
            return False

        if not Blockchain.valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)

        return True

    def add_transaction(self, transaction):
        """
        :param transaction: transaction à ajouter
        :return:            transaction ajoutée aux transactions à verifier
        """
        self.unconfirmed_transactions.append(transaction)

    def mine(self):
        """
        Interface pour les transactions en attente d'ajout à la blockchain.
        Pour cela, on ajoute ces transactions au bloc actuel et on trouve leur hachage.

        :return:    index du nouveau bloc
        """
        if not self.unconfirmed_transactions:
            return False

        previous_block = self.previous_block()

        block_to_add = Block(index=previous_block.index + 1,
                             transactions=self.unconfirmed_transactions,
                             timestamp=time.time(),
                             last_hash=previous_block.hash)

        proof = self.proof_of_work(block_to_add)
        self.new_block(block_to_add, proof)
        self.unconfirmed_transactions = []

        return block_to_add.index


    # ----------------------- PARTIE OBSCURE -----------------------

    def check_chain_valididty(self, cls, chain):
        """
        Verification de l'entièreté de la blockchain
        :return:    True si blockchain compléte sinon False
        """
        result = True
        last_hash = '0'

        for block in chain:
            block_hash = block.hash
            delattr(block, 'hash')  # on supprime pour vérifier de nouveau le hachage

            if not cls.valid_proof(block, block_hash) or last_hash != block.last_hash:
                result = False
                break

            block.hash = block_hash
            last_hash = block_hash

        return result

    def consensus(self):
        """
        Simple algorithme de consensus (possibilité d'implémenter un algo plus sophistiqué...) :
        si une chaine valide est trouvée, elle remplace alors la chaîne actuelle.

        :return:    True si consensus, False sinon
        """
        global blockchain

        longest_chain = None
        current_len = len(blockchain.chain)

        for node in peers:
            response = requests.get(f'{node}/chain')
            length = response.json()['length']
            chain = response.json()['chain']

            if length > current_len and blockchain.check_chain_valididty(chain):
                current_len = length
                longest_chain = chain

            if longest_chain:
                blockchain = longest_chain
                return True

        return False


# ----------------------- COMPLIQUE -----------------------

# Nous crééons ici une interface entre notre blockchain et
# le reste des applications que nous allons faire par la suite,
# grâce à Flask.

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    """
    Permet à l'application de soumettre une nouvelle transaction.
    :return:    'Success' (201) si la transaction a bien été ajoutée, sinon erreur (404)
    """
    tx_data = request.get_json()
    fields_needed = ['author', 'content']

    for field in fields_needed:
        if not tx_data.get(field):
            return 'Invalid transaction data', 404

    tx_data['timestamp'] = time.time()
    blockchain.add_transaction(tx_data)

    return 'Succes', 201


@app.route('/chain', methods=['GET'])
def get_chain():
    """
    Donne la chaine entière lorsque demandée par l'application.
    :return:    Dictionnaire avec 'length' et 'chain'
    """
    data = []

    for block in blockchain.chain:
        data.append(block.__dict__)

    return dumps({'length': len(data), 'chain': data})


@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    """
    Donne au noeud l'index d'un bloc à miner (s'il est en attente de vérification).
    :return:    Si bloc à miner, retourne son index
    """
    result = blockchain.mine()

    if not result:
        return 'Pas de transactions à miner'

    return f'Bloc n°{result} miné.'


@app.route('/pendinx_tx')
def get_pending_tx():
    """
    :return:    Transactions à verifier au format json
    """
    return dumps(blockchain.unconfirmed_transactions)



# Ici, nous crééons les fonctions nécessaires pour que le réseau contiennent plusieurs noeuds
peers = set()

@app.route('/register_node', methods=['POST'])
def register_node():
    """
    Permet à l'application d'ajouter un nouveau noeud au réseau.
    :return:    la blockchain avec le nouveau noeud
    """
    node_address = request.get_json()['node_address']

    if not node_address:
        return 'Donnée invalide', 400

    peers.add(node_address)

    return get_chain()


def create_chain_from_dump(chain_dump):
    blockchain = Blockchain()

    for idx, block_data in enumerate(chain_dump):
        block = Block(block_data['index'], block_data['transactions'], block_data['timestamp'], block_data['last_hash'])
        proof = block_data['hash']

        if idx > 0:
            added = blockchain.new_block(block, proof)

            if not added:
                raise Exception('La chaîne vidée a été falsifiée')

            else:
                blockchain.append(block)

    return blockchain


@app.route('/register_with', methods=['POST'])
def register_with_existing_nodes():
    """
    Appelle register_node pour enrgistrer le noeud actuel avec le noeud distant spécifié dans la requête,
    puis synchronise la blockchain avec ce noeud éloigné.   # éloigné/distant <- 'remote'
    :return:    Enregistre avec succès (ou non si erreur) un nouveau noeud
    """
    node_address = request.get_json()['node_address']

    if not node_address:
        return 'Donnée invalide', 400

    data = {'node_address': request.host_url}
    header = {'content_type': 'applications/json'}

    response = requests.post(node_address + '/register_node', data=dumps(data), header=header)

    if response.status_code == 200:
        global blockchain, peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return 'Ajout du noeud réussi', 200

    else:
        return response.content, response.status_code


if __name__ == '__main__':
    # block = Block(0, " ", time.time(), '0', 0)
    # print(block)

    blockchain = Blockchain()
    db = ['hello world', 'hola', 'bonjour', 'privet']
    num = 0
    for data in db:
        num += 1
        blockchain.mine()

    print(blockchain.chain)
    for block in blockchain.chain:
        print(block)