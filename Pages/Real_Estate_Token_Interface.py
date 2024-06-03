import streamlit as st
from web3 import Web3
import folium
import requests
import matplotlib.pyplot as plt
import math 
import pandas as pd
import numpy_financial as npf
import numpy as np
from io import StringIO
import requests
import json 
import numpy as np
import datetime as dt
import time
import math 
from streamlit_folium import st_folium
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, NumeralTickFormatter
import pandas as pd


# Zillow API Information 
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
    try:
        response = requests.get(url, headers = headers, params = querystring)
        response.raise_for_status()  # Check if the request was successful
        return response
    except requests.exceptions.RequestException as e:
        print("Price currently unavailable, please try again in a few minutes")
        print(f"Error details: {e}")
        return None


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

def house_map():
    # Sample data: list of (latitude, longitude) tuples
                    #Latitude First, Longitude Second,
    coordinates = [(38.011734, -121.36025)]

    # Calculate the center of the map as the average of the coordinates
    map_center = [
        sum([coord[0] for coord in coordinates]) / len(coordinates),
        sum([coord[1] for coord in coordinates]) / len(coordinates)
    ]

    # Create a folium map centered around the calculated center
    mymap = folium.Map(location=map_center, zoom_start=10)

    # Add markers to the map
    for coord in coordinates:
        folium.Marker(location=coord, popup=f'Location: {coord}').add_to(mymap)
    return mymap
  

st.title("Real Estate Token Interface")

# UI for NFT functionalities
st.header("Overview")

# Add a description paragraph
st.markdown("""
    Welcome to our Real Estate Token Interface! Sections of this platform focuses on interactive tools and resources regarding the asset you are investing in. 
""")

# Tabs for different functionalities
tab1, tab2, tab3, tab4 = st.tabs(["Real Estate Value", "Asset Photos", "Mortgage Calculator", "Real Estate Investment Sensitivity Analysis"])

with tab1:
    most_recent_price, investment_return_asset,  asset_price_historical, house_price_num = call_house_prices()
    photos_df = call_photos()
    st.subheader("Real Estate Value")
    zpid = "15302053"  # Example property ID, replace with actual ID

    if st.button("Refresh Price"):
        # Fetch property value using the rapid_api_caller function from zillow_doc1
        value = house_price_num
        st.write(f"Current value of the property: ${value} USD")

    st.title("Data Visualization")

    # Assuming asset_price_historical is already defined and loaded with a DateTime index and a 'value' column
    source = ColumnDataSource(data={
        'date': asset_price_historical.index,
        'value': asset_price_historical['value']
    })

    # Create a new plot with a title and axis labels
    p = figure(title='Value over Time', x_axis_label='Date', y_axis_label='Current Property Value (USD)', x_axis_type='datetime')

    # Add a line renderer with legend and line thickness
    p.line(x='date', y='value', source=source, legend_label='Property Value', line_width=2)

    # Customizing the datetime format on x-axis
    p.xaxis.formatter = DatetimeTickFormatter(days=["%d %b %Y"], months=["%b %Y"], hours=["%d %b %Y %H:%M"])

    # Customizing the y-axis to display whole numbers
    p.yaxis.formatter = NumeralTickFormatter(format='0')

    # Streamlit function to display Bokeh chart
    st.bokeh_chart(p, use_container_width=True)

with tab2:
    for width, url in photos_df.iterrows():
        st.image(url.values[0], caption=f"Image {width}")

with tab3: 
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

with tab4: 

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





