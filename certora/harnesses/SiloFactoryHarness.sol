// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { SiloFactory } from "silo-core/contracts/SiloFactory.sol";

 contract SiloFactoryHarness is SiloFactory {
    constructor(address _daoFeeReceiver) SiloFactory(_daoFeeReceiver) { }
}