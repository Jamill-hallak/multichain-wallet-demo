import requests

BASE_URL = "http://127.0.0.1:5000"
generated_otp = None  # Global variable to store the generated OTP for verification
generated_address = None  # Global variable to store the generated Ethereum address


def test_generate_wallet():
    global generated_address  # Access the global variable to store the generated address
    response = requests.get(f"{BASE_URL}/wallet/generate-wallet")
    response_data = response.json()
    
    # Extract the Ethereum address from the response
    if response_data.get("status") == "success":
        generated_address = response_data["data"]["address"]
        print("Generate Wallet Response:", response_data)
    else:
        print("Failed to generate wallet:", response_data)


def test_get_balance():
    global generated_address  # Access the global generated address
    if not generated_address:
        print("No address generated. Run test_generate_wallet first.")
        return

    # Fetch balance for the generated Ethereum address
    response = requests.get(f"{BASE_URL}/balance/get-balance/{generated_address}")
    print("Get Balance Response:", response.json())


def test_generate_otp():
    global generated_otp  # Access the global variable to store OTP
    response = requests.post(f"{BASE_URL}/2fa/generate-otp", json={"user_id": "user123"})
    response_data = response.json()
    
    if response_data.get("status") == "success":
        generated_otp = response_data.get("otp")  # Store the OTP for later use
        print("Generate OTP Response:", response_data)
    else:
        print("Failed to generate OTP:", response_data)


def test_verify_otp():
    global generated_otp  # Access the global OTP generated earlier
    if not generated_otp:
        print("No OTP generated. Run test_generate_otp first.")
        return

    response = requests.post(f"{BASE_URL}/2fa/verify-otp", json={"user_id": "user123", "otp": generated_otp})
    print("Verify OTP Response:", response.json())


if __name__ == "__main__":
    print("Testing API Endpoints:")
    
    # Step-by-step execution
    test_generate_wallet()  # Generate wallet and store the address
    test_get_balance()      # Fetch balance for the generated address
    test_generate_otp()     # Generate OTP for 2FA
    test_verify_otp()       # Verify the generated OTP
