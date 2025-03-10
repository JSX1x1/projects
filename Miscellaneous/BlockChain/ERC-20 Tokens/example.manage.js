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
