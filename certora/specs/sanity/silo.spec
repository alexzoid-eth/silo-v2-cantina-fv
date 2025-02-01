// Silo sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../invariants.spec";

rule sanity_accrueInterestForConfig(env e, calldataarg args) {
    setupSilo(e);
    accrueInterestForConfig(e, args);
    satisfy(true);
}

rule sanity_withdraw(method f, env e, calldataarg args) filtered { f -> 
    f.selector == sig:withdraw(uint256, address, address).selector 
        || f.selector == sig:withdraw(uint256, address, address, ISilo.CollateralType).selector 
    }  {
    setupSilo(e);
    f(e, args);
    satisfy(true);
}

rule sanity_redeem(method f, env e, calldataarg args) filtered { f -> 
    f.selector == sig:redeem(uint256, address, address).selector 
        || f.selector == sig:redeem(uint256, address, address, ISilo.CollateralType).selector 
    }  {
    setupSilo(e);
    f(e, args);
    satisfy(true);
}

rule sanity_approve(env e, calldataarg args) {
    setupSilo(e);
    approve(e, args);
    satisfy(true);
}

rule sanity_flashFee(env e, calldataarg args) {
    setupSilo(e);
    flashFee(e, args);
    satisfy(true);
}

rule sanity_transfer(env e, calldataarg args) {
    setupSilo(e);
    transfer(e, args);
    satisfy(true);
}

rule sanity_allowance(env e, calldataarg args) {
    setupSilo(e);
    allowance(e, args);
    satisfy(true);
}

rule sanity_borrowSameAsset(env e, calldataarg args) {
    setupSilo(e);
    borrowSameAsset(e, args);
    satisfy(true);
}

rule sanity_borrow(env e, calldataarg args) {
    setupSilo(e);
    borrow(e, args);
    satisfy(true);
}

rule sanity_borrowShares(env e, calldataarg args) {
    setupSilo(e);
    borrowShares(e, args);
    satisfy(true);
}

rule sanity_totalAssets(env e, calldataarg args) {
    setupSilo(e);
    totalAssets(e, args);
    satisfy(true);
}

rule sanity_getCollateralAndProtectedTotalsStorage(env e, calldataarg args) {
    setupSilo(e);
    getCollateralAndProtectedTotalsStorage(e, args);
    satisfy(true);
}

rule sanity_getDebtAssets(env e, calldataarg args) {
    setupSilo(e);
    getDebtAssets(e, args);
    satisfy(true);
}

rule sanity_silo(env e, calldataarg args) {
    setupSilo(e);
    silo(e, args);
    satisfy(true);
}

rule sanity_siloConfig(env e, calldataarg args) {
    setupSilo(e);
    siloConfig(e, args);
    satisfy(true);
}

rule sanity_updateHooks(env e, calldataarg args) {
    setupSilo(e);
    updateHooks(e, args);
    satisfy(true);
}

rule sanity_factory(env e, calldataarg args) {
    setupSilo(e);
    factory(e, args);
    satisfy(true);
}

rule sanity_accrueInterest(env e, calldataarg args) {
    setupSilo(e);
    accrueInterest(e, args);
    satisfy(true);
}

rule sanity_getCollateralAssets(env e, calldataarg args) {
    setupSilo(e);
    getCollateralAssets(e, args);
    satisfy(true);
}

rule sanity_switchCollateralToThisSilo(env e, calldataarg args) {
    setupSilo(e);
    switchCollateralToThisSilo(e, args);
    satisfy(true);
}

rule sanity_utilizationData(env e, calldataarg args) {
    setupSilo(e);
    utilizationData(e, args);
    satisfy(true);
}

rule sanity_getSiloStorage(env e, calldataarg args) {
    setupSilo(e);
    getSiloStorage(e, args);
    satisfy(true);
}

rule sanity_hookReceiver(env e, calldataarg args) {
    setupSilo(e);
    hookReceiver(e, args);
    satisfy(true);
}

rule sanity_eip712Domain(env e, calldataarg args) {
    setupSilo(e);
    eip712Domain(e, args);
    satisfy(true);
}

rule sanity_config(env e, calldataarg args) {
    setupSilo(e);
    config(e, args);
    satisfy(true);
}

rule sanity_withdrawFees(env e, calldataarg args) {
    setupSilo(e);
    withdrawFees(e, args);
    satisfy(true);
}

rule sanity_getCollateralAndDebtTotalsStorage(env e, calldataarg args) {
    setupSilo(e);
    getCollateralAndDebtTotalsStorage(e, args);
    satisfy(true);
}