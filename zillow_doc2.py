
import requests
import json
import pandas as pd 
import numpy as np
import datetime as dt 
from io import StringIO



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
        return response.json()
    except requests.exceptions.RequestException as e:
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

def call_details():
    data = get_property_details()
    zestimate_current = data['onsiteMessage']['messages'][0]['decisionContext']['zestimate']
    hoa_fees = data['resoFacts']['hoaFee']
    tax_annual = data['resoFacts']['taxAnnualAmount']
    description = data['description']
    year_built = data['resoFacts']['yearBuilt']

    return zestimate_current, hoa_fees, tax_annual, description, year_built
    

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


def main():
    most_recent_price, investment_return, asset_price_hist ,value_of_asset = call_house_prices()
    photos = call_photos()
    zestimate_current, hoa_fees, tax_annual, description, year_built = call_details()

    print("Value of real-estate: ", value_of_asset)
    
    print("Asset Prices Historicals")
    print(asset_price_hist)

    print("Investment Return")
    print(investment_return)

    print("Most recent price data")
    print(most_recent_price)

    print("High-Def photos")
    print(photos)

    print(zestimate_current)
    print(hoa_fees)
    print(tax_annual)
    print(description)
    print(year_built)

main()