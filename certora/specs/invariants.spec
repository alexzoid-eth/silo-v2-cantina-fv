// Silo valid state invariants working for all Silo contracts 

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";

function requireValidStateInvariants(env e) {

    // ERC20
    requireInvariant inv_eip20_totalSupplySolvency(e);
    
    // SiloConfig
    
    requireInvariant inv_crossReentrancyGuardOpenedOnExit(e);
    
    // Silo
    requireInvariant inv_transferWithChecksAlwaysEnabled(e);
    requireInvariant inv_interestRateTimestampNotInFuture(e);
    requireInvariant inv_borrowerCannotHaveTwoDebts(e);
    requireInvariant inv_borrowerCannotHaveDebtWithoutCollateralSet(e); 
    requireInvariant inv_borrowerCannotHaveDebtWithoutCollateralShares(e); // @todo violated

    // SiloX
    requireInvariant inv_liquiditySolvency0(e); requireInvariant inv_liquiditySolvency1(e);
    requireInvariant inv_siloMustNotHaveUserAllowances0(e); requireInvariant inv_siloMustNotHaveUserAllowances1(e);
    requireInvariant inv_protectedCollateralAlwaysLiquid0(e); requireInvariant inv_protectedCollateralAlwaysLiquid1(e);
    requireInvariant inv_zeroCollateralMeansZeroDebt0(e); requireInvariant inv_zeroCollateralMeansZeroDebt1(e);
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
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// 
// CrossReentrancyGuard
//

// The cross reentrancy guard must remain opened on exit
invariant inv_crossReentrancyGuardOpenedOnExit(env e)
    ghostCrossReentrantStatus == NOT_ENTERED()
filtered { 
    // SAFE: Ignore turning on protection function 
    f -> f.selector != 0x9dd41330   // Config.turnOnReentrancyProtection()
    && !VIEW_OR_FALLBACK_FUNCTION(f)
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

//
// Silo
// 

// The silo’s transferWithChecks feature must always remain enabled
invariant inv_transferWithChecksAlwaysEnabled(env e)
    forall address shareToken. ghostShareTokenTransferWithChecks[shareToken] == true
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// The interest rate timestamp must never be set in the future
invariant inv_interestRateTimestampNotInFuture(env e)
    ghostInterestRateTimestamp[_Silo0] <= e.block.timestamp 
    && ghostInterestRateTimestamp[_Silo1] <= e.block.timestamp 
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// A borrower must never hold debt in more than one silo at the same time
invariant inv_borrowerCannotHaveTwoDebts(env e)
    forall address user.
        // No debt at all
        (ghostERC20Balances[_Debt0][user] == 0 
            && ghostERC20Balances[_Debt1][user] == 0)
        || (
        // Debt in one Silo only
        ghostERC20Balances[_Debt0][user] != 0
            <=> ghostERC20Balances[_Debt1][user] == 0
        )
filtered { 
    // SAFE: Can be executed by Silo only
    f -> f.selector != 0xc6c3bbe6     // ShareDebtToken.mint()
    && !VIEW_OR_FALLBACK_FUNCTION(f)
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// Borrower cannot have debt without collateral set in the config
invariant inv_borrowerCannotHaveDebtWithoutCollateralSet(env e) 
    forall address user.
        // User has a debt
        (ghostERC20Balances[_Debt0][user] != 0 || ghostERC20Balances[_Debt1][user] != 0)
            => (
                ghostConfigBorrowerCollateralSilo[user] == _Silo0 || ghostConfigBorrowerCollateralSilo[user] == _Silo1
            )
filtered { 
    // SAFE: Can be executed by Silo only
    f -> f.selector != 0xc6c3bbe6     // ShareDebtToken.mint()
    // SAFE: Can be executed by HookReceiver only, but there is no debt transfer from it
    && f.selector != 0xd985616c     // ShareDebtToken.forwardTransferFromNoChecks()
    && !VIEW_OR_FALLBACK_FUNCTION(f)
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// Borrower cannot have debt without collateral shares
invariant inv_borrowerCannotHaveDebtWithoutCollateralShares(env e) 
    forall address borrower.
        // User has a debt
        ghostERC20Balances[_Debt0][borrower] != 0 || ghostERC20Balances[_Debt1][borrower] != 0
                // Collateral could be in any Silo, moreover configBorrowerCollateralSilo[] could be 
                //  outdated (after debt transfer or repay)
            => ((
                ghostERC20Balances[_Protected0][borrower] + ghostERC20Balances[_Collateral0][borrower] != 0
            ) || (
                ghostERC20Balances[_Protected1][borrower] + ghostERC20Balances[_Collateral1][borrower] != 0
            ))
filtered { 
    // SAFE: Can be executed by Silo only
    f -> f.selector != 0x40c755e1   // Config.setThisSiloAsCollateralSilo()
    && f.selector != 0xf6f8174f     // Config.setOtherSiloAsCollateralSilo()
    && f.selector != 0xc6c3bbe6     // ShareDebtToken.mint()
    && f.selector != 0xf6b911bc     // ShareDebtToken.burn()
    // SAFE: Can be executed by HookReceiver only, but there is no debt transfer from it
    && f.selector != 0xd985616c     // ShareDebtToken.forwardTransferFromNoChecks()
    && !VIEW_OR_FALLBACK_FUNCTION(f)
    } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

//
// SiloX
// 

// The Silo's liquidity must cover its protected collateral, collateral, 
//  and fees minus any outstanding debt
definition liquiditySolvency(bool zero) returns bool =
    ghostERC20Balances[ghostTokenX(zero)][ghostSiloX(zero)] >= 
        ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_PROTECTED()] 
        + ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] 
        + ghostDaoAndDeployerRevenue[ghostSiloX(zero)]
        - ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()];

invariant inv_liquiditySolvency0(env e) liquiditySolvency(true)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_liquiditySolvency1(env e) liquiditySolvency(false)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// The Silo contract must never have an allowance to withdraw assets
definition siloMustNotHaveUserAllowances(bool zero) returns bool =
    forall address user. ghostERC20Allowances[ghostTokenX(zero)][ghostSiloX(zero)][user] == 0;

invariant inv_siloMustNotHaveUserAllowances0(env e) siloMustNotHaveUserAllowances(true)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_siloMustNotHaveUserAllowances1(env e) siloMustNotHaveUserAllowances(false)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// Protected collateral must remain fully available for withdrawal
definition protectedCollateralAlwaysLiquid(bool zero) returns bool =
    ghostERC20Balances[ghostTokenX(zero)][ghostSiloX(zero)]
        >= ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_PROTECTED()];

invariant inv_protectedCollateralAlwaysLiquid0(env e) protectedCollateralAlwaysLiquid(true)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_protectedCollateralAlwaysLiquid1(env e) protectedCollateralAlwaysLiquid(false)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

// If the Silo's total collateral is zero, then its total debt must also be zero
definition zeroCollateralMeansZeroDebt(bool zero) returns bool = 
    ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_COLLATERAL()] == 0
        => ghostTotalAssets[ghostSiloX(zero)][ASSET_TYPE_DEBT()] == 0;

invariant inv_zeroCollateralMeansZeroDebt0(env e) zeroCollateralMeansZeroDebt(true)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

invariant inv_zeroCollateralMeansZeroDebt1(env e) zeroCollateralMeansZeroDebt(false)
filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) }
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }