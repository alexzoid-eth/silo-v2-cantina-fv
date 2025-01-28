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
            requireValidSilo0E(e);
        }
    }
