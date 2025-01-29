// Silo config valid state invariants working both for Silo0 and Silo1

function requireSiloValidStateCommon() {

    requireErc20ValidState();

    // SAFE: assume realistic initial amount of accumulated fee to avoid overflow in
    //  `unchecked { $.daoAndDeployerRevenue += uint192(totalFees); }`
    require(forall address silo. ghostDaoAndDeployerRevenue[silo] < max_uint96);

    requireInvariant crossReentrancyGuardOpenedOnExit;
    requireInvariant crossReentrancyProtectionNoDoubleCall;
    requireInvariant shareTokenHooksSynchronization;
}

function requireSiloValidStateCommonE(env e) {
    requireSiloValidStateCommon();
    
    requireInvariant interestRateTimestampNotInFuture(e);
    requireInvariant zeroCollateralMeansZeroDebt(e);
    requireInvariant onlyOneDebtPerBorrower(e);
    requireInvariant borrowerCollateralSiloMustMatchDebt(e);
    requireInvariant zeroDebtMeansNoCollateralSilo(e);
}

// CrossReentrancyGuard

// VS- The cross reentrancy guard must remain opened on exit
invariant crossReentrancyGuardOpenedOnExit()
    ghostCrossReentrantStatus == _NOT_ENTERED();

// VS- No double calls to cross reentrancy protection
invariant crossReentrancyProtectionNoDoubleCall()
    ghostReentrancyProtectionDoubleCall == false;

// ShareToken

// VS- The share token’s hooks must always match the hookReceiver’s configuration
strong invariant shareTokenHooksSynchronization()
    forall address contract. ghostShareTokenHooksBefore[contract] == ghostHooksBefore[_Silo0]
        && ghostShareTokenHooksAfter[contract] == ghostHooksAfter[_Silo0] {
            preserved synchronizeHooks(uint24 hooksBefore, uint24 hooksAfter) with (env e) {
                // SAFE: Only silo executes this function with parameters from IHookReceiver.hookReceiverConfig()
                require(hooksBefore == ghostHooksBefore[_Silo0] && hooksAfter == ghostHooksAfter[_Silo0]);
            }   
        }

// Silo

// VS- The interest rate timestamp must never be set in the future
strong invariant interestRateTimestampNotInFuture(env e)
    forall address silo. ghostInterestRateTimestamp[silo] <= e.block.timestamp {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
        }
    }

// VS- If the Silo's total collateral is zero, then its total debt must also be zero
strong invariant zeroCollateralMeansZeroDebt(env e)
    forall address silo. ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()] == 0
        => ghostTotalAssets[silo][ASSET_TYPE_DEBT()] == 0 {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment
            requireSiloValidStateCommonE(e);
        }
    }

// VS- A borrower must never hold debt in more than one silo at the same time
strong invariant onlyOneDebtPerBorrower(env e)
    forall address user. (
        ghostERC20Balances[ghostConfigDebtShareToken0][user] != 0 
            && ghostERC20Balances[ghostConfigDebtShareToken1][user] != 0
        ) == false {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment
            requireSiloValidStateCommonE(e);
        }
    }

// VS- A borrower's collateral silo must always match the silo in which they hold debt
strong invariant borrowerCollateralSiloMustMatchDebt(env e)
    forall address user. (
        ghostConfigBorrowerCollateralSilo[user] == 0
            || ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo0
            || ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo1
        ) && (ghostERC20Balances[ghostConfigDebtShareToken0][user] != 0
            <=> ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo0
        ) && (
        ghostERC20Balances[ghostConfigDebtShareToken1][user] != 0
            <=> ghostConfigBorrowerCollateralSilo[user] == ghostConfigSilo1
        ) 
    // UNSAFE: an issue in switchCollateralToThisSilo() - collateral silo in config 
    // could be set to silo without any debt at all
    filtered { f -> f.selector != sig:switchCollateralToThisSilo().selector } {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment
            requireSiloValidStateCommonE(e);
        }
    }

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
    filtered { f -> f.selector != sig:switchCollateralToThisSilo().selector } {
        preserved with (env eInv) {
            // SAFE: Same environment inside a function and invariant
            requireSameEnv(e, eInv);
            // SAFE: Valid state and environment
            requireSiloValidStateCommonE(e);
        }
    }
