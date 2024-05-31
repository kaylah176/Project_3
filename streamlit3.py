import streamlit as st
from web3 import Web3
import requests
import matplotlib.pyplot as plt
from zillow_doc2 import call_house_prices, call_photos 
import math 
import pandas as pd

# Connect to the Ethereum network
infura_url = "https://rinkeby.infura.io/v3/YOUR_INFURA_PROJECT_ID"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Contract details
contract_address = "0x15fb46E1A5d56872052bADE0cABc1Ea479186F90"
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

# Function to get details of an NFT 
def get_nft_details(token_id):
    owner = contract.functions.ownerOf(token_id).call()
    token_uri = contract.functions.tokenURI(token_id).call()
    return owner, token_uri

# Function to transfer an NFT 
def transfer_nft(token_id, to_address, private_key):
    nonce = web3.eth.getTransactionCount(web3.eth.defaultAccount)
    txn = contract.functions.safeTransferFrom(web3.eth.defaultAccount, to_address, token_id).buildTransaction({
        'chainId': 4,  # Rinkeby testnet ID
        'gas': 70000,
        'gasPrice': web3.toWei('1', 'gwei'),
        'nonce': nonce,
    })

    signed_txn = web3.eth.account.signTransaction(txn, private_key)
    txn_hash = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
    return web3.toHex(txn_hash)

# UI for NFT functionalities
st.header("NFT Section")

token_id = st.number_input("Token ID", min_value=0, format="%d")
if st.button("Get NFT Details"):
    owner, token_uri = get_nft_details(token_id)
    st.write(f"Owner: {owner}")
    st.write(f"Token URI: {token_uri}")

to_address = st.text_input("Recipient Address for NFT Transfer")
private_key = st.text_input("Your Private Key", type="password")
if st.button("Transfer NFT"):
    txn_hash = transfer_nft(token_id, to_address, private_key)
    st.write(f"Transaction Hash: {txn_hash}")


# Add a description paragraph
st.markdown("""
    Welcome to AssetCoin! This platform allows you to buy and manage tokens representing shares in a real estate asset.
""")

# Tabs for different functionalities
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💸 Buy Tokens", "💰 View Token Price", "📈 Real Estate Value", "Asset Photos", "Mortgage Calculator"])

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
    most_recent_price, investment_return_asset,  asset_price_historical, house_price_num = call_house_prices()
    photos_df = call_photos()
    st.subheader("Real Estate Value")
    zpid = "15302053"  # Example property ID, replace with actual ID

    if st.button("Refresh Price"):
        # Fetch property value using the rapid_api_caller function from zillow_doc1
        value = house_price_num
        st.write(f"Current value of the property: ${value} USD")

    st.title("Data Visualization")

    # Plot data using matplotlib
    fig, ax = plt.subplots()
    ax.plot(asset_price_historical.index, asset_price_historical['value'])
    ax.set_xlabel('Date')
    ax.set_ylabel('value')
    ax.set_title('Value over Time')
    plt.xticks(rotation=45)
    st.pyplot(fig)

with tab4:
    for width, url in photos_df.iterrows():
        st.subheader(f"Image {width}")
        st.image(url.values[0], caption=f"Image {width}")

        # Plotting the data
        #plt.figure(figsize=(10, 5))
        # plt.plot(dates, values, marker='o')
        # plt.xlabel("Date")
        # plt.ylabel("Value (USD)")
        # plt.title("Real Estate Asset Value Over Time")
        # plt.grid(True)
        # plt.xticks(rotation=45)
        # st.pyplot(plt)

with tab5: 
    st.title("Mortgage Repayments Calculator")

    st.write("### Input Data")
    col1, col2 = st.columns(2)
    home_value = house_price_num
    deposit = col1.number_input("Deposit", min_value=0)
    interest_rate = col2.number_input("Interest Rate (in %)", min_value=0.0, value=8.0)
    loan_term = col2.number_input("Loan Term (in years)", min_value=1, value=30)

    # Calculate the repayments.
    loan_amount = home_value - deposit
    monthly_interest_rate = (interest_rate / 100) / 12
    number_of_payments = loan_term * 12
    monthly_payment = (
        loan_amount
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
        / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    )

    # Display the repayments.
    total_payments = monthly_payment * number_of_payments
    total_interest = total_payments - loan_amount

    st.write("### Repayments")
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Monthly Repayments", value=f"${monthly_payment:,.2f}")
    col2.metric(label="Total Repayments", value=f"${total_payments:,.0f}")
    col3.metric(label="Total Interest", value=f"${total_interest:,.0f}")


    # Create a data-frame with the payment schedule.
    schedule = []
    remaining_balance = loan_amount

    for i in range(1, number_of_payments + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        year = math.ceil(i / 12)  # Calculate the year into the loan
        schedule.append(
            [
                i,
                monthly_payment,
                principal_payment,
                interest_payment,
                remaining_balance,
                year,
            ]
        )

    df = pd.DataFrame(
        schedule,
        columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
    )

    # Display the data-frame as a chart.
    st.write("### Payment Schedule")
    payments_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
    st.line_chart(payments_df)

