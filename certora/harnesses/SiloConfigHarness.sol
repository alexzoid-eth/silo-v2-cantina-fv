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

    function onlySiloOrTokenOrHookReceiverHarness() external view {
        if (msg.sender != _SILO0 &&
            msg.sender != _SILO1 &&
            msg.sender != _HOOK_RECEIVER &&
            msg.sender != _COLLATERAL_SHARE_TOKEN0 &&
            msg.sender != _COLLATERAL_SHARE_TOKEN1 &&
            msg.sender != _PROTECTED_COLLATERAL_SHARE_TOKEN0 &&
            msg.sender != _PROTECTED_COLLATERAL_SHARE_TOKEN1 &&
            msg.sender != _DEBT_SHARE_TOKEN0 &&
            msg.sender != _DEBT_SHARE_TOKEN1
        ) {
            revert ISiloConfig.OnlySiloOrTokenOrHookReceiver();
        }
    }
}
