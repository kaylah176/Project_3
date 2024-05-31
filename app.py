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
        
        if data:
            st.write("Property Value Data:")
            st.json(data)
    else:
        st.warning("Please enter both the API key and property address.")

# To run the app, use the command:
# streamlit run app.py

st.divider()

zestimate_current = data['onsiteMessage']['messages'][0]['decisionContext']['zestimate']
st.write(zestimate_current)
