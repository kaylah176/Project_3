// SPDX-License-Identifier: MIT
pragma solidity ^0.5.5;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/token/ERC721/ERC721Full.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/token/ERC721/ERC721Mintable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/v2.5.0/contracts/ownership/Ownable.sol";

contract RealEstateNFT is ERC721Full, ERC721Mintable, Ownable {
    struct Property {
        string propertyAddress;
        uint256 initialPurchasePrice;
        string holdingCompanyName;
        string description;
        uint256 currentPropertyValue;
    }

    mapping(uint256 => Property) public properties;

    constructor() ERC721Full("RealEstateNFT", "REALESTATE") public {}

    function mintProperty(
        address to,
        uint256 tokenId,
        string memory propertyAddress,
        uint256 initialPurchasePrice,
        string memory holdingCompanyName,
        string memory description,
        uint256 currentPropertyValue
    ) public onlyMinter {
        _mint(to, tokenId);
        properties[tokenId] = Property(
            propertyAddress,
            initialPurchasePrice,
            holdingCompanyName,
            description,
            currentPropertyValue
        );
    }

    function updateDescription(uint256 tokenId, string memory newDescription) public {
        require(ownerOf(tokenId) == msg.sender, "Caller is not the owner");
        properties[tokenId].description = newDescription;
    }

    function updateCurrentPropertyValue(uint256 tokenId, uint256 newValue) public {
        require(ownerOf(tokenId) == msg.sender, "Caller is not the owner");
        properties[tokenId].currentPropertyValue = newValue;
    }
}
