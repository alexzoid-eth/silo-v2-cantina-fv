// Silo valid state invariants working for all Silo contracts 

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";

function requireValidStateInvariants(env e) {

    // ERC20
    requireInvariant inv_eip20_totalSupplySolvency(e);              // ok
    
    // SiloConfig
    requireInvariant inv_crossReentrancyGuardOpenedOnExit(e);       // ok
    requireInvariant inv_crossReentrancyProtectionNoDoubleCall(e);  // ok
    
    // Silo
    requireInvariant inv_interestRateTimestampNotInFuture(e);       // ok
    requireInvariant inv_zeroCollateralMeansZeroDebt(e);            // ok 
    requireInvariant inv_onlyOneDebtPerBorrower(e);                 // ok
    requireInvariant inv_borrowerCollateralSiloMustMatchDebt(e);    // violated in borrow/borrowShares/borrowSameAsset
    requireInvariant inv_zeroDebtMeansNoCollateralSilo(e);          // ?
    requireInvariant inv_protectedCollateralAlwaysLiquid(e);        // ok
    requireInvariant inv_liquiditySolvency(e);                      // ?
    requireInvariant inv_siloMustNotHaveUserAllowances(e);          // ok
    requireInvariant inv_protectedSharesMustBeBackedWithAssets(e);  // violated in withdraw/redeem/transitionCollateral
    requireInvariant inv_collateralSharesMustBeBackedWithAssets(e); // violated in withdraw/redeem/transitionCollateral
    requireInvariant inv_debtSharesMustBeBackedWithAssets(e);       // ok
}

// ERC20

invariant inv_eip20_totalSupplySolvency(env e)
    forall address token. ghostERC20TotalSupply[token] 
        == ghostERC20Balances[token][ghostErc20AccountsValues[token][0]] 
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][1]] 
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][2]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][3]] 
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][4]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][5]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][6]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][7]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][8]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][9]]
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }
        
// CrossReentrancyGuard

// VS- The cross reentrancy guard must remain opened on exit
strong invariant inv_crossReentrancyGuardOpenedOnExit(env e)
    ghostCrossReentrantStatus == _NOT_ENTERED()
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- No double calls to cross reentrancy protection
strong invariant inv_crossReentrancyProtectionNoDoubleCall(env e)
    ghostReentrancyProtectionDoubleCall == false
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// Silo

// VS- The interest rate timestamp must never be set in the future
strong invariant inv_interestRateTimestampNotInFuture(env e)
    forall address silo. ghostInterestRateTimestamp[silo] <= e.block.timestamp 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If the Silo's total collateral is zero, then its total debt must also be zero
strong invariant inv_zeroCollateralMeansZeroDebt(env e)
    forall address silo. ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()] == 0
        => ghostTotalAssets[silo][ASSET_TYPE_DEBT()] == 0 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- A borrower must never hold debt in more than one silo at the same time
strong invariant inv_onlyOneDebtPerBorrower(env e)
    forall address user. (
        ghostERC20Balances[ghostConfigDebtShareToken0][user] != 0 
            && ghostERC20Balances[ghostConfigDebtShareToken1][user] != 0
        ) == false 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- A borrower's collateral silo must always match the silo in which they hold debt
strong invariant inv_borrowerCollateralSiloMustMatchDebt(env e)
    forall address user. (
        ghostConfigBorrowerCollateralSilo[user] == 0
            || ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo0
            || ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo1
        ) && (ghostERC20Balances[ghostConfigDebtShareToken0][user] != 0
            <=> ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo0
        ) && (ghostERC20Balances[ghostConfigDebtShareToken1][user] != 0
            <=> ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo1
        ) 
filtered { 
    // UNSAFE: an issue in switchCollateralToThisSilo() - collateral silo in config 
    // could be set to silo without any debt at all
    f -> f.selector != 0xa1ecef5c   // Silo.switchCollateralToThisSilo()
    // SAFE: Can be executed by Silo only
    && f.selector != 0x40c755e1     // SiloConfig.setThisSiloAsCollateralSilo()
    && f.selector != 0xf6f8174f     // SiloConfig.setOtherSiloAsCollateralSilo()
    && f.selector != 0xc6c3bbe6     // ShareToken.mint()
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If a user has no debt in either debt share token, their collateral 
//  silo must be unset
strong invariant inv_zeroDebtMeansNoCollateralSilo(env e)
    forall address user. (
        ghostERC20Balances[ghostConfigDebtShareToken0][user] == 0
            <=> ghostConfigBorrowerCollateralSilo[user] == 0
        ) && (
            ghostERC20Balances[ghostConfigDebtShareToken1][user] == 0
                <=> ghostConfigBorrowerCollateralSilo[user] == 0
        )
filtered { 
    // UNSAFE: an issue in switchCollateralToThisSilo() - collateral silo in config 
    //  could be set to silo without any debt at all
    f -> f.selector != 0xa1ecef5c   // Silo.switchCollateralToThisSilo()
    // SAFE: Can be executed by Silo only
    && f.selector != 0x40c755e1     // SiloConfig.setThisSiloAsCollateralSilo()
    && f.selector != 0xf6f8174f     // SiloConfig.setOtherSiloAsCollateralSilo()
    && f.selector != 0xc6c3bbe6     // ShareToken.mint()
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- Protected collateral must remain fully available for withdrawal
strong invariant inv_protectedCollateralAlwaysLiquid(env e) (
    ghostERC20Balances[ghostConfigToken0][ghostConfigSilo0] 
        >= ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()]
    ) && (!IS_MODE_SINGLE() => (
    ghostERC20Balances[ghostConfigToken1][ghostConfigSilo1] 
        >= ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()]
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo's liquidity must cover its protected collateral, collateral, 
//  and fees minus any outstanding debt
strong invariant inv_liquiditySolvency(env e) (
    ghostERC20Balances[ghostConfigToken0][ghostConfigSilo0] >= 
        ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo0]
        - ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_DEBT()] 
    ) && (!IS_MODE_SINGLE() => (
    ghostERC20Balances[ghostConfigToken1][ghostConfigSilo1] >= 
        ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo1]
        - ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_DEBT()] 
    ))
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo contract must never have an allowance to withdraw assets
strong invariant inv_siloMustNotHaveUserAllowances(env e) (
    forall address user. ghostERC20Allowances[ghostConfigToken0][ghostConfigSilo0][user] == 0
    ) && (!IS_MODE_SINGLE() => (
    forall address user. ghostERC20Allowances[ghostConfigToken1][ghostConfigSilo1][user] == 0
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo’s collateral protected share tokens must always be backed by the assets
strong invariant inv_protectedSharesMustBeBackedWithAssets(env e) (
    ghostERC20TotalSupply[ghostConfigProtectedCollateralShareToken0] != 0
        => ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()] != 0 
    ) && (!IS_MODE_SINGLE() => (
    ghostERC20TotalSupply[ghostConfigProtectedCollateralShareToken1] != 0
        => ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()] != 0 
    )) 
filtered { 
    // SAFE: Can be executed by Silo only
    f -> f.selector != 0xc6c3bbe6     // ShareToken.mint()
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo’s collateral share tokens must always be backed by the assets
strong invariant inv_collateralSharesMustBeBackedWithAssets(env e) (
    ghostERC20TotalSupply[ghostConfigCollateralShareToken0] != 0
        => ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_COLLATERAL()] != 0 
    ) && (!IS_MODE_SINGLE() => (
    ghostERC20TotalSupply[ghostConfigCollateralShareToken1] != 0
        => ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_COLLATERAL()] != 0 
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo’s collateral share tokens must always be backed by the assets
strong invariant inv_debtSharesMustBeBackedWithAssets(env e) (
    ghostERC20TotalSupply[ghostConfigDebtShareToken0] != 0
        => ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_DEBT()] != 0 
    ) && (!IS_MODE_SINGLE() => (
    ghostERC20TotalSupply[ghostConfigDebtShareToken1] != 0
        => ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_DEBT()] != 0 
    )) 
filtered { 
    // SAFE: Can be executed by Silo only
    f -> f.selector != 0xc6c3bbe6     // ShareToken.mint()
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

