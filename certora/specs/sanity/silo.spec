// Silo sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../invariants.spec";

// These functions are replaced in harness contract 
definition SIMPLIFIED_IN_HARNESS_FUNCTIONS(method f) returns bool =
    // single-argument EIP-4626
    f.selector == sig:convertToShares(uint256).selector
    || f.selector == sig:convertToAssets(uint256).selector
    || f.selector == sig:previewDeposit(uint256).selector
    || f.selector == sig:deposit(uint256,address).selector
    || f.selector == sig:previewMint(uint256).selector
    || f.selector == sig:mint(uint256,address).selector
    || f.selector == sig:maxWithdraw(address).selector
    || f.selector == sig:previewWithdraw(uint256).selector
    || f.selector == sig:withdraw(uint256,address,address).selector
    || f.selector == sig:maxRedeem(address).selector
    || f.selector == sig:previewRedeem(uint256).selector
    || f.selector == sig:redeem(uint256,address,address).selector
    || f.selector == sig:maxDeposit(address).selector
    || f.selector == sig:maxMint(address).selector
    || f.selector == sig:transitionCollateral(uint256,address,ISilo.CollateralType).selector
    // overloaded EIP-4626 + CollateralType/AssetType versions
    || f.selector == sig:convertToShares(uint256,ISilo.AssetType).selector
    || f.selector == sig:convertToAssets(uint256,ISilo.AssetType).selector
    || f.selector == sig:previewDeposit(uint256,ISilo.CollateralType).selector
    || f.selector == sig:deposit(uint256,address,ISilo.CollateralType).selector
    || f.selector == sig:previewMint(uint256,ISilo.CollateralType).selector
    || f.selector == sig:mint(uint256,address,ISilo.CollateralType).selector
    || f.selector == sig:maxWithdraw(address,ISilo.CollateralType).selector
    || f.selector == sig:previewWithdraw(uint256,ISilo.CollateralType).selector
    || f.selector == sig:withdraw(uint256,address,address,ISilo.CollateralType).selector
    || f.selector == sig:maxRedeem(address,ISilo.CollateralType).selector
    || f.selector == sig:previewRedeem(uint256,ISilo.CollateralType).selector
    || f.selector == sig:redeem(uint256,address,address,ISilo.CollateralType).selector;

definition HELPER_HARNESS_FUNCTIONS(method f) returns bool =
    f.selector == sig:getCollateralAmountsWithInterestHarness(uint256, uint256, uint256, uint256, uint256).selector
    || f.selector == sig:makeUnresolvedCall().selector
    || f.selector == sig:assertOnFalse(bool).selector
    ;


rule sanity_transitionCollateralFromCollateral(env e, calldataarg args) {
    setupSilo(e);
    transitionCollateralFromCollateral(e, args);
    satisfy(true);
}

rule sanity_transitionCollateralFromProtected(env e, calldataarg args) {
    setupSilo(e);
    transitionCollateralFromProtected(e, args);
    satisfy(true);
}

rule sanity_redeemCollateral(env e, calldataarg args) {
    setupSilo(e);
    redeemCollateral(e, args);
    satisfy(true);
}

rule sanity_redeemProtected(env e, calldataarg args) {
    setupSilo(e);
    redeemProtected(e, args);
    satisfy(true);
}

rule sanity_withdrawCollateral(env e, calldataarg args) {
    setupSilo(e);
    withdrawCollateral(e, args);
    satisfy(true);
}

rule sanity_withdrawProtected(env e, calldataarg args) {
    setupSilo(e);
    withdrawProtected(e, args);
    satisfy(true);
}

rule sanity_borrowShares(env e, calldataarg args) {
    setupSilo(e);
    borrowShares(e, args);
    satisfy(true);
}

rule sanity_borrow(env e, calldataarg args) {
    setupSilo(e);
    borrow(e, args);
    satisfy(true);
}

rule sanity_borrowSameAsset(env e, calldataarg args) {
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
    // Exclude helper functions
    && !HELPER_HARNESS_FUNCTIONS(f)
} {
    setupSilo(e);
    f(e, args);
    satisfy(true);
}