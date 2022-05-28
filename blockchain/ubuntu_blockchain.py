import os


# /!\ Having Solana CLI installed is required

def send_transaction(token: str, quantity: float, recipient: str, memo: str) -> object:
    """
    Send a transaction through the Solana blockchain, for a desired token and with a message

    :param str token: desired token
    :param float quantity: quantity of token to send
    :param str recipient: receiver of the transaction
    :param str memo: message to attach to the transaction
    :return: transaction request through the command line
    :rtype: exit status on Linux, returned value by shell on Windows
    """

    return os.system(f'spl-token transfer {token} {quantity} {recipient} --fund-recipient --with-memo "{memo}"')


def obtain_last_block():
    return os.system()

if __name__ == '__main__':
    tkn = '9Cn5bRH8KaCpk91zZyLQDF6AFkp6ycZyP7TDMDWps1uc'
    qty = 1
    recipient = 'AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw'
    memo = 'Python test'
    send_transaction(tkn, qty, recipient, memo)
