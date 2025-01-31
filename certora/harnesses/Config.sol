// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { SiloConfig } from "silo-core/contracts/SiloConfig.sol";
import { ISiloConfig } from "silo-core/contracts/interfaces/ISiloConfig.sol";

contract Config is SiloConfig {
    constructor(
        uint256 _siloId, 
        ConfigData memory _configData0,
        ConfigData memory _configData1
    ) SiloConfig(_siloId, _configData0, _configData1) { }   

    // Set as Silo0 address in single silo configuration and Silo1 in double silo configuration
    address public _LAST_SILO_ADDRESS;
}
