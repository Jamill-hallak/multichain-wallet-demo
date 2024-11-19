import os
from dotenv import load_dotenv
import requests
from cryptography.fernet import Fernet

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:5000"
jwt_token = None
generated_solana_address = None
encrypted_private_key = None

# Load encryption key for decrypting the private key
encryption_key = os.getenv("ENCRYPTION_KEY")
if not encryption_key:
    raise ValueError("ENCRYPTION_KEY not found in environment variables.")
fernet = Fernet(encryption_key.encode())


def decrypt_private_key(encrypted_key):
    """
    Decrypt the encrypted private key.
    """
    try:
        return fernet.decrypt(encrypted_key.encode()).decode()
    except Exception as e:
        print(f"Failed to decrypt private key. Error: {e}")
        raise


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
    """
    Generate a Solana wallet using the API.
    """
    global generated_solana_address, encrypted_private_key

    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BASE_URL}/solana/wallet", headers=headers)
    response_data = response.json()

    if response_data.get("status") == "success":
        generated_solana_address = response_data["data"]["address"]
        encrypted_private_key = response_data["data"]["encrypted_private_key"]
        print("Solana wallet generated successfully:", response_data)
    else:
        print("Failed to generate Solana wallet:", response_data)


def test_sign_solana_message():
    """
    Sign a message using the Solana private key.
    """
    global encrypted_private_key

    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not encrypted_private_key:
        print("No Solana wallet generated. Run test_generate_solana_wallet first.")
        return

    try:
        # Decrypt the private key
        private_key = decrypt_private_key(encrypted_private_key)

        # Test message
        message = "Hello, this is a Solana test message!"

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }
        data = {
            "message": message,
            "private_key": private_key,  # Decrypted private key (32 bytes)
        }

        # Send request to signing route
        response = requests.post(f"{BASE_URL}/solana/signing/sign-message", headers=headers, json=data)
        response_data = response.json()

        if response.status_code == 200 and response_data.get("status") == "success":
            signed_message = response_data["data"]
            print(f"Message: {signed_message['message']}")
            print(f"Signature: {signed_message['signature']}")
            print(f"Test passed: Signed message is valid.")

        else:
            print("Test failed: API response indicates an error.")
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {response_data}")

    except Exception as e:
        print(f"Failed to decrypt private key or sign message. Error: {e}")


if __name__ == "__main__":
    print("Testing Solana API Endpoints...")
    login()
    test_generate_solana_wallet()
    test_sign_solana_message()
