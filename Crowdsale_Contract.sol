pragma solidity ^0.5.0;

import "./house.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";


// Have the KaseiCoinCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract Crowdsale_Contract is Crowdsale, MintedCrowdsale{ // UPDATE THE CONTRACT SIGNATURE TO ADD INHERITANCE
    
    // Provide parameters for all of the features of your crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(uint rate, address payable wallet, HomeNFT token)
        public
        Crowdsale(rate, wallet, token) 
      
    {
        // constructor can stay empty
    }
}


contract Crowdsale_ContractDeployer {
    // Create an `address public` variable called `kasei_token_address`.
    address public home_token_address;

    // Create an `address public` variable called `kasei_crowdsale_address`.
    address public home_crowdsale_address;

    // Add the constructor.
    constructor(
       string memory name,
       string memory symbol, 
       address payable wallet
    ) public {
        // Create a new instance of the KaseiCoin contract.
        HomeNFT token = new HomeNFT(name, symbol, 0);
        
        // Assign the token contract’s address to the `home_token_address` variable.
        home_token_address = address(token);

        // Create a new instance of the `KaseiCoinCrowdsale` contract
        HomeNFTCrowdsale home_crowdsale = new HomeNFTCrowdsale(1, wallet, token);
            
        // Aassign the `KaseiCoinCrowdsale` contract’s address to the `home_crowdsale_address` variable.
        home_crowdsale_address = address(home_crowdsale);

        // Set the `KaseiCoinCrowdsale` contract as a minter
        token.addMinter(home_crowdsale_address);
        
        // Have the `KaseiCoinCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
}
