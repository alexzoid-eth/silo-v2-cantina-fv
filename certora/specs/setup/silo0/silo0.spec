import "../silo.spec";

// ShareToken
import "./collateralShareToken0.spec";
import "./shareDebtToken0.spec";
import "./shareProtectedCollateralToken0.spec";

using Silo0 as _Silo0;
using Silo0 as _ERC20;
using Silo0 as _ERC4626;

methods {
    function _Silo0.initialize(address _config) external => NONDET DELETE;
}

// ShareToken

persistent ghost mapping (address => address) ghostShareTokenSilo {
    axiom forall address contract. ghostShareTokenSilo[contract] == _Silo0;
}

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
