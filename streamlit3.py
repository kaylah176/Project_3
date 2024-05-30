import streamlit as st
from web3 import Web3
import requests
import matplotlib.pyplot as plt
from zillow_doc1 import rapid_api_caller # Import the required function from zillow_doc1

# Connect to the Ethereum network
infura_url = "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = "0xaE036c65C649172b43ef7156b009c6221B596B8b"
contract_abi = [
    {
        "constant": False,
        "inputs": [
            {
                "name": "beneficiary",
                "type": "address"
            }
        ],
        "name": "buyTokens",
        "outputs": [],
        "payable": True,
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "distributeDividends",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [],
        "name": "renounceOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "to",
                "type": "address"
            },
            {
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "transfer",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "constant": False,
        "inputs": [
            {
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "transferOwnership",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "name": "rate",
                "type": "uint256"
            },
            {
                "name": "wallet",
                "type": "address"
            },
            {
                "name": "token",
                "type": "address"
            },
            {
                "name": "location",
                "type": "string"
            },
            {
                "name": "squareFeet",
                "type": "uint256"
            },
            {
                "name": "appraisalValue",
                "type": "uint256"
            },
            {
                "name": "propertyType",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "payable": True,
        "stateMutability": "payable",
        "type": "fallback"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "purchaser",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "beneficiary",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            },
            {
                "indexed": False,
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "TokensPurchased",
        "type": "event"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "isOwner",
        "outputs": [
            {
                "name": "",
                "type": "bool"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "minimumHoldingPeriod",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "property",
        "outputs": [
            {
                "name": "location",
                "type": "string"
            },
            {
                "name": "yearbuilt",
                "type": "uint256"
            },
            {
                "name": "squareFeet",
                "type": "uint256"
            },
            {
                "name": "purchaseprice",
                "type": "uint256"
            },
            {
                "name": "appraisalValue",
                "type": "uint256"
            },
            {
                "name": "propertyType",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "rate",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "token",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "tokenHolders",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "name": "tokenHoldingStartTime",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "wallet",
        "outputs": [
            {
                "name": "",
                "type": "address"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "weiRaised",
        "outputs": [
            {
                "name": "",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

# Load the contract
contract = web3.eth.contract(address=contract_address, abi=contract_abi)

st.title("Real Estate Token Interface")

# Add a description paragraph
st.markdown("""
    Welcome to AssetCoin! This platform allows you to buy and manage tokens representing shares in a real estate asset.
""")

# Tabs for different functionalities
tab1, tab2, tab3 = st.tabs(["💸 Buy Tokens", "💰 View Token Price", "📈 Real Estate Value"])

with tab1:
    st.subheader("Buy Tokens")
    user_address = st.text_input("User Address")
    private_key = st.text_input("Private Key", type="password")
    amount = st.number_input("Amount", min_value=0.0, step=0.01)

    if st.button("Buy Tokens"):
        try:
            nonce = web3.eth.getTransactionCount(user_address)
            txn = contract.functions.buyTokens(user_address).buildTransaction({
                'chainId': 4,  # Rinkeby testnet
                'gas': 70000,
                'gasPrice': web3.toWei('1', 'gwei'),
                'nonce': nonce,
                'value': web3.toWei(amount, 'ether')
            })
            signed_txn = web3.eth.account.signTransaction(txn, private_key)
            tx_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
            st.success(f"Transaction submitted with hash: {web3.toHex(tx_hash)}")
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.subheader("View Token Price")
    try:
        token_price = contract.functions.rate().call()
        st.write(f"The current token price is {web3.fromWei(token_price, 'ether')} ETH")
    except Exception as e:
        st.error(f"Error fetching token price: {e}")

with tab3:
    st.subheader("Real Estate Value")
    zpid = "15302053"  # Example property ID, replace with actual ID

    if st.button("Refresh Price"):
        try:
            # Fetch property value using the rapid_api_caller function from zillow_doc1
            response = rapid_api_caller()
            if response.status_code == 200:
                property_data = response.json()
                value = property_data['zestimate']['amount']
                st.write(f"Current value of the property: ${value} USD")

                # Example data: replace with actual data fetching
                dates = ["2024-01-01", "2024-02-01", "2024-03-01", "2024-04-01", "2024-05-01"]
                values = [value, value * 0.98, value * 1.02, value * 1.01, value * 1.03]

                # Plotting the data
                plt.figure(figsize=(10, 5))
                plt.plot(dates, values, marker='o')
                plt.xlabel("Date")
                plt.ylabel("Value (USD)")
                plt.title("Real Estate Asset Value Over Time")
                plt.grid(True)
                plt.xticks(rotation=45)
                st.pyplot(plt)
            else:
                st.error("Failed to fetch property value from Zillow API")
        except Exception as e:
            st.error(f"Error: {e}")
