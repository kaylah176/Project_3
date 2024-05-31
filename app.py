import streamlit as st
import requests

# Function to fetch property value from RapidAPI
def get_property_value(address, api_key):
    url = "https://zillow56.p.rapidapi.com/search_address"
    querystring = {"address": address}
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data: {e}")
        return None

# Streamlit interface
st.title("Zillow Property Value Checker")

api_key = "2315539591msh7278b70970d7d2dp1a485ajsnf96560e49b39"
address = st.text_input("Enter Property Address:")

if st.button("Get Property Value"):
    if api_key and address:
        data = get_property_value(address, api_key)
        
        # if data:
        #     st.write("Property Value Data:")
        #     st.json(data)
    else:
        st.warning("Please enter both the API key and property address.")

# To run the app, use the command:
# streamlit run app.py

st.divider()

zestimate_current = data['onsiteMessage']['messages'][0]['decisionContext']['zestimate']
st.write(f"Current Zestimate: {zestimate_current}")
hoa_fees = data['resoFacts']['hoaFee']
st.write(f"HOA Fees: {hoa_fees}")
tax_annual = data['resoFacts']['taxAnnualAmount']
st.write(f"Annual Tax: {tax_annual}")
description = data['description']
st.write(f"Property Description: {description}")
year_built = data['resoFacts']['yearBuilt']
st.write(f"Year Built: {year_built}")
living_area = data['livingArea']
st.write(f"Living Area: {living_area} sqft")
longitude = data['longitude']
st.write(f"Longitude: {longitude}")
latitude = data['latitude']
st.write(f"Latitude: {latitude}")
lot_size = data['lotAreaValue']
st.write(f"Lot Size: {lot_size} sqft")
bathrooms = data['bathrooms']
st.write(f"Bathrooms: {bathrooms}")
bedrooms = data['bedrooms']
st.write(f"Bedrooms: {bedrooms}")


