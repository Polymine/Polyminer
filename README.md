### PolyMiner - A Python-Based Mining & Staking Script for Polymine (POLM)

PolyMiner is a Python-based script designed to interact with the **Polymine (POLM)** smart contract, enabling seamless mining, staking, and unstaking functionalities. It supports the Polygon network and provides flexibility for both beginners and advanced users.

---

### Features
- **Mining**: Mine POLM tokens via the Proof of Work mechanism.
- **Staking**: Stake POLM tokens to earn additional rewards.
- **Unstaking**: Unstake your POLM tokens and claim rewards.

---

### Prerequisites

1. **Python**:
   - Ensure you have Python 3.8 or later installed.
   - Download Python from [python.org](https://www.python.org/) if not already installed.

2. **Dependencies**:
   - Install the required Python packages using:
     ```bash
     pip install web3 eth-abi argparse
     ```

---

### Setup Instructions

#### Windows

1. **Install Python**:
   - Download the latest Python version from [python.org](https://www.python.org/).
   - During installation, check **Add Python to PATH**.

2. **Clone or Download PolyMiner**:
   - Clone the repository or download the script.

3. **Install Dependencies**:
   Open Command Prompt and run:
   ```cmd
   pip install web3 eth-abi argparse
   ```

4. **Run the Script**:
   Use the commands provided in the "Usage" section below.

#### Linux

1. **Install Python**:
   - Most Linux distributions come with Python pre-installed.
   - Verify by running:
     ```bash
     python3 --version
     ```

2. **Install pip** (if not installed):
   ```bash
   sudo apt update
   sudo apt install python3-pip
   ```

3. **Clone or Download PolyMiner**:
   ```bash
   git clone https://github.com/Polymine/Polyminer.git
   cd polyminer
   ```

4. **Install Dependencies**:
   ```bash
   pip3 install web3 eth-abi argparse
   ```

5. **Run the Script**:
   Use the commands provided in the "Usage" section below.

#### Mac

1. **Install Python**:
   - Install Python using [Homebrew](https://brew.sh/):
     ```bash
     brew install python
     ```

2. **Clone or Download PolyMiner**:
   ```bash
   git clone https://github.com/<your-repo>/polyminer.git
   cd Polyminer
   ```

3. **Install Dependencies**:
   ```bash
   pip3 install web3 eth-abi argparse
   ```

4. **Run the Script**:
   Use the commands provided in the "Usage" section below.

---

### Usage

1. **Mining**:
   Start mining POLM tokens by providing the RPC URL, wallet address, private key, and thread count.

   ```bash
   python polyminer.py mine <rpc_url> <wallet_address> -p <private_key> -t <threads>
   ```

   Example:
   ```bash
   python polyminer.py mine https://polygon-mainnet.g.alchemy.com/v2/YOUR_RPC_URL 0xYourWalletAddress -p YourPrivateKey -t 4
   ```

2. **Staking**:
   Stake a specified amount of POLM tokens.

   ```bash
   python polyminer.py stake <rpc_url> <wallet_address> -p <private_key> -a <amount>
   ```

   Example:
   ```bash
   python polyminer.py stake https://polygon-mainnet.g.alchemy.com/v2/YOUR_RPC_URL 0xYourWalletAddress -p YourPrivateKey -a 100
   ```

3. **Unstaking**:
   Unstake your POLM tokens and claim staking rewards.

   ```bash
   python polyminer.py unstake <rpc_url> <wallet_address> -p <private_key>
   ```

   Example:
   ```bash
   python polyminer.py unstake https://polygon-mainnet.g.alchemy.com/v2/YOUR_RPC_URL 0xYourWalletAddress -p YourPrivateKey
   ```

---

### Arguments

| Argument         | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `<rpc_url>`      | The RPC URL of the Polygon network (e.g., from Alchemy or Infura).          |
| `<wallet_address>` | Your wallet address to interact with the POLM smart contract.              |
| `-p <private_key>` | The private key of your wallet for signing transactions.                   |
| `-t <threads>`    | (Mining only) The number of threads to use for mining.                     |
| `-a <amount>`     | (Staking only) The amount of POLM tokens to stake.                         |

---

### Example Outputs

#### Mining:
```plaintext
2024-12-03 23:32:03,269 - INFO - Connected to RPC: https://polygon-mainnet.g.alchemy.com/v2/YOUR_RPC_URL
2024-12-03 23:32:04,527 - INFO - Account balance: 9.982008 MATIC
2024-12-03 23:32:05,199 - INFO - Starting mining. Difficulty: 1000
2024-12-03 23:32:19,316 - INFO - Thread 0 found a valid nonce: 1338
2024-12-03 23:32:20,137 - INFO - Thread 0 mined a block. TX Hash: 0xecf01b049a06315b5214fea83577a44b000274978d1889c765ac93fe72962584
```

#### Staking:
```plaintext
2024-12-03 23:45:10,137 - INFO - Connected to RPC: https://polygon-mainnet.g.alchemy.com/v2/YOUR_RPC_URL
2024-12-03 23:45:11,427 - INFO - Successfully staked 100 POLM tokens.
2024-12-03 23:45:12,057 - INFO - Transaction Hash: 0x5f72a2e93b7e4a347f8a6db5e5e743d0e20b7a9e5efb5e79874c6f3c
```

#### Unstaking:
```plaintext
2024-12-03 23:55:20,437 - INFO - Connected to RPC: https://polygon-mainnet.g.alchemy.com/v2/YOUR_RPC_URL
2024-12-03 23:55:21,847 - INFO - Successfully unstaked 100 POLM tokens. Rewards: 5 POLM.
2024-12-03 23:55:22,577 - INFO - Transaction Hash: 0x7d82f9a4b1e4b81b3a924e90b0e5f9b4a4c6d7e4e5f9b6f7a0e7b9d3
```

---

### License
This project is licensed under the **MIT License**.

Happy mining, staking, and growing your Polymine ecosystem! 🚀
