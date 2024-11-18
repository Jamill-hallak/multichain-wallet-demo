import requests

BASE_URL = "http://127.0.0.1:5000"
jwt_token = "JBSWY3DPEHPK3PXP"  # Replace with a valid JWT token

def test_generate_solana_wallet():
    headers = {"Authorization": f"Bearer {jwt_token}"}
    response = requests.get(f"{BASE_URL}/solana/wallet", headers=headers)
    print("Status Code:", response.status_code)
    print("Response Data:", response.json())

test_generate_solana_wallet()
