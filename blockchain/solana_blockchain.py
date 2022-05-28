import json

# pip install solana

from spl.token.constants import TOKEN_PROGRAM_ID
from spl.token.instructions import transfer_checked, TransferCheckedParams

from solana.rpc.commitment import Confirmed
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.transaction import Transaction


client = Client(endpoint="https://api.mainnet-beta.solana.com", commitment=Confirmed)

# import here your id.json file containing your keypair (mine is hidden)
# or generate a new one using Keypair()
f = open('id_auth.json')
secret_key = json.load(f)
f.close()
owner = Keypair.from_secret_key(bytes(secret_key))

# Creation a transaction object, then addition of parameters for our request
transaction = Transaction()

transaction.add(
    transfer_checked(
        TransferCheckedParams(
    program_id=TOKEN_PROGRAM_ID,
    source=PublicKey("Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi"),
    mint=PublicKey("9Cn5bRH8KaCpk91zZyLQDF6AFkp6ycZyP7TDMDWps1uc"),
    dest=PublicKey("AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw"),
    owner=PublicKey("CCfW2si2HFPLpQhLVc3tXLFtYrYRG92a6Z97ZxZbuyZW"),
    amount=100,
    decimals=9,
    signers=[])))

print("Initial balances")
print(Client.get_balance(client,PublicKey("Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi")))
print(Client.get_balance(client, PublicKey("AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw")))
print(Client.get_balance(client, PublicKey("CCfW2si2HFPLpQhLVc3tXLFtYrYRG92a6Z97ZxZbuyZW")))

print("Transaction processing...")
print(client.send_transaction(transaction, owner, opts=TxOpts(skip_confirmation=False, preflight_commitment=Confirmed)))

print("Final balances")
print(Client.get_balance(client, PublicKey("Chup9he48sSAuPKGF7M2eXNVJXYbxDWFnrC6dSbDqkgi")))
print(Client.get_balance(client, PublicKey("AfzPooLwjpmhjjo7KR44fSivhwuxCsgHiEPAuhNgakvw")))
print(Client.get_balance(client, PublicKey("CCfW2si2HFPLpQhLVc3tXLFtYrYRG92a6Z97ZxZbuyZW")))

# /!\ ISSUE : memo program not implemented yet !
# We have to find another mean to send messages through solana transactions ...