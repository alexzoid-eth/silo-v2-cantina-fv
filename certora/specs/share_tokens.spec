// Common rules for Protected, Collateral and Debt share tokens

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./invariants.spec";

methods {
    function Hook.matchAction(uint256 _action, uint256 _expectedHook) internal returns (bool)
        => matchActionCVL(_action, _expectedHook);
}

////////////////////////////////////////////////// Hooks

// Execute all hooks when set true
persistent ghost bool ghostHookActionAllowAll;
persistent ghost uint256 ghostExpectedHook;
function matchActionCVL(uint256 _action, uint256 _expectedHook) returns bool {
    ghostExpectedHook = _expectedHook;
    if (ghostHookActionAllowAll) {
        require(_action & _expectedHook == _expectedHook);
        return true;
    } else {
        return (_action & _expectedHook == _expectedHook);
    }
}

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

// Functions that must never trigger hooks
definition NO_HOOKS_FUNCTIONS(method f) returns bool = 
    
    // Silo
    f.selector == 0xa6afed95 // accrueInterest()
    || f.selector == 0x6e236614 // accrueInterestForConfig()
    || f.selector == 0xcad1aacf // updateHooks()
    || f.selector == 0x476343ee // withdrawFees()

    // Common share tokens
    || f.selector == 0x095ea7b3 // approve()
    || f.selector == 0x4c7b0f3c // synchronizeHooks()
    || f.selector == 0x336c8d70 // initialize()

    // Debt share tokens
    || f.selector == 0x80d4336e // decreaseReceiveAllowance()
    || f.selector == 0x75d68016 // increaseReceiveAllowance()
    || f.selector == 0x34deadf2 // setReceiveApproval()
    ;

// Transfer-related functions
definition TRANSFER_FUNCTIONS(method f) returns bool = 
    f.selector == 0xa9059cbb    // transfer()
    || f.selector == 0x23b872dd // transferFrom()
    ;

// Ensures no storage writes happen before `hookBefore` or after `hookAfter`
rule share_enforceHookBeforeAfterOrdering(env e, method f, calldataarg args) 
    filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f) 
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
    filtered { f -> !VIEW_OR_FALLBACK_FUNCTION(f)
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

// Function Executes Configured Hooks
rule share_functionExecutesHooksBasedOnConfig(env e, method f, calldataarg args) 
    filtered { f-> !VIEW_OR_FALLBACK_FUNCTION(f) } 
{
    setupSilo(e);
    require(ghostHookActionAllowAll == true);

    f(e, args);

    // Verify the function’s hooks match ghostExpectedHook
    assert(!NO_HOOKS_FUNCTIONS(f) 
        // UNSAFE: TODO - add a support of transfer functions in `ghostSelectorHooks[]`
        && !TRANSFER_FUNCTIONS(f) 
        => (
        ghostExpectedHook == ghostSelectorHooks[to_bytes4(f.selector)]
    ));
}

// No Hook Function Must Not Execute Hook
//  Any function in NO_HOOKS_FUNCTIONS must not call hooks at all.
rule share_noHookFunctionMustNotExecuteHook(env e, method f, calldataarg args)
    filtered { f-> !VIEW_OR_FALLBACK_FUNCTION(f) } 
{
    setupSilo(e);

    // No hooks to start
    require(!ghostBeforeActionCalled && !ghostAfterActionCalled);

    f(e, args);

    // Hooks must remain disabled
    assert(NO_HOOKS_FUNCTIONS(f) => (
        !ghostBeforeActionCalled && !ghostAfterActionCalled
    ));
}

// Ensures that the share token’s internal hook configuration is consistent
invariant share_hooksShouldBeSynchronized(env e)
    // Silo0 group
    ghostShareTokenHooksBefore[_Collateral0] == ghostShareTokenHooksBefore[_Protected0]
    && ghostShareTokenHooksBefore[_Protected0] == ghostShareTokenHooksBefore[_Debt0]
    // Silo1 group
    && ghostShareTokenHooksBefore[_Collateral1] == ghostShareTokenHooksBefore[_Protected1]
    && ghostShareTokenHooksBefore[_Protected1] == ghostShareTokenHooksBefore[_Debt1]
    // SAFE: Could be executed by Silo only
    filtered { f -> f.selector != 0x4c7b0f3c } // synchronizeHooks(uint24, uint24)
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

////////////////////////////////////////////////// ReentrancyGuard

// Functions function that is intentionally allowed to reenter
definition ALLOWED_REENTER_FUNCTIONS(method f) returns bool = 

    // Do not touch shares
    f.selector == 0xa6afed95 // accrueInterest()
    || f.selector == 0x6e236614 // accrueInterestForConfig()
    || f.selector == 0x5cffe9de // flashLoan()

    // Only owner
    || f.selector == 0x336c8d70 // initialize()

    // Only silo
    || f.selector == 0x4c7b0f3c // synchronizeHooks()
    || f.selector == 0xc6c3bbe6 // mint()
    || f.selector == 0xf6b911bc // burn()

    // Only hook receiver
    || f.selector == 0xd985616c // forwardTransferFromNoChecks()
    
    // Only set user allowances
    || f.selector == 0x80d4336e // decreaseReceiveAllowance()
    || f.selector == 0x75d68016 // increaseReceiveAllowance()
    || f.selector == 0x34deadf2 // setReceiveApproval()
    ;

// No double calls (even reverted) to cross reentrancy protection 
rule share_crossReentrancyProtectionNoDoubleCall(env e, method f, calldataarg args) {

    setupSilo(e);

    require(ghostReentrancyProtectionDoubleCall == false);

    f@withrevert(e, args);

    assert(ghostReentrancyProtectionDoubleCall == false);
}

// Enforces no state-changing calls may occur while already in the ENTERED reentrancy state
rule share_noStateChangingCallInsideReentrancyEntered(env e, method f, calldataarg args)
    filtered { f-> !VIEW_OR_FALLBACK_FUNCTION(f) } 
{
    // Do not setup silo due to `inv_crossReentrancyGuardOpenedOnExit` invariant

    mathint statusBefore = ghostCrossReentrantStatus;

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    // If we are currently ENTERED, then calling a second stateful function is reentrant
    assert(statusBefore == ENTERED() && !ALLOWED_REENTER_FUNCTIONS(f)
        => (
            before[_Silo0] == after[_Silo0]
            && before[_Protected0] == after[_Protected0]
            && before[_Debt0] == after[_Debt0]
            && before[_Silo1] == after[_Silo1]
            && before[_Protected1] == after[_Protected1]
            && before[_Debt1] == after[_Debt1]
        )
    );
}

// Enforces no state-changing calls may occur while already in the ENTERED reentrancy state
rule share_noSharesTransferringInsideReentrancyEntered(env e, method f, calldataarg args)
    filtered { f-> !VIEW_OR_FALLBACK_FUNCTION(f) } 
{
    // Do not setup silo due to `inv_crossReentrancyGuardOpenedOnExit` invariant

    mathint statusBefore = ghostCrossReentrantStatus;

    storage before = lastStorage;

    f(e, args);

    storage after = lastStorage;

    // If we are currently ENTERED, then calling a second stateful function is reentrant
    assert(statusBefore == ENTERED() && !ALLOWED_REENTER_FUNCTIONS(f)
        => (
            before[_Silo0] == after[_Silo0]
            && before[_Protected0] == after[_Protected0]
            && before[_Debt0] == after[_Debt0]
            && before[_Silo1] == after[_Silo1]
            && before[_Protected1] == after[_Protected1]
            && before[_Debt1] == after[_Debt1]
        )
    );
}

// Moving shares is not allowed inside a reentrant call
rule share_noMovingSharesInsideReentrancyEntered(env e, method f, calldataarg args, address sharesUser)
    filtered { f-> !VIEW_OR_FALLBACK_FUNCTION(f) } 
{
    // Do not setup silo due to `inv_crossReentrancyGuardOpenedOnExit` invariant

    mathint statusBefore = ghostCrossReentrantStatus;

    mathint protectedShares0Before = ghostERC20Balances[_Protected0][sharesUser];
    mathint collateralShares0Before = ghostERC20Balances[_Collateral0][sharesUser];
    mathint debtShares0Before = ghostERC20Balances[_Debt0][sharesUser];

    mathint protectedShares1Before = ghostERC20Balances[_Protected1][sharesUser];
    mathint collateralShares1Before = ghostERC20Balances[_Collateral1][sharesUser];
    mathint debtShares1Before = ghostERC20Balances[_Debt1][sharesUser];

    f(e, args);

    mathint protectedShares0After = ghostERC20Balances[_Protected0][sharesUser];
    mathint collateralShares0After = ghostERC20Balances[_Collateral0][sharesUser];
    mathint debtShares0After = ghostERC20Balances[_Debt0][sharesUser];

    mathint protectedShares1After = ghostERC20Balances[_Protected1][sharesUser];
    mathint collateralShares1After = ghostERC20Balances[_Collateral1][sharesUser];
    mathint debtShares1After = ghostERC20Balances[_Debt1][sharesUser];

    // If we are currently ENTERED, then transferring shares is not allowed
    assert(statusBefore == ENTERED() => (
        // Silo0 group
        protectedShares0Before == protectedShares0After
        && collateralShares0Before == collateralShares0After
        && debtShares0Before == debtShares0After
        // Silo1 group
        && protectedShares1Before == protectedShares1After
        && collateralShares1Before == collateralShares1After
        && debtShares1Before == debtShares1After
    ));
}

// Allowed reentrancy function never call to CrossReentrancyGuard
rule share_allowedReenterFunctionDoNotCallCrossReentrancyGuard(env e, method f, calldataarg args)
    filtered { f-> !VIEW_OR_FALLBACK_FUNCTION(f) } 
{
    setupSilo(e);

    require(ghostReentrancyCalled == false);

    f(e, args);
    
    assert(ALLOWED_REENTER_FUNCTIONS(f)
        => (ghostReentrancyCalled == false)
    );
}
