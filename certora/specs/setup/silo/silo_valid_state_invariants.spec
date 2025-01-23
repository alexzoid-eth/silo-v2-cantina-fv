// Silo config valid state invariants working both for Silo0 and Silo1

function requireSiloValidState() {
    requireInvariant crossReentrancyGuardOpenedOnExit;
    requireInvariant crossReentrancyProtectionNoDoubleCall;
    requireInvariant shareTokenHooksSynchronization;
}

function requireSiloValidStateEnv(env e) {
    requireSiloValidState();
    requireErc20ValidState();

    requireInvariant interestRateTimestampNotInFuture(e);
}

// CrossReentrancyGuard

invariant crossReentrancyGuardOpenedOnExit()
    ghostCrossReentrantStatus == _NOT_ENTERED();

invariant crossReentrancyProtectionNoDoubleCall()
    ghostReentrancyProtectionDoubleCall == false;

// ShareToken

// VS- The share token’s hooks must always match the hookReceiver’s configuration
strong invariant shareTokenHooksSynchronization()
    forall address contract. ghostShareTokenHooksBefore[contract] == ghostHooksBefore[_Silo0]
        && ghostShareTokenHooksAfter[contract] == ghostHooksAfter[_Silo0] {
            preserved synchronizeHooks(uint24 hooksBefore, uint24 hooksAfter) {
                // Only silo executes this function with parameters from IHookReceiver.hookReceiverConfig
                require(hooksBefore == ghostHooksBefore[_Silo0]);
                require(hooksAfter == ghostHooksAfter[_Silo0]);
            }   
        }

// Silo

// VS- The interest rate timestamp must never be set in the future
strong invariant interestRateTimestampNotInFuture(env e)
    forall address silo. ghostInterestRateTimestamp[silo] <= e.block.timestamp {
        preserved with (env eInv) {
            // Same environment inside a function call
            require(e.block.timestamp == eInv.block.timestamp);
        }
    }