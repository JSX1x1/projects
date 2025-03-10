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

// Example token addresses (ERC-20 contracts) and user address
const userAddress = "<USER_ADDRESS>";
const tokenAddresses = [
    "<TOKEN_ADDRESS_1>",
    "<TOKEN_ADDRESS_2>",
    // Add more token addresses here
];

getBalances(userAddress, tokenAddresses);
