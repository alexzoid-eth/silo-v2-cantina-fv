// Import this file in single Silo configuration

import "../silo/silo_common.spec";

import "./collateral_share_token_0.spec";
import "./share_debt_token_0.spec";
import "./share_protected_collateral_token_0.spec";
import "./token_0.spec";
import "../../valid_state/silo0_valid_state_invariants.spec";

using Silo0 as _Silo0;

// Valid state for Silo0. You only one of these functions to setup the whole Silo0 

function requireValidSilo0() {
    // Common for Silo0 and Silo1
    requireValidSiloCommon();

    // Valid state invariants working both for Silo0
    requireSilo0ValidState();
}

function requireValidSilo0E(env e) {
    requireValidSilo0();

    // Common for Silo0 and Silo1
    requireValidSiloCommonE(e);

    // Valid state invariants working both for Silo0
    requireSilo0ValidStateE(e);
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
