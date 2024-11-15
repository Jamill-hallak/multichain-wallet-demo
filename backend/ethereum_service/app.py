from flask import Flask, jsonify
from wallet import EthereumWallet

app = Flask(__name__)

@app.route("/generate-wallet", methods=["GET"])
def generate_wallet():
    """
    API endpoint to generate an Ethereum wallet.
    """
    try:
        eth_wallet = EthereumWallet()
        wallet = eth_wallet.generate_wallet()
        return jsonify({
            "status": "success",
            "data": wallet
        }), 200
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
