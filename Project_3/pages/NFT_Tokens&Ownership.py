import streamlit as st
from web3 import Web3
import os
import json
import time
import requests
import pandas as pd 
import numpy as np
import datetime as dt 
from io import StringIO
import threading

# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Construct the relative path to the JSON files
base_dir = os.path.dirname(__file__)
ownership_token_path = os.path.join(base_dir, '..', 'contracts', 'compiled', 'OwnershipToken.json')
real_estate_nft_path = os.path.join(base_dir, '..', 'contracts', 'compiled', 'RealEstateNFT.json')

# Load the compiled smart contracts (ABI and bytecode)
with open(ownership_token_path) as f:
    ownership_token_data = json.load(f)
with open(real_estate_nft_path) as f:
    real_estate_nft_data = json.load(f)

# Load the deployed OwnershipToken contract
ownership_token_address = '0xefBdd03b439a91C8e44b71975A4C99740eF9C676'
ownership_token = w3.eth.contract(address=ownership_token_address, abi=ownership_token_data['abi'])

# Load the deployed RealEstateNFT contract
real_estate_nft_address = '0xE8b46F91A4Bb0307F6750C939f27254049733bBA'
real_estate_nft = w3.eth.contract(address=real_estate_nft_address, abi=real_estate_nft_data['abi'])

# Fixed ETH/USD exchange rate
eth_usd_rate = 3772.25

st.write(f"Fixed ETH/USD exchange rate: {eth_usd_rate} USD")

st.title("Real Estate NFT DApp")

# Map accounts to names
account_names = {
    w3.eth.accounts[0]: "Holding Account LLC",
    w3.eth.accounts[1]: "Jack",
    w3.eth.accounts[2]: "Gabe",
    w3.eth.accounts[3]: "Kayla",
    w3.eth.accounts[4]: "Ravi"
}

def get_account_name(address):
    return account_names.get(address, address)

# Select the first five accounts
accounts = w3.eth.accounts[:5]

# Mint a New Property NFT
st.subheader("Mint New Property NFT")
st.write("NOTE: Only Mint the NFT once")
property_address = st.text_input("Property Address")
initial_purchase_price_usd = st.number_input("Initial Purchase Price (in USD)", min_value=0.0, step=0.01)
holding_company_name = st.text_input("Holding Company Name")
description = st.text_area("Description")
current_property_value_usd = st.number_input("Current Property Value (in USD)", min_value=0.0, step=0.01)
token_uri = st.text_input("Token URI")

initial_purchase_price_eth = initial_purchase_price_usd / eth_usd_rate
current_property_value_eth = current_property_value_usd / eth_usd_rate

st.write(f"Initial Purchase Price in ETH: {initial_purchase_price_eth:.6f}")
st.write(f"Current Property Value in ETH: {current_property_value_eth:.6f}")

if st.button("Mint Property NFT"):
    account_address = w3.eth.accounts[0]  # Holding Account LLC
    token_id = 1  # Assuming there is only one NFT
    tx_hash = real_estate_nft.functions.mintProperty(
        account_address,
        token_id,
        property_address,
        w3.toWei(initial_purchase_price_eth, 'ether'),
        holding_company_name,
        description,
        w3.toWei(current_property_value_eth, 'ether'),
        token_uri
    ).transact({'from': account_address})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(f"Minted RealEstateNFT with token ID {token_id}")
    st.write(f"Contract Address: {real_estate_nft_address}")
    st.write(f"Token ID: {token_id}")

st.write("---")

# Display Property Details
st.subheader("Property Details")
token_id_details = 1  # Assuming there is only one NFT

if st.button("Show Property Details"):
    property_details = real_estate_nft.functions.properties(token_id_details).call()
    initial_purchase_price_eth = float(w3.fromWei(property_details[1], 'ether'))
    current_property_value_eth = float(w3.fromWei(property_details[4], 'ether'))
    initial_purchase_price_usd = initial_purchase_price_eth * eth_usd_rate
    current_property_value_usd = current_property_value_eth * eth_usd_rate

    st.write(f"Property Details for token ID {token_id_details}:")
    st.write(f"Address: {property_details[0]}")
    st.write(f"Initial Purchase Price: {initial_purchase_price_eth} ETH (${initial_purchase_price_usd:.2f} USD)")
    st.write(f"Holding Company Name: {property_details[2]}")
    st.write(f"Description: {property_details[3]}")
    st.write(f"Current Property Value: {current_property_value_eth} ETH (${current_property_value_usd:.2f} USD)")

st.write("---")

# Update Contract Description
st.subheader("Update Contract Description")

# Fetch the current description
account_address = w3.eth.accounts[0]  # Holding Account LLC
token_id_desc = 1  # Assuming there is only one NFT
current_description = real_estate_nft.functions.properties(token_id_desc).call()[3]
new_description = st.text_area("New Description", value=current_description)

if st.button("Update Description"):
    tx_hash = real_estate_nft.functions.updateDescription(token_id_desc, new_description).transact({'from': account_address})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Updated contract description")

st.write("---")

# Update Current Property Value
st.subheader("Update Current Property Value")
new_property_value_usd = st.number_input("New Property Value (in USD)", min_value=0.0, step=0.01)
new_property_value_eth = new_property_value_usd / eth_usd_rate

st.write(f"New Property Value in ETH: {new_property_value_eth:.6f}")

if st.button("Update Property Value"):
    account_address = w3.eth.accounts[0]  # Holding Account LLC
    tx_hash = real_estate_nft.functions.updateCurrentPropertyValue(1, w3.toWei(new_property_value_eth, 'ether')).transact({'from': account_address})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write("Updated current property value")

st.write("---")

# Select the account
st.subheader("Check Ownership Token Balance")
account = st.selectbox("Select Account to see OWN token balance/value", options=[get_account_name(acc) for acc in accounts])

# Display Ownership Token Balance
def get_token_balance(account):
    balance = ownership_token.functions.balanceOf(account).call()
    return balance / (10 ** 2)

def get_initial_value(account):
    # Retrieve the initial value of the tokens for the given account
    initial_value = ownership_token.functions.getInitialTokenValue(account).call()
    return initial_value / (10 ** 2)

if st.button("Show Ownership Token Balance"):
    account_address = [acc for acc in accounts if get_account_name(acc) == account][0]
    balance = get_token_balance(account_address)
    initial_value_eth = get_initial_value(account_address)
    initial_value_usd = initial_value_eth * eth_usd_rate
    current_property_value_eth = float(w3.fromWei(real_estate_nft.functions.properties(1).call()[4], 'ether'))
    current_property_value_usd = current_property_value_eth * eth_usd_rate
    current_value_usd = (balance / 100) * current_property_value_usd
    current_value_eth = (balance / 100) * current_property_value_eth
    st.write(f"Ownership Tokens balance of {account}: {balance}")
    #st.write(f"Initial Value in USD: ${initial_value_usd:.2f}")
    #st.write(f"Initial Value in ETH: {initial_value_eth:.6f}")
    st.write(f"Current Value in USD: ${current_value_usd:.2f}")
    st.write(f"Current Value in ETH: {current_value_eth:.6f}")

st.write("---")

# Transfer Ownership Tokens
st.subheader("Transfer Ownership Tokens")
default_sending_address = account  # Default sending address set to the holding company account
sending_address = st.selectbox("Select Sending Address", options=[get_account_name(acc) for acc in accounts], index=accounts.index([acc for acc in accounts if get_account_name(acc) == default_sending_address][0]))
recipient = st.selectbox("Select Recipient", options=[get_account_name(acc) for acc in accounts])
amount = st.number_input("Amount to Transfer", min_value=0.0, step=0.01)

if st.button("Transfer Tokens"):
    sending_address_actual = [acc for acc in accounts if get_account_name(acc) == sending_address][0]
    recipient_actual = [acc for acc in accounts if get_account_name(acc) == recipient][0]
    if sending_address_actual == recipient_actual:
        st.error("Sender cannot transfer tokens to themselves.")
    elif amount == 0:
        st.error("Transfer amount must be greater than 0.")
    else:
        sender_balance = get_token_balance(sending_address_actual)
        if amount > sender_balance:
            st.error(f"Sender does not have enough tokens to transfer. Your current balance is {sender_balance}.")
        else:
            tx_hash = ownership_token.functions.transfer(recipient_actual, int(amount * 100)).transact({'from': sending_address_actual})
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.write(f"Transferred {amount} Ownership Tokens from {sending_address} to {recipient}")
            st.write("To import the tokens into MetaMask, use the following details:")
            st.write(f"Contract Address: {ownership_token_address}")

st.write("---")

# Event listener for Ownership Token transfers
def handle_event(event):
    st.write(f"Transfer event: {event}")

def log_loop(event_filter, poll_interval):
    while True:
        for event in event_filter.get_new_entries():
            handle_event(event)
        time.sleep(poll_interval)

# Start listening for Ownership Token transfer events
ownership_token_event_filter = ownership_token.events.Transfer.createFilter(fromBlock='latest')

event_listener = threading.Thread(target=log_loop, args=(ownership_token_event_filter, 2), daemon=True)
event_listener.start()

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Real Estate NFT DApp")
