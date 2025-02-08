// Import this file among with `silo0/silo0.spec` in full Silo configuration 

import "../silo/silo_common.spec";

import "./collateral1.spec";
import "./debt1.spec";
import "./protected1.spec";

using Silo1 as _Silo1;

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
