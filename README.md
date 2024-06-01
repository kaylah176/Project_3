# Project 3
## Project Overview: 

Project 3: Tokenization and Real Estate is an MVP which does the following: Enables transaction of an asset as an NFT. For this Minimum-Viable-Product, we set out to enable tokenization of real-estate (pulled from Zillow RapidAPI), where investors can buy and sell assets as seamless as buying and selling securities on the stock market. 

### The Current Problem: 
Private-Equity transactions in general take time, energy, effort, and documentation between financial institutions to enable transition between sellers to potential buyers. 

### The Solution: 
Our process aims to cut out the bureaucracy when conducting private-equity like transactions. For our example, we chose real-estate as our example to showcase the simplicity to provide investors the ability to purchase or sell houses as NFT. 

## Installation Instructions:
### Necessary Files: 
1. **Zillow_doc2.py**: Contains the rapid-api callers to obtain property price and details.
2. **App.py**: Identifies property details from: Bathroom, bedroom, living area count/dimensions. This displays as a streamlit file, independent and instantly deployable. 
3. **Streamlit3.py**: Imports from Zillow_doc2.py, ganache, and gets NFT details from web3. This streamlit file allows buyers to purchase tokens, view house photos, and view the historical investment value of the house (including the house price) pulled from teh Zillow_doc2.py.
4. **NFT_mint.sol**: Creates the house token to be used for transactions 

### Steps to deploy: 


