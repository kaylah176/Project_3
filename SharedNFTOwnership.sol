// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract SharedNFTOwnership {
    struct Owner {
        address ownerAddress;
        uint256 ownershipShare;
    }

    Owner[4] public owners;

    constructor(
        string memory _name,
        string memory _symbol,
        address[4] memory _owners,
        uint256[4] memory _shares
    ) {
        uint256 totalShares = 0;
        for (uint256 i = 0; i < 4; i++) {
            owners[i] = Owner({
                ownerAddress: _owners[i],
                ownershipShare: _shares[i]
            });
            totalShares += _shares[i];
        }
        require(totalShares == 100, "Total shares must sum up to 100%");
    }

    function getOwnershipShare(address _owner) public view returns (uint256) {
        for (uint256 i = 0; i < owners.length; i++) {
            if (owners[i].ownerAddress == _owner) {
                return owners[i].ownershipShare;
            }
        }
        return 0;
    }

    // Placeholder function for transferring ownership
    function transferOwnership(address _newOwner) public {
        // Implement your ownership transfer logic here
        // For example, update the ownership share for the new owner
        // based on your business rules.
        // Replace this placeholder with your actual implementation.
    }
}

