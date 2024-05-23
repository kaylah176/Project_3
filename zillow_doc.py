
import requests
import json
import csv
import pandas as pd 

# url = "https://zillow-base1.p.rapidapi.com/WebAPIs/zillow/locationSuggestions/v2"

# querystring = {"location":"Brownsville, TX"}

# headers = {
# 	"X-RapidAPI-Key": "7b97135f56msh8b19882fa1c06c6p13a91djsn169f4a00e1f6",
# 	"X-RapidAPI-Host": "zillow-base1.p.rapidapi.com"
# }

# response = requests.get(url, headers=headers, params=querystring)

# print(response.json())


def rapid_api_caller(): 
    url = "https://zillow56.p.rapidapi.com/zestimate_history"
    querystring = {"zpid":"249664766"}

    headers = {
	"X-RapidAPI-Key": "7b97135f56msh8b19882fa1c06c6p13a91djsn169f4a00e1f6",
	"X-RapidAPI-Host": "zillow56.p.rapidapi.com"
    }
    response = requests.get(url, headers = headers, params = querystring)
    return response

    """
            url = "https://zillow56.p.rapidapi.com/zestimate_history"

        querystring = {"zpid":"20476226"}

        headers = {
            "X-RapidAPI-Key": "7b97135f56msh8b19882fa1c06c6p13a91djsn169f4a00e1f6",
            "X-RapidAPI-Host": "zillow56.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=querystring)

        print(response.json())


    """


# def pull_specific():


def createdf(file):
    df = pd.DataFrame(file)
    return df


def save_file_json(file): 
    with open('data.json_zillow','w') as f:
        json.dump(file, f)

def main():
    resp = rapid_api_caller()
    respdf = createdf(resp)
    respdf.to_csv("Zillow Prices.csv")
    file_name = resp.json()

    # saved_ = save_file_json(file_name)
    # j = "data.json"


    # df = createdf(file_name)
    # df.to_csv("Output.csv", index = False)
    # print(resp.json())
# https://www.zillow.com/homes/181-Fremont-St-.num.63A-San-Francisco,-CA-94105_rb/249664766_zpid/

# Sources: 
# https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file 
# https://rapidapi.com/tvhaudev/api/zillow-base1 
# https://www.squash.io/how-to-convert-json-to-csv-in-python/ 

main()

