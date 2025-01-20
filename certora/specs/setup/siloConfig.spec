// Silo config contract support

import "./siloConfigCrossReentrancyGuard.spec";

using SiloConfigHarness as _SiloConfig;

methods {

    // Resolve external calls to SiloConfig
    
    function _.getConfig(address _silo) external with (env e)
        => getConfigCVL(e) expect (ISiloConfig.ConfigData memory);

    function _.getFeesWithAsset(address _silo) external with (env e) 
        => getFeesWithAssetCVL(e) expect (uint256, uint256, uint256, address);
}

// Universal methods summarizes

function setOtherSiloAsCollateralSiloCVL(env e, address _borrower) {
    _SiloConfig.setOtherSiloAsCollateralSilo(e, _borrower);
}

// Storage hooks

persistent ghost mapping(address => address) ghostConfigBorrowerCollateralSilo {
    init_state axiom forall address borrower. ghostConfigBorrowerCollateralSilo[borrower] == 0;
}

hook Sload address collateralSilo _SiloConfig.borrowerCollateralSilo[KEY address borrower] {
    require(ghostConfigBorrowerCollateralSilo[borrower] == collateralSilo);
}

hook Sstore _SiloConfig.borrowerCollateralSilo[KEY address borrower] address collateralSilo {
    ghostConfigBorrowerCollateralSilo[borrower] = collateralSilo;
}