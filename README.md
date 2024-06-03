# Project 3
## Project Overview: 

Project 3: Tokenization and Real Estate is an MVP which does the following: Enables transaction of an asset as an NFT. For this Minimum-Viable-Product, we set out to enable tokenization of real-estate (pulled from Zillow RapidAPI), where investors can buy and sell assets as seamless as buying and selling securities on the stock market. 

### The Current Problem: 
Private-Equity transactions in general take time, energy, effort, and documentation between financial institutions to enable transition between sellers to potential buyers. 

### The Solution: 
Our process aims to cut out the bureaucracy when conducting private-equity like transactions. For our example, we chose real-estate as our example to showcase the simplicity to provide investors the ability to purchase or sell houses as NFT. 

## Installation Instructions:
### Neccessary Imports: 
1. Streamlit
2. Web3
3. Matplotlib
4. Math
5. Pandas
6. Numpy
7. IO
8. Request
9. json
10. time

### Necessary Files: 
1. **App.py**: Identifies property details from: Bathroom, bedroom, living area count/dimensions. 
2. **Streamlit3.py**: Imports from Zillow_doc2.py, ganache, and gets NFT details from web3. This streamlit file allows buyers to purchase tokens, view house photos, and view the historical investment value of the house (including the house price).
3. **RealEstateNFT.sol**: Creates the house token to be used for transactions.
4. **OwnershipToken.sol**: Assigns % of tokens to the shareholders (manages the OWN token). 

### Steps to deploy - Stage 1: 
1. Compile the RealEstateNFT.sol and deploy it. 
2. Compile the OwnershipToken.sol and deploy it.
3. Pick your injected provider as Metamask, and account.
4. Hit transact on Remix
5. Open up Metamask and hit import: Tokens, and paste the contract asset (OWN symbol).
6. Hit Next and hit import. This represenets 100 OWN coi.
7. Scroll down to the two contract addresses, adn hit copy, and paste that into **App.py**. This is grabbed and pasted into the ownership_token_address and real_estate_nft address contract. 
8. In python Terminal under **App.py** type: *streamlit run App.py*
   
### RealEstate DApp - Stage 2: 
1. Enter property price, initial purchase price, and holding company name, description, and current property value, and hit Mint Property NFT.
2. The sidebar menu (on the left) provides you access to current real-estate value (of the asset), as well as historical returns of the real-estate. Furthermore, a built-in mortgage calculator is built in to provide investors with quick and easy access to calculate their monthly payments for the property.

#### Navigation - Stage 3: 
To navigate through the app, use the sidebar on the left. Here are the main sections available:
        - **Home:** You are currently here. This section provides an overview and navigation instructions.
        - **NFT Tokens and Owernship:** This section allows you to mint an NFT that will represent the real estate property you want to invest in.
        This needs to be done under a holding company, also known as an LLC. Through this, each stakeholder in the LLC has the ability to purchase or sell to others in the LLC. 
        Here are some basic rules: 
            - You can only buy 25 tokens out of 100 at a time 
            - You can not sell to yourself. Only to other individuals in the LLC or back to the holding company itself
            - You can make updates to your contract's description once its deployed and even update the house's value. 
        - **Real Estate Token Interface:** This gives you interactive tools and resources regarding the asset your investing in. This includes ... 
            - Real Estate Valuation Visualization (past 10 years)
            - Current Asset Photos According to Zillow 
            - Mortgate Repayments Calculator 
            - Real Investment Analysis similar to a Pro Forma that is used to project the financial aspect of buying and leasing a home 







