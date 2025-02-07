// Silo config contract support

import "./silo_config_cvl.spec";

using Config as _SiloConfig;

methods {

    // Let spec know the type of configuration (Silo0, Silo0+Silo1 or Silo0+Silo1+Hook)

    function _SiloConfig._SILO_MODE() external returns address envfree;

    // Resolve external calls to SiloConfig
    
    function _.getConfig(address _silo) external
        => DISPATCHER(true);

    function _.getFeesWithAsset(address _silo) external
        => DISPATCHER(true);

    function _.getCollateralShareTokenAndAsset(address _silo, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);
}

// Immutables

definition BP2DP_NORMALIZATION() returns mathint = 10^14;
definition CONFIG_100_PERCENT() returns mathint = 10^18;

definition FEE_5_PERCENT() returns mathint = 5 * 10^16;
definition FEE_15_PERCENT() returns mathint = 15 * 10^16;
definition FEE_30_PERCENT() returns mathint = 3 * 10^17;
definition FEE_50_PERCENT() returns mathint = 5 * 10^17;

definition silo0contractsAddress(address a) returns bool = 
    a == ghostSilo0
    || a == ghostDebtToken0
    || a == ghostProtectedToken0
    || a == ghostCollateralToken0
    || a == ghostToken0
    || a == ghostConfigSolvencyOracle0
    || a == ghostConfigMaxLtvOracle0
    || a == ghostConfigInterestRateModel0
    ;

definition silo1contractsAddress(address a) returns bool = 
    a == ghostSilo1
    || a == ghostDebtToken1
    || a == ghostProtectedToken1
    || a == ghostCollateralToken1
    || a == ghostToken1
    || a == ghostConfigSolvencyOracle1
    || a == ghostConfigMaxLtvOracle1
    || a == ghostConfigInterestRateModel1
    ;

definition ghostSiloX(bool zero) returns address = 
    zero ? ghostSilo0 : ghostSilo1;

definition ghostProtectedTokenX(bool zero) returns address = 
    zero ? ghostProtectedToken0 : ghostProtectedToken1;

definition ghostCollateralTokenX(bool zero) returns address = 
    zero ? ghostCollateralToken0 : ghostCollateralToken1;

definition ghostDebtTokenX(bool zero) returns address = 
    zero ? ghostDebtToken0 : ghostDebtToken1;

definition ghostTokenX(bool zero) returns address = 
    zero ? ghostToken0 : ghostToken1;

// Set true to use static config values from `silo-core/deploy/input/mainnet/FULL_CONFIG_TEST.json`
persistent ghost bool ghostUseStaticConfig;

persistent ghost mathint ghostSiloId;

persistent ghost address ghostSiloConfig {
    axiom ghostSiloConfig == _SiloConfig;
}

// SAFE: Assumptions made based on `Views.validateSiloInitData()` and `SiloConfigData.getConfigData()`

persistent ghost mathint ghostConfigDaoFee {
    axiom ghostConfigDaoFee == _SiloConfig._DAO_FEE;
    axiom ghostConfigDaoFee >= FEE_5_PERCENT() && ghostConfigDaoFee <= FEE_50_PERCENT(); 
}

persistent ghost mathint ghostConfigDeployerFee {
    axiom ghostConfigDeployerFee == _SiloConfig._DEPLOYER_FEE;
    axiom ghostConfigDeployerFee == 0 
        || ghostConfigDeployerFee >= BP2DP_NORMALIZATION() && ghostConfigDeployerFee <= FEE_15_PERCENT(); 
}

persistent ghost address ghostConfigHookReceiver {
    axiom ghostConfigHookReceiver == _SiloConfig._HOOK_RECEIVER;
}

// Silo0

persistent ghost address ghostSilo0 {
    axiom ghostSilo0 == _SiloConfig._SILO0;
}

persistent ghost address ghostToken0 {
    axiom ghostToken0 == _SiloConfig._TOKEN0;
}

persistent ghost address ghostProtectedToken0 {
    axiom ghostProtectedToken0 == _SiloConfig._PROTECTED_COLLATERAL_SHARE_TOKEN0;
}

persistent ghost address ghostCollateralToken0 {
    axiom ghostCollateralToken0 == _SiloConfig._COLLATERAL_SHARE_TOKEN0;
}

persistent ghost address ghostDebtToken0 {
    axiom ghostDebtToken0 == _SiloConfig._DEBT_SHARE_TOKEN0;
}

persistent ghost address ghostConfigSolvencyOracle0 {
    axiom ghostConfigSolvencyOracle0 == _SiloConfig._SOLVENCY_ORACLE0;
}

persistent ghost address ghostConfigMaxLtvOracle0 {
    axiom ghostConfigMaxLtvOracle0 == _SiloConfig._MAX_LTV_ORACLE0;
}

persistent ghost address ghostConfigInterestRateModel0 {
    axiom ghostConfigInterestRateModel0 == _SiloConfig._INTEREST_RATE_MODEL0;
}

persistent ghost mathint ghostConfigMaxLtv0 {
    axiom ghostConfigMaxLtv0 == _SiloConfig._MAX_LTV0;

    // `maxLtv0: config.maxLtv0 * BP2DP_NORMALIZATION,` 
    axiom ghostConfigMaxLtv0 == 0 || 
        ghostConfigMaxLtv0 >= BP2DP_NORMALIZATION() && ghostConfigMaxLtv0 <= CONFIG_100_PERCENT();
    // `require(_initData.maxLtv0 != 0 || _initData.maxLtv1 != 0, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv0 == 0 => ghostConfigMaxLtv1 != 0;
    // `require(_initData.maxLtv0 <= _initData.lt0, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv0 <= ghostConfigLt0;
}

persistent ghost mathint ghostConfigLt0 {
    axiom ghostConfigLt0 == _SiloConfig._LT0;

    // `lt0: config.lt0 * BP2DP_NORMALIZATION`
    axiom ghostConfigLt0 >= BP2DP_NORMALIZATION() && ghostConfigLt0 <= CONFIG_100_PERCENT();
    // `require(_initData.lt0 + _initData.liquidationFee0 <= _100_PERCENT, ISiloFactory.InvalidLt());`
    axiom ghostConfigLt0 + ghostConfigLiquidationFee0 <= CONFIG_100_PERCENT();

}

persistent ghost mathint ghostConfigLiquidationTargetLtv0 {
    axiom ghostConfigLiquidationTargetLtv0 == _SiloConfig._LIQUIDATION_TARGET_LTV0;

    // `liquidationTargetLtv0: config.liquidationTargetLtv0 * BP2DP_NORMALIZATION`
    axiom ghostConfigLiquidationTargetLtv0 >= BP2DP_NORMALIZATION() 
        && ghostConfigLiquidationTargetLtv0 <= CONFIG_100_PERCENT();
    // `require(_initData.liquidationTargetLtv0 <= _initData.lt0, ISiloFactory.LiquidationTargetLtvTooHigh());`
    axiom ghostConfigLiquidationTargetLtv0 <= ghostConfigLt0;
}

persistent ghost mathint ghostConfigLiquidationFee0 {
    axiom ghostConfigLiquidationFee0 == _SiloConfig._LIQUIDATION_FEE0;

    axiom ghostConfigLiquidationFee0 == 0 || 
        ghostConfigLiquidationFee0 >= BP2DP_NORMALIZATION() && ghostConfigLiquidationFee0 <= FEE_30_PERCENT();
}

persistent ghost mathint ghostConfigFlashloanFee0 {
    axiom ghostConfigFlashloanFee0 == _SiloConfig._FLASHLOAN_FEE0;

    axiom ghostConfigFlashloanFee0 == 0 ||
        ghostConfigFlashloanFee0 >= BP2DP_NORMALIZATION() && ghostConfigFlashloanFee0 <= FEE_15_PERCENT();
}

persistent ghost bool ghostConfigCallBeforeQuote0 {
    axiom ghostConfigCallBeforeQuote0 == _SiloConfig._CALL_BEFORE_QUOTE0;
}

// Silo1

persistent ghost address ghostSilo1 {
    axiom ghostSilo1 == _SiloConfig._SILO1;
}

persistent ghost address ghostToken1 {
    axiom ghostToken1 == _SiloConfig._TOKEN1;
}

persistent ghost address ghostProtectedToken1 {
    axiom ghostProtectedToken1 == _SiloConfig._PROTECTED_COLLATERAL_SHARE_TOKEN1;
}

persistent ghost address ghostCollateralToken1 {
    axiom ghostCollateralToken1 == _SiloConfig._COLLATERAL_SHARE_TOKEN1;
}

persistent ghost address ghostDebtToken1 {
    axiom ghostDebtToken1 == _SiloConfig._DEBT_SHARE_TOKEN1;
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

    // `maxLtv1: config.maxLtv1 * BP2DP_NORMALIZATION,` 
    axiom ghostConfigMaxLtv1 == 0 || 
        ghostConfigMaxLtv1 >= BP2DP_NORMALIZATION() && ghostConfigMaxLtv1 <= CONFIG_100_PERCENT();
    // `require(_initData.maxLtv1 != 0 || _initData.maxLtv1 != 0, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv1 == 0 => ghostConfigMaxLtv0 != 0;
    // `require(_initData.maxLtv1 <= _initData.lt1, ISiloFactory.InvalidMaxLtv());`
    axiom ghostConfigMaxLtv1 <= ghostConfigLt1;
}

persistent ghost mathint ghostConfigLt1 {
    axiom ghostConfigLt1 == _SiloConfig._LT1;

    // `lt1: config.lt1 * BP2DP_NORMALIZATION`
    axiom ghostConfigLt1 >= BP2DP_NORMALIZATION() && ghostConfigLt1 <= CONFIG_100_PERCENT();
    // `require(_initData.lt1 + _initData.liquidationFee1 <= _100_PERCENT, ISiloFactory.InvalidLt());`
    axiom ghostConfigLt1 + ghostConfigLiquidationFee1 <= CONFIG_100_PERCENT();

}

persistent ghost mathint ghostConfigLiquidationTargetLtv1 {
    axiom ghostConfigLiquidationTargetLtv1 == _SiloConfig._LIQUIDATION_TARGET_LTV1;

    // `liquidationTargetLtv1: config.liquidationTargetLtv1 * BP2DP_NORMALIZATION`
    axiom ghostConfigLiquidationTargetLtv1 >= BP2DP_NORMALIZATION() 
        && ghostConfigLiquidationTargetLtv1 <= CONFIG_100_PERCENT();
    // `require(_initData.liquidationTargetLtv1 <= _initData.lt1, ISiloFactory.LiquidationTargetLtvTooHigh());`
    axiom ghostConfigLiquidationTargetLtv1 <= ghostConfigLt1;
}

persistent ghost mathint ghostConfigLiquidationFee1 {
    axiom ghostConfigLiquidationFee1 == _SiloConfig._LIQUIDATION_FEE1;

    axiom ghostConfigLiquidationFee1 == 0 || 
        ghostConfigLiquidationFee1 >= BP2DP_NORMALIZATION() && ghostConfigLiquidationFee1 <= FEE_30_PERCENT();
}

persistent ghost mathint ghostConfigFlashloanFee1 {
    axiom ghostConfigFlashloanFee1 == _SiloConfig._FLASHLOAN_FEE1;

    axiom ghostConfigFlashloanFee1 == 0 ||
        ghostConfigFlashloanFee1 >= BP2DP_NORMALIZATION() && ghostConfigFlashloanFee1 <= FEE_15_PERCENT();
}

persistent ghost bool ghostConfigCallBeforeQuote1 {
    axiom ghostConfigCallBeforeQuote1 == _SiloConfig._CALL_BEFORE_QUOTE1;
}

// CrossReentrancyGuard

definition _NOT_ENTERED() returns mathint = 0;
definition _ENTERED() returns mathint = 1;

persistent ghost bool ghostReentrancyProtectionDoubleCall {
    init_state axiom ghostReentrancyProtectionDoubleCall == false;
}

persistent ghost mathint ghostCrossReentrantStatus {
    init_state axiom ghostCrossReentrantStatus == _NOT_ENTERED();
    axiom ghostCrossReentrantStatus == _NOT_ENTERED() || ghostCrossReentrantStatus == _ENTERED();
}

hook ALL_TLOAD(uint256 addr) uint256 val {
    if(executingContract == _SiloConfig) {
        require(require_uint256(ghostCrossReentrantStatus) == val);
    }
}

hook ALL_TSTORE(uint256 addr, uint256 val)  {
    if(executingContract == _SiloConfig) {
        ghostReentrancyProtectionDoubleCall = (val == ghostCrossReentrantStatus);
        ghostCrossReentrantStatus = val;
    }
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
