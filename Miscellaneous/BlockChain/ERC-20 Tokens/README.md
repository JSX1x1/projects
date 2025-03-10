# ERC-20 Token Management & Listing

This repository contains four separate Solidity contracts that work together to manage and interact with ERC-20 tokens. The contracts include:

1. **Token Balance Checker**: To check the balances of ERC-20 tokens for a specific user.
2. **Token Manager**: To transfer and approve ERC-20 tokens for management.
3. **ERC-20 Token Contract**: To create and manage your own ERC-20 tokens (for context).
4. **ERC-20 Token**: A basic ERC-20 token contract that can be deployed and used to create custom tokens.

Each contract serves a unique purpose. These contracts can be deployed to the Ethereum network or any Ethereum-compatible chain such as Binance Smart Chain, Polygon, etc.

---

## Table of Contents

1. [Token Balance Checker](#token-balance-checker)
    - Purpose
    - How It Works
    - Example Usage
2. [Token Manager](#token-manager)
    - Purpose
    - How It Works
    - Example Usage
3. [ERC-20 Token Contract](#erc-20-token-contract)
    - Purpose
    - How It Works
    - Example Usage
4. [ERC-20 Token](#erc-20-token)
    - Purpose
    - How It Works
    - Example Usage

---

## Token Balance Checker

### Purpose

The **Token Balance Checker** contract is designed to check the balances of multiple ERC-20 tokens for a specific user. By providing an array of token addresses and a user address, this contract returns an array of balances for each token.

### How It Works

- The contract defines an interface for ERC-20 tokens (`IERC20`).
- The `getBalances` function takes the user's address and a list of ERC-20 token contract addresses.
- It returns an array of balances corresponding to each of the provided tokens.

### Example Usage

#### Example Solidity Code:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
}

contract TokenBalanceChecker {
    function getBalances(address user, address[] memory tokenAddresses) public view returns (uint256[] memory) {
        uint256[] memory balances = new uint256[](tokenAddresses.length);
        for (uint256 i = 0; i < tokenAddresses.length; i++) {
            IERC20 token = IERC20(tokenAddresses[i]);
            balances[i] = token.balanceOf(user);
        }
        return balances;
    }
}
```

#### How to Use:

1. Deploy the contract.
2. Call the `getBalances` function with the user’s address and an array of ERC-20 token contract addresses.
3. It will return an array with the balances of each token that the user holds.

#### Frontend (JavaScript) Example:

You can use **ethers.js** to interact with this contract.

```javascript
const { ethers } = require("ethers");

async function getBalances(userAddress, tokenAddresses) {
    const provider = new ethers.JsonRpcProvider("<INFURA_OR_ALCHEMY_URL>");
    const contract = new ethers.Contract(
        "<TOKEN_BALANCE_CHECKER_CONTRACT_ADDRESS>",
        ["function getBalances(address user, address[] memory tokenAddresses) public view returns (uint256[] memory)"],
        provider
    );

    const balances = await contract.getBalances(userAddress, tokenAddresses);
    console.log(balances); // Outputs an array of token balances
}

const userAddress = "<USER_ADDRESS>";
const tokenAddresses = [
    "<TOKEN_ADDRESS_1>",
    "<TOKEN_ADDRESS_2>",
    // Add more token addresses here
];

getBalances(userAddress, tokenAddresses);
```

---

## Token Manager

### Purpose

The **Token Manager** contract allows users to manage their ERC-20 tokens. Users can transfer tokens to other addresses and approve third-party spenders to use their tokens.

### How It Works

- The contract interacts with ERC-20 tokens by using the `IERC20` interface.
- Users can:
  - Transfer tokens using the `transferTokens` function.
  - Approve a third-party spender to use their tokens with the `approveTokens` function.
  - Check their token balance with the `getTokenBalance` function.

### Example Usage

#### Example Solidity Code:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract TokenManager {
    function transferTokens(address tokenAddress, address recipient, uint256 amount) public returns (bool) {
        IERC20 token = IERC20(tokenAddress);
        require(token.balanceOf(msg.sender) >= amount, "Insufficient balance");
        bool success = token.transfer(recipient, amount);
        require(success, "Transfer failed");
        return true;
    }

    function approveTokens(address tokenAddress, address spender, uint256 amount) public returns (bool) {
        IERC20 token = IERC20(tokenAddress);
        bool success = token.approve(spender, amount);
        require(success, "Approval failed");
        return true;
    }

    function getTokenBalance(address tokenAddress) public view returns (uint256) {
        IERC20 token = IERC20(tokenAddress);
        return token.balanceOf(msg.sender);
    }
}
```

#### How to Use:

1. Deploy the contract.
2. Users can call the following functions:
   - `transferTokens` to transfer tokens to another address.
   - `approveTokens` to approve another address to spend tokens on their behalf.
   - `getTokenBalance` to check the token balance of the caller (user).

#### Frontend (JavaScript) Example:

```javascript
const { ethers } = require("ethers");

async function transferTokens(tokenAddress, recipient, amount) {
    const provider = new ethers.JsonRpcProvider("<INFURA_OR_ALCHEMY_URL>");
    const wallet = new ethers.Wallet("<PRIVATE_KEY>", provider);

    const contract = new ethers.Contract(
        "<TOKEN_MANAGER_CONTRACT_ADDRESS>",
        [
            "function transferTokens(address tokenAddress, address recipient, uint256 amount) public returns (bool)"
        ],
        wallet
    );

    const tx = await contract.transferTokens(tokenAddress, recipient, amount);
    console.log("Transaction Hash:", tx.hash);
    await tx.wait();
    console.log("Transfer Complete!");
}

async function approveTokens(tokenAddress, spender, amount) {
    const provider = new ethers.JsonRpcProvider("<INFURA_OR_ALCHEMY_URL>");
    const wallet = new ethers.Wallet("<PRIVATE_KEY>", provider);

    const contract = new ethers.Contract(
        "<TOKEN_MANAGER_CONTRACT_ADDRESS>",
        [
            "function approveTokens(address tokenAddress, address spender, uint256 amount) public returns (bool)"
        ],
        wallet
    );

    const tx = await contract.approveTokens(tokenAddress, spender, amount);
    console.log("Transaction Hash:", tx.hash);
    await tx.wait();
    console.log("Approval Complete!");
}

// Example addresses and amounts
const tokenAddress = "<ERC20_TOKEN_ADDRESS>";
const recipient = "<RECIPIENT_ADDRESS>";
const spender = "<SPENDER_ADDRESS>";
const amount = ethers.utils.parseUnits("10", 18); // 10 tokens with 18 decimals

transferTokens(tokenAddress, recipient, amount);
approveTokens(tokenAddress, spender, amount);
```

---

## ERC-20 Token Contract

### Purpose

This contract allows you to create your own ERC-20 token. You can mint, burn, and transfer tokens as needed.

### How It Works

- Implements the standard ERC-20 interface for creating a fungible token.
- Provides functions like `transfer`, `approve`, `mint`, and `burn`.
- Supports minting new tokens and burning existing tokens.

### Example Usage

#### Example Solidity Code:
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transfer(address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract MyERC20Token is IERC20 {
    string public name = "MyToken";
    string public symbol = "MTK";
    uint8 public decimals = 18;
    uint256 private _totalSupply;
    mapping(address => uint256) private _balances;

    constructor(uint256 initialSupply) {
        _totalSupply = initialSupply * 10 ** uint256(decimals);
        _balances[msg.sender] = _totalSupply;
    }

    function totalSupply() public view returns (uint256) {
        return _totalSupply;
    }

    function balanceOf(address account) public view returns (uint256) {
        return _balances[account];
    }

    function transfer(address recipient, uint256 amount) public returns (bool) {
        require(_balances[msg.sender] >= amount, "Insufficient balance");
        _balances[msg.sender] -= amount;
        _balances[recipient] += amount;
        return true;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        // Implement approve logic (omitted for simplicity)
        return true;
    }

    function mint(address account, uint256 amount) public {
        _totalSupply += amount;
        _balances[account] += amount;
    }

    function burn(uint256 amount) public {
        _totalSupply -= amount;
        _balances[msg.sender] -= amount;
    }
}
```

#### How to Use:

1. Deploy the contract by passing an initial supply amount (e.g., `1000000 * 10^18`).
2. Use `mint` to create new tokens and allocate them to an account.
3. Use `burn` to destroy tokens from an account.

---

## ERC-20 Token

### Purpose

This is a simple and generic implementation of an ERC-20 token that can be deployed and interacted with for basic token operations.

### How It Works

The contract supports the following ERC-20 features:

- **Transfer**: Move tokens from one address to another.
- **Approve**: Approve a third-party to spend tokens on behalf of the sender.
- **Minting**: Create new tokens and assign them to an account.
- **Burning**: Destroy tokens from an account.