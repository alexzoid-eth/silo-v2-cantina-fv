// Silo0 valid state invariants

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
    requireInvariant silo0TotalTrackedAssetsNotExceedERC20TokenSupply(e);

    requireInvariant silo0ProtectedSharesMustBeBackedWithAssets(e);
    requireInvariant silo0CollateralSharesMustBeBackedWithAssets(e);
    requireInvariant silo0DebtSharesMustBeBackedWithAssets(e);

    requireInvariant silo0AllProtectedSharesAlwaysWithdrawable(e);
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

// VS- The Silo's total tracked assets must not exceed the token's total supply
strong invariant silo0TotalTrackedAssetsNotExceedERC20TokenSupply(env e)
    ghostERC20TotalSupply[_Token0] >= 
        ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[_Silo0] 
        + getAccruedInterestCVL(e, _Silo0) {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
        }
    }

// VS- The Silo’s collateral protected share tokens must always be backed by the assets
strong invariant silo0ProtectedSharesMustBeBackedWithAssets(env e)
    ghostERC20TotalSupply[_ShareProtectedCollateralToken0] != 0
        => ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] != 0 {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
        }
    }

// VS- The Silo’s collateral share tokens must always be backed by the assets
strong invariant silo0CollateralSharesMustBeBackedWithAssets(env e)
    ghostERC20TotalSupply[_CollateralShareToken0] != 0
        => ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] != 0 {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
        }
    }

// VS- The Silo’s collateral share tokens must always be backed by the assets
strong invariant silo0DebtSharesMustBeBackedWithAssets(env e)
    ghostERC20TotalSupply[_ShareDebtToken0] != 0
        => ghostTotalAssets[_Silo0][ASSET_TYPE_DEBT()] != 0 {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
        }
    }

// VS- All protected shares must be fully backed so they can always be withdrawn
strong invariant silo0AllProtectedSharesAlwaysWithdrawable(env e) 
    previewRedeem(e, require_uint256(ghostERC20TotalSupply[_ShareProtectedCollateralToken0]))
        <= ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment 
            requireValidSilo0E(e);
            // SAFE: Assume no interest accrues as it must not affect protected shares
            require(e.block.timestamp == ghostInterestRateTimestamp[_Silo0]);
        }
    }