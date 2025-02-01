import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";

// Silo valid state invariants working for all Silo contracts 

function requireValidStateInvariants(env e) {

    // ERC20
    requireInvariant inv_eip20_totalSupplySolvency(e);
    
    // Silo config
    requireInvariant inv_crossReentrancyGuardOpenedOnExit(e);
    requireInvariant inv_crossReentrancyProtectionNoDoubleCall(e);
    
    // Silo
    requireInvariant inv_interestRateTimestampNotInFuture(e);
    requireInvariant inv_zeroCollateralMeansZeroDebt(e);
    requireInvariant inv_onlyOneDebtPerBorrower(e);
    requireInvariant inv_borrowerCollateralSiloMustMatchDebt(e); // config, debt
    requireInvariant inv_zeroDebtMeansNoCollateralSilo(e); // config, debt
    requireInvariant inv_protectedCollateralAlwaysLiquid(e);
    requireInvariant inv_liquiditySolvency(e);
    requireInvariant inv_siloMustNotHaveUserAllowances(e);
    
    requireInvariant inv_totalTrackedAssetsNotExceedERC20TokenSupply(e); // config
    requireInvariant inv_protectedSharesMustBeBackedWithAssets(e); // protected
    requireInvariant inv_collateralSharesMustBeBackedWithAssets(e);
    requireInvariant inv_debtSharesMustBeBackedWithAssets(e); // debt
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
    // SAFE: an issue in switchCollateralToThisSilo() - collateral silo in config 
    // could be set to silo without any debt at all
    f -> f.selector != 0xa1ecef5c   // Silo.switchCollateralToThisSilo()
    // SAFE: Can be executed by Silo only
    && f.selector != 0xe1355921     // SiloConfig.setThisSiloAsCollateralSilo()
    && f.selector != 0x97902a20     // SiloConfig.setOtherSiloAsCollateralSilo()
    && f.selector != 0xc6c3bbe6     // ShareDebtToken.mint()
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
    // SAFE: an issue in switchCollateralToThisSilo() - collateral silo in config 
    //  could be set to silo without any debt at all
    f -> f.selector != 0xa1ecef5c   // Silo.switchCollateralToThisSilo()
    // SAFE: Can be executed by Silo only
    && f.selector != 0xe1355921     // SiloConfig.setThisSiloAsCollateralSilo()
    && f.selector != 0x97902a20     // SiloConfig.setOtherSiloAsCollateralSilo()
    && f.selector != 0xc6c3bbe6     // ShareDebtToken.mint()
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

// VS- The Silo's total tracked assets must not exceed the token's total supply
strong invariant inv_totalTrackedAssetsNotExceedERC20TokenSupply(env e) (
    ghostERC20TotalSupply[ghostConfigToken0] >= 
        ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo0][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo0] 
        + getAccruedInterestCVL(e, ghostConfigSilo0) 
    ) && (!IS_MODE_SINGLE() => (
    ghostERC20TotalSupply[ghostConfigToken1] >= 
        ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostConfigSilo1][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostConfigSilo1] 
        + getAccruedInterestCVL(e, ghostConfigSilo1) 
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
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

