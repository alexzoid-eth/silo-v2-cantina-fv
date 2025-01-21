// Import this file in single Silo configuration

import "../silo/silo_common.spec";

import "./collateral_share_token_0.spec";
import "./share_debt_token_0.spec";
import "./share_protected_collateral_token_0.spec";
import "./token_0.spec";

using Silo0 as _Silo0;

// IERC20R

hook Sload uint256 val _Silo0.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] {
    require(require_uint256(ghostReceiveAllowances[executingContract][owner][recipient]) == val);
}

hook Sstore _Silo0.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] uint256 val {
    ghostReceiveAllowances[executingContract][owner][recipient] = val;
}

// SiloStorage

// Hooks for `SiloStorage.daoAndDeployerRevenue`

hook Sload uint192 val _Silo0.siloStorage.daoAndDeployerRevenue {
    require(require_uint192(ghostDaoAndDeployerRevenue[executingContract]) == val);
}

hook Sstore _Silo0.siloStorage.daoAndDeployerRevenue uint192 val {
    ghostDaoAndDeployerRevenue[executingContract] = val;
}

// Hooks for `SiloStorage.interestRateTimestamp`

hook Sload uint64 val _Silo0.siloStorage.interestRateTimestamp {
    require(require_uint64(ghostInterestRateTimestamp[executingContract]) == val);
}

hook Sstore _Silo0.siloStorage.interestRateTimestamp uint64 val {
    ghostInterestRateTimestamp[executingContract] = val;
}

// Hooks for `SiloStorage.totalAssets`

hook Sload uint256 val _Silo0.siloStorage.totalAssets[KEY ISilo.AssetType assetType] {
    require(require_uint256(ghostTotalAssets[executingContract][to_mathint(assetType)]) == val);
}

hook Sstore _Silo0.siloStorage.totalAssets[KEY ISilo.AssetType assetType] uint256 val {
    ghostTotalAssets[executingContract][to_mathint(assetType)] = val;
}
