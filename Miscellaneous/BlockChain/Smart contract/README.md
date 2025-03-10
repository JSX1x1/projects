# Deploying an Ethereum Smart Contract (Step-by-Step)

This guide will help you deploy a smart contract on Ethereum using **Remix IDE**, **MetaMask**, and **the Sepolia test network**.

---

## **1️⃣ Set Up MetaMask**
### ✅ **Install & Configure**
- Download and install **MetaMask**: [https://metamask.io/](https://metamask.io/)
- Create a wallet and **switch to the Sepolia Test Network**:
  1. Open MetaMask.
  2. Click on the network dropdown (top).
  3. Select **Sepolia Test Network**.
  4. If it’s not visible, enable it in **Settings > Advanced Networks**.

---

## **2️⃣ Get Free Test ETH**
Since we're using the test network, we need **test ETH** to cover gas fees.  
### 🔗 **Get Test ETH from a Faucet**
- Visit: [Alchemy Faucet](https://www.alchemy.com/faucets) (or search for **"Sepolia ETH faucet"**).
- Paste your MetaMask **wallet address** and request test ETH.

---

## **3️⃣ Open Remix IDE**
- Go to **[Remix Ethereum IDE](https://remix.ethereum.org/)**.
- Remix is an online tool for writing, compiling, and deploying Solidity smart contracts.

---

## **4️⃣ Create a New Solidity File**
1. Click the **"+" icon** in the "File Explorers" panel (left side).
2. Name the file **SimpleStorage.sol** (**.sol** = Solidity file extension).
3. Copy & paste the following contract:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {

    uint storedData;  // This is where we store the number

    // This function lets you set (store) a number
    function set(uint x) public {
        storedData = x;
    }

    // This function lets you get (retrieve) the stored number
    function get() public view returns (uint) {
        return storedData;
    }
}
```
### For Advanced/ Intermediate BlockChain Developers

This code comes with following extensions:

✅ **Owner-based access control**  
✅ **Events for logging transactions**  
✅ **Mappings for user balances**  
✅ **Deposit & withdrawal functionality**  
✅ **Security features (reentrancy protection, access control, and SafeMath)**  


```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

import "@openzeppelin/contracts/utils/math/SafeMath.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AdvancedVault is Ownable {
    using SafeMath for uint256;

    mapping(address => uint256) private balances;
    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    event EmergencyWithdraw(address indexed owner, uint256 amount);
    
    // Modifier to prevent reentrancy attacks
    bool private locked;
    modifier noReentrant() {
        require(!locked, "Reentrancy detected!");
        locked = true;
        _;
        locked = false;
    }

    constructor() Ownable(msg.sender) {}

    // Function to deposit ETH into the contract
    function deposit() external payable {
        require(msg.value > 0, "Deposit must be greater than zero");
        balances[msg.sender] = balances[msg.sender].add(msg.value);
        emit Deposit(msg.sender, msg.value);
    }

    // Function to withdraw ETH from the contract
    function withdraw(uint256 amount) external noReentrant {
        require(amount > 0, "Withdrawal amount must be greater than zero");
        require(balances[msg.sender] >= amount, "Insufficient balance");
        
        balances[msg.sender] = balances[msg.sender].sub(amount);
        payable(msg.sender).transfer(amount);

        emit Withdrawal(msg.sender, amount);
    }

    // Allows the owner to withdraw all funds in case of an emergency
    function emergencyWithdraw() external onlyOwner {
        uint256 contractBalance = address(this).balance;
        require(contractBalance > 0, "No funds available");

        payable(owner()).transfer(contractBalance);
        emit EmergencyWithdraw(owner(), contractBalance);
    }

    // Function to check user balance
    function getBalance(address user) external view returns (uint256) {
        return balances[user];
    }

    // Fallback function to accept ETH transfers
    receive() external payable {
        deposit();
    }
}
```

---

## **5️⃣ Compile the Smart Contract**
1. Click the **Solidity Compiler icon** (Ethereum logo in Remix).
2. Select **Compiler Version** `0.8.x` (must match `^0.8.0` in the contract).
3. Click **Compile SimpleStorage.sol**.
4. If successful, a **green checkmark ✅** appears.

---

## **6️⃣ Deploy the Smart Contract**
1. Click the **Deploy & Run Transactions** icon (Ethereum logo with an arrow).
2. In the **Environment** dropdown, select **Injected Provider - MetaMask**.
   - MetaMask will ask to **connect Remix to your wallet** → Click **Confirm**.
3. Make sure the **Contract** is set to `SimpleStorage`.
4. Click **Deploy** and confirm the MetaMask transaction.

---

## **7️⃣ Interact with the Smart Contract**
Once deployed, you’ll see the contract listed under **"Deployed Contracts"**.

### **📝 Set a Number**
1. Enter a number in the **set** input field (e.g., `123`).
2. Click **set**, then confirm the transaction in MetaMask.
3. This stores the number on the blockchain.

### **🔍 Retrieve the Number**
1. Click **get**.
2. The stored number appears below the button (**this action is free**).

---

## **🛑 Important Notes**
- **Gas Fees**: Writing data (`set`) requires **gas fees**, but reading (`get`) is **free**.
- **Sepolia Testnet**: Make sure you are on the **Sepolia Test Network** to avoid spending real ETH.
- **Transaction Status**: You can track transactions in MetaMask or on **[Sepolia Etherscan](https://sepolia.etherscan.io/)**.
- **Contract Address**: After deployment, Remix will show the **contract address** (used for interacting with the contract elsewhere).

---

## **🎯 Next Steps**
✅ Experiment by modifying the contract (e.g., add more functions).  
✅ Deploy to **Goerli or Ethereum Mainnet** (requires real ETH).  
✅ Use **Web3.js or Ethers.js** to interact with the contract from a website.  

---

And done. Its that simple to do by using these steps!
Best time in learning,
JSX_1x1