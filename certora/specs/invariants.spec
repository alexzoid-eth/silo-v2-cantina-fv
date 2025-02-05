// Silo valid state invariants working for all Silo contracts 

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";

function requireValidStateInvariants(env e) {

    // ERC20
    requireInvariant inv_eip20_totalSupplySolvency(e);
    
    // SiloConfig
    
    requireInvariant inv_crossReentrancyGuardOpenedOnExit(e);
    requireInvariant inv_crossReentrancyProtectionNoDoubleCall(e);
    
    // Silo

    requireInvariant inv_transferWithChecksAlwaysEnabled(e);
    requireInvariant inv_interestRateTimestampNotInFuture(e);
    requireInvariant inv_onlyOneDebtPerBorrower(e);
    requireInvariant inv_borrowerCollateralSiloMustMatchDebt(e); // violated: Silo1.switchCollateralToThisSilo(), Silo1.borrowSameAsset()

    // SiloX
    requireInvariant inv_liquiditySolvency0(e); requireInvariant inv_liquiditySolvency1(e);
    requireInvariant inv_collateralPlusFeesCoverDebt0(e); requireInvariant inv_collateralPlusFeesCoverDebt1(e);
    requireInvariant inv_borrowerCannotHaveDebtWithoutCollateral0(e); requireInvariant inv_borrowerCannotHaveDebtWithoutCollateral1(e); // violated: Silo1.borrowSameAsset()
    requireInvariant inv_siloMustNotHaveUserAllowances0(e); requireInvariant inv_siloMustNotHaveUserAllowances1(e);
    requireInvariant inv_protectedCollateralAlwaysLiquid0(e); requireInvariant inv_protectedCollateralAlwaysLiquid1(e);
    requireInvariant inv_zeroCollateralMeansZeroDebt0(e); requireInvariant inv_zeroCollateralMeansZeroDebt1(e);

    // debt tracked assets >= total shares
    requireInvariant inv_debtAssetsGteShares0(e); requireInvariant inv_debtAssetsGteShares1(e);        

    // zero assets <=> zero shares (based on `SiloMathLib._commonConvertTo()`; UNSAFE: don't prove due timeouts)
    requireInvariant inv_protectedZeroAssetsMustZeroShares0(e); requireInvariant inv_protectedZeroAssetsMustZeroShares1(e);        
    requireInvariant inv_collateralZeroAssetsMustZeroShares0(e); requireInvariant inv_collateralZeroAssetsMustZeroShares1(e);        
    requireInvariant inv_debtZeroAssetsMustZeroShares0(e); requireInvariant inv_debtZeroAssetsMustZeroShares1(e);        

    // non-zero shares total supply => non-zero tracked assets
    requireInvariant inv_protectedNonZeroSharesMustNonZeroAssets0(e); requireInvariant inv_protectedNonZeroSharesMustNonZeroAssets1(e);        
    requireInvariant inv_collateralNonZeroSharesMustNonZeroAssets0(e); requireInvariant inv_collateralNonZeroSharesMustNonZeroAssets1(e);        
    requireInvariant inv_debtNonZeroSharesMustNonZeroAssets0(e); requireInvariant inv_debtNonZeroSharesMustNonZeroAssets1(e);        
}

//
// ERC20
//

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

// 
// CrossReentrancyGuard
//

// VS- The cross reentrancy guard must remain opened on exit
invariant inv_crossReentrancyGuardOpenedOnExit(env e)
    ghostCrossReentrantStatus == _NOT_ENTERED()
filtered { 
    // SAFE: Ignore turning on protection function 
    f -> f.selector != 0x9dd41330   // Config.turnOnReentrancyProtection()
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- No double calls to cross reentrancy protection
invariant inv_crossReentrancyProtectionNoDoubleCall(env e)
    ghostReentrancyProtectionDoubleCall == false
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

//
// Silo
// 

// VS- The silo’s transferWithChecks feature must always remain enabled
invariant inv_transferWithChecksAlwaysEnabled(env e)
    forall address shareToken. ghostShareTokenTransferWithChecks[shareToken] == true
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The interest rate timestamp must never be set in the future
invariant inv_interestRateTimestampNotInFuture(env e)
    forall address silo. ghostInterestRateTimestamp[silo] <= e.block.timestamp 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- A borrower must never hold debt in more than one silo at the same time
invariant inv_onlyOneDebtPerBorrower(env e)
    forall address user. (
        ghostERC20Balances[ghostDebtToken0][user] != 0
            => ghostERC20Balances[ghostDebtToken1][user] == 0
    ) && (
        ghostERC20Balances[ghostDebtToken1][user] != 0
            => ghostERC20Balances[ghostDebtToken0][user] == 0
    )
filtered { 
    // SAFE: Can be executed by Silo only
    f -> f.selector != 0xc6c3bbe6     // ShareToken.mint()
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- A borrower's collateral silo must always match the silo in which they hold debt
invariant inv_borrowerCollateralSiloMustMatchDebt(env e)
    forall address user. (
        ghostConfigBorrowerCollateralSilo[user] == 0
            || ghostConfigBorrowerCollateralSilo[user] == ghostSilo0
            || ghostConfigBorrowerCollateralSilo[user] == ghostSilo1
        ) && (
        // Debt in Silo0 not zero
        ghostERC20Balances[ghostDebtToken0][user] != 0
            // Config's collateral is Silo1 (and vise versa)
            => ghostConfigBorrowerCollateralSilo[user] == ghostSilo1
        ) && (
        ghostERC20Balances[ghostDebtToken1][user] != 0
            => ghostConfigBorrowerCollateralSilo[user] == ghostSilo0
        )
filtered { 
    f -> 
    // SAFE: Can be executed by Silo only
    f.selector != 0x40c755e1        // Config.setThisSiloAsCollateralSilo()
    && f.selector != 0xf6f8174f     // Config.setOtherSiloAsCollateralSilo()
    && f.selector != 0xc6c3bbe6     // ShareDebtToken.mint()
    // SAFE: Can be executed by Debt only
    && f.selector != 0x72db6559     // Config.onDebtTransfer()
    // SAFE: Can be executed by HookReceiver only, but there is no debt transfer from it
    && f.selector != 0xd985616c     // ShareDebtToken.forwardTransferFromNoChecks()
    // UNSAFE: an issue here - `borrowerCollateralSilo[_recipient]` doesn't update on debt transfer when it is `!= 0`
    // https://prover.certora.com/output/52567/a6a6d74d0f884801b0883b16b9bba4d4/?anonymousKey=773f7d1f9e00145c4e1a48cdefbbad98fcffe256
    && f.selector != 0xa9059cbb     // ShareDebtToken.transfer()
    && f.selector != 0x23b872dd     // ShareDebtToken.transferFrom()
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

//
// SiloX
// 

// VS- The Silo's liquidity must cover its protected collateral, collateral, 
//  and fees minus any outstanding debt
definition liquiditySolvency(bool zero) returns bool =
    ghostERC20Balances[ghostTokenX(zero)][ghostSiloX(zero)] >= 
        ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostSiloX(zero)]
        - ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()];

invariant inv_liquiditySolvency0(env e) liquiditySolvency(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_liquiditySolvency1(env e) liquiditySolvency(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo's collateral plus distributor fees must always cover its total debt
definition collateralPlusFeesCoverDebt(bool zero) returns bool =
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostSiloX(zero)]
        >= ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()];

invariant inv_collateralPlusFeesCoverDebt0(env e) collateralPlusFeesCoverDebt(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_collateralPlusFeesCoverDebt1(env e) collateralPlusFeesCoverDebt(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- Borrower cannot have debt in one silo without collateral in the other
definition borrowerCannotHaveDebtWithoutCollateral(bool zero) returns bool =
    forall address user.
        ghostERC20Balances[ghostDebtTokenX(zero)][user] != 0
            => (
                ghostERC20Balances[ghostProtectedTokenX(!zero)][user] +
                ghostERC20Balances[ghostCollateralTokenX(!zero)][user]
                != 0
            );

invariant inv_borrowerCannotHaveDebtWithoutCollateral0(env e) borrowerCannotHaveDebtWithoutCollateral(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_borrowerCannotHaveDebtWithoutCollateral1(env e) borrowerCannotHaveDebtWithoutCollateral(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- The Silo contract must never have an allowance to withdraw assets
definition siloMustNotHaveUserAllowances(bool zero) returns bool =
    forall address user. ghostERC20Allowances[ghostTokenX(zero)][ghostSiloX(zero)][user] == 0;

invariant inv_siloMustNotHaveUserAllowances0(env e) siloMustNotHaveUserAllowances(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_siloMustNotHaveUserAllowances1(env e) siloMustNotHaveUserAllowances(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- Protected collateral must remain fully available for withdrawal
definition protectedCollateralAlwaysLiquid(bool zero) returns bool =
    ghostERC20Balances[ghostTokenX(zero)][ghostSiloX(zero)]
        >= ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_PROTECTED()];

invariant inv_protectedCollateralAlwaysLiquid0(env e) protectedCollateralAlwaysLiquid(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_protectedCollateralAlwaysLiquid1(env e) protectedCollateralAlwaysLiquid(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If the Silo's total collateral is zero, then its total debt must also be zero
definition zeroCollateralMeansZeroDebt(bool zero) returns bool = 
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] == 0
        => ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()] == 0;

invariant inv_zeroCollateralMeansZeroDebt0(env e) zeroCollateralMeansZeroDebt(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_zeroCollateralMeansZeroDebt1(env e) zeroCollateralMeansZeroDebt(false)
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

/////////////////// zero assets <=> zero shares (based on `SiloMathLib._commonConvertTo()`

// VS- If the Silo has zero protected assets, then totalSupply(protectedToken) must also be zero
definition protectedZeroAssetsMustZeroShares(bool zero) returns bool =
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_PROTECTED()] == 0
        <=> ghostERC20TotalSupply[ghostProtectedTokenX(zero)] == 0;

invariant inv_protectedZeroAssetsMustZeroShares0(env e) protectedZeroAssetsMustZeroShares(true)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_protectedZeroAssetsMustZeroShares1(env e) protectedZeroAssetsMustZeroShares(false)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If the Silo has zero collateral assets, then totalSupply(collateralToken) must also be zero
definition collateralZeroAssetsMustZeroShares(bool zero) returns bool =
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] == 0
        <=> ghostERC20TotalSupply[ghostCollateralTokenX(zero)] == 0;

invariant inv_collateralZeroAssetsMustZeroShares0(env e) collateralZeroAssetsMustZeroShares(true)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_collateralZeroAssetsMustZeroShares1(env e) collateralZeroAssetsMustZeroShares(false)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If the Silo has zero debt assets, then totalSupply(debtToken) must also be zero
definition debtZeroAssetsMustZeroShares(bool zero) returns bool =
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()] == 0
        <=> ghostERC20TotalSupply[ghostDebtTokenX(zero)] == 0;

invariant inv_debtZeroAssetsMustZeroShares0(env e) debtZeroAssetsMustZeroShares(true)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_debtZeroAssetsMustZeroShares1(env e) debtZeroAssetsMustZeroShares(false)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

/////////////////// non-zero shares total supply => non-zero tracked assets

// VS- If totalSupply(protectedToken) is non-zero, then the Silo's protected assets must not be zero
definition protectedNonZeroSharesMustNonZeroAssets(bool zero) returns bool =
    ghostERC20TotalSupply[ghostProtectedTokenX(zero)] != 0
        => ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_PROTECTED()] != 0;

invariant inv_protectedNonZeroSharesMustNonZeroAssets0(env e) protectedNonZeroSharesMustNonZeroAssets(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_protectedNonZeroSharesMustNonZeroAssets1(env e) protectedNonZeroSharesMustNonZeroAssets(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If totalSupply(collateralToken) is non-zero, then the Silo's collateral assets must not be zero
definition collateralNonZeroSharesMustNonZeroAssets(bool zero) returns bool =
    ghostERC20TotalSupply[ghostCollateralTokenX(zero)] != 0
        => ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] != 0;

invariant inv_collateralNonZeroSharesMustNonZeroAssets0(env e) collateralNonZeroSharesMustNonZeroAssets(true)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_collateralNonZeroSharesMustNonZeroAssets1(env e) collateralNonZeroSharesMustNonZeroAssets(false)
filtered { f -> f.selector != 0xc6c3bbe6 } // SAFE: ShareToken.mint() can be executed by Silo only 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// VS- If totalSupply(debtToken) is non-zero, then the Silo's debt assets must not be zero
definition debtNonZeroSharesMustNonZeroAssets(bool zero) returns bool =
    ghostERC20TotalSupply[ghostDebtTokenX(zero)] != 0
        => ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()] != 0;

invariant inv_debtNonZeroSharesMustNonZeroAssets0(env e) debtNonZeroSharesMustNonZeroAssets(true)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_debtNonZeroSharesMustNonZeroAssets1(env e) debtNonZeroSharesMustNonZeroAssets(false)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

//
// Borrower
//

