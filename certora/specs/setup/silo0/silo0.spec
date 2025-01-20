import "../silo.spec";

// ShareToken
import "./collateralShareToken0.spec";
import "./shareDebtToken0.spec";
import "./shareProtectedCollateralToken0.spec";

using Silo0 as _Silo0;
using Silo0 as _ERC20;
using Silo0 as _ERC4626;

// Methods summarizes

function getCollateralAndDebtTotalsStorageCVL(env e) returns (uint256, uint256) {
    uint256 totalCollateralAssets; uint256 totalDebtAssets;
    totalCollateralAssets, totalDebtAssets = _Silo0.getCollateralAndDebtTotalsStorage(e);
    return (totalCollateralAssets, totalDebtAssets);
}

function getTotalAssetsStorageCVL(env e, ISilo.AssetType _assetType) returns uint256 {
    return _Silo0.getTotalAssetsStorage(e, _assetType);
}

function getConfigCVL(env e) returns ISiloConfig.ConfigData {
    return _SiloConfig.getConfig(e, _Silo0);
}

function getFeesWithAssetCVL(env e) returns (uint256, uint256, uint256, address) {
    uint256 daoFee; uint256 deployerFee; uint256 flashloanFee; address asset;
    daoFee, deployerFee, flashloanFee, asset = _SiloConfig.getFeesWithAsset(e, _Silo0);
    return (daoFee, deployerFee, flashloanFee, asset);
}

function hookReceiverConfigCVL(env e) returns (uint24, uint24) {
    uint24 hooksBefore; uint24 hooksAfter;
    hooksBefore, hooksAfter = _EmptyHookReceiver.hookReceiverConfig(e, _Silo0);
    return (hooksBefore, hooksAfter);
}

ghost mapping(uint256 => uint256) ghostInterestSilo;
function getCompoundInterestRateForSiloCVL(uint256 _blockTimestamp) returns uint256 {
    return ghostInterestSilo[_blockTimestamp];
}

function getCollateralAndProtectedTotalsStorageCVL(env e) returns (uint256, uint256) {
    uint256 totalCollateralAssets; uint256 totalProtectedAssets;
    (totalCollateralAssets, totalProtectedAssets) = _Silo0.getCollateralAndProtectedTotalsStorage(e);
    return (totalCollateralAssets, totalProtectedAssets);
}

function synchronizeHooksCVL(env e, address contract, uint24 _hooksBefore, uint24 _hooksAfter) {
    ASSERT(e.msg.sender == _Silo0);
    ghostShareTokenHooksBefore[contract] = _hooksBefore;
    ghostShareTokenHooksAfter[contract] = _hooksAfter;
}

function balanceOfAndTotalSupplyCVL(env e, address contract, address _account) returns (uint256, uint256) {
    return (
        require_uint256(ghostERC20Balances[contract][_account]), 
        require_uint256(ghostERC20TotalSupply[contract])
        );
}

// Link immutables in SiloConfig

persistent ghost address ghostConfigSilo0 {
    axiom ghostConfigSilo0 == _Silo0;
    axiom ghostConfigSilo0 == _SiloConfig._SILO0;
}

persistent ghost address ghostConfigToken0 {
    axiom ghostConfigToken0 == ghostERC20CVLToken[0];
    axiom ghostConfigToken0 == _SiloConfig._TOKEN0;
}

persistent ghost address ghostConfigProtectedCollateralShareToken0 {
    axiom ghostConfigProtectedCollateralShareToken0 == _ShareProtectedCollateralToken0;
    axiom ghostConfigProtectedCollateralShareToken0 == _SiloConfig._PROTECTED_COLLATERAL_SHARE_TOKEN0;
}

persistent ghost address ghostConfigCollateralShareToken0 {
    axiom ghostConfigCollateralShareToken0 == _Silo0;
    axiom ghostConfigCollateralShareToken0 == _SiloConfig._COLLATERAL_SHARE_TOKEN0;
}

persistent ghost address ghostConfigDebtShareToken0 {
    axiom ghostConfigDebtShareToken0 == _ShareDebtToken0;
    axiom ghostConfigDebtShareToken0 == _SiloConfig._DEBT_SHARE_TOKEN0;
}

persistent ghost address ghostConfigSolvencyOracle0 {
    // @todo
    axiom ghostConfigSolvencyOracle0 == _SiloConfig._SOLVENCY_ORACLE0;
}

persistent ghost address ghostConfigMaxLtvOracle0 {
    // @todo
    axiom ghostConfigMaxLtvOracle0 == _SiloConfig._MAX_LTV_ORACLE0;
}

persistent ghost address ghostConfigInterestRateModel0 {
    // @todo
    axiom ghostConfigInterestRateModel0 == _SiloConfig._INTEREST_RATE_MODEL0;
}

persistent ghost uint256 ghostConfigMaxLtv0 {
    // @todo
    axiom ghostConfigMaxLtv0 == _SiloConfig._MAX_LTV0;
}

persistent ghost uint256 ghostConfigLt0 {
    // @todo
    axiom ghostConfigLt0 == _SiloConfig._LT0;
}

persistent ghost uint256 ghostConfigLiquidationTargetLtv0 {
    // @todo
    axiom ghostConfigLiquidationTargetLtv0 == _SiloConfig._LIQUIDATION_TARGET_LTV0;
}

persistent ghost uint256 ghostConfigLiquidationFee0 {
    // @todo
    axiom ghostConfigLiquidationFee0 == _SiloConfig._LIQUIDATION_FEE0;
}

persistent ghost uint256 ghostConfigFlashloanFee0 {
    // @todo
    axiom ghostConfigFlashloanFee0 == _SiloConfig._FLASHLOAN_FEE0;
}

persistent ghost bool ghostConfigCallBeforeQuote0 {
    // @todo
    axiom ghostConfigCallBeforeQuote0 == _SiloConfig._CALL_BEFORE_QUOTE0;
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
