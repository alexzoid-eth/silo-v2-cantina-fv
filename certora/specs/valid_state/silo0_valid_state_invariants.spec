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
    requireInvariant silo0LiquiditySolvency(e);
    requireInvariant silo0NetDebtNotExceedCollateral(e);
    requireInvariant silo0TotalTrackedAssetsNotExceedERC20TokenSupply(e);
}

// VS- Protected collateral must remain fully available for withdrawal
strong invariant silo0ProtectedCollateralAlwaysLiquid(env e)
    ghostERC20Balances[_Token0][_Silo0] >= ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
        }
    }

// VS- The Silo's liquidity must cover its protected collateral, collateral, 
//  and fees minus any outstanding debt
strong invariant silo0LiquiditySolvency(env e)
    ghostERC20Balances[_Token0][_Silo0] >= 
        ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[_Silo0]
        - ghostTotalAssets[_Silo0][ASSET_TYPE_DEBT()] {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
        }
    }

// VS- The Silo's net debt (debt minus accrued fees) must never exceed its collateral
strong invariant silo0NetDebtNotExceedCollateral(env e)
    ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()]
        >= require_uint256(
            ghostTotalAssets[_Silo0][ASSET_TYPE_DEBT()] - ghostDaoAndDeployerRevenue[_Silo0]
            ) {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
        }
    }

// VS- The Silo's total tracked assets must not exceed the token's total supply
strong invariant silo0TotalTrackedAssetsNotExceedERC20TokenSupply(env e)
    ghostERC20TotalSupply[_Token0] >= 
        ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[_Silo0] {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
            // SAFE: Don't check interest increase, assume it cannot overflow ERC20 supply
            require(e.block.timestamp == ghostInterestRateTimestamp[_Silo0]);
        }
    }