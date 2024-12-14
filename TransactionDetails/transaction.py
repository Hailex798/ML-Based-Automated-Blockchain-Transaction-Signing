import requests
import csv

def fetch_transactions(address, api_key):
    url = f"https://api.etherscan.io/api"
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": api_key
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    if data["status"] == "1":
        transactions = data["result"]
        for tx in transactions[:10]:  # Display first 10 transactions
            print(f"Hash: {tx['hash']}")
            print(f"From: {tx['from']}")
            print(f"To: {tx['to']}")
            print(f"Value: {int(tx['value']) / 1e18} Ether")
            print(f"Gas Price: {int(tx['gasPrice']) / 1e9} Gwei")
            print(f"Block Number: {tx['blockNumber']}")
            print("-" * 50)
        
        # Save to CSV
        save_to_csv(transactions)
        print("Transactions saved to transactions.csv")
    else:
        print("Error:", data["message"])

def save_to_csv(transactions, filename="transactions.csv"):
    keys = transactions[0].keys()
    with open(filename, "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(transactions)

# Replace with your wallet address and API key
wallet_address = "0x4838B106FCe9647Bdf1E7877BF73cE8B0BAD5f97"
api_key = "HSUMDBV98GJYCBZCEQ7HIVY4G32HCACGU6"

fetch_transactions(wallet_address, api_key)

# USER ADDRESS OF WALLET -> https://etherscan.io/address/0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97