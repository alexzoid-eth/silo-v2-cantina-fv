// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

contract HelperCVL {
    function assertOnFalse(bool b) external pure {
        assert(b);
    }
}