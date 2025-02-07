// Silo config contract support

import "./config_cvl.spec";

// Immutables

definition BP2DP_NORMALIZATION() returns mathint = 10^14;
definition CONFIG_100_PERCENT() returns mathint = 10^18;

definition FEE_5_PERCENT() returns mathint = 5 * 10^16;
definition FEE_15_PERCENT() returns mathint = 15 * 10^16;
definition FEE_30_PERCENT() returns mathint = 3 * 10^17;
definition FEE_50_PERCENT() returns mathint = 5 * 10^17;

definition silo0contractsAddress(address a) returns bool = 
    a == _Silo0
    || a == _Debt0
    || a == _Protected0
    || a == _Silo0
    || a == ghostToken0
    || a == ghostConfigSolvencyOracle0
    || a == ghostConfigMaxLtvOracle0
    || a == ghostConfigInterestRateModel0
    ;

definition silo1contractsAddress(address a) returns bool = 
    a == _Silo1
    || a == _Debt1
    || a == _Protected1
    || a == _Silo1
    || a == ghostToken1
    || a == ghostConfigSolvencyOracle1
    || a == ghostConfigMaxLtvOracle1
    || a == ghostConfigInterestRateModel1
    ;

definition ghostSiloX(bool zero) returns address = 
    zero ? ghostSilo0 : ghostSilo1;

definition ghostProtectedTokenX(bool zero) returns address = 
    zero ? ghostProtected0 : ghostProtected1;

definition ghostCollateralTokenX(bool zero) returns address = 
    ghostSiloX(zero);

definition ghostDebtTokenX(bool zero) returns address = 
    zero ? ghostDebt0 : ghostDebt1;

definition ghostTokenX(bool zero) returns address = 
    zero ? ghostToken0 : ghostToken1;

// Set true to use static config values from `silo-core/deploy/input/mainnet/FULL_CONFIG_TEST.json`
persistent ghost bool ghostUseStaticConfig;

persistent ghost mapping(address => address) ghostConfigBorrowerCollateralSilo {
    init_state axiom forall address borrower. ghostConfigBorrowerCollateralSilo[borrower] == 0;
}

persistent ghost address ghostSiloConfig;

// SAFE: Assumptions made based on `Views.validateSiloInitData()` and `SiloConfigData.getConfigData()`

persistent ghost mathint ghostConfigDaoFee {
    axiom ghostConfigDaoFee >= FEE_5_PERCENT() && ghostConfigDaoFee <= FEE_50_PERCENT(); 
}

persistent ghost mathint ghostConfigDeployerFee {
    axiom ghostConfigDeployerFee == 0 
        || ghostConfigDeployerFee >= BP2DP_NORMALIZATION() && ghostConfigDeployerFee <= FEE_15_PERCENT(); 
}

persistent ghost address ghostHookReceiver;

// Silo0

persistent ghost address ghostToken0 {
    axiom ghostToken0 == _Token0;
}

persistent ghost address ghostProtected0 {
    axiom ghostProtected0 == _Protected0;
}

persistent ghost address ghostSilo0 {
    axiom ghostSilo0 == _Silo0;
}

persistent ghost address ghostDebt0 {
    axiom ghostDebt0 == _Debt0;
}

persistent ghost address ghostConfigSolvencyOracle0;

persistent ghost address ghostConfigMaxLtvOracle0;

persistent ghost address ghostConfigInterestRateModel0;

persistent ghost mathint ghostConfigMaxLtv0 {
    // `maxLtv0: config.maxLtv0 * BP2DP_NORMALIZATION,` 
    axiom ghostConfigMaxLtv0 == 0 || 
        ghostConfigMaxLtv0 >= BP2DP_NORMALIZATION() && ghostConfigMaxLtv0 <= CONFIG_100_PERCENT();
    // `require(_initData.maxLtv0 != 0 || _initData.maxLtv1 != 0, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv0 == 0 => ghostConfigMaxLtv1 != 0;
    // `require(_initData.maxLtv0 <= _initData.lt0, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv0 <= ghostConfigLt0;
}

persistent ghost mathint ghostConfigLt0 {
    // `lt0: config.lt0 * BP2DP_NORMALIZATION`
    axiom ghostConfigLt0 >= BP2DP_NORMALIZATION() && ghostConfigLt0 <= CONFIG_100_PERCENT();
    // `require(_initData.lt0 + _initData.liquidationFee0 <= _100_PERCENT, ISiloFactory.InvalidLt());`
    axiom ghostConfigLt0 + ghostConfigLiquidationFee0 <= CONFIG_100_PERCENT();

}

persistent ghost mathint ghostConfigLiquidationTargetLtv0 {
    // `liquidationTargetLtv0: config.liquidationTargetLtv0 * BP2DP_NORMALIZATION`
    axiom ghostConfigLiquidationTargetLtv0 >= BP2DP_NORMALIZATION() 
        && ghostConfigLiquidationTargetLtv0 <= CONFIG_100_PERCENT();
    // `require(_initData.liquidationTargetLtv0 <= _initData.lt0, ISiloFactory.LiquidationTargetLtvTooHigh());`
    axiom ghostConfigLiquidationTargetLtv0 <= ghostConfigLt0;
}

persistent ghost mathint ghostConfigLiquidationFee0 {
    axiom ghostConfigLiquidationFee0 == 0 || 
        ghostConfigLiquidationFee0 >= BP2DP_NORMALIZATION() && ghostConfigLiquidationFee0 <= FEE_30_PERCENT();
}

persistent ghost mathint ghostConfigFlashloanFee0 {
    axiom ghostConfigFlashloanFee0 == 0 ||
        ghostConfigFlashloanFee0 >= BP2DP_NORMALIZATION() && ghostConfigFlashloanFee0 <= FEE_15_PERCENT();
}

persistent ghost bool ghostConfigCallBeforeQuote0;

// Silo1

persistent ghost address ghostToken1 {
    axiom ghostToken1 == _Token1;
}

persistent ghost address ghostProtected1 {
    axiom ghostProtected1 == _Protected1;
}

persistent ghost address ghostSilo1 {
    axiom ghostSilo1 == _Silo1;
}

persistent ghost address ghostDebt1 {
    axiom ghostDebt1 == _Debt1;
}

persistent ghost address ghostConfigSolvencyOracle1;

persistent ghost address ghostConfigMaxLtvOracle1;

persistent ghost address ghostConfigInterestRateModel1;

persistent ghost mathint ghostConfigMaxLtv1 {
    // `maxLtv1: config.maxLtv1 * BP2DP_NORMALIZATION,` 
    axiom ghostConfigMaxLtv1 == 0 || 
        ghostConfigMaxLtv1 >= BP2DP_NORMALIZATION() && ghostConfigMaxLtv1 <= CONFIG_100_PERCENT();
    // `require(_initData.maxLtv1 != 0 || _initData.maxLtv1 != 0, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv1 == 0 => ghostConfigMaxLtv0 != 0;
    // `require(_initData.maxLtv1 <= _initData.lt1, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv1 <= ghostConfigLt1;
}

persistent ghost mathint ghostConfigLt1 {
    // `lt1: config.lt1 * BP2DP_NORMALIZATION`
    axiom ghostConfigLt1 >= BP2DP_NORMALIZATION() && ghostConfigLt1 <= CONFIG_100_PERCENT();
    // `require(_initData.lt1 + _initData.liquidationFee1 <= _100_PERCENT, ISiloFactory.InvalidLt());`
    axiom ghostConfigLt1 + ghostConfigLiquidationFee1 <= CONFIG_100_PERCENT();

}

persistent ghost mathint ghostConfigLiquidationTargetLtv1 {
    // `liquidationTargetLtv1: config.liquidationTargetLtv1 * BP2DP_NORMALIZATION`
    axiom ghostConfigLiquidationTargetLtv1 >= BP2DP_NORMALIZATION() 
        && ghostConfigLiquidationTargetLtv1 <= CONFIG_100_PERCENT();
    // `require(_initData.liquidationTargetLtv1 <= _initData.lt1, ISiloFactory.LiquidationTargetLtvTooHigh());`
    axiom ghostConfigLiquidationTargetLtv1 <= ghostConfigLt1;
}

persistent ghost mathint ghostConfigLiquidationFee1 {
    axiom ghostConfigLiquidationFee1 == 0 || 
        ghostConfigLiquidationFee1 >= BP2DP_NORMALIZATION() && ghostConfigLiquidationFee1 <= FEE_30_PERCENT();
}

persistent ghost mathint ghostConfigFlashloanFee1 {
    axiom ghostConfigFlashloanFee1 == 0 ||
        ghostConfigFlashloanFee1 >= BP2DP_NORMALIZATION() && ghostConfigFlashloanFee1 <= FEE_15_PERCENT();
}

persistent ghost bool ghostConfigCallBeforeQuote1;