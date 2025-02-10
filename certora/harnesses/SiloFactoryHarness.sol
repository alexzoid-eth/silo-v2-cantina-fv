// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { SiloFactory } from "silo-core/contracts/SiloFactory.sol";
import { ISiloConfig } from "silo-core/contracts/SiloConfig.sol";

 contract SiloFactoryHarness is SiloFactory {
    constructor(address _daoFeeReceiver) SiloFactory(_daoFeeReceiver) { }

    // Override due to its complexity
    function createSilo( 
        ISiloConfig.InitData memory _initData,
        ISiloConfig _siloConfig,
        address _siloImpl,
        address _shareProtectedCollateralTokenImpl,
        address _shareDebtTokenImpl
        ) external override { }
}