# Project 3: Tokenization of Real-Estate Asset
## Project Overview: 

Project 3: Tokenization and Real Estate is an MVP which does the following: Enables transaction of an asset as an NFT. For this Minimum-Viable-Product, we set out to enable tokenization of real-estate (pulled from Zillow RapidAPI), where investors can buy and sell assets as seamless as buying and selling securities on the stock market. 

This project was completed by: Jack Richey, Kayla Hoffman, Gabriel Morano, Ravi Chailertborisuth for the UCB Fintech Bootcamp Project #3. 

### The Current Problem: 
Private-Equity transactions in general take time, energy, effort, and documentation between financial institutions to enable transition between sellers to potential buyers. In our example we create an interface with buyers and sellers can purchase tokens (effectively shares) of a house. According to [homecity.com](https://www.homecity.com/blog/how-long-does-it-take-to-buy-a-house/#:~:text=So%2C%20from%20offer%20to%20keys,in%20less%20than%2045%20days.]), closing on a house could take between 40-60 days. This process could be significantly streamlined to be faster and safer across the board. 

### The Solution: 
Our process aims to cut out the bureaucracy when conducting private-equity like transactions such as purchasing a house. For our example, we chose real-estate as our example to showcase the simplicity to provide investors the ability to purchase or sell houses as NFT. For our current software, the four "investors": Kayla, Jack, Ravi, Gabriel were alloted 25 coins that represented their "shares" of the asset. For simplicity, the maximum coins an individual can own is 100 coins (which represents all coins outstanding). This solutions is beneficial as it can enable liquidity within private-equity style assets, our platform acts similar to a public stock exchange where buyers can buy-and-sell tokens at will. However, unlike a public stock exchange, the asset value is more regulated being pegged to the Zillow Estimate (Zestimates) to ground the value of the asset to reality, preventing pump-and-dumps, and most importantly preventing bubbles from being created. Our software can take the time to purchase a house from **40-60** days to as little as **5-10 minutes** with transactions occuring within a blink of an eye. 


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
9. Json
10. Time
11. Threading

## Necessary Files:
1. **HomePage.py**: Parent directory for the app. Contains the instructions on how to navigate across our software.
2. **Pages Folder**:
   - NFT_Tokens&Ownership.py: Calls in the **OwnershipToken.sol** and **RealEstateNFT.sol** solidity files
   - Real_Estate_Token_Interface.py:
      - Tab 1: Calls in the real-estate price, and asset returns (on a $ amount since inception).
      - Tab 2: Calls in photos from the Zillow API to view any and all images from the house. 
      - Tab 3: Contains mortgage calculator for investors to stress-test how applying leverage could impact their monthly payments.
      - Tab 4: Contains a more in-depth sensitivity analysis to provide investors with greater ability to make an investment decision based on stress-testing: interest-rate, vacancy, insurance costs and how that could impact the cashflows from the asset.
   - Zillow_Location.py: Map function for potential investors to view the location of the real-estate.
   - zillow_url: Contains the url's of the photos for additional viewing

4. **contracts folder**:
   - OwnershipToken.sol: Fungible token (allows the NFT to have multiple coin-holders)
   - RealEstateNFT.sol: Non-Fungible creation which allows the creation of the house as a 1 of 1.
      -  **compiled folder**
         -  OwnershipToken.json: Contains the contract address for the OwnershipToken
         -  RealEstateNFT.json: Contains the contract address for the RealEstateNFT.json
         
   
   
   **RealEstateNFT.sol**: Creates the house token to be used for transactions.
9. **OwnershipToken.sol**: Assigns % of tokens to the shareholders (manages the OWN token). 

## Steps to deploy - Stage 1:
The following videos contain detailed step by step instructions from compiling the NFT token, connecting to Metamask, deployment of the token, transacting between investors and calculating asset returns.
1. https://youtu.be/ViRI_zeGosQ: Compiling the NFT. 
2. https://youtu.be/bvUSPix2aBQ: Deployment NFT & Interlinking with MetaMask.
3. https://youtu.be/j5mqZS82bkA: Enabling transactions between investors.
4. https://youtu.be/nmHxF00BNPM: Real-Estate/Asset analysis to determine investment returns and valuation.
   
## RealEstate DApp - Stage 2:
Pages & Navigation: 
1. **HomePage**
2. **NFTTokens&Ownership**
3. **Real Estate Token Interface**
4. **Zillow Location**

## Navigation - Stage 3:
To navigate through the app, use the sidebar on the left. Here are the main sections available:
1. **Home:** You are currently here. This section provides an overview and navigation instructions.
2. **NFT Tokens and Ownership:** This section allows you to mint an NFT that will represent the real estate property you want to invest in.
This needs to be done under a holding company, also known as an LLC. Through this, each stakeholder in the LLC has the ability to purchase or sell to others in the LLC.
Here are some basic rules: 
   - There are a total of 100 shares, each representing 1% ownership of the property.
   - You can not sell to yourself. Only to other individuals in the LLC or back to the holding company itself.
   - You can make updates to your contract's description once its deployed and even update the house's value.
3. **Real Estate Token Interface:** This gives you interactive tools and resources regarding the asset your investing in. This includes ... 
   - Real Estate Valuation Visualization (past 10 years)
   - Current Asset Photos According to Zillow 
   - Mortgate Repayments Calculator 
   - Real Investment Analysis similar to a Pro Forma that is used to project the financial aspect of buying and leasing a home 


## Future Applications of Software 
Our software can be adapted to other private-equity backed assets as our platform effectively acts as a way to purchase and sell any security pegged to cashflows from the asset. This allows the software to tap into the speed, accessibility, and security of crypto-currency with the asset price pegged to a value deemed appropriate. For our example we used the Zillow Zestimates, we can also used a 'Discounted Cashflow Model' for buyers and sellers to find an appropriate pricing for their assets. Mainly the following can be achieved:
1. **Improve available analytics for property valuation**: Buyers & Sellers can use alternatives to value real-estate (or any asset for that matter).
2. **Open doors for creating financial instruments**: Through crypto-currency, individuals can use more complex financial instruments such as options contracts, or shorting to bet on or against price increase/decrease of a particular asset. Furthermore, this could introduce liquidity across private-equity.
3. **Host Multiple Assets**: Investors could have accounts where they can view multiple holdings (beyond real-estate).
4. **Exchange tokens for ETH**: Individuals could exchange the OWN tokens to Ethereum. 


## Sources: 
1. https://stackoverflow.com/questions/12309269/how-do-i-write-json-data-to-a-file
2. https://rapidapi.com/tvhaudev/api/zillow-base1
3. https://www.squash.io/how-to-convert-json-to-csv-in-python/
5. Generative AI (ChatGPT) 
6. https://www.youtube.com/watch?v=GwFQg8ROZfo&t=1015s
7. Python Instructor: Edward Rees, Adjunct Professor University of San Francisco: https://www.edwardrees.info
8. UCB Fintech Bootcamp Tutor
9. https://www.leewayhertz.com/fractionalized-nft/#:~:text=NFT%20fractionalization%20offers%20the%20same%20benefit%20to%20NFT%20investors.&text=To%20fractionalize%20an%20NFT%2C%20it,partial%20ownership%20of%20the%20NFT
10. https://github.com/pixegami/streamlit-demo-app
11. https://realpython.com/intro-to-python-threading/ 





