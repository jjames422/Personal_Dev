import os
import json
import redis
from web3 import Web3
import docx

# Initialize Redis
r = redis.Redis()

# Web3 Initialization
infura_url = "https://mainnet.infura.io/v3/503e90fc852a499b974ec64e229f6def"  # Your actual Infura project ID
w3 = Web3(Web3.HTTPProvider(infura_url))

UPLOAD_DIR = "/home/clientuser/uploads/"  # Updated directory where the uploaded file is stored

def list_files():
    return [f for f in os.listdir(UPLOAD_DIR) if os.path.isfile(os.path.join(UPLOAD_DIR, f))]

def parse_mt103(filepath):
    doc = docx.Document(filepath)
    content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return extract_mt103_data(content)

def extract_mt103_data(content):
    data = {}
    for line in content.split('\n'):
        if "TRANSACTION NUMBER:" in line:
            data["transaction_number"] = line.split("TRANSACTION NUMBER:")[1].strip()
        elif "AMOUNT:" in line:
            data["amount"] = clean_amount(line.split("AMOUNT:")[1].strip())
        elif "CURRENCY:" in line:
            data["currency"] = line.split("CURRENCY:")[1].strip()
        elif "STATUS:" in line:
            data["status"] = line.split("STATUS:")[1].strip()
        elif "BIC SENDER:" in line:
            data["bic_sender"] = line.split("BIC SENDER:")[1].strip()
        elif "SENDER NAME:" in line:
            data["sender_name"] = line.split("SENDER NAME:")[1].strip()
        elif "BENEFICIARY NAME:" in line:
            data["beneficiary_name"] = line.split("BENEFICIARY NAME:")[1].strip()
    return data

def clean_amount(amount_str):
    return float(amount_str.strip().replace(",", "").replace("OO", "00"))

def convert_currency(data):
    amount = data["amount"]
    currency = data["currency"]
    target_currency = input("Select the target currency:\n1. USDC\n2. USDT\n3. ETH\nEnter choice (1-3): ")
    if target_currency == "1":
        conversion_rate = 1.18
        target_currency = "USDC"
    elif target_currency == "2":
        conversion_rate = 1.18
        target_currency = "USDT"
    else:
        conversion_rate = 0.00042
        target_currency = "ETH"
    converted_amount = amount * conversion_rate
    print(f"Using fallback rate: 1 EUR = {conversion_rate} {target_currency}")
    print(f"Converted amount: {converted_amount} {target_currency}")
    print(f"Estimated gas fee: {w3.from_wei(estimate_gas_fee(), 'ether')} ETH")
    confirmation = input(f"Proceeding with this transaction will deduct {converted_amount} {target_currency} and a gas fee of {w3.from_wei(estimate_gas_fee(), 'ether')} ETH from the master wallet.\nDo you want to continue? (yes/no): ")
    if confirmation.lower() == 'yes':
        update_master_wallet(converted_amount, target_currency)
    else:
        print("Transaction cancelled.")

def estimate_gas_fee():
    gas_price = w3.to_wei('50', 'gwei')
    gas_limit = 21000
    return gas_price * gas_limit

def update_master_wallet(amount, target_currency):
    master_wallet_key = f"MASTER_WALLET_{target_currency}"
    master_wallet_data = r.get(master_wallet_key)
    if not master_wallet_data:
        print(f"Master wallet for {target_currency} not found in Redis.")
        return
    master_wallet = json.loads(master_wallet_data)
    master_wallet["balance"] += amount
    r.set(master_wallet_key, json.dumps(master_wallet))
    print(f"Updated master wallet balance: {master_wallet['balance']} {target_currency}")

    if target_currency == "ETH":
        gas_fee_address, gas_fee_private_key = ensure_gas_fee_wallet_balance(estimate_gas_fee())
        send_eth(master_wallet["address"], amount, master_wallet["private_key"], gas_fee_address, gas_fee_private_key)

def send_eth(to_address, amount, master_wallet_private_key, gas_fee_wallet_address, gas_fee_wallet_private_key):
    gas_limit = 21000
    gas_price = w3.to_wei('50', 'gwei')
    tx_cost = gas_limit * gas_price
    gas_fee_wallet_balance = get_wallet_balance(gas_fee_wallet_private_key)
    
    print(f"Gas fee wallet balance: {w3.from_wei(gas_fee_wallet_balance, 'ether')} ETH")
    print(f"Estimated gas fee: {w3.from_wei(tx_cost, 'ether')} ETH")
    
    if gas_fee_wallet_balance < tx_cost:
        print(f"Insufficient ETH balance in gas fee wallet to cover the gas fee. Required: {w3.from_wei(tx_cost, 'ether')} ETH, Available: {w3.from_wei(gas_fee_wallet_balance, 'ether')} ETH")
        return

    # Deduct the gas fee from the gas fee wallet
    gas_tx = {
        'to': gas_fee_wallet_address,
        'value': 0,
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': w3.eth.get_transaction_count(gas_fee_wallet_address)
    }
    signed_gas_tx = w3.eth.account.sign_transaction(gas_tx, gas_fee_wallet_private_key)
    gas_tx_hash = w3.eth.send_raw_transaction(signed_gas_tx.rawTransaction)
    print(f"Gas fee transaction sent with hash: {gas_tx_hash.hex()}")

    # Transfer the actual amount from the master wallet
    tx = {
        'to': to_address,
        'value': w3.to_wei(amount, 'ether'),
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': w3.eth.get_transaction_count(w3.eth.account.from_key(master_wallet_private_key).address)
    }
    signed_tx = w3.eth.account.sign_transaction(tx, master_wallet_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transaction sent with hash: {tx_hash.hex()}")

def get_wallet_balance(private_key):
    address = w3.eth.account.from_key(private_key).address
    return w3.eth.get_balance(address)

def ensure_gas_fee_wallet_balance(required_balance):
    gas_fee_wallet_key = "GAS_FEE_WALLET"
    gas_fee_wallet_data = r.get(gas_fee_wallet_key)
    
    if not gas_fee_wallet_data:
        address, private_key = create_wallet()
        gas_fee_wallet = {"address": address, "private_key": private_key}
        r.set(gas_fee_wallet_key, json.dumps(gas_fee_wallet))
        print(f"Created new gas fee wallet: {address}")
    else:
        gas_fee_wallet = json.loads(gas_fee_wallet_data)
    
    gas_fee_wallet_balance = get_wallet_balance(gas_fee_wallet["private_key"])
    if gas_fee_wallet_balance < required_balance:
        amount_needed = required_balance - gas_fee_wallet_balance
        transfer_eth(master_wallet["private_key"], gas_fee_wallet["address"], w3.from_wei(amount_needed, 'ether'))

    return gas_fee_wallet["address"], gas_fee_wallet["private_key"]

def create_wallet():
    account = w3.eth.account.create()
    return account.address, account.key.hex()

def transfer_eth(from_private_key, to_address, amount_eth):
    gas_limit = 21000
    gas_price = w3.to_wei('50', 'gwei')
    tx_cost = gas_limit * gas_price
    total_transfer_cost = tx_cost + w3.to_wei(amount_eth, 'ether')
    
    from_address = w3.eth.account.from_key(from_private_key).address
    from_balance = get_wallet_balance(from_private_key)

    if from_balance < total_transfer_cost:
        print(f"Insufficient balance in the from wallet. Required: {w3.from_wei(total_transfer_cost, 'ether')} ETH, Available: {w3.from_wei(from_balance, 'ether')} ETH")
        return
    
    tx = {
        'to': to_address,
        'value': w3.to_wei(amount_eth, 'ether'),
        'gas': gas_limit,
        'gasPrice': gas_price,
        'nonce': w3.eth.get_transaction_count(from_address)
    }
    signed_tx = w3.eth.account.sign_transaction(tx, from_private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Transferred {amount_eth} ETH to {to_address} with hash: {tx_hash.hex()}")

if __name__ == "__main__":
    files = list_files()
    if not files:
        print("No files found in the upload directory.")
        exit(0)
    print("Select the file to process:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    file_choice = int(input(f"Enter the number of the file to process (1-{len(files)}): ")) - 1
    data = parse_mt103(os.path.join(UPLOAD_DIR, files[file_choice]))
    convert_currency(data)
