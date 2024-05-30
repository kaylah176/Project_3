
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

def dataset_call(data_name, data_source, start, end, part):

def main():
    # NOTE: API Caller
    # resp = rapid_api_caller()
    # photos = photos_api_caller()

    # NOTE: put everything into a df
    # respdf = createdf(resp)
    # photos_df = createdf(photos)


    # NOTE: Put everything into a JSON 
    # respdf.to_csv("House_prices.csv")
    # file_name = resp.json()

    # photos_df_json = save_file_json(photos.json(), "home_desc.json_zillow")
    
    json_file_downloaded = "data.json_zillow"
    file = open_json_file(json_file_downloaded)


    
    df = pd.read_json(json_file_downloaded)


    real_estate = "Real-Estate Return"

    df = normalize(df,"data")
    df = set_i(df, "date")
    df = df.drop(columns = ["timestamp"])
    df = set_dates(df)
    df = date_index(df)
    df = pct(df)
    dfc = cumulative(df)
    dfc = rename(dfc, real_estate)
    print(dfc)
    




    
    # recent = df["data"].tail(1)
    # print(recent["date"])
    # r = pd.DataFrame(recent)
    # print(r)




    # df = createdf(file_name)
    # df.to_csv("Output.csv", index = False)
    # print(resp.json())
# https://www.zillow.com/homes/181-Fremont-St-.num.63A-San-Francisco,-CA-94105_rb/249664766_zpid/

# Sources: 
# https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file 
# https://rapidapi.com/tvhaudev/api/zillow-base1 
# https://www.squash.io/how-to-convert-json-to-csv-in-python/ 

main()

