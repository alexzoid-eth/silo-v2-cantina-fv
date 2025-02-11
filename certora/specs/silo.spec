// Silo1 rules

import "./setup/silo/hard_methods.spec";
import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./setup/silo/silo_valid_state.spec";

definition COLLATERAL_HARNESS_FUNCTIONS(method f) returns bool =
    f.selector == sig:convertToSharesCollateral(uint256).selector
 || f.selector == sig:convertToAssetsCollateral(uint256).selector
 || f.selector == sig:previewDepositCollateral(uint256).selector
 || f.selector == sig:depositCollateral(uint256,address).selector
 || f.selector == sig:previewMintCollateral(uint256).selector
 || f.selector == sig:mintCollateral(uint256,address).selector
 || f.selector == sig:maxWithdrawCollateral(address).selector
 || f.selector == sig:previewWithdrawCollateral(uint256).selector
 || f.selector == sig:withdrawCollateral(uint256,address,address).selector
 || f.selector == sig:maxRedeemCollateral(address).selector
 || f.selector == sig:previewRedeemCollateral(uint256).selector
 || f.selector == sig:redeemCollateral(uint256,address,address).selector
 || f.selector == sig:transitionCollateralFromCollateral(uint256,address).selector
 || f.selector == sig:maxDepositCollateral(address).selector
 || f.selector == sig:maxMintCollateral(address).selector
 ;

definition PROTECTED_HARNESS_FUNCTIONS(method f) returns bool =
    f.selector == sig:convertToSharesProtected(uint256).selector
 || f.selector == sig:convertToAssetsProtected(uint256).selector
 || f.selector == sig:previewDepositProtected(uint256).selector
 || f.selector == sig:depositProtected(uint256,address).selector
 || f.selector == sig:previewMintProtected(uint256).selector
 || f.selector == sig:mintProtected(uint256,address).selector
 || f.selector == sig:maxWithdrawProtected(address).selector
 || f.selector == sig:previewWithdrawProtected(uint256).selector
 || f.selector == sig:withdrawProtected(uint256,address,address).selector
 || f.selector == sig:maxRedeemProtected(address).selector
 || f.selector == sig:previewRedeemProtected(uint256).selector
 || f.selector == sig:redeemProtected(uint256,address,address).selector
 || f.selector == sig:transitionCollateralFromProtected(uint256,address).selector
 || f.selector == sig:maxDepositProtected(address).selector
 || f.selector == sig:maxMintProtected(address).selector
 ;

////////////////////////////////////////////////// State Transition

// Accrue interest does not affect shares
rule silo_accrueInterestNoSharesChanged(env e, address user) {

    setupSilo(e);

    // Record share balances for 'user' before
    mathint debt0BalBefore = ghostERC20Balances[_Debt0][user];
    mathint debt1BalBefore = ghostERC20Balances[_Debt1][user];
    mathint coll0BalBefore = ghostERC20Balances[_Collateral0][user];
    mathint coll1BalBefore = ghostERC20Balances[_Collateral1][user];
    mathint prot0BalBefore = ghostERC20Balances[_Protected0][user];
    mathint prot1BalBefore = ghostERC20Balances[_Protected1][user];

    // Record total supply of share tokens before
    mathint debt0SupplyBefore = ghostERC20TotalSupply[_Debt0];
    mathint debt1SupplyBefore = ghostERC20TotalSupply[_Debt1];
    mathint coll0SupplyBefore = ghostERC20TotalSupply[_Collateral0];
    mathint coll1SupplyBefore = ghostERC20TotalSupply[_Collateral1];
    mathint prot0SupplyBefore = ghostERC20TotalSupply[_Protected0];
    mathint prot1SupplyBefore = ghostERC20TotalSupply[_Protected1];

    accrueInterest(e);

    // After calling accrueInterest, none of the share balances or supplies may change
    assert(
        ghostERC20Balances[_Debt0][user] == debt0BalBefore
        && ghostERC20Balances[_Debt1][user] == debt1BalBefore
        && ghostERC20Balances[_Collateral0][user] == coll0BalBefore
        && ghostERC20Balances[_Collateral1][user] == coll1BalBefore
        && ghostERC20Balances[_Protected0][user] == prot0BalBefore
        && ghostERC20Balances[_Protected1][user] == prot1BalBefore

        && ghostERC20TotalSupply[_Debt0] == debt0SupplyBefore
        && ghostERC20TotalSupply[_Debt1] == debt1SupplyBefore
        && ghostERC20TotalSupply[_Collateral0] == coll0SupplyBefore
        && ghostERC20TotalSupply[_Collateral1] == coll1SupplyBefore
        && ghostERC20TotalSupply[_Protected0] == prot0SupplyBefore
        && ghostERC20TotalSupply[_Protected1] == prot1SupplyBefore
    );
}

// Possible that a user holds deposits in both silo0 and silo1 after deposit
rule silo_possibilityOfCollateralsInTwoSilos(env e, uint256 assets, address receiver) {

    setupSilo(e);

    // Have deposits in Silo0, deposit to Silo1
    require(ghostERC20Balances[_Collateral0][receiver] != 0 
        && ghostERC20Balances[_Collateral1][receiver] == 0);

    depositCollateral(e, assets, receiver);

    satisfy(
        ghostERC20Balances[_Collateral0][receiver] != 0
        && ghostERC20Balances[_Collateral1][receiver] != 0
    );
}

// Possible that a user holds deposits in both silo0 and silo1 after deposit
rule silo_possibilityOfProtectedInTwoSilos(env e, uint256 assets, address receiver) {

    setupSilo(e);

    // Have deposits in Silo0, deposit to Silo1
    require(ghostERC20Balances[_Protected0][receiver] != 0 
        && ghostERC20Balances[_Protected1][receiver] == 0);

    depositProtected(e, assets, receiver);

    satisfy(
        ghostERC20Balances[_Protected0][receiver] != 0
        && ghostERC20Balances[_Protected1][receiver] != 0
    );
}
