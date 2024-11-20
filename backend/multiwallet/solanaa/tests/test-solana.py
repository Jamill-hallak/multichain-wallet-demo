import os
from dotenv import load_dotenv
import requests
from cryptography.fernet import Fernet
from solders.keypair import Keypair  # For deriving keypair from seed

# Load environment variables
load_dotenv()

BASE_URL = "http://127.0.0.1:5000"
jwt_token = None
generated_solana_address = None
encrypted_private_key = None
encrypted_seed = None  # Global variable for encrypted seed

# Load encryption key for decrypting the seed or private key
encryption_key = os.getenv("ENCRYPTION_KEY")
if not encryption_key:
    raise ValueError("ENCRYPTION_KEY not found in environment variables.")
fernet = Fernet(encryption_key.encode())


def decrypt_seed(encrypted_seed):
    """
    Decrypt the encrypted seed.
    """
    try:
        return fernet.decrypt(encrypted_seed.encode()).decode()
    except Exception as e:
        print(f"Failed to decrypt seed. Error: {e}")
        raise


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
    try:
        response = requests.post(
            f"{BASE_URL}/ethereum/auth/login",
            json={"user_id": "user123", "password": "password123"}
        )
        response_data = response.json()

        if response_data.get("status") == "success":
            jwt_token = response_data["token"]
            print("Login successful:", response_data)
        else:
            print("Failed to log in:", response_data)
    except Exception as e:
        print(f"Login failed due to an error: {e}")


def test_generate_solana_wallet():
    """
    Generate a Solana wallet using the API.
    """
    global generated_solana_address, encrypted_private_key, encrypted_seed

    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    try:
        headers = {"Authorization": f"Bearer {jwt_token}"}
        response = requests.get(f"{BASE_URL}/solana/wallet", headers=headers)
        response_data = response.json()
        if response_data.get("status") == "success":
            generated_solana_address = response_data["data"]["address"]
            encrypted_private_key = response_data["data"]["encrypted_private_key"]
            encrypted_seed = response_data["data"].get("encrypted_seed")
            if not encrypted_seed:
                print("Warning: 'encrypted_seed' not found in response.")
            print("Solana wallet generated successfully:", response_data)
        else:
            print("Failed to generate Solana wallet:", response_data)
    except Exception as e:
        print(f"Failed to generate Solana wallet due to an error: {e}")


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


def test_solana_transaction():
    """
    Test Solana transaction by simulating a transfer with insufficient balance.
    """
    if not jwt_token:
        print("No JWT token. Run login() first.")
        return

    if not generated_solana_address or not encrypted_seed:
        print("No Solana wallet generated or seed not available. Run test_generate_solana_wallet first.")
        return

    try:
        # Decrypt the seed
        seed = decrypt_seed(encrypted_seed)
        seed_bytes = bytes.fromhex(seed)
        if len(seed_bytes) != 32:
            raise ValueError("Seed must be 32 bytes long.")

        # Derive Keypair from the seed
        signer_keypair = Keypair.from_seed(seed_bytes)
        derived_from_address = str(signer_keypair.pubkey())
        if derived_from_address != generated_solana_address:
            print("Error: Seed does not match the generated Solana address.")
            return

        recipient_address = "7yXjgkYGpsZ5WJjtoDiAk3qaGWzmRXF25gCYm8RwYBLh"

        # Attempting to transfer an amount likely exceeding the wallet's balance
        transfer_amount = 10_000  # Adjust this based on the system's expected balance threshold

        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Content-Type": "application/json",
        }
        data = {
            "from_address": generated_solana_address,
            "to_address": recipient_address,
            "amount": transfer_amount,
            "seed": seed,  # Use the decrypted seed
        }

        # Send request to transaction route
        response = requests.post(f"{BASE_URL}/solana/transaction/send", headers=headers, json=data)
        response_data = response.json()
        if response.status_code in [400, 500] and (
            "Insufficient balance" in response_data.get("message", "") or
            "Attempt to debit an account but found no record of a prior credit" in response_data.get("message", "")
        ):
            print("Test passed: Transaction failed as expected due to insufficient balance.")
        elif response.status_code != 200:
            print("Test failed: Unexpected error occurred during the transaction.")
            print(f"Status Code: {response.status_code}")
            print(f"Response Data: {response_data}")
        else:
            print("Test failed: Transaction succeeded unexpectedly.")
            print("Response Data:", response_data)

    except Exception as e:
        print(f"Error occurred while testing the transaction. Error: {e}")



if __name__ == "__main__":
    print("Testing Solana API Endpoints...")
    login()
    test_generate_solana_wallet()
    test_sign_solana_message()
    test_solana_transaction()
