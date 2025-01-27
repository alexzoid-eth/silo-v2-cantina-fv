// Silo config contract support

import "./silo_config_cross_reentrancy_guard_cvl.spec";

using SiloConfigHarness as _SiloConfig;

methods {

    // Resolve external calls to SiloConfig
    
    function _.getConfig(address _silo) external
        => DISPATCHER(true);

    function _.getFeesWithAsset(address _silo) external
        => DISPATCHER(true);

    function _.getCollateralShareTokenAndAsset(address _silo, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);
}

// Immutables

persistent ghost address ghostConfigSilo0 {
    axiom ghostConfigSilo0 == _SiloConfig._SILO0;
}

persistent ghost address ghostConfigSilo1 {
    axiom ghostConfigSilo1 == _SiloConfig._SILO1;
}

persistent ghost mathint ghostConfigDaoFee {
    axiom ghostConfigDaoFee == _SiloConfig._DAO_FEE;
}

persistent ghost mathint ghostConfigDeployerFee {
    axiom ghostConfigDeployerFee == _SiloConfig._DEPLOYER_FEE;
}

// Storage hooks

persistent ghost mapping(address => address) ghostConfigBorrowerCollateralSilo {
    init_state axiom forall address borrower. ghostConfigBorrowerCollateralSilo[borrower] == 0;
    // Can be silo0 or silo1
    axiom forall address borrower. ghostConfigBorrowerCollateralSilo[borrower] == _SiloConfig._SILO0 
        || ghostConfigBorrowerCollateralSilo[borrower] == _SiloConfig._SILO1;
}

hook Sload address collateralSilo _SiloConfig.borrowerCollateralSilo[KEY address borrower] {
    require(ghostConfigBorrowerCollateralSilo[borrower] == collateralSilo);
}

hook Sstore _SiloConfig.borrowerCollateralSilo[KEY address borrower] address collateralSilo {
    ghostConfigBorrowerCollateralSilo[borrower] = collateralSilo;
}