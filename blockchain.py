from json import dumps
from hashlib import sha256
from time import time


class Block:
    def __init__(self, index=0, transactions=None, timestamp=time(), previous_hash='0'*64, nonce=0):
        """
        Constructor of our Block class
        :param index:           Unique id
        :param transactions:    List of transactions
        :param timestamp:       Time where the block was created
        :param previous_hash:   Previous hash of the block
        :param nonce:           Arbitrary number to find for the miner, enables to add a new block if found
        """
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        """
        After having convert hash into a string json, return hash of actual block
        """
        # We're sorting keys in order to have consistent hash
        str_block = dumps(self.__dict__, sort_keys=True)

        # We can implement here an hash for every transaction and finally make a Merkle Tree
        return sha256(str_block.encode()).hexdigest()

    def __str__(self):
        """
        Enables to have good display of our block
        """
        return str(f'Block: {self.index} \n'
                   f'Hash: {self.hash()} \n'
                   f'Previous hash: {self.previous_hash} \n'
                   f'Timestamp: {self.timestamp} \n'
                   f'Nonce: {self.nonce} \n'
                   f'Transactions: {self.transactions} \n')


class Blockchain:
    # number of 0 required at the beginning of the hash
    difficulty = 4

    def __init__(self):
        """
        Constructor of the Blockchain class
        """
        self.chain = []

    def add_block(self, block):
        """
        Add a new block to the chain
        :param block:   the block to append
        :return:        the has been added to the chain
        """
        self.chain.append(block)

    def mine(self, block):
        """
        Enables to mine new blocks
        :param block:   block to mine
        :return:        index of the new block
        """
        try:
            block.previous_hash = self.chain[-1].hash()
        except:
            pass

        # We verify if the block's hash match with the number of 0 required, otherwise we increase the nonce
        while True:
            if block.hash()[:self.difficulty] == '0' * self.difficulty:
                self.add_block(block)
                break
            else:
                block.nonce += 1

    def is_valid(self):
        """
        Verify if the blockchain is valid
        :return:
        """
        for i in range(1, len(self.chain)):
            previous_hash = self.chain[i].previous_hash
            current_hash = self.chain[i-1].hash()

            if previous_hash != current_hash or current_hash[:self.difficulty] != '0' * self.difficulty:
                return False

        return True


def main():
    blockchain = Blockchain()
    database = ['hello', 'hola', 'bonjour']
    idx = 0

    for data in database:
        blockchain.mine(Block(idx, data, time()))
        idx += 1

    for block in blockchain.chain:
        print(block)

    blockchain.chain[2].transactions = 'aurevoir'
    blockchain.mine(blockchain.chain[2])

    print(blockchain.is_valid())


if __name__ == '__main__':
    main()