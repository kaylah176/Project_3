pragma solidity ^0.5.0;

import "./Token_Creation.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";

// PropertyDetails structure to store real estate information
struct PropertyDetails {
    string location;
    uint256 yearbuilt;
    uint256 squareFeet;
    uint256 purchaseprice;
    uint256 appraisalValue;
    string propertyType;
}

// Main crowdsale contract
contract AssetCoinCrowdsale is Crowdsale, MintedCrowdsale {
    PropertyDetails public property;
    uint256 public minimumHoldingPeriod;
    mapping(address => uint256) public tokenHoldingStartTime;

    // Constructor for the crowdsale, setting initial values
    constructor(
        uint rate,
        address payable wallet,
        AssetCoin token,
        string memory location,
        uint256 squareFeet,
        uint256 appraisalValue,
        string memory propertyType
    ) 
        public 
        Crowdsale(rate, wallet, token) 
    {
        property = PropertyDetails(location, squareFeet, appraisalValue, propertyType);
        minimumHoldingPeriod = 5 years;  // Minimum holding period for tokens
    }

    // Overriding the basic transfer function to include a holding period
    function transfer(address to, uint256 amount) public {
        require(block.timestamp >= tokenHoldingStartTime[msg.sender] + minimumHoldingPeriod, "Cannot transfer within holding period");
        super.transfer(to, amount);
        tokenHoldingStartTime[to] = block.timestamp;
    }

    // Function to distribute dividends based on property income
    function distributeDividends() public onlyOwner {
        uint256 income = address(this).balance;
        uint256 totalSupply = totalSupply();
        for (uint i = 0; i < totalSupply; i++) {
            address payable wallet = address(uint160(ownerOf(i)));
            wallet.transfer(income * balanceOf(wallet) / totalSupply);
        }
    }
}

// Contract deployer for the crowdsale
contract AssetCoinCrowdsaleDeployer {
    address public asset_token_address;
    address public asset_crowdsale_address;

    constructor(
       string memory name,
       string memory symbol, 
       address payable wallet,
       string memory propertyLocation,
       uint256 propertySize,
       uint256 propertyValue,
       string memory propertyType
    ) public {
        AssetCoin token = new AssetCoin(name, symbol, 0);
        asset_token_address = address(token);

        AssetCoinCrowdsale asset_crowdsale = new AssetCoinCrowdsale(
            1, 
            wallet, 
            token,
            propertyLocation,
            propertySize,
            propertyValue,
            propertyType
        );
        asset_crowdsale_address = address(asset_crowdsale);

        token.addMinter(asset_crowdsale_address);
        token.renounceMinter();
    }
}

// Here is how our smart contract is going to interact with the Zillow API key 
// We should integrate it into the above code 
// DataRetrievalContract.sol
pragma solidity ^0.8.7;

contract DataRetrievalContract {
    // Example data storage
    mapping(address => string) public propertyDetails;

    // Function to set property details
    function setPropertyDetails(address user, string memory details) public {
        propertyDetails[user] = details;
    }

    // Other oracle-related functions would go here
}

// TokenContract.sol
pragma solidity ^0.8.7;

interface IDataRetrievalContract {
    function propertyDetails(address user) external view returns (string memory);
}

contract TokenContract {
    IDataRetrievalContract public dataContract;

    constructor(address _dataContractAddress) {
        dataContract = IDataRetrievalContract(_dataContractAddress);
    }

    function getPropertyDetails(address user) public view returns (string memory) {
        return dataContract.propertyDetails(user);
    }

    // Token-specific logic here
}

