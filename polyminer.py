import sys
import logging
import time
from web3 import Web3
from threading import Thread, Lock
import argparse
import json
from eth_abi.packed import encode_packed  # Corrected import statement

# Logging configuration
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Contract details
CONTRACT_ADDRESS = "0xb745b960a244157029eDe392956a299ddf3F90b3"
GAS_LIMIT = 300000
CHAIN_ID = 137  # Polygon Mainnet chain ID

# Amount of MATIC to send with the mining transaction
TRANSACTION_VALUE = Web3.to_wei(0.01, 'ether')  # Adjust this value as needed

# Load contract ABI
CONTRACT_ABI = '''
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "approve",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "ownerAddress",
				"type": "address"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "allowance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientAllowance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "balance",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "needed",
				"type": "uint256"
			}
		],
		"name": "ERC20InsufficientBalance",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "approver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidApprover",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "receiver",
				"type": "address"
			}
		],
		"name": "ERC20InvalidReceiver",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "sender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSender",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "ERC20InvalidSpender",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			}
		],
		"name": "OwnableInvalidOwner",
		"type": "error"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "OwnableUnauthorizedAccount",
		"type": "error"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "spender",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Approval",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "MaticTransferred",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "nonce",
				"type": "uint256"
			}
		],
		"name": "mine",
		"outputs": [],
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "miner",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "reward",
				"type": "uint256"
			}
		],
		"name": "Mined",
		"type": "event"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "previousOwner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnershipTransferred",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "renounceOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "_amount",
				"type": "uint256"
			}
		],
		"name": "stake",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "staker",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			}
		],
		"name": "Staked",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transfer",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "Transfer",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "from",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}
		],
		"name": "transferFrom",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "transferOwnership",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "unstake",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "staker",
				"type": "address"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"indexed": false,
				"internalType": "uint256",
				"name": "rewards",
				"type": "uint256"
			}
		],
		"name": "Unstaked",
		"type": "event"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "owner",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "spender",
				"type": "address"
			}
		],
		"name": "allowance",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "account",
				"type": "address"
			}
		],
		"name": "balanceOf",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "decimals",
		"outputs": [
			{
				"internalType": "uint8",
				"name": "",
				"type": "uint8"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "difficulty",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "emissionEndTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "getBlockReward",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "HALVING_INTERVAL",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "INITIAL_BLOCK_REWARD",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "INITIAL_DIFFICULTY",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "lastBlockTime",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "name",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "owner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "rewardPool",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "stakes",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "amount",
				"type": "uint256"
			},
			{
				"internalType": "uint256",
				"name": "stakeTime",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "symbol",
		"outputs": [
			{
				"internalType": "string",
				"name": "",
				"type": "string"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "TOTAL_SUPPLY",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalStaked",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "totalSupply",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
'''

# Flag to stop mining
mining_active = True

def connect_to_web3(rpc_url):
    """Connect to the Web3 provider."""
    web3 = Web3(Web3.HTTPProvider(rpc_url))
    if not web3.is_connected():
        raise Exception("Unable to connect to RPC URL")
    logging.info("Connected to RPC: %s", rpc_url)
    return web3

def fetch_difficulty(contract):
    """Fetch the current mining difficulty."""
    try:
        difficulty = contract.functions.difficulty().call()
        return difficulty
    except Exception as e:
        logging.error("Error fetching difficulty: %s", e)
        return None

def mine(web3, private_key, contract_address, threads):
    """Start mining tokens."""
    global mining_active

    account = web3.eth.account.from_key(private_key)
    contract = web3.eth.contract(address=contract_address, abi=json.loads(CONTRACT_ABI))
    difficulty = fetch_difficulty(contract)
    if not difficulty:
        logging.error("Could not fetch difficulty. Exiting mining.")
        return

    # Check account balance
    balance = web3.eth.get_balance(account.address)
    logging.info("Account balance: %s POLYGON", web3.from_wei(balance, 'ether'))
    if balance == 0:
        logging.error("Account balance is zero. Cannot send transactions.")
        return

    # Initialize the shared nonce and nonce lock
    nonce_lock = Lock()
    with nonce_lock:
        shared_nonce = web3.eth.get_transaction_count(account.address)

    logging.info("Starting mining. Difficulty: %d", difficulty)

    def miner_thread(thread_id):
        nonlocal shared_nonce  # Access the shared_nonce variable from the outer scope
        nonce = thread_id
        while mining_active:
            nonce += threads
            # Compute the hash according to Solidity's keccak256(abi.encodePacked(msg.sender, nonce))
            hash_input = encode_packed(['address', 'uint256'], [account.address, nonce])
            hash_value = Web3.keccak(hash_input)
            hash_int = int.from_bytes(hash_value, byteorder='big')

            if hash_int < (2 ** 256) // difficulty:
                logging.info("Thread %d found a valid nonce: %d", thread_id, nonce)

                with nonce_lock:
                    # Use and increment the shared nonce safely
                    tx_nonce = shared_nonce
                    shared_nonce += 1

                try:
                    # Fetch the dynamic gas price
                    GAS_PRICE = web3.eth.gas_price

                    # Build transaction using contract function
                    tx = contract.functions.mine(nonce).build_transaction({
                        'from': account.address,
                        'gas': GAS_LIMIT,
                        'gasPrice': GAS_PRICE,
                        'nonce': tx_nonce,
                        'chainId': CHAIN_ID,
                        'value': TRANSACTION_VALUE  # Include value in the transaction
                    })

                    signed_tx = web3.eth.account.sign_transaction(tx, private_key)
                    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
                    logging.info("Thread %d mined a block. TX Hash: %s", thread_id, tx_hash.hex())

                    # Wait for the transaction receipt
                    receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
                    if receipt.status == 1:
                        logging.info("Transaction succeeded. Block number: %d", receipt.blockNumber)
                    else:
                        logging.error("Transaction failed. Receipt: %s", receipt)
                except Exception as e:
                    logging.error("Thread %d failed to submit mined block: %s", thread_id, e)
            time.sleep(0.01)

    threads_list = []
    for i in range(threads):
        thread = Thread(target=miner_thread, args=(i,))
        threads_list.append(thread)
        thread.start()

    try:
        for thread in threads_list:
            thread.join()
    except KeyboardInterrupt:
        logging.info("Stopping mining... Please wait for threads to exit.")
        mining_active = False
        for thread in threads_list:
            thread.join()

def stake(web3, private_key, contract_address, amount):
    """Stake tokens."""
    account = web3.eth.account.from_key(private_key)
    contract = web3.eth.contract(address=contract_address, abi=json.loads(CONTRACT_ABI))
    GAS_PRICE = web3.eth.gas_price

    try:
        # Build transaction using contract function
        tx = contract.functions.stake(Web3.to_wei(amount, 'ether')).build_transaction({
            'from': account.address,
            'gas': GAS_LIMIT,
            'gasPrice': GAS_PRICE,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': CHAIN_ID
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info("Staking transaction sent. TX Hash: %s", tx_hash.hex())

        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            logging.info("Staking successful.")
        else:
            logging.error("Staking failed. Receipt: %s", receipt)
    except Exception as e:
        logging.error("Staking transaction failed: %s", e)

def unstake(web3, private_key, contract_address):
    account = web3.eth.account.from_key(private_key)
    contract = web3.eth.contract(address=contract_address, abi=json.loads(CONTRACT_ABI))
    GAS_PRICE = web3.eth.gas_price

    try:
        user_stake = contract.functions.stakes(account.address).call()
        reward_pool = contract.functions.rewardPool().call()
        total_staked = contract.functions.totalStaked().call()

        logging.info(f"User Stake: {Web3.from_wei(user_stake[0], 'ether')} POLM")
        logging.info(f"Reward Pool: {Web3.from_wei(reward_pool, 'ether')} POLM")
        logging.info(f"Total Staked: {Web3.from_wei(total_staked, 'ether')} POLM")

        # Build transaction using contract function
        tx = contract.functions.unstake().build_transaction({
            'from': account.address,
            'gas': GAS_LIMIT,
            'gasPrice': GAS_PRICE,
            'nonce': web3.eth.get_transaction_count(account.address),
            'chainId': CHAIN_ID
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        logging.info("Unstaking transaction sent. TX Hash: %s", tx_hash.hex())

        # Wait for transaction receipt
        receipt = web3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        if receipt.status == 1:
            logging.info("Unstaking successful.")
        else:
            logging.error("Unstaking failed. Receipt: %s", receipt)

        # Log updated contract state
        reward_pool = contract.functions.rewardPool().call()
        total_staked = contract.functions.totalStaked().call()
        logging.info(f"Updated Reward Pool: {Web3.from_wei(reward_pool, 'ether')} POLM")
        logging.info(f"Updated Total Staked: {Web3.from_wei(total_staked, 'ether')} POLM")
    except Exception as e:
        logging.error("Unstaking transaction failed: %s", e)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PolyMiner - Stake, Unstake, and Mine")
    parser.add_argument("command", choices=["mine", "stake", "unstake"], help="Action to perform")
    parser.add_argument("rpc_url", help="RPC URL of the blockchain network")
    parser.add_argument("wallet_address", help="Wallet address to interact with")
    parser.add_argument("-p", "--private_key", required=True, help="Private key for the wallet")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads for mining")
    parser.add_argument("-a", "--amount", type=float, help="Amount to stake (in POLM)")

    args = parser.parse_args()

    web3 = connect_to_web3(args.rpc_url)
    contract_address = Web3.to_checksum_address(CONTRACT_ADDRESS)

    if args.command == "mine":
        mine(web3, args.private_key, contract_address, args.threads)
    elif args.command == "stake":
        if args.amount is None:
            logging.error("You must provide an amount to stake using the -a option.")
        else:
            stake(web3, args.private_key, contract_address, args.amount)
    elif args.command == "unstake":
        unstake(web3, args.private_key, contract_address)
