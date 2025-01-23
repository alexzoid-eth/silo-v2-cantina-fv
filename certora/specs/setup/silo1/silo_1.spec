// Import this file among with `silo0/silo0.spec` in full Silo configuration 

import "../silo/silo_common.spec";

import "./collateral_share_token_1.spec";
import "./share_debt_token_1.spec";
import "./share_protected_collateral_token_1.spec";
import "./token_1.spec";
import "./silo1_valid_state_invariants.spec";

using Silo1 as _Silo1;

// Valid state for Silo1. You only one of these functions to setup the whole Silo1

function requireValidSilo1() {
    // Valid state for Silo1
    requireValidSilo1();
}

function requireValidSilo1Env(env e) {

    // Valid state for Silo1
    requireValidSilo1Env(e);

    // Silo0 specific environment
    require(e.msg.sender != _CollateralShareToken1
        && e.msg.sender != _ShareDebtToken1
        && e.msg.sender != _ShareProtectedCollateralToken1
        && e.msg.sender != _Token1
        );
}

// SiloStorage

// Hooks for `SiloStorage.daoAndDeployerRevenue`

hook Sload uint192 val _Silo1.siloStorage.daoAndDeployerRevenue {
    require(require_uint192(ghostDaoAndDeployerRevenue[_Silo1]) == val);
}

hook Sstore _Silo1.siloStorage.daoAndDeployerRevenue uint192 val {
    ghostDaoAndDeployerRevenue[_Silo1] = val;
}

// Hooks for `SiloStorage.interestRateTimestamp`

hook Sload uint64 val _Silo1.siloStorage.interestRateTimestamp {
    require(require_uint64(ghostInterestRateTimestamp[_Silo1]) == val);
}

hook Sstore _Silo1.siloStorage.interestRateTimestamp uint64 val {
    ghostInterestRateTimestamp[_Silo1] = val;
}

// Hooks for `SiloStorage.totalAssets`

hook Sload uint256 val _Silo1.siloStorage.totalAssets[KEY ISilo.AssetType assetType] {
    require(require_uint256(ghostTotalAssets[_Silo1][to_mathint(assetType)]) == val);
}

hook Sstore _Silo1.siloStorage.totalAssets[KEY ISilo.AssetType assetType] uint256 val {
    ghostTotalAssets[_Silo1][to_mathint(assetType)] = val;
}
