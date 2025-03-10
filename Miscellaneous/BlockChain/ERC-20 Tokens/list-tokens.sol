// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
}

contract TokenBalanceChecker {

    // Function to check the balance of ERC-20 tokens for a user
    function getBalances(address user, address[] memory tokenAddresses) public view returns (uint256[] memory) {
        uint256[] memory balances = new uint256[](tokenAddresses.length);

        // Loop through each token address and get the balance of the user
        for (uint256 i = 0; i < tokenAddresses.length; i++) {
            IERC20 token = IERC20(tokenAddresses[i]);
            balances[i] = token.balanceOf(user);
        }
        
        return balances;
    }
}
