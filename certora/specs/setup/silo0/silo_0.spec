// Import this file in single Silo configuration

import "../silo/silo_common.spec";

import "./collateral_share_token_0.spec";
import "./share_debt_token_0.spec";
import "./share_protected_collateral_token_0.spec";
import "./token_0.spec";
import "./silo_0_valid_state.spec";

using Silo0 as _Silo0;

function requireValidSilo0Env(env e) {

    // Common environment for all tested contracts
    requireValidEnv(e);

    // Silo0 specific environment
    require(e.msg.sender != _CollateralShareToken0 
        && e.msg.sender != _ShareDebtToken0
        && e.msg.sender != _ShareProtectedCollateralToken0
        && e.msg.sender != _Token0
        );

    // Common valid state invariants working both for Silo0 and Silo1
    requireSiloCommonValidStateEnv(e);

    // Silo0 specific valid state invariants
    requireSilo0ValidStateEnv(e);
}

// IERC20R

hook Sload uint256 val _Silo0.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] {
    require(require_uint256(ghostReceiveAllowances[_Silo0][owner][recipient]) == val);
}

hook Sstore _Silo0.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] uint256 val {
    ghostReceiveAllowances[_Silo0][owner][recipient] = val;
}

// SiloStorage

// Hooks for `SiloStorage.daoAndDeployerRevenue`

hook Sload uint192 val _Silo0.siloStorage.daoAndDeployerRevenue {
    require(require_uint192(ghostDaoAndDeployerRevenue[_Silo0]) == val);
}

hook Sstore _Silo0.siloStorage.daoAndDeployerRevenue uint192 val {
    ghostDaoAndDeployerRevenue[_Silo0] = val;
}

// Hooks for `SiloStorage.interestRateTimestamp`

hook Sload uint64 val _Silo0.siloStorage.interestRateTimestamp {
    require(require_uint64(ghostInterestRateTimestamp[_Silo0]) == val);
}

hook Sstore _Silo0.siloStorage.interestRateTimestamp uint64 val {
    ghostInterestRateTimestamp[_Silo0] = val;
}

// Hooks for `SiloStorage.totalAssets`

hook Sload uint256 val _Silo0.siloStorage.totalAssets[KEY ISilo.AssetType assetType] {
    require(require_uint256(ghostTotalAssets[_Silo0][to_mathint(assetType)]) == val);
}

hook Sstore _Silo0.siloStorage.totalAssets[KEY ISilo.AssetType assetType] uint256 val {
    ghostTotalAssets[_Silo0][to_mathint(assetType)] = val;
}
