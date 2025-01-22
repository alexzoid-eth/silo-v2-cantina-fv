// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { SiloConfig } from "silo-core/contracts/SiloConfig.sol";
import { ISiloConfig } from "silo-core/contracts/interfaces/ISiloConfig.sol";

contract SiloConfigHarness is SiloConfig {
    constructor(
        uint256 _siloId, 
        ConfigData memory _configData0,
        ConfigData memory _configData1
    ) SiloConfig(_siloId, _configData0, _configData1) { }   
}
