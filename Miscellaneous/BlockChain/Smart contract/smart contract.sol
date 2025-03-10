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