// Silo valid state invariants working for all Silo contracts 

function requireValidStateInvariants(env e) {

    // ERC20
    requireInvariant eip20_totalSupplySolvency(e);
    /*
    // Silo config
    requireInvariant crossReentrancyGuardOpenedOnExit(e);
    requireInvariant crossReentrancyProtectionNoDoubleCall(e);
    
    // Silo
    requireInvariant interestRateTimestampNotInFuture(e);
    requireInvariant zeroCollateralMeansZeroDebt(e);
    requireInvariant onlyOneDebtPerBorrower(e); // @todo
    requireInvariant borrowerCollateralSiloMustMatchDebt(e); 
    requireInvariant zeroDebtMeansNoCollateralSilo(e);
    requireInvariant protectedCollateralAlwaysLiquid(e);
    requireInvariant liquiditySolvency(e);
    requireInvariant siloMustNotHaveUserAllowances(e);
    
    requireInvariant totalTrackedAssetsNotExceedERC20TokenSupply(e); // @todo 
    requireInvariant protectedSharesMustBeBackedWithAssets(e); // @todo 
    requireInvariant collateralSharesMustBeBackedWithAssets(e); // @todo 
    requireInvariant debtSharesMustBeBackedWithAssets(e); // @todo
    */
}

// ERC20

invariant eip20_totalSupplySolvency(env e)
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
invariant crossReentrancyGuardOpenedOnExit(env e)
    ghostCrossReentrantStatus == _NOT_ENTERED()
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- No double calls to cross reentrancy protection
invariant crossReentrancyProtectionNoDoubleCall(env e)
    ghostReentrancyProtectionDoubleCall == false
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// Silo

// VS- The interest rate timestamp must never be set in the future
strong invariant interestRateTimestampNotInFuture(env e)
    forall address silo. ghostInterestRateTimestamp[silo] <= e.block.timestamp 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If the Silo's total collateral is zero, then its total debt must also be zero
strong invariant zeroCollateralMeansZeroDebt(env e)
    forall address silo. ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()] == 0
        => ghostTotalAssets[silo][ASSET_TYPE_DEBT()] == 0 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- A borrower must never hold debt in more than one silo at the same time
strong invariant onlyOneDebtPerBorrower(env e)
    forall address user. (
        ghostERC20Balances[ghostConfigDebtShareToken0][user] != 0 
            && ghostERC20Balances[ghostConfigDebtShareToken1][user] != 0
        ) == false 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- A borrower's collateral silo must always match the silo in which they hold debt
strong invariant borrowerCollateralSiloMustMatchDebt(env e)
    forall address user. (
        ghostConfigBorrowerCollateralSilo[user] == 0
            || ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo0
            || ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo1
        ) && (ghostERC20Balances[ghostConfigDebtShareToken0][user] != 0
            <=> ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo0
        ) && (ghostERC20Balances[ghostConfigDebtShareToken1][user] != 0
            <=> ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo1
        ) 
// UNSAFE: an issue in switchCollateralToThisSilo() - collateral silo in config 
// could be set to silo without any debt at all
filtered { f -> f.selector != 0xa1ecef5c } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If a user has no debt in either debt share token, their collateral 
//  silo must be unset
strong invariant zeroDebtMeansNoCollateralSilo(env e)
    forall address user. (
        ghostERC20Balances[ghostConfigDebtShareToken0][user] == 0
            <=> ghostConfigBorrowerCollateralSilo[user] == 0
        ) && (
            ghostERC20Balances[ghostConfigDebtShareToken1][user] == 0
                <=> ghostConfigBorrowerCollateralSilo[user] == 0
        )
// UNSAFE: an issue in switchCollateralToThisSilo() - collateral silo in config 
// could be set to silo without any debt at all
filtered { f -> f.selector != 0xa1ecef5c } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- Protected collateral must remain fully available for withdrawal
strong invariant protectedCollateralAlwaysLiquid(env e) (
    ghostERC20Balances[ghostConfigToken0][ghostConfigSilo0] 
        >= ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()]
    ) && (IS_FULL_SILO() => (
    ghostERC20Balances[ghostConfigToken1][ghostConfigSilo1] 
        >= ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()]
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo's liquidity must cover its protected collateral, collateral, 
//  and fees minus any outstanding debt
strong invariant liquiditySolvency(env e) (
    ghostERC20Balances[ghostConfigToken0][ghostConfigSilo0] >= 
        ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo0]
        - ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_DEBT()] 
    ) && (IS_FULL_SILO() => (
    ghostERC20Balances[ghostConfigToken1][ghostConfigSilo1] >= 
        ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo1]
        - ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_DEBT()] 
    ))
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo contract must never have an allowance to withdraw assets
strong invariant siloMustNotHaveUserAllowances(env e) (
    forall address user. ghostERC20Allowances[ghostConfigToken0][ghostConfigSilo0][user] == 0
    ) && (IS_FULL_SILO() => (
    forall address user. ghostERC20Allowances[ghostConfigToken1][ghostConfigSilo1][user] == 0
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

//////////////////////////////////////////////////////////////////////////////

// VS- The Silo's total tracked assets must not exceed the token's total supply
strong invariant totalTrackedAssetsNotExceedERC20TokenSupply(env e) (
    ghostERC20TotalSupply[ghostConfigToken0] >= 
        ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo0] 
        + getAccruedInterestCVL(e, ghostConfigSilo0) 
    ) && (IS_FULL_SILO() => (
    ghostERC20TotalSupply[ghostConfigToken1] >= 
        ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo1] 
        + getAccruedInterestCVL(e, ghostConfigSilo1) 
    ))
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo’s collateral protected share tokens must always be backed by the assets
strong invariant protectedSharesMustBeBackedWithAssets(env e) (
    ghostERC20TotalSupply[ghostConfigProtectedCollateralShareToken0] != 0
        => ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()] != 0 
    ) && (IS_FULL_SILO() => (
    ghostERC20TotalSupply[ghostConfigProtectedCollateralShareToken1] != 0
        => ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()] != 0 
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo’s collateral share tokens must always be backed by the assets
strong invariant collateralSharesMustBeBackedWithAssets(env e) (
    ghostERC20TotalSupply[ghostConfigCollateralShareToken0] != 0
        => ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_COLLATERAL()] != 0 
    ) && (IS_FULL_SILO() => (
    ghostERC20TotalSupply[ghostConfigCollateralShareToken1] != 0
        => ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_COLLATERAL()] != 0 
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo’s collateral share tokens must always be backed by the assets
strong invariant debtSharesMustBeBackedWithAssets(env e) (
    ghostERC20TotalSupply[ghostConfigDebtShareToken0] != 0
        => ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_DEBT()] != 0 
    ) && (IS_FULL_SILO() => (
    ghostERC20TotalSupply[ghostConfigDebtShareToken1] != 0
        => ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_DEBT()] != 0 
    )) 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

