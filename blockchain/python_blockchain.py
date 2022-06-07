from time import time
from hashlib import sha256


class Block:

    def __init__(self, index: int, nonce: int, prev_hash: str, data: list, timestamp=None) -> None:
        """
        Initialisation of the Block class

        :param int index: index of the block
        :param int nonce: number of tries to find a hash that satisfies the difficulty
        :param str prev_hash: previous block hash
        :param list data: attached data to the block
        :param float timestamp: given timestamp or generated one with time module
        """

        self.index = index
        self.nonce = nonce
        self.prev_hash = prev_hash
        self.data = data
        self.timestamp = timestamp or time()


    @property
    def hash_calculation(self) -> str:
        """
        Calculation of a SHA256 hash

        :return: hash of the block
        :rtype: str
        """

        str_block = f'{self.index}{self.nonce}{self.prev_hash}{self.data}{self.timestamp}'
        return sha256(str_block.encode()).hexdigest()


    def __repr__(self) -> str:
        """
        Printable presentation of one block

        :return: presentation of a Block
        :rtype: str
        """
        return f'\nIndex: {self.index} \nNonce: {self.nonce} \nPrevious hash: {self.prev_hash} \nData: {self.data}' \
               f'\nTimestamp: {self.timestamp}\n'



class Blockchain:
    global difficulty
    difficulty = 4

    def __init__(self) -> None:
        """
        Initialization of the Blockchain class
        """

        self.chain = []
        self.current_data = []
        self.nodes = {}
        self.genesis_block()


    def genesis_block(self) -> None:
        """
        First block added to the blockchain, with arbitrary value of 0 for both nonce and previous hash
        """

        self.add_block(nonce=0, prev_hash='0')


    def add_block(self, nonce: int, prev_hash: str) -> Block:
        """
        Addition of a block to the blockchain

        :param int nonce: number of tries to find a hash that satisfies the difficulty
        :param str prev_hash: previous block hash
        :return: the block added
        :rtype: Block
        """

        block = Block(
            index=len(self.chain),
            nonce=nonce,
            prev_hash=prev_hash,
            data=self.current_data)
        self.current_data = []

        self.chain.append(block)
        return block


    @staticmethod
    def check_validity(prev_block: Block, block: Block) -> bool:
        """
        Check the validity of 2 given blocks according to their hash, timestamp, proof and index

        :param Block prev_block: previous block
        :param Block block: new block
        :return: True if blockchain is valid, False otherwise
        :rtype: bool
        """

        if prev_block.hash_calculation != block.prev_hash:
            return False

        elif block.timestamp <= prev_block.timestamp:
            return False

        elif not Blockchain.verify_proof(prev_block.nonce, block.nonce):
            return False

        elif prev_block.index + 1 != block.index:
            return False

        return True


    def new_data(self, sender: str, recipient: str, quantity: float, message: str) -> bool:
        """
        Attach new data to the current one

        :param str sender: sender of the transaction
        :param str recipient: receiver of the transaction
        :param float quantity: quantity of tokens to send
        :param str message: message attached to the transaction
        :return: True
        :rtype: bool
        """

        self.current_data.append({
            'sender': sender,
            'recipient': recipient,
            'quantity': quantity,
            'message': message})

        return True


    @staticmethod
    def proof_of_work(last_nonce: int) -> int:
        """
        Proof of work algorithm : count the attempts to verify the proof with the nonce variable

        :param int last_nonce: previous number of tries required to find the hash
        :return: nonce
        :rtype: int
        """

        nonce = 0

        while not Blockchain.verify_proof(last_nonce, nonce):
            nonce += 1

        return nonce


    @staticmethod
    def verify_proof(last_nonce: int, nonce: int) -> int:
        """
        Verify that the given hash match the desired one, with the difficulty required

        :param int last_nonce: previous nonce
        :param int nonce: current nonce
        :return: True if sha256 of last_nonce & nonce match the difficulty required, False otherwise
        :rtype: bool
        """

        to_find = f'{last_nonce}{nonce}'.encode()
        hash_to_find = sha256(to_find).hexdigest()

        return hash_to_find[:difficulty] == '0'*difficulty


    @property
    def last_block(self) -> Block:
        """
        Return the last block of the chain

        :return: last block of the chain
        :rtype: Block
        """

        return self.chain[-1]


    def block_mining(self, miner_details: str) -> Block:
        """
        Add a new block with the given miner details when validations are completed

        :param str miner_details: details of the miner
        :return: the last block when validations are completed
        :rtype: Block
        """

        self.new_data(
            sender='0', # chosen value 0 for a new block
            recipient=miner_details,
            quantity=1, # arbitrary value of 1
            message='***Mining new block***')

        last_block = self.last_block
        last_nonce = last_block.nonce
        last_hash = last_block.hash_calculation

        nonce = self.proof_of_work(last_nonce)
        block = self.add_block(nonce, last_hash)

        return block


    def new_node(self, address:  str) -> bool:
        """
        Add a new node address

        :param str address: address of the new node
        :return: True
        :rtype: bool
        """

        self.nodes.add(address)
        return True



if __name__ == '__main__':

    '''Let's test our functions:
    -at first, we create a blockchain with 1 node, the genesis block and add 1 block
    -then, we mine another one'''

    global difficulty
    difficulty = 4  # number of 0 required at the beginning of the hash
    print('Difficulty:', difficulty)


    # test 1
    blockchain = Blockchain()
    blockchain.nodes = {'PC 1', 'PC 2', 'PC 3'}
    print('Nodes:', blockchain.nodes, '\n')
    print('Initial blockchain:\n', blockchain.chain)

    prev_block = blockchain.last_block
    last_nonce = prev_block.nonce
    nonce = blockchain.proof_of_work(last_nonce)

    blockchain.new_data(
        sender='PC 1',
        recipient='PC 2',
        quantity=1,
        message='First Test')

    last_hash = prev_block.hash_calculation
    block = blockchain.add_block(nonce, last_hash)

    print('\nBlockchain with 1 validated block:\n', blockchain.chain)
    print('\nValidity of the blockchain:', blockchain.check_validity(prev_block, block))


    # test 2
    blockchain.new_data(
        sender='PC 2',
        recipient='PC 3',
        quantity=2,
        message='Second Test')

    print('\n\nData to mine:', blockchain.current_data)

    block = blockchain.block_mining('PC 3')
    print("Let's directly use the block_mining() function:", block)
    print("Finally, our blockchain:\n", blockchain.chain)
