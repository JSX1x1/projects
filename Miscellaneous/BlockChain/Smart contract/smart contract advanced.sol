// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Incase for this to work you will need to install those dependencies!
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/utils/math/SafeMath.sol";

// SimpleStorage contract with advanced features
contract AdvancedStorage is Ownable, Initializable, ReentrancyGuard {
    using SafeMath for uint;

    uint256 private storedData;  // Variable to store the data

    // Event to log when the stored data is updated
    event DataStored(uint256 newData, address updatedBy);

    // Initializer function (for upgradeable contracts)
    function initialize() public initializer {
        storedData = 0;  // Initialize with a default value
    }

    // Function to set the stored value with access control for the owner
    function set(uint256 x) public onlyOwner nonReentrant {
        require(x > 0, "Value must be greater than zero"); // Prevent malicious behavior
        storedData = x;
        emit DataStored(storedData, msg.sender);  // Log the change
    }

    // Function to get the stored value
    function get() public view returns (uint256) {
        return storedData;
    }

    // Function to reset the stored value (only callable by the owner)
    function reset() public onlyOwner nonReentrant {
        storedData = 0;
        emit DataStored(storedData, msg.sender);  // Log the reset
    }

    // Function to upgrade the contract (used with a proxy pattern)
    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}
}
