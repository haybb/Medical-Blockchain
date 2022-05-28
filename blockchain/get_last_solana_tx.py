import asyncio
from solana.keypair import Keypair
from solana.rpc.websocket_api import connect


# WORK IN PROGRESS

async def main():
    async with connect("wss://api.devnet.solana.com") as websocket:
        # Create a Test Wallet
        wallet = Keypair()
        # Subscribe to the Test wallet to listen for events
        await websocket.account_subscribe(wallet.public_key)
        # Capture response from account subscription
        first_resp = await websocket.recv()
        print("Subscription successful with id {}, listening for events \n".format(first_resp.result))
        updated_account_info = await websocket.recv()
        print(updated_account_info)


asyncio.run(main())

