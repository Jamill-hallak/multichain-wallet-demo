
# Multichain Wallet Demo

## Overview

This project demonstrates a **multi-wallet system** capable of managing wallets and transactions on multiple blockchain platforms, specifically **Ethereum** and **Solana**. It features wallet generation, message signing, balance checks, and transaction handling with robust testing for real-world scenarios.

## Features

### Ethereum:
- Wallet generation and encrypted private key storage.
- Message signing and validation.
- Transaction creation and simulation.
- Insufficient balance detection with proper error handling.

### Solana:
- Wallet generation with seed encryption.
- Message signing and validation.
- Transaction creation and simulation.
- Error handling for insufficient balance and non-existent accounts.

## Project Structure

```
multichain-wallet-demo/
├── backend/
│   ├── multiwallet/
│   │   ├── ethereum/          # Ethereum-specific logic
│   │   │   ├── middleware/    # JWT authentication and middleware
│   │   │   ├── routes/        # Ethereum API routes
│   │   │   ├── services/      # Ethereum business logic
│   │   │   └── tests/         # Ethereum test cases
│   │   ├── solana/            # Solana-specific logic
│   │   │   ├── middleware/    # JWT authentication and middleware
│   │   │   ├── routes/        # Solana API routes
│   │   │   ├── services/      # Solana business logic
│   │   │   └── tests/         # Solana test cases
│   │   ├── _init_.py          # empty module
│   │   ├── app.py             # App Logic
│   │   ├── requirements.txt   # Python dependencies
│   │   └── docker-compose.yml # Docker setup for deployment(need some fix)
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Jamill-hallak/multichain-wallet-demo.git
   cd multichain-wallet-demo/backend/multiwallet
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate    # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Create a `.env` file in the `backend/multiwallet` directory with the following keys:
   ```env
   SOLANA_RPC_URL=https://solana-devnet.g.alchemy.com/v2/your-alchemy-key
   SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/your-alchemy-key
   TP_SECRET=JBSWY3DPEHPK3PXP
   ENCRYPTION_KEY=LWKSesyVJ-JpaxqH_0kn7hByu91d7Xu1ldKi8R7sPWk=

   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Testing

### Ethereum Tests
Run the Ethereum-specific tests:
```bash
python test-ethereum.py
```

### Solana Tests
Run the Solana-specific tests:
```bash
python test-solana.py
```

## Technologies Used
- **Blockchain Platforms**: Ethereum, Solana
- **Programming Language**: Python
- **Web Framework**: Flask
- **API Testing**: Postman, Requests library
- **Environment Management**: Docker

## Future Enhancements
- Add support for more blockchain platforms like Binance Smart Chain or Polygon.
- Implement real-time transaction monitoring.
- Extend the test suite to cover more edge cases and integration scenarios.

## Author
Jamil Hallack
## License
This project is licensed under the MIT License. See the LICENSE file for details.
