// Silo sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../invariants.spec";

rule sanity_transitionCollateralFromCollateral(method f, env e, calldataarg args) {
    setupSilo(e);
    transitionCollateralFromCollateral(e, args);
    satisfy(true);
}

rule sanity_transitionCollateralFromProtected(method f, env e, calldataarg args) {
    setupSilo(e);
    transitionCollateralFromProtected(e, args);
    satisfy(true);
}

rule sanity_redeemCollateral(method f, env e, calldataarg args) {
    setupSilo(e);
    redeemCollateral(e, args);
    satisfy(true);
}

rule sanity_redeemProtected(method f, env e, calldataarg args) {
    setupSilo(e);
    redeemProtected(e, args);
    satisfy(true);
}

rule sanity_withdrawCollateral(method f, env e, calldataarg args) {
    setupSilo(e);
    withdrawCollateral(e, args);
    satisfy(true);
}

rule sanity_withdrawProtected(method f, env e, calldataarg args) {
    setupSilo(e);
    withdrawProtected(e, args);
    satisfy(true);
}

rule sanity_borrowShares(method f, env e, calldataarg args) {
    setupSilo(e);
    borrowShares(e, args);
    satisfy(true);
}

rule sanity_borrow(method f, env e, calldataarg args) {
    setupSilo(e);
    borrow(e, args);
    satisfy(true);
}

rule sanity_borrowSameAsset(method f, env e, calldataarg args) {
    setupSilo(e);
    borrowSameAsset(e, args);
    satisfy(true);
}

rule sanity_others(method f, env e, calldataarg args) filtered { f->
    f.selector != sig:transitionCollateralFromCollateral(uint256,address).selector
    && f.selector != sig:transitionCollateralFromProtected(uint256,address).selector
    && f.selector != sig:redeemCollateral(uint256,address,address).selector
    && f.selector != sig:redeemProtected(uint256,address,address).selector
    && f.selector != sig:withdrawCollateral(uint256,address,address).selector
    && f.selector != sig:withdrawProtected(uint256,address,address).selector
    && f.selector != sig:borrowShares(uint256,address,address).selector
    && f.selector != sig:borrow(uint256,address,address).selector
    && f.selector != sig:borrowSameAsset(uint256,address,address).selector
    // Exclude all functions which were harnessed
    && !SIMPLIFIED_IN_HARNESS_FUNCTIONS(f)
} {
    setupSilo(e);
    f(e, args);
    satisfy(true);
}