import streamlit as st
from web3 import Web3
import json
import time
import requests
import json
import pandas as pd 
import numpy as np
import datetime as dt 
from io import StringIO


# Connect to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

# Load the compiled smart contracts (ABI and bytecode)
with open('OwnershipToken.json') as f:
    ownership_token_data = json.load(f)
with open('RealEstateNFT.json') as f:
    real_estate_nft_data = json.load(f)

# Load the deployed OwnershipToken contract
ownership_token_address = '0xC9091De433de1110011Bbe6F25EAE0D0e2Da662d'
ownership_token = w3.eth.contract(address=ownership_token_address, abi=ownership_token_data['abi'])

# Load the deployed RealEstateNFT contract
real_estate_nft_address = '0x3d15f2eDEAd5F94017e4395B9CC883161A58C0d3'
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

# Select the account
account = st.selectbox("Select Account", options=[get_account_name(acc) for acc in accounts])

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
    st.write(f"Initial Value in USD: ${initial_value_usd:.2f}")
    st.write(f"Initial Value in ETH: {initial_value_eth:.6f}")
    st.write(f"Current Value in USD: ${current_value_usd:.2f}")
    st.write(f"Current Value in ETH: {current_value_eth:.6f}")

# Mint a New Property NFT
st.subheader("Mint New Property NFT")
property_address = st.text_input("Property Address")
initial_purchase_price_usd = st.number_input("Initial Purchase Price (in USD)", min_value=0.0, step=0.01)
holding_company_name = st.text_input("Holding Company Name")
description = st.text_area("Description")
current_property_value_usd = st.number_input("Current Property Value (in USD)", min_value=0.0, step=0.01)

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
        w3.toWei(current_property_value_eth, 'ether')
    ).transact({'from': account_address})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    st.write(f"Minted RealEstateNFT with token ID {token_id}")
    st.write(f"Contract Address: {real_estate_nft_address}")
    st.write(f"Token ID: {token_id}")

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

import threading
event_listener = threading.Thread(target=log_loop, args=(ownership_token_event_filter, 2), daemon=True)
event_listener.start()

# Run the Streamlit app
if __name__ == "__main__":
    st.write("Real Estate NFT DApp")

def rapid_api_caller(): 
    url = "https://zillow56.p.rapidapi.com/zestimate_history"
    querystring = {"zpid":"15302053"}

    headers = {
	"X-RapidAPI-Key": "2315539591msh7278b70970d7d2dp1a485ajsnf96560e49b39",
	"X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }
    response = requests.get(url, headers = headers, params = querystring)
    return response

def photos_api_caller():
    url = "https://zillow56.p.rapidapi.com/photos"
    querystring = {"zpid":"15302053"} 

    headers = {
	"X-RapidAPI-Key": "2315539591msh7278b70970d7d2dp1a485ajsnf96560e49b39",
	"X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }
    response = requests.get(url, headers = headers, params = querystring)
    return response


def get_property_details():
    url = "https://zillow56.p.rapidapi.com/search_address"
    querystring = {"address": "15302053"}
    headers = {
        "X-RapidAPI-Key": "2315539591msh7278b70970d7d2dp1a485ajsnf96560e49b39",
        "X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        # print(response.json()) 
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Get Property Details error: {e}")
        return None

def createdf(file):
    df = pd.DataFrame(file)
    return df


def normalize(df,column):
    normalized_df = pd.json_normalize(df[column])
    return normalized_df

def set_i(df,col):
    df = df.set_index(col)
    return df

def set_dates(df):
    df.index = pd.to_datetime(df.index)
    return df

def date_index(df):
    df.index = df.index.date
    return df

def pct(df):
    df = df.pct_change()
    return df

def cumulative(df): 
    dfc = (1+df).cumprod()
    return dfc

def rename(df, old,new):
    df = df.rename(columns = {old:new})
    return df

def extract_url_df(df):
    df_links = pd.DataFrame()
    for item in df:
        if isinstance(item, list):
            for sub_item in item:
                df_i = pd.DataFrame(sub_item, index = [0])
                df_links = pd.concat([df_links, df_i], ignore_index = True)
    return df_links

def high_def_pix(df):
    df = df.set_index("width")
    df.index = df.index.astype(int)
    max_width = df.index.max()
    filtered_df = df[df.index == max_width]
    return filtered_df

# def call_details():
#     data = get_property_details()

#     zestimate_current = data['onsiteMessage']['messages'][0]['decisionContext']['zestimate']
#     hoa_fees = data['resoFacts']['hoaFee']
#     tax_annual = data['resoFacts']['taxAnnualAmount']
#     description = data['description']
#     year_built = data['resoFacts']['yearBuilt']

#     return zestimate_current, hoa_fees, tax_annual, description, year_built

        

def call_photos():
    # NOTE: Calls Photos_api
    photos = photos_api_caller()

    # NOTE: Converts to JSON()
    photos = photos.json()
    
    # NOTE: Convert python object to a JSON String (see sources)
    photos = json.dumps(photos)

    # NOTE: reads JSON 
    photos = pd.read_json(photos)

    # NOTE: Normalizes the json file, and only extracts "photos"
    photos = normalize(photos, "photos")    

    # NOTE: Pulls out only JPEG links
    jpeg = photos["mixedSources.jpeg"]

    # NOTE: converts this into a dataframe
    df = pd.DataFrame(jpeg)

    # NOTE: Extracts the "mixedsources.jpeg column"
    photos_df = df["mixedSources.jpeg"] #[0]

    # NOTE: Extracts out the URL and organizes it into a dataframe to read, filter through 
    photos_df = extract_url_df(photos_df)

    # NOTE: Filters out every and all photos that are "low def"
    photos_df = high_def_pix(photos_df)
    
    return photos_df




def call_house_prices():
    # NOTE: Calls in our Rapid_API 
    house_prices = rapid_api_caller()

    # NOTE: Converts it as JSON() file
    house_prices = house_prices.json()

    # NOTE: Json.dumps():
    house_prices = json.dumps(house_prices)

    # NOTE: put everything into a df
    df = pd.read_json(house_prices)

    # NOTE: Allows you to access key-value pairs in the JSON (so it behaves like a dictionary)
    df = normalize(df,"data")

    # NOTE: Set's index as date  
    df = set_i(df, "date")

    # NOTE: Drops the timestamp 
    df = df.drop(columns = ["timestamp"])

    # NOTE: Converts the index (Date) into Date.time format
    df = set_dates(df)
    
    # NOTE: Cleans up the date_index (by removing the hours)
    df = date_index(df)
    

    # NOTE: pct allows us to calculate the monthly returns from the beginning 
    dfpct= pct(df)

    # NOTE: cumulative allows us to calculate the cumulative returns year-over-year
    dfc = cumulative(dfpct)
    #print(dfc)

    # NOTE: You can rename this anything. Replaced "Value" with "Real-Estate-Return, used as the column head on the DataFrame"
    real_estate = "Real-Estate-Returns (rebased to $1)"
    dfc = rename(dfc,"value" ,real_estate)
    # print(dfc)

    investment_return_asset = dfc
    asset_price_historical = df

    # NOTE: gets the most recent house value and prints it out 
    most_recent_price = df.tail(1)

    house_price_num = 0
    for i in most_recent_price["value"]:
        house_price_num += i
# Sources: 
# https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file 
# https://rapidapi.com/tvhaudev/api/zillow-base1 
# https://www.squash.io/how-to-convert-json-to-csv-in-python/ 
# https://www.zillow.com/homes/181-Fremont-St-.num.63A-San-Francisco,-CA-94105_rb/249664766_zpid/

    return most_recent_price, investment_return_asset, asset_price_historical, house_price_num

def json_convert(contents, filename):
    with open(filename, 'w') as f:
        json.dump(contents, f, indent = 2)
    return contents

def convert_list(contents, section):
    contents = contents.reset_index()
    section = contents[section]
    list_1 = []
    for link in section: 
        list_1.append(link)
    return list_1

def photo_conversion_json(df):
    file = convert_list(df,"url")
    file_json = json_convert(file, "zillow_url")
    return file_json

# def main():
#     most_recent_price, investment_return, asset_price_hist ,value_of_asset = call_house_prices()
#     photos_df = call_photos()
#     #conversion = photo_conversion_json(photos_df)
#     #zestimate_current, hoa_fees, tax_annual, description, year_built = call_details()



