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
