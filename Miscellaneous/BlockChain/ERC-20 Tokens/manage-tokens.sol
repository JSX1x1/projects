// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract TokenManager {

    // Function to transfer tokens from the user's address to another address
    function transferTokens(address tokenAddress, address recipient, uint256 amount) public returns (bool) {
        IERC20 token = IERC20(tokenAddress);
        require(token.balanceOf(msg.sender) >= amount, "Insufficient balance");

        bool success = token.transfer(recipient, amount);
        require(success, "Transfer failed");
        return true;
    }

    // Function to approve another address to spend tokens on the user's behalf
    function approveTokens(address tokenAddress, address spender, uint256 amount) public returns (bool) {
        IERC20 token = IERC20(tokenAddress);
        bool success = token.approve(spender, amount);
        require(success, "Approval failed");
        return true;
    }

    // Function to check token balance (for convenience)
    function getTokenBalance(address tokenAddress) public view returns (uint256) {
        IERC20 token = IERC20(tokenAddress);
        return token.balanceOf(msg.sender);
    }
}
