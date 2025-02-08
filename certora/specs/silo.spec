// Silo rules

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./invariants.spec";

rule silo_test() {
    assert(true);
}

strong invariant silo_test_inv() true;

/*
// High Level

// The protected collateral portion must not accrue interest or be counted as borrowed liquidity.
//  It should increase/decrease only from user deposits/withdrawals (no borrow/repay events).
// rule protectedCollateralNoInterestAccumulation(method f, env e, calldataarg args)

// VS- The share token’s hooks must always match the hookReceiver’s configuration
strong invariant shareTokenHooksSynchronization(env e)
    forall address contract. ghostShareTokenHooksBefore[contract] == ghostHooksBefore[_Silo0]
        && ghostShareTokenHooksAfter[contract] == ghostHooksAfter[_Silo0] {
            preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); }
            preserved synchronizeHooks(uint24 hooksBefore, uint24 hooksAfter) with (env eInv) {
                requireSameEnv(e, eInv); setupSilo(e);
                // SAFE: Only silo executes this function with parameters from IHookReceiver.hookReceiverConfig()
                require(hooksBefore == ghostHooksBefore[_Silo0] && hooksAfter == ghostHooksAfter[_Silo0]);
            }   
        }

// VS- All protected shares must be fully backed so they can always be withdrawn
strong invariant allProtectedSharesAlwaysWithdrawable(env e) (
    previewRedeem(e, require_uint256(ghostERC20TotalSupply[_Protected0]))
        <= ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] 
    ) && (IS_FULL_SILO() => (
    previewRedeem(e, require_uint256(ghostERC20TotalSupply[_Protected1]))
        <= ghostTotalAssets[_Silo1][ASSET_TYPE_PROTECTED()] 
    )) {
        preserved with (env eInv) {
            requireSameEnv(e, eInv); setupSilo(e);
            // UNSAFE: Assume no interest accrues as it must not affect protected shares
            require(e.block.timestamp == ghostInterestRateTimestamp[_Silo0]);
            require(e.block.timestamp == ghostInterestRateTimestamp[_Silo1]);
        }
    }

// SS- The Silo's debt plus accrued fees must never exceed its total collateral 
//  plus accrued fees under normal operations
strong invariant silo0DebtNotExceedCollateralExceptOnFeeWithdraw(env e)
    ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] + ghostDaoAndDeployerRevenue[_Silo0]
        >= ghostTotalAssets[_Silo0][ASSET_TYPE_DEBT()] 
    filtered {
        // EXCEPTION: During withdrawFees, it's possible for debt to exceed 
        //  collateral if the fees are withdrawn
        f -> f.selector != sig:withdrawFees().selector
    } {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            setupSilo(e);
        }
    }

// @todo when interest accrued
// VS- The Silo's total tracked assets must not exceed the token's total supply
strong invariant inv_totalTrackedAssetsNotExceedERC20TokenSupply(env e) (
    ghostERC20TotalSupply[ghostToken0] >= 
        ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[_Silo0] 
        + getAccruedInterestCVL(e, _Silo0) 
    ) && (!IS_MODE_SINGLE() => (
    ghostERC20TotalSupply[ghostToken1] >= 
        ghostTotalAssets[_Silo1][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[_Silo1][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[_Silo1] 
        + getAccruedInterestCVL(e, _Silo1) 
    ))
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// AS a rule
// VS- No double calls to cross reentrancy protection
invariant inv_crossReentrancyProtectionNoDoubleCall(env e)
    ghostReentrancyProtectionDoubleCall == false
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo's collateral plus distributor fees must always cover its total debt
definition collateralPlusFeesCoverDebt(bool zero) returns bool =
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostSiloX(zero)]
        >= ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()];

invariant inv_collateralPlusFeesCoverDebt0(env e) collateralPlusFeesCoverDebt(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// withdrawFees https://prover.certora.com/output/52567/69bc811b32f04100ac4efad8f764f01d/?anonymousKey=41fc11d80e5435d438ba7e07ea012d5de588913c
invariant inv_collateralPlusFeesCoverDebt1(env e) collateralPlusFeesCoverDebt(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- Debt assets >= totalSupply(debtToken)
definition debtAssetsGteShares(bool zero) returns bool =
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()] 
        >= ghostERC20TotalSupply[ghostDebtTokenX(zero)];

invariant inv_debtAssetsGteShares0(env e) debtAssetsGteShares(true)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_debtAssetsGteShares1(env e) debtAssetsGteShares(false)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

*/