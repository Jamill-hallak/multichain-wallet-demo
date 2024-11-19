import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:5000"
jwt_token = None
generated_solana_address = None
private_key = None

# Load the OTP secret (if used for Solana)
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


def test_generate_solana_wallet():
    global generated_solana_address, private_key
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BASE_URL}/solana/wallet", headers=headers)
    response_data = response.json()


    if response_data.get("status") == "success":
        generated_solana_address = response_data["data"]["address"]
        private_key = response_data["data"]["encrypted_private_key"]
        print("Solana wallet generated successfully:", response_data)
    else:
        print("Failed to generate Solana wallet:", response_data)



def test_get_solana_balance():
    """
    Fetch and display the SOL balance of the generated wallet.
    """
    global generated_solana_address
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not generated_solana_address:
        print("No Solana wallet generated. Run test_generate_solana_wallet first.")
        return

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BASE_URL}/solana/balance/{generated_solana_address}", headers=headers)
    response_data = response.json()

    if response.status_code == 200 and response_data.get("status") == "success":
        balance = response_data.get("balance", 0)
        print(f"Solana wallet balance: {balance} SOL")
    else:
        print("Failed to fetch Solana wallet balance:")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response_data}")


def test_send_solana():
    """
    Send SOL from the generated wallet to a recipient.
    """
    global generated_solana_address, private_key
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not generated_solana_address or not private_key:
        print("No Solana wallet generated. Run test_generate_solana_wallet first.")
        return

    headers = {"Authorization": f"Bearer {jwt_token}"}
    data = {
        "from_address": generated_solana_address,
        "to_address": "recipient_solana_address",  # Replace with a valid recipient address
        "amount": 1.0,  # Test with an amount likely to cause insufficient balance
        "private_key": private_key,
    }
    response = requests.post(f"{BASE_URL}/solana/transaction/send", headers=headers, json=data)
    response_data = response.json()

    if response_data.get("status") == "error" and "Not enough balance" in response_data.get("message", ""):
        print("Test passed: Transaction failed due to insufficient balance.")
    elif response_data.get("status") == "success":
        print("SOL sent successfully:", response_data)
    else:
        print("Test failed: Unexpected response:", response_data)


def test_sign_solana_message():
    """
    Test signing a message using the Solana private key.
    """
    global private_key
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not private_key:
        print("No Solana wallet generated. Run test_generate_solana_wallet first.")
        return

    # Test input
    message = "Hello, this is a Solana test message!"

    headers = {"Authorization": f"Bearer {jwt_token}"}
    data = {"message": message, "private_key": private_key}

    # Send request
    response = requests.post(f"{BASE_URL}/solana/sign-message", headers=headers, json=data)
    response_data = response.json()

    if response_data.get("status") == "success":
        signed_message = response_data["data"]
        print(f"Test passed: Signed message is valid. Signed message: {signed_message}")
    else:
        print("Test failed: API response indicates an error.", response_data)


if __name__ == "__main__":
    print("Testing Solana API Endpoints:")
    login()  # Log in to get JWT token
    test_generate_solana_wallet()  # Generate Solana wallet
    test_get_solana_balance()  # Fetch and display Solana wallet balance
    #test_send_solana()  # Attempt to send SOL
    #test_sign_solana_message()  # Test Solana message signing
