
import requests
import json
import csv
import pandas as pd 
import numpy as np
import hvplot.pandas
import statsmodels.api as sm
import pandas_datareader.famafrench as ff
import hvplot.pandas
import datetime as dt 

def rapid_api_caller(): 
    url = "https://zillow56.p.rapidapi.com/zestimate_history"
    querystring = {"zpid":"15302053"}

    headers = {
	"X-RapidAPI-Key": "7b97135f56msh8b19882fa1c06c6p13a91djsn169f4a00e1f6",
	"X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }
    response = requests.get(url, headers = headers, params = querystring)
    return response

def photos_api_caller():
    url = "https://zillow56.p.rapidapi.com/photos"
    querystring = {"zpid":"15302053"}

    headers = {
	"X-RapidAPI-Key": "7b97135f56msh8b19882fa1c06c6p13a91djsn169f4a00e1f6",
	"X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }
    response = requests.get(url, headers = headers, params = querystring)
    return response

def createdf(file):
    df = pd.DataFrame(file)
    return df

def save_file_json(file, name): 
    with open(name,'w') as f:
        json.dump(file, f)


# Replace 'path/to/your/file.json' with the actual file path
def open_json_file(file_path):
# Open and read the JSON file
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

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

def sets_date(ys,ms,ds, ye,me,de):
    start = dt.date(ys,ms,ds)
    end = dt.date(ye,me,de)
    return start, end

# def dataset_call(data_name, data_source, start, end, part):

def main():
    # NOTE: Calls in our Rapid_API 
    # house_prices = rapid_api_caller()
    # photos = photos_api_caller()

    # NOTE: put everything into a df
    # respdf = createdf(resp)
    # photos_df = createdf(photos)


    # NOTE: Put everything into a JSON 
    # respdf.to_csv("House_prices.csv")
    # file_name = resp.json()

    # photos_df_json = save_file_json(photos.json(), "home_desc.json_zillow")
    
    # NOTE: 1) Reads the lcoal file data_zillow.json). You can comment this out
    json_file_downloaded = "data_zillow.json"

    # NOTE: 2) instead of 'json_file_downloaded', use the variable that has the JSON file stored in it
    df = pd.read_json(json_file_downloaded)

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
    print(dfc)

    # NOTE: You can rename this anything. Replaced "Value" with "Real-Estate-Return, used as the column head on the DataFrame"
    real_estate = "Real-Estate Return"
    dfc = rename(dfc,"value" ,real_estate)
    print(dfc)

    # NOTE: gets the most recent house value and prints it out 
    most_recent_price = df.tail(1)
    print(most_recent_price)

# Sources: 
# https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file 
# https://rapidapi.com/tvhaudev/api/zillow-base1 
# https://www.squash.io/how-to-convert-json-to-csv-in-python/ 
# https://www.zillow.com/homes/181-Fremont-St-.num.63A-San-Francisco,-CA-94105_rb/249664766_zpid/

main()


