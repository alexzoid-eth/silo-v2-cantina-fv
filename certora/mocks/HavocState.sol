// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

interface IUnresolvedCall {
    function unresolvedCall() external;
}

contract HavocState {
    address public _target;
    function makeUnresolvedCall() external {
        IUnresolvedCall(_target).unresolvedCall();
    }
}