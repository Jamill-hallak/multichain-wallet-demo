import requests

def test_generate_wallet():
    url = "http://localhost:5000/generate-wallet"
    response = requests.get(url)
    if response.status_code == 200:
        print("Test Passed:", response.json())
    else:
        print("Test Failed:", response.status_code, response.text)

if __name__ == "__main__":
    test_generate_wallet()
