# from flask import Flask, request, jsonify

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return jsonify({"message": "Welcome to the Blockchain Signing API!"})

# @app.route('/sign', methods=['POST'])
# def sign_transaction():
#     # Get the JSON data from the request
#     data = request.get_json()

#     # Print the received data for debugging purposes
#     print("Received data:", data)
    
#     # Check if 'transaction' is provided in the data
#     if not data or 'transaction' not in data:
#         return jsonify({"status": "error", "message": "Transaction data missing"}), 400

#     # Extract the transaction data
#     transaction = data['transaction']
    
#     # Print the transaction data for debugging purposes
#     print("Transaction data:", transaction)
    
#     # Simulate signing the transaction (you can replace this with actual signing logic)
#     signed_transaction = f"Signed: {transaction}"

#     # Return the signed transaction
#     return jsonify({"status": "success", "signed_transaction": signed_transaction})

# if __name__ == '__main__':
#     # Run the Flask app
#     app.run(debug=True)




from flask import Flask, request, jsonify
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

app = Flask(__name__)

# Generate private and public keys for signing (you would typically store these securely)
private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
public_key = private_key.public_key()

@app.route('/')
def home():
    return {"message": "Welcome to the Blockchain Signing API!"}

@app.route('/sign', methods=['POST'])
def sign_transaction():
    # Get the transaction data from the request
    data = request.get_json()
    
    # Check if transaction data is provided
    if not data or 'transaction' not in data:
        return jsonify({"status": "error", "message": "Transaction data is missing"}), 400
    
    transaction = data['transaction']
    
    # Validate required fields
    required_fields = ['from', 'to', 'value', 'gas', 'gasPrice', 'nonce']
    for field in required_fields:
        if field not in transaction:
            return jsonify({"status": "error", "message": f"{field} is required"}), 400
    
    # Perform cryptographic signing
    try:
        # Convert the transaction data to a string and encode it as bytes
        transaction_data = str(transaction).encode('utf-8')
        
        # Hash the transaction data
        hashed_data = hashes.Hash(hashes.SHA256())
        hashed_data.update(transaction_data)
        digest = hashed_data.finalize()

        # Sign the transaction using the private key
        signature = private_key.sign(
            digest,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )

        # Convert the signature to hexadecimal format for readability
        signed_transaction = signature.hex()

        return jsonify({"status": "success", "signed_transaction": signed_transaction})

    except Exception as e:
        # Handle any exceptions during the signing process
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# from web3 import Web3
# from eth_account import Account

# # Initialize Flask app
# app = Flask(__name__)

# # Connect to Ethereum node (local Ganache instance or remote node)
# w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))  # Change this URL if needed (for Ganache or Infura)

# # Check if connection is successful
# if not w3.is_connected():
#     print("Failed to connect to the Ethereum node.")
#     exit()

# # Home route
# @app.route('/')
# def home():
#     return {"message": "Welcome to the Blockchain Signing API!"}

# # Sign transaction route
# @app.route('/sign', methods=['POST'])
# def sign_transaction():
#     data = request.get_json()  # Get the JSON data from the request
#     if not data or 'transaction' not in data:
#         return jsonify({"status": "error", "message": "Transaction data is required"}), 400

#     transaction = data['transaction']
    
#     # Check if the necessary fields are present in the transaction data
#     required_fields = ['from', 'to', 'value', 'gas', 'gasPrice', 'nonce']
#     for field in required_fields:
#         if field not in transaction:
#             return jsonify({"status": "error", "message": f"{field} is missing from transaction data"}), 400
    
#     # Simulate the private key (In a real scenario, use your wallet's private key)
#     private_key = "0x8665f0e05ac6d6385992893062c82ef0cb78b9da94824b9d05188a5bc0aa5795"  # Replace with your actual private key
#     account = Account.privateKeyToAccount(private_key)
    
#     # Prepare the transaction
#     tx = {
#         'from': transaction['from'],
#         'to': transaction['to'],
#         'value': w3.toWei(transaction['value'], 'ether'),  # Convert value to Wei
#         'gas': transaction['gas'],
#         'gasPrice': w3.toWei(transaction['gasPrice'], 'gwei'),  # Convert gasPrice to Gwei
#         'nonce': transaction['nonce'],
#         'chainId': 1337  # Chain ID for Ganache (replace with the correct one for your network)
#     }

#     # Sign the transaction
#     signed_tx = w3.eth.account.signTransaction(tx, private_key)
    
#     # Send the signed transaction
#     try:
#         txn_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
#         receipt = w3.eth.waitForTransactionReceipt(txn_hash)
#         print("Transaction Receipt:", receipt)

#         return jsonify({
#             "status": "success",
#             "signed_transaction": signed_tx.rawTransaction.hex(),
#             "txn_hash": txn_hash.hex(),  # Return the transaction hash as confirmation
#             "receipt": receipt
#         })
#     except Exception as e:
#         return jsonify({"status": "error", "message": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
