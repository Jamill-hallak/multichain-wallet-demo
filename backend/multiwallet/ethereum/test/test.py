import os
from dotenv import load_dotenv
import pyotp
import requests
from eth_account.messages import encode_defunct
from web3.auto import w3
import hashlib

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:5000"
jwt_token = None
generated_address = None
encrypted_private_key = None

# Load the OTP secret from the .env file
otp_secret = os.getenv("OTP_SECRET")
if not otp_secret:
    raise ValueError("OTP_SECRET not found in environment variables.")


def login():
    """
    Log in to the application and obtain a JWT token.
    """
    global jwt_token
    response = requests.post(f"{BASE_URL}/ethereum/auth/login", json={"user_id": "user123", "password": "password123"})
    response_data = response.json()

    if response_data.get("status") == "success":
        jwt_token = response_data["token"]
        print("Login successful:", response_data)
    else:
        print("Failed to log in:", response_data)


def test_generate_wallet():
    """
    Generate a new Ethereum wallet.
    """
    global generated_address, encrypted_private_key
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BASE_URL}/ethereum/wallet/generate", headers=headers)
    response_data = response.json()

    if response_data.get("status") == "success":
        generated_address = response_data["data"]["address"]
        encrypted_private_key = response_data["data"]["encrypted_private_key"]
        print("Wallet generated successfully:", response_data)
    else:
        print("Failed to generate wallet:", response_data)


def test_get_balance():
    """
    Fetch and display the ETH balance of the generated wallet.
    """
    global generated_address
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not generated_address:
        print("No wallet generated. Run test_generate_wallet first.")
        return

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BASE_URL}/ethereum/balance/eth/{generated_address}", headers=headers)
    response_data = response.json()

    if response_data.get("status") == "success":
        balance = response_data.get("balance", 0)
        print(f"Wallet balance: {balance} ETH")
    else:
        print("Failed to fetch wallet balance:", response_data)


def test_send_eth():
    """
    Send ETH from the generated wallet to a recipient.
    Passes if the transaction fails due to insufficient balance.
    """
    global generated_address, encrypted_private_key
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not generated_address or not encrypted_private_key:
        print("No wallet generated. Run test_generate_wallet first.")
        return

    # Generate a dynamic OTP using the loaded OTP secret
    totp = pyotp.TOTP(otp_secret)
    otp = totp.now()

    headers = {"Authorization": f"Bearer {jwt_token}"}
    data = {
        "from_address": generated_address,
        "to_address": "0x9728875Fa171c008B183dD1e8aE987acb2A1919A",  # Replace with a valid recipient address
        "amount": 10.0,  # Set an amount likely to exceed the wallet's balance
        "encrypted_private_key": encrypted_private_key,
        "otp": otp
    }
    response = requests.post(f"{BASE_URL}/ethereum/transaction/send-eth", headers=headers, json=data)
    response_data = response.json()

    if response_data.get("status") == "error" and "Not enough balance" in response_data.get("message", ""):
        print("Test passed: Transaction failed due to insufficient balance.")
    elif response_data.get("status") == "success":
        print("ETH sent successfully:", response_data)
    else:
        print("Test failed: Unexpected response:", response_data)


def test_gas_estimation():
    """
    Estimate gas for a transaction.
    """
    global generated_address
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not generated_address:
        print("No wallet generated. Run test_generate_wallet first.")
        return

    headers = {"Authorization": f"Bearer {jwt_token}"}
    data = {
        "from_address": generated_address,
        "to_address": "0x9728875Fa171c008B183dD1e8aE987acb2A1919A",  # Replace with a valid recipient address
        "amount": 0.01
    }
    response = requests.post(f"{BASE_URL}/ethereum/gas-estimation/estimate-gas", headers=headers, json=data)
    response_data = response.json()
    
    if response_data.get("status") == "success":
        gas_estimate = response_data["data"]["gas_estimate"]
        gas_price = response_data["data"]["gas_price"]
        print(f"Gas estimate: {gas_estimate}, Gas price: {gas_price}")
    elif " Insufficient funds for gas estimation" in response_data.get("message", ""):
        print("Test passed: Gas estimation failed due to insufficient funds")
    else:
        print("Failed to estimate gas:", response_data)
        
        

def test_sign_message():
    """
    Test signing a message and validate the response using Ethereum's message hash logic.
    """
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    # Test input
    message = "Hello, this is a test message!"
    private_key = "0x4c0883a69102937d6231471b5dbb6204fe512961708279f02d5bb9040e1ef2b1"

    # Headers and request data
    headers = {"Authorization": f"Bearer {jwt_token}"}
    data = {"message": message, "private_key": private_key}

    # Send request
    response = requests.post(f"{BASE_URL}/ethereum/signing/sign-message", headers=headers, json=data)
    response_data = response.json()

    if response_data.get("status") == "success":
        signed_message = response_data["data"]

        # Extract the signed message components
        signature = signed_message.get("signature")
        message_hash = signed_message.get("message_hash")

        # Validate the signature and hash
        if not signature or not message_hash:
            print("Test failed: Signature or message hash is missing in the response.")
            return

        # Recompute the hash using Ethereum's encoding
        encoded_message = encode_defunct(text=message)
        computed_hash = w3.keccak(encoded_message.body).hex()

        # Check if the hash matches
        if computed_hash != message_hash:
            print(f"Test failed: Computed hash ({computed_hash}) does not match the returned hash ({message_hash}).")
        else:
            print(f"Test passed: Signed message is valid. Signed message: {signed_message}")
    else:
        print("Test failed: API response indicates an error.", response_data)

if __name__ == "__main__":
    print("Testing API Endpoints:")
    login()  # Log in to get JWT token
    test_generate_wallet()  # Generate wallet and store the address
    test_get_balance()  # Fetch and display the wallet balance
    test_sign_message()
    test_gas_estimation() #test estimation gas 
    test_send_eth()  # Attempt to send ETH and handle insufficient balance gracefully