pragma solidity ^0.5.0;

import "./KaseiCoin.sol";
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
contract KaseiCoinCrowdsale is Crowdsale, MintedCrowdsale {
    PropertyDetails public property;
    uint256 public minimumHoldingPeriod;
    mapping(address => uint256) public tokenHoldingStartTime;

    // Constructor for the crowdsale, setting initial values
    constructor(
        uint rate,
        address payable wallet,
        KaseiCoin token,
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
contract KaseiCoinCrowdsaleDeployer {
    address public kasei_token_address;
    address public kasei_crowdsale_address;

    constructor(
       string memory name,
       string memory symbol, 
       address payable wallet,
       string memory propertyLocation,
       uint256 propertySize,
       uint256 propertyValue,
       string memory propertyType
    ) public {
        KaseiCoin token = new KaseiCoin(name, symbol, 0);
        kasei_token_address = address(token);

        KaseiCoinCrowdsale kasei_crowdsale = new KaseiCoinCrowdsale(
            1, 
            wallet, 
            token,
            propertyLocation,
            propertySize,
            propertyValue,
            propertyType
        );
        kasei_crowdsale_address = address(kasei_crowdsale);

        token.addMinter(kasei_crowdsale_address);
        token.renounceMinter();
    }
}
