import os
import json
from dotenv import load_dotenv
from web3 import Web3
from web3.middleware import geth_poa_middleware

load_dotenv(".env")
load_dotenv(".env.local", override=True)

class ERC8004Registry:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(os.getenv("RPC_URL")))
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.from_key(os.getenv("PRIVATE_KEY"))

        # Official hackathon shared contracts on Sepolia
        self.AGENT_REGISTRY = "0x97b07dDc405B0c28B17559aFFE63BdB3632d0ca3"

        # Minimal ABI for register function (from hackathon template)
        self.abi = [
            {
                "inputs": [
                    {"name": "agentWallet", "type": "address"},
                    {"name": "name", "type": "string"},
                    {"name": "description", "type": "string"},
                    {"name": "capabilities", "type": "string[]"},
                    {"name": "agentURI", "type": "string"}
                ],
                "name": "register",
                "outputs": [{"name": "agentId", "type": "uint256"}],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "anonymous": False,
                "inputs": [
                    {"indexed": True, "name": "agentId", "type": "uint256"},
                    {"indexed": False, "name": "agentURI", "type": "string"},
                    {"indexed": True, "name": "owner", "type": "address"}
                ],
                "name": "Registered",
                "type": "event"
            }
        ]

        self.contract = self.w3.eth.contract(address=self.AGENT_REGISTRY, abi=self.abi)

    def register_agent(self):
        agent_wallet = self.account.address
        name = os.getenv("AGENT_NAME")
        description = os.getenv("AGENT_DESCRIPTION")
        capabilities = ["trading", "risk-analysis", "orthogonal-verification", "mcp-execution"]
        agent_uri = os.getenv("AGENT_URI")

        print(f"🔐 Registering OrthoAgent from {agent_wallet}...")

        tx = self.contract.functions.register(
            agent_wallet,
            name,
            description,
            capabilities,
            agent_uri
        ).build_transaction({
            'from': agent_wallet,
            'nonce': self.w3.eth.get_transaction_count(agent_wallet),
            'gas': 500000,
            'gasPrice': self.w3.eth.gas_price
        })

        signed_tx = self.w3.eth.account.sign_transaction(tx, os.getenv("PRIVATE_KEY"))
        tx_hash = self.w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        print(f"⏳ Transaction sent: {tx_hash.hex()}")

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        if receipt.status == 1:
            # Parse Registered event
            logs = self.contract.events.Registered().process_receipt(receipt)
            if logs:
                agent_id = logs[0]['args']['agentId']
                print(f"✅ SUCCESS! OrthoAgent registered with Agent ID: {agent_id}")
                print(f"View on Etherscan: https://sepolia.etherscan.io/tx/{tx_hash.hex()}")
                # Save agent ID for later use
                with open("agent-id.json", "w") as f:
                    json.dump({"agent_id": int(agent_id), "tx_hash": tx_hash.hex()}, f)
                return agent_id
        else:
            print("❌ Registration failed")
            return None

if __name__ == "__main__":
    registry = ERC8004Registry()
    registry.register_agent()