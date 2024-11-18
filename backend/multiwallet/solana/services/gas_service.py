from solana.rpc.api import Client

class GasService:
    def __init__(self, rpc_url):
        self.client = Client(rpc_url)

    def get_fees(self):
        """
        Fetch the current fee structure for Solana transactions.
        Returns:
            dict: The fee structure, including the base fee.
        """
        try:
            response = self.client.get_fee_calculator_for_blockhash()
            if "result" in response and response["result"]["value"]:
                fee_calculator = response["result"]["value"]["fee_calculator"]
                return {"lamports_per_signature": fee_calculator["lamports_per_signature"]}
            else:
                raise ValueError("Failed to fetch fee data.")
        except Exception as e:
            raise ValueError(f"Failed to retrieve fees. Error: {str(e)}")
