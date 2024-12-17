
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