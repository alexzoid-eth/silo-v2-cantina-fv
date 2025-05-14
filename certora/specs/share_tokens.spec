// Common rules for Protected, Collateral and Debt share tokens

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./setup/silo/silo_valid_state.spec";
import "./setup/silo/hard_methods.spec";

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

definition TRANSFER_ALL_FUNCTIONS(method f) returns bool = 
    TRANSFER_FUNCTIONS(f)
    || f.selector == 0xd985616c // forwardTransferFromNoChecks()
    ;

// Check valid action ids inside hooks
rule share_functionExecutesHooksBasedOnConfig(env e, method f, calldataarg args) 
    filtered { f-> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) } {
        
    setupSilo(e);

    require(ghostHookActionAllowAll == true);
    require(ghostBeforeActionId == 0 && ghostAfterActionId == 0);

    f(e, args);

    // Correct id inside match function and hook call 
    assert(!NO_HOOKS_FUNCTIONS(f) 
        // UNSAFE: TODO - add a support of transfer functions in `ghostSelectorHooks[]`
        && !TRANSFER_ALL_FUNCTIONS(f) 
        => (
        ghostExpectedHook == ghostSelectorHooks[to_bytes4(f.selector)]
        && ghostBeforeActionId == ghostExpectedHook
        && ghostAfterActionId == ghostBeforeActionId
    ));
}

// No Hook Function Must Not Execute Hook
//  Any function in NO_HOOKS_FUNCTIONS must not call hooks at all.
rule share_noHookFunctionMustNotExecuteHook(env e, method f, calldataarg args)
    filtered { f-> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) } {

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
    filtered { f -> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f)
        // SAFE: Could be executed by Silo only
        && f.selector != 0x4c7b0f3c // synchronizeHooks(uint24, uint24)
        } 
{ preserved with (env eInv) { requireSameEnv(e, eInv); setupSilo(e); } }

////////////////////////////////////////////////// ReentrancyGuard

// Functions function that is intentionally allowed to reenter
definition ALLOWED_REENTER_FUNCTIONS(method f) returns bool = 

    // Do not touch shares
    f.selector == 0xa6afed95    // accrueInterest()
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
rule share_crossReentrancyProtectionNoDoubleCall(env e, method f, calldataarg args) 
    filtered { f-> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) } {

    setupSilo(e);

    require(ghostReentrancyProtectionDoubleCall == false);

    f@withrevert(e, args);

    assert(ghostReentrancyProtectionDoubleCall == false);
}

// Enforces no state-changing calls may occur while already in the ENTERED reentrancy state
rule share_noStateChangingCallInsideReentrancyEntered(env e, method f, calldataarg args)
    filtered { f-> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) } {

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
    filtered { f-> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) 
        // SAFE: Only silo
        && f.selector != 0xc6c3bbe6 // mint()
        && f.selector != 0xf6b911bc // burn()
        // SAFE: Only hook receiver
        && f.selector != 0xd985616c // forwardTransferFromNoChecks()
    } {

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

    // Transferring shares requires reentrancy involving
    assert((
        // Silo0 group
        protectedShares0Before != protectedShares0After
        || collateralShares0Before != collateralShares0After
        || debtShares0Before != debtShares0After
        // Silo1 group
        || protectedShares1Before != protectedShares1After
        || collateralShares1Before != collateralShares1After
        || debtShares1Before != debtShares1After
        ) 
        => ghostReentrancyCalled
    );
}

// Allowed reentrancy function never call to CrossReentrancyGuard
rule share_allowedReenterFunctionDoNotCallCrossReentrancyGuard(env e, method f, calldataarg args)
    filtered { f-> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) } {

    setupSilo(e);

    require(ghostReentrancyCalled == false);

    f(e, args);
    
    assert(ALLOWED_REENTER_FUNCTIONS(f)
        => (ghostReentrancyCalled == false)
    );
}

////////////////////////////////////////////////// Interest

// Any change in share balances or total supply must have interest up-to-date (same block)
rule share_groupShareChangeRequireGroupTimestamp(env e, method f, calldataarg args, address user) 
    filtered {
    // SAFE: Can be executed by Silo only
    f -> f.selector != 0xc6c3bbe6   // ShareDebtToken.mint()
    && f.selector != 0xf6b911bc     // ShareDebtToken.burn()
    // SAFE: Can be executed by HookReceiver only
    && f.selector != 0xd985616c     // ShareDebtToken.forwardTransferFromNoChecks()
    && !EXCLUDED_OR_VIEW_SILO_FUNCTION(f)
    // UNSOUND: we can transfer collateral shares which are not used as a collateral
    && f.selector != 0xa9059cbb // transfer()
    && f.selector != 0x23b872dd // transferFrom()
    } {
    
    setupSilo(e);

    // --- Group0: (Debt0, Collateral0, Protected0) ---

    // Record Group0 share balances for `user` before
    mathint debt0BalBefore = ghostERC20Balances[_Debt0][user];
    mathint coll0BalBefore = ghostERC20Balances[_Collateral0][user];
    mathint prot0BalBefore = ghostERC20Balances[_Protected0][user];

    // Record total supply for Group0 share tokens before
    mathint debt0SupplyBefore = ghostERC20TotalSupply[_Debt0];
    mathint coll0SupplyBefore = ghostERC20TotalSupply[_Collateral0];
    mathint prot0SupplyBefore = ghostERC20TotalSupply[_Protected0];

    // --- Group1: (Debt1, Collateral1, Protected1) ---

    // Record Group1 share balances for `user` before
    mathint debt1BalBefore = ghostERC20Balances[_Debt1][user];
    mathint coll1BalBefore = ghostERC20Balances[_Collateral1][user];
    mathint prot1BalBefore = ghostERC20Balances[_Protected1][user];

    // Record total supply for Group1 share tokens before
    mathint debt1SupplyBefore = ghostERC20TotalSupply[_Debt1];
    mathint coll1SupplyBefore = ghostERC20TotalSupply[_Collateral1];
    mathint prot1SupplyBefore = ghostERC20TotalSupply[_Protected1];

    f(e, args);

    // After
    mathint debt0BalAfter = ghostERC20Balances[_Debt0][user];
    mathint coll0BalAfter = ghostERC20Balances[_Collateral0][user];
    mathint prot0BalAfter = ghostERC20Balances[_Protected0][user];
    mathint debt0SupplyAfter = ghostERC20TotalSupply[_Debt0];
    mathint coll0SupplyAfter = ghostERC20TotalSupply[_Collateral0];
    mathint prot0SupplyAfter = ghostERC20TotalSupply[_Protected0];
    mathint silo0InterestAfter = ghostInterestRateTimestamp[_Silo0];

    mathint debt1BalAfter = ghostERC20Balances[_Debt1][user];
    mathint coll1BalAfter = ghostERC20Balances[_Collateral1][user];
    mathint prot1BalAfter = ghostERC20Balances[_Protected1][user];
    mathint debt1SupplyAfter = ghostERC20TotalSupply[_Debt1];
    mathint coll1SupplyAfter = ghostERC20TotalSupply[_Collateral1];
    mathint prot1SupplyAfter = ghostERC20TotalSupply[_Protected1];
    mathint silo1InterestAfter = ghostInterestRateTimestamp[_Silo1];

    bool changedGroup0 = (
        debt0BalBefore != debt0BalAfter
     || coll0BalBefore != coll0BalAfter
     || prot0BalBefore != prot0BalAfter
     || debt0SupplyBefore != debt0SupplyAfter
     || coll0SupplyBefore != coll0SupplyAfter
     || prot0SupplyBefore != prot0SupplyAfter
    );

    bool changedGroup1 = (
        debt1BalBefore != debt1BalAfter
     || coll1BalBefore != coll1BalAfter
     || prot1BalBefore != prot1BalAfter
     || debt1SupplyBefore != debt1SupplyAfter
     || coll1SupplyBefore != coll1SupplyAfter
     || prot1SupplyBefore != prot1SupplyAfter
    );

    // If shares for groups changed, silo’s interest must have updated
    assert(changedGroup0 => silo0InterestAfter == e.block.timestamp);
    assert(changedGroup1 => silo1InterestAfter == e.block.timestamp);
}

// Block timestamp never goes backwards
rule share_InterestTimestampAlwaysGrow(env e, method f, calldataarg args)
    filtered { f -> !EXCLUDED_OR_VIEW_SILO_FUNCTION(f) } {

    setupSilo(e);

    mathint silo0InterestBefore = ghostInterestRateTimestamp[_Silo0];
    mathint silo1InterestBefore = ghostInterestRateTimestamp[_Silo1];

    f(e, args);

    mathint silo0InterestAfter = ghostInterestRateTimestamp[_Silo0];
    mathint silo1InterestAfter = ghostInterestRateTimestamp[_Silo1];

    assert(silo0InterestAfter >= silo0InterestBefore);
    assert(silo1InterestAfter >= silo1InterestBefore);
}
