import os
from dotenv import load_dotenv
import pyotp
import requests

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
    response = requests.post(f"{BASE_URL}/auth/login", json={"user_id": "user123", "password": "password123"})
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
    response = requests.get(f"{BASE_URL}/wallet/generate", headers=headers)
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
    response = requests.get(f"{BASE_URL}/balance/eth/{generated_address}", headers=headers)
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
    response = requests.post(f"{BASE_URL}/transaction/send-eth", headers=headers, json=data)
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
    response = requests.post(f"{BASE_URL}/gas-estimation/estimate-gas", headers=headers, json=data)
    response_data = response.json()
    
    if response_data.get("status") == "success":
        gas_estimate = response_data["data"]["gas_estimate"]
        gas_price = response_data["data"]["gas_price"]
        print(f"Gas estimate: {gas_estimate}, Gas price: {gas_price}")
    elif " Insufficient funds for gas estimation" in response_data.get("message", ""):
        print("Test passed: Gas estimation failed due to insufficient funds")
    else:
        print("Failed to estimate gas:", response_data)
        
        
        
if __name__ == "__main__":
    print("Testing API Endpoints:")
    login()  # Log in to get JWT token
    test_generate_wallet()  # Generate wallet and store the address
    test_get_balance()  # Fetch and display the wallet balance
    test_gas_estimation() #test estimation gas 
    test_send_eth()  # Attempt to send ETH and handle insufficient balance gracefully
