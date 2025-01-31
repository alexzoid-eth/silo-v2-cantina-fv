// SiloConfig sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";

rule sanity_hasDebtInOtherSilo(env e, calldataarg args) {
    setupSilo(e);
    hasDebtInOtherSilo(e, args);
    satisfy(true);
}

rule sanity_onDebtTransfer(env e, calldataarg args) {
    setupSilo(e);
    onDebtTransfer(e, args);
    satisfy(true);
}

rule sanity_getConfigsForWithdraw(env e, calldataarg args) {
    setupSilo(e);
    getConfigsForWithdraw(e, args);
    satisfy(true);
}

rule sanity_reentrancyGuardEntered(env e, calldataarg args) {
    setupSilo(e);
    reentrancyGuardEntered(e, args);
    satisfy(true);
}

rule sanity_getSilos(env e, calldataarg args) {
    setupSilo(e);
    getSilos(e, args);
    satisfy(true);
}

rule sanity_turnOnReentrancyProtection(env e, calldataarg args) {
    setupSilo(e);
    turnOnReentrancyProtection(e, args);
    satisfy(true);
}

rule sanity_turnOffReentrancyProtection(env e, calldataarg args) {
    setupSilo(e);
    turnOffReentrancyProtection(e, args);
    satisfy(true);
}

rule sanity_getAssetForSilo(env e, calldataarg args) {
    setupSilo(e);
    getAssetForSilo(e, args);
    satisfy(true);
}

rule sanity_setOtherSiloAsCollateralSilo(env e, calldataarg args) {
    setupSilo(e);
    setOtherSiloAsCollateralSilo(e, args);
    satisfy(true);
}

rule sanity_getConfig(env e, calldataarg args) {
    setupSilo(e);
    getConfig(e, args);
    satisfy(true);
}

rule sanity_borrowerCollateralSilo(env e, calldataarg args) {
    setupSilo(e);
    borrowerCollateralSilo(e, args);
    satisfy(true);
}

rule sanity_getFeesWithAsset(env e, calldataarg args) {
    setupSilo(e);
    getFeesWithAsset(e, args);
    satisfy(true);
}

rule sanity_getConfigsForSolvency(env e, calldataarg args) {
    setupSilo(e);
    getConfigsForSolvency(e, args);
    satisfy(true);
}

rule sanity_getShareTokens(env e, calldataarg args) {
    setupSilo(e);
    getShareTokens(e, args);
    satisfy(true);
}

rule sanity_setThisSiloAsCollateralSilo(env e, calldataarg args) {
    setupSilo(e);
    setThisSiloAsCollateralSilo(e, args);
    satisfy(true);
}

rule sanity_getDebtShareTokenAndAsset(env e, calldataarg args) {
    setupSilo(e);
    getDebtShareTokenAndAsset(e, args);
    satisfy(true);
}

rule sanity_getConfigsForBorrow(env e, calldataarg args) {
    setupSilo(e);
    getConfigsForBorrow(e, args);
    satisfy(true);
}

rule sanity_accrueInterestForSilo(env e, calldataarg args) {
    setupSilo(e);
    accrueInterestForSilo(e, args);
    satisfy(true);
}

rule sanity_getDebtSilo(env e, calldataarg args) {
    setupSilo(e);
    getDebtSilo(e, args);
    satisfy(true);
}

rule sanity_getCollateralShareTokenAndAsset(env e, calldataarg args) {
    setupSilo(e);
    getCollateralShareTokenAndAsset(e, args);
    satisfy(true);
}
