// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/token/ERC20/ERC20.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/token/ERC20/ERC20Detailed.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/token/ERC20/ERC20Mintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/ownership/Ownable.sol";

contract OwnershipToken is ERC20, ERC20Detailed, ERC20Mintable, Ownable {
    uint256 public initialPropertyPrice;
    uint256 public currentPropertyValue;
    mapping(address => uint256) private initialTokenValues;

    constructor(uint256 _initialPropertyPrice, uint256 _currentPropertyValue) ERC20Detailed("OwnershipToken", "OWN", 2) public {
        initialPropertyPrice = _initialPropertyPrice;
        currentPropertyValue = _currentPropertyValue;
        _mint(msg.sender, 100 * (10 ** uint256(decimals()))); // Mint 100 tokens to owner
        initialTokenValues[msg.sender] = _initialPropertyPrice / 100; // Set initial value for the owner
    }

    function updateTokenValue(uint256 newPropertyValue) public onlyOwner {
        currentPropertyValue = newPropertyValue;
    }

    function getTokenValue() public view returns (uint256) {
        return currentPropertyValue / 100;
    }

    function purchaseTokens() public payable {
        uint256 tokenPrice = getTokenValue();
        uint256 tokensToMint = msg.value / tokenPrice;
        require(tokensToMint > 0, "Not enough ETH sent to purchase tokens");

        _mint(msg.sender, tokensToMint);
        initialTokenValues[msg.sender] = tokenPrice; // Record the token acquisition value
    }

    // Override transfer function to include additional checks
    function transfer(address recipient, uint256 amount) public returns (bool) {
        require(recipient != msg.sender, "Sender cannot transfer tokens to themselves.");
        require(amount > 0, "Transfer amount must be greater than 0.");
        require(balanceOf(msg.sender) >= amount, "Sender does not have enough tokens to transfer.");

        _transfer(msg.sender, recipient, amount);
        initialTokenValues[recipient] = initialTokenValues[msg.sender]; // Set the initial value for the recipient
        emit Transfer(msg.sender, recipient, amount); // Emit Transfer event
        return true;
    }

    function getInitialTokenValue(address account) public view returns (uint256) {
        return initialTokenValues[account];
    }
}
