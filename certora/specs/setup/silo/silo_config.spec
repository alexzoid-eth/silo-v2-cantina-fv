// Silo config contract support

import "./silo_config_cross_reentrancy_guard_cvl.spec";

using SiloConfigHarness as _SiloConfig;

methods {

    // Summarize getDebtSilo() internal call in SiloConfig to avoid unlinked `_DEBT_SHARE_TOKEN1` call 
    //  in single silo configuration

    function _SiloConfig.getDebtSilo(address _borrower) internal returns address
        => getDebtSiloCVL(_borrower);

    // Resolve external calls to SiloConfig
    
    function _.getConfig(address _silo) external
        => DISPATCHER(true);

    function _.getFeesWithAsset(address _silo) external
        => DISPATCHER(true);

    function _.getCollateralShareTokenAndAsset(address _silo, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);
}

// Summarizes

function getDebtSiloCVL(address _borrower) returns address {
    mathint debtBal0 = ghostERC20Balances[ghostConfigDebtShareToken0][_borrower];
    mathint debtBal1 = ghostERC20Balances[ghostConfigDebtShareToken0][_borrower];

    ASSERT(debtBal0 == 0 || debtBal1 == 0);

    return (debtBal0 == 0 && debtBal1 == 0) ? 0 : (debtBal0 != 0 ? ghostConfigSilo0 : ghostConfigSilo1);
}

// Immutables

definition FEE_15_PERCENT() returns mathint = 15 * 10^16;
definition FEE_30_PERCENT() returns mathint = 3 * 10^17;
definition FEE_50_PERCENT() returns mathint = 5 * 10^17;

definition silo0contractsAddress(address a) returns bool = 
    a == ghostConfigSilo0
    || a == ghostConfigDebtShareToken0
    || a == ghostConfigProtectedCollateralShareToken0
    || a == ghostConfigCollateralShareToken0
    || a == ghostConfigToken0
    || a == ghostConfigSolvencyOracle0
    || a == ghostConfigMaxLtvOracle0
    || a == ghostConfigInterestRateModel0
    ;

definition silo1contractsAddress(address a) returns bool = 
    a == ghostConfigSilo1
    || a == ghostConfigDebtShareToken1
    || a == ghostConfigProtectedCollateralShareToken1
    || a == ghostConfigCollateralShareToken1
    || a == ghostConfigToken1
    || a == ghostConfigSolvencyOracle1
    || a == ghostConfigMaxLtvOracle1
    || a == ghostConfigInterestRateModel1
    ;

persistent ghost address ghostSiloConfig {
    axiom ghostSiloConfig == _SiloConfig;
    axiom silo0contractsAddress(ghostSiloConfig) == false;
    axiom silo1contractsAddress(ghostSiloConfig) == false;
}

persistent ghost mathint ghostConfigDaoFee {
    axiom ghostConfigDaoFee == _SiloConfig._DAO_FEE;
    axiom ghostConfigDaoFee <= FEE_50_PERCENT(); 
}

persistent ghost mathint ghostConfigDeployerFee {
    axiom ghostConfigDeployerFee == _SiloConfig._DEPLOYER_FEE;
    axiom ghostConfigDeployerFee <= FEE_15_PERCENT(); 
}

// Hook Receiver
persistent ghost address ghostConfigHookReceiver {
    axiom ghostConfigHookReceiver == _SiloConfig._HOOK_RECEIVER;
    axiom silo0contractsAddress(ghostConfigHookReceiver) == false;
    axiom silo1contractsAddress(ghostConfigHookReceiver) == false;
}

persistent ghost address ghostConfigSilo0 {
    axiom ghostConfigSilo0 == _SiloConfig._SILO0;
    axiom silo1contractsAddress(ghostConfigSilo0) == false;
}

persistent ghost address ghostConfigToken0 {
    axiom ghostConfigToken0 == _SiloConfig._TOKEN0;
    axiom silo1contractsAddress(ghostConfigToken0) == false;
}

persistent ghost address ghostConfigProtectedCollateralShareToken0 {
    axiom ghostConfigProtectedCollateralShareToken0 == _SiloConfig._PROTECTED_COLLATERAL_SHARE_TOKEN0;
    axiom silo1contractsAddress(ghostConfigProtectedCollateralShareToken0) == false;
}

persistent ghost address ghostConfigCollateralShareToken0 {
    axiom ghostConfigCollateralShareToken0 == _SiloConfig._COLLATERAL_SHARE_TOKEN0;
    axiom silo1contractsAddress(ghostConfigCollateralShareToken0) == false;
}

persistent ghost address ghostConfigDebtShareToken0 {
    axiom ghostConfigDebtShareToken0 == _SiloConfig._DEBT_SHARE_TOKEN0;
    axiom silo1contractsAddress(ghostConfigDebtShareToken0) == false;
}

persistent ghost address ghostConfigSolvencyOracle0 {
    axiom ghostConfigSolvencyOracle0 == _SiloConfig._SOLVENCY_ORACLE0;
    axiom silo1contractsAddress(ghostConfigSolvencyOracle0) == false;
}

persistent ghost address ghostConfigMaxLtvOracle0 {
    axiom ghostConfigMaxLtvOracle0 == _SiloConfig._MAX_LTV_ORACLE0;
    axiom silo1contractsAddress(ghostConfigMaxLtvOracle0) == false;
}

persistent ghost address ghostConfigInterestRateModel0 {
    axiom ghostConfigInterestRateModel0 == _SiloConfig._INTEREST_RATE_MODEL0;
    axiom silo1contractsAddress(ghostConfigInterestRateModel0) == false;
}

persistent ghost mathint ghostConfigMaxLtv0 {
    axiom ghostConfigMaxLtv0 == _SiloConfig._MAX_LTV0;
}

persistent ghost mathint ghostConfigLt0 {
    axiom ghostConfigLt0 == _SiloConfig._LT0;
}

persistent ghost mathint ghostConfigLiquidationTargetLtv0 {
    axiom ghostConfigLiquidationTargetLtv0 == _SiloConfig._LIQUIDATION_TARGET_LTV0;
}

persistent ghost mathint ghostConfigLiquidationFee0 {
    axiom ghostConfigLiquidationFee0 == _SiloConfig._LIQUIDATION_FEE0;
    axiom ghostConfigLiquidationFee0 <= FEE_30_PERCENT();
}

persistent ghost mathint ghostConfigFlashloanFee0 {
    axiom ghostConfigFlashloanFee0 == _SiloConfig._FLASHLOAN_FEE0;
    axiom ghostConfigFlashloanFee0 <= FEE_15_PERCENT();
}

persistent ghost bool ghostConfigCallBeforeQuote0 {
    axiom ghostConfigCallBeforeQuote0 == _SiloConfig._CALL_BEFORE_QUOTE0;
}

persistent ghost address ghostConfigSilo1 {
    axiom ghostConfigSilo1 == _SiloConfig._SILO1;
    axiom ghostConfigSilo1 != 0;
}

persistent ghost address ghostConfigToken1 {
    axiom ghostConfigToken1 == _SiloConfig._TOKEN1;
}

persistent ghost address ghostConfigProtectedCollateralShareToken1 {
    axiom ghostConfigProtectedCollateralShareToken1 == _SiloConfig._PROTECTED_COLLATERAL_SHARE_TOKEN1;
}

persistent ghost address ghostConfigCollateralShareToken1 {
    axiom ghostConfigCollateralShareToken1 == _SiloConfig._COLLATERAL_SHARE_TOKEN1;
}

persistent ghost address ghostConfigDebtShareToken1 {
    axiom ghostConfigDebtShareToken1 == _SiloConfig._DEBT_SHARE_TOKEN1;
}

persistent ghost address ghostConfigSolvencyOracle1 {
    axiom ghostConfigSolvencyOracle1 == _SiloConfig._SOLVENCY_ORACLE1;
}

persistent ghost address ghostConfigMaxLtvOracle1 {
    axiom ghostConfigMaxLtvOracle1 == _SiloConfig._MAX_LTV_ORACLE1;
}

persistent ghost address ghostConfigInterestRateModel1 {
    axiom ghostConfigInterestRateModel1 == _SiloConfig._INTEREST_RATE_MODEL1;
}

persistent ghost mathint ghostConfigMaxLtv1 {
    axiom ghostConfigMaxLtv1 == _SiloConfig._MAX_LTV1;
}

persistent ghost mathint ghostConfigLt1 {
    axiom ghostConfigLt1 == _SiloConfig._LT1;
}

persistent ghost mathint ghostConfigLiquidationTargetLtv1 {
    axiom ghostConfigLiquidationTargetLtv1 == _SiloConfig._LIQUIDATION_TARGET_LTV1;
}

persistent ghost mathint ghostConfigLiquidationFee1 {
    axiom ghostConfigLiquidationFee1 == _SiloConfig._LIQUIDATION_FEE1;
    axiom ghostConfigLiquidationFee1 <= FEE_30_PERCENT();
}

persistent ghost mathint ghostConfigFlashloanFee1 {
    axiom ghostConfigFlashloanFee1 == _SiloConfig._FLASHLOAN_FEE1;
    axiom ghostConfigFlashloanFee1 <= FEE_15_PERCENT();
}

persistent ghost bool ghostConfigCallBeforeQuote1 {
    axiom ghostConfigCallBeforeQuote1 == _SiloConfig._CALL_BEFORE_QUOTE1;
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