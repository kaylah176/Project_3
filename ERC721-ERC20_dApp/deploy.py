import json
from web3 import Web3

# Connect to Ganache (or another Ethereum node) on port 7545
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Set the default account (from which transactions will be sent)
w3.eth.defaultAccount = w3.eth.accounts[0]

# Load the compiled smart contracts (ABI and bytecode)
with open('OwnershipToken.json') as f:
    ownership_token_data = json.load(f)
with open('RealEstateNFT.json') as f:
    real_estate_nft_data = json.load(f)

# Deploy the OwnershipToken contract
OwnershipToken = w3.eth.contract(abi=ownership_token_data['abi'], bytecode=ownership_token_data['bytecode'])
initial_property_price = w3.toWei(100, 'ether')  # Example price
tx_hash = OwnershipToken.constructor(initial_property_price).transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
ownership_token_address = tx_receipt.contractAddress
print(f"OwnershipToken deployed at {ownership_token_address}")

# Load the deployed OwnershipToken contract
ownership_token = w3.eth.contract(address=ownership_token_address, abi=ownership_token_data['abi'])

# Check initial balance of the deploying account
initial_balance = ownership_token.functions.balanceOf(w3.eth.defaultAccount).call()
print(f"Initial Ownership Tokens balance of deploying account: {initial_balance / (10 ** 2)}")  # Adjust for 2 decimal precision

# Verify initial mint
if initial_balance == 0:
    print("Error: No tokens were minted to the deploying account during contract deployment.")
else:
    print("Tokens were successfully minted to the deploying account.")

# Load the deployed RealEstateNFT contract
real_estate_nft_address = '0x61aC9bD518B51CcB0faB99eb124EEed20a5B9a86'  # Replace with actual address
real_estate_nft = w3.eth.contract(address=real_estate_nft_address, abi=real_estate_nft_data['abi'])

# Mint a new property NFT
token_id = 1
property_address = "123 Real Estate St."
initial_purchase_price = w3.toWei(100, 'ether')  # Example price
holding_company_name = "Holding Company LLC"
description = "A beautiful real estate property."
current_property_value = initial_purchase_price
tx_hash = real_estate_nft.functions.mintProperty(
    w3.eth.accounts[1],
    token_id,
    property_address,
    initial_purchase_price,
    holding_company_name,
    description,
    current_property_value
).transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(f"Minted RealEstateNFT with token ID {token_id}")

# Verify the owner of the token ID 1
owner_of_token = real_estate_nft.functions.ownerOf(token_id).call()
print(f"Owner of token ID {token_id}: {owner_of_token}")

# Update Property Description if the owner is correct
if owner_of_token == w3.eth.accounts[1]:
    new_description = "Updated description for the real estate property."
    tx_hash = real_estate_nft.functions.updateDescription(token_id, new_description).transact({'from': w3.eth.accounts[1]})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Updated property description")
else:
    print(f"Error: Account {w3.eth.accounts[1]} is not the owner of token ID {token_id}")

# Update Current Property Value if the owner is correct
if owner_of_token == w3.eth.accounts[1]:
    new_property_value = w3.toWei(120, 'ether')  # Example new value
    tx_hash = real_estate_nft.functions.updateCurrentPropertyValue(token_id, new_property_value).transact({'from': w3.eth.accounts[1]})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Updated current property value")
else:
    print(f"Error: Account {w3.eth.accounts[1]} is not the owner of token ID {token_id}")

# Transfer Ownership Tokens
tx_hash = ownership_token.functions.transfer(w3.eth.accounts[2], 10 * (10 ** 2)).transact()  # Transfer 10 tokens
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print("Transferred 10 Ownership Tokens to account 2")

# Query Property Details
property_details = real_estate_nft.functions.properties(token_id).call()
print(f"Property Details: {property_details}")

# Query Ownership Token Balances
balance0 = ownership_token.functions.balanceOf(w3.eth.accounts[0]).call()
balance1 = ownership_token.functions.balanceOf(w3.eth.accounts[1]).call()
balance2 = ownership_token.functions.balanceOf(w3.eth.accounts[2]).call()
print(f"Ownership Tokens balance of account 0: {balance0 / (10 ** 2)}")  # Adjust for 2 decimal precision
print(f"Ownership Tokens balance of account 1: {balance1 / (10 ** 2)}")  # Adjust for 2 decimal precision
print(f"Ownership Tokens balance of account 2: {balance2 / (10 ** 2)}")  # Adjust for 2 decimal precision
