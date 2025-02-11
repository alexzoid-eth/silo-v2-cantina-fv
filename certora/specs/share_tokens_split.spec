// Version of `share_tokens.spec` with support of `ALL_SSTORE`. Keep it in a separate spec because 
//  storage view is not available with `enableStorageSplitting false` option enabled

import "./share_tokens.spec";

// Set true at every storage write
persistent ghost bool ghostStorageTouched;
// Set true at every storage write before hookBefore
persistent ghost bool ghostStorageTouchedBeforeEntryActionHook;
// Set true at every storage write after hookAfter
persistent ghost bool ghostStorageTouchedAfterExitActionHook;

hook ALL_SSTORE(uint256 slot, uint256 val)  {
    ghostStorageTouchedBeforeEntryActionHook = (ghostBeforeActionCalled == false);    
    ghostStorageTouchedAfterExitActionHook = (ghostAfterActionCalled == true);
    ghostStorageTouched = true;
}

// Ensures no storage writes happen before `hookBefore` or after `hookAfter`
rule hooks_enforceHookBeforeAfterOrdering(env e, method f, calldataarg args) 
    filtered { f -> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) 
        // `$.transferWithChecks = true` in `forwardTransferFromNoChecks()` breaks the rule
        && !(f.selector == 0xd985616c) // forwardTransferFromNoChecks()
    } 
{
    setupSilo(e);
    require(ghostHookActionAllowAll == true);

    // No writes or hooks at the start
    require(
        !ghostStorageTouchedBeforeEntryActionHook 
        && !ghostStorageTouchedAfterExitActionHook
        && !ghostBeforeActionCalled
        && !ghostAfterActionCalled
    );

    f(e, args);

    // For non-transfer functions, no writes should happen before `hookBefore`.
    // For all functions, no writes should happen after `hookAfter`.
    assert(!NO_HOOKS_FUNCTIONS(f) => (
        (TRANSFER_FUNCTIONS(f) ? true : ghostStorageTouchedBeforeEntryActionHook == false)
        && ghostStorageTouchedAfterExitActionHook == false
    ));
}

// Hooks Must Execute If Storage Changes
//  If storage was changed, then both hooks must be called.
//  For transfers, the before hook is optional, but after hook is required.
rule share_hooksMustExecuteIfStorageChanged(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f)
        // `$.transferWithChecks = true` in `forwardTransferFromNoChecks()` breaks the rule
        && !(f.selector == 0xd985616c) // forwardTransferFromNoChecks()
    } 
{
    setupSilo(e);
    require(ghostHookActionAllowAll == true);

    // Reset flags
    require(!ghostStorageTouched && !ghostBeforeActionCalled && !ghostAfterActionCalled);

    f(e, args);

    // If storage changed, both hooks must be called.
    // Transfer-only => before hook might be skipped, but after hook must be triggered.
    assert(!NO_HOOKS_FUNCTIONS(f) && ghostStorageTouched => (
        (TRANSFER_FUNCTIONS(f) ? true : ghostBeforeActionCalled)
        && ghostAfterActionCalled
    ));
}

rule share_possibilityOfStorageTouchedWhenHookInvolved(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) } 
{
    setupSilo(e);

    require(!ghostStorageTouched 
        && !ghostBeforeActionCalled 
        && !ghostAfterActionCalled 
        && ghostExpectedHook == 0
        );

    f(e, args);

    satisfy(ghostBeforeActionCalled || ghostAfterActionCalled || ghostExpectedHook != 0
        => ghostStorageTouched
    );
}