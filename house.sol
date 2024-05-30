// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
// import "@openzeppelin/contracts/access/Ownable.sol";

// Currently open to everyone 

contract HomeNFT is ERC721URIStorage{
    constructor() ERC721("HomeNFT","HOME"){}

    function mint(
        address _to,
        uint256 _tokenId,
        string calldata _uri) 
    external{
        _mint(_to, _tokenId);
        _setTokenURI(_tokenId, _uri);
    }

}