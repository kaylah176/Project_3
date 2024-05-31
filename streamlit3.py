import streamlit as st
from web3 import Web3
import requests
import matplotlib.pyplot as plt
from zillow_doc2 import call_house_prices, call_photos 
import math 
import pandas as pd
import numpy_financial as npf
import numpy as np

# Connect to the Ethereum network
ganache = "HTTP://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache))

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["💸 Buy Tokens", "💰 View Token Price", "📈 Real Estate Value", "Asset Photos", "Mortgage Calculator", "Real Estate Investment Analysis"])

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
        #st.subheader(f"Image {width}")
        #st.image(url.values[0], caption=f"Image {width}")

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

with tab6: 

    st.title("Real Estate Investment Analysis")

    initial_market_value = st.number_input("Initial Market Value", value=360000)
    purchase_price = st.number_input("Purchase Price", value=280000)
    estimated_closing_costs = st.number_input("Estimated Closing Costs", value=5000)
    downpayment_percentage = st.number_input("Downpayment Percentage (%)", value=20)
    estimated_monthly_gross_rent = st.number_input("Estimated Monthly Gross Rent", value=2000)
    property_taxes = st.number_input("Property Taxes", value=3000)
    insurance_costs = st.number_input("Insurance Costs", value=1200)
    loan_term = st.number_input("Loan Term (years)", value=30)
    interest_rate = st.number_input("Interest Rate (%)", value=3.5)
    appreciation_rate = st.number_input("Appreciation Rate (%)", value=2)
    vacancy_rate = st.number_input("Vacancy Rate (%)", value=5)
    management_fees = st.number_input("Management Fees (%)", value=10)
    maintenance_percentage = st.number_input("Maintenance Percentage (%)", value=1)
    rental_income_increase = st.number_input("Rental Income Increase (%)", value=2)

# # Calculations
    downpayment_dollars = (downpayment_percentage / 100) * purchase_price
    initial_cash_invested = downpayment_dollars + estimated_closing_costs
    annual_gross_rent = estimated_monthly_gross_rent * 12
    vacancy_losses = (vacancy_rate / 100) * annual_gross_rent
    property_taxes_dollars = property_taxes
    insurance_costs_dollars = insurance_costs
    management_fees_dollars = (management_fees / 100) * annual_gross_rent
    maintenance_fees_dollars = (maintenance_percentage / 100) * initial_market_value
    total_operating_expenses = vacancy_losses + property_taxes_dollars + insurance_costs_dollars + management_fees_dollars + maintenance_fees_dollars

# # Mortgage Calculation
    loan_amount = purchase_price - downpayment_dollars
    monthly_interest_rate = (interest_rate / 100) / 12
    num_payments = loan_term * 12
    monthly_mortgage_payment = npf.pmt(monthly_interest_rate, num_payments, -loan_amount)
    annual_mortgage_payment = monthly_mortgage_payment * 12

# # Cash Flow Calculation
    cash_flow = annual_gross_rent - total_operating_expenses - annual_mortgage_payment

# # Gross Equity Income Calculation
    annual_appreciation = (appreciation_rate / 100) * initial_market_value
    gross_equity_income = annual_appreciation + (annual_mortgage_payment - loan_amount * monthly_interest_rate * 12)

# # GEI with Tax Savings (simplified)
    tax_savings = annual_mortgage_payment * 0.3  # Assuming 30% tax bracket
    gei_with_tax_savings = gross_equity_income + tax_savings

# # Display Results
    st.header("Investment Analysis Results")
    st.write(f"Downpayment in Dollars: ${downpayment_dollars:,.2f}")
    st.write(f"Initial Cash Invested: ${initial_cash_invested:,.2f}")
    st.write(f"Annual Gross Rent: ${annual_gross_rent:,.2f}")
    st.write(f"Vacancy Losses: ${vacancy_losses:,.2f}")
    st.write(f"Property Taxes: ${property_taxes_dollars:,.2f}")
    st.write(f"Insurance Costs: ${insurance_costs_dollars:,.2f}")
    st.write(f"Management Fees: ${management_fees_dollars:,.2f}")
    st.write(f"Maintenance Fees: ${maintenance_fees_dollars:,.2f}")
    st.write(f"Total Operating Expenses: ${total_operating_expenses:,.2f}")
    st.write(f"Annual Mortgage Payment: ${annual_mortgage_payment:,.2f}")
    st.write(f"Cash Flow: ${cash_flow:,.2f}")
    st.write(f"Gross Equity Income: ${gross_equity_income:,.2f}")
    st.write(f"GEI with Tax Savings: ${gei_with_tax_savings:,.2f}")

# # 30-Year Projections
    years = np.arange(1, 31)
    cash_flows = []
    equity_accumulation = []
    current_rent = estimated_monthly_gross_rent * 12
    current_market_value = initial_market_value

    for year in years:
        current_rent *= (1 + rental_income_increase / 100)
        annual_gross_rent = current_rent
        vacancy_losses = (vacancy_rate / 100) * annual_gross_rent
        management_fees_dollars = (management_fees / 100) * annual_gross_rent
        total_operating_expenses = vacancy_losses + property_taxes_dollars + insurance_costs_dollars + management_fees_dollars + maintenance_fees_dollars
        cash_flow = annual_gross_rent - total_operating_expenses - annual_mortgage_payment
        cash_flows.append(cash_flow)

        current_market_value *= (1 + appreciation_rate / 100)
        annual_appreciation = current_market_value * (appreciation_rate / 100)
        equity_accumulation.append(annual_appreciation + (annual_mortgage_payment - loan_amount * monthly_interest_rate * 12))

# # Plotting
    st.header("30-Year Cash Flow and Equity Projections")
    fig, ax = plt.subplots()
    ax.plot(years, cash_flows, label='Annual Cash Flow')
    ax.plot(years, equity_accumulation, label='Equity Accumulation')
    ax.set_xlabel('Year')
    ax.set_ylabel('Amount ($)')
    ax.legend()
    st.pyplot(fig)

    st.header("30-Year Annual Cash Flow Projections")
    fig, ax = plt.subplots()
    ax.plot(years, cash_flows, label='Annual Cash Flow')
    ax.set_xlabel('Year')
    ax.set_ylabel('Cash Flow ($)')
    ax.legend()
    st.pyplot(fig)

    st.header("30-Year Equity Accumulation Projections")
    fig, ax = plt.subplots()
    ax.plot(years, equity_accumulation, label='Equity Accumulation')
    ax.set_xlabel('Year')
    ax.set_ylabel('Equity Accumulation ($)')
    ax.legend()
    st.pyplot(fig)


