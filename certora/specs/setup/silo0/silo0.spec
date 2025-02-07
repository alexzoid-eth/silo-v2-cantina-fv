// Import this file in single Silo configuration

import "../silo/silo_common.spec";

import "./collateral0.spec";
import "./debt0.spec";
import "./protected0.spec";
import "./token0.spec";

using Silo0 as _Silo0;

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
