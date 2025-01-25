// Silo config valid state invariants working both for Silo0

import "./silo_valid_state_invariants.spec";

// Use it when env is not needed
function requireSilo0ValidState() {

    // Valid state invariants both for silo0 and silo1
    requireValidSiloCommon();
}

// Use it when env matters
function requireSilo0ValidStateE(env e) {
    requireSilo0ValidState();

    // Valid state invariants both for silo0 and silo1
    requireValidSiloCommonE(e);

    requireInvariant silo0ProtectedCollateralAlwaysLiquid(e);
    requireInvariant silo0TotalDebtNotExceedCollateral(e);
}

// Protected collateral must remain fully available for withdrawal
strong invariant silo0ProtectedCollateralAlwaysLiquid(env e)
    ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] <= ghostERC20Balances[_Token0][_Silo0] {
        preserved with (env eInv) {
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
        }
    }

// VS- The Silo's total debt must never exceed its total collateral
strong invariant silo0TotalDebtNotExceedCollateral(env e)
    ghostTotalAssets[_Silo0][ASSET_TYPE_DEBT()] <= ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] {
        preserved with (env eInv) {
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
        }
    }
