import "setup/silo0/silo_0.spec";

// Sanity

use builtin rule sanity;

// High Level

// The protected collateral portion must not accrue interest or be counted as borrowed liquidity.
//  It should increase/decrease only from user deposits/withdrawals (no borrow/repay events).
// rule protectedCollateralNoInterestAccumulation(method f, env e, calldataarg args)

// SS- The Silo's debt plus accrued fees must never exceed its total collateral 
//  plus accrued fees under normal operations
strong invariant silo0DebtNotExceedCollateralExceptOnFeeWithdraw(env e)
    ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_COLLATERAL()] + ghostDaoAndDeployerRevenue[ghostConfigSilo0]
        >= ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_DEBT()] 
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


// VS- The share token’s hooks must always match the hookReceiver’s configuration
strong invariant shareTokenHooksSynchronization(env e)
    forall address contract. ghostShareTokenHooksBefore[contract] == ghostHooksBefore[ghostConfigSilo0]
        && ghostShareTokenHooksAfter[contract] == ghostHooksAfter[ghostConfigSilo0] {
            preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); }
            preserved synchronizeHooks(uint24 hooksBefore, uint24 hooksAfter) with (env eInv) {
                requireSameEnv(e, eInv); setupSilo(e);
                // SAFE: Only silo executes this function with parameters from IHookReceiver.hookReceiverConfig()
                require(hooksBefore == ghostHooksBefore[ghostConfigSilo0] && hooksAfter == ghostHooksAfter[ghostConfigSilo0]);
            }   
        }

// VS- All protected shares must be fully backed so they can always be withdrawn
strong invariant allProtectedSharesAlwaysWithdrawable(env e) (
    previewRedeem(e, require_uint256(ghostERC20TotalSupply[ghostConfigProtectedCollateralShareToken0]))
        <= ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()] 
    ) && (IS_FULL_SILO() => (
    previewRedeem(e, require_uint256(ghostERC20TotalSupply[ghostConfigProtectedCollateralShareToken1]))
        <= ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()] 
    )) {
        preserved with (env eInv) {
            requireSameEnv(e, eInv); setupSilo(e);
            // UNSAFE: Assume no interest accrues as it must not affect protected shares
            require(e.block.timestamp == ghostInterestRateTimestamp[ghostConfigSilo0]);
            require(e.block.timestamp == ghostInterestRateTimestamp[ghostConfigSilo1]);
        }
    }
