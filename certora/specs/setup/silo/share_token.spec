// Common ShareTokenStorage ghosts for all contracts

methods {

    // External calls to `IShareToken`
    
    function _.synchronizeHooks(uint24 _hooksBefore, uint24 _hooksAfter) external
        => DISPATCHER(true);
    
    function _.mint(address _owner, address _spender, uint256 _amount) external
        => DISPATCHER(true);
        
    function _.burn(address _owner, address _spender, uint256 _amount) external
        => DISPATCHER(true);

    function _.balanceOfAndTotalSupply(address _account) external with (env e)
        => balanceOfAndTotalSupplyCVL(e, calledContract, _account) expect (uint256, uint256);

    // Delete from the scene

    function _.callOnBehalfOfShareToken(address _target, uint256 _value, ISilo.CallType _callType, bytes _input) external
        => NONDET DELETE;
}

//
// Methods summarizes
//

function balanceOfAndTotalSupplyCVL(env e, address contract, address _account) returns (uint256, uint256) {
    return (
        require_uint256(ghostERC20Balances[contract][_account]), 
        require_uint256(ghostERC20TotalSupply[contract])
        );
}

//
// Hooks 
//

definition HOOK_NONE() returns uint256 = 0;
definition HOOK_DEPOSIT() returns uint256 = 2 ^ 1;
definition HOOK_BORROW() returns uint256 = 2 ^ 2;
definition HOOK_BORROW_SAME_ASSET() returns uint256 = 2 ^ 3;
definition HOOK_REPAY() returns uint256 = 2 ^ 4;
definition HOOK_WITHDRAW() returns uint256 = 2 ^ 5;
definition HOOK_FLASH_LOAN() returns uint256 = 2 ^ 6;
definition HOOK_TRANSITION_COLLATERAL() returns uint256 = 2 ^ 7;
definition HOOK_SWITCH_COLLATERAL() returns uint256 = 2 ^ 8;
definition HOOK_LIQUIDATION() returns uint256 = 2 ^ 9;
definition HOOK_SHARE_TOKEN_TRANSFER() returns uint256 = 2 ^ 10;
definition HOOK_COLLATERAL_TOKEN() returns uint256 = 2 ^ 11;
definition HOOK_PROTECTED_TOKEN() returns uint256 = 2 ^ 12;
definition HOOK_DEBT_TOKEN() returns uint256 = 2 ^ 13;

persistent ghost mapping (bytes4 => uint256) ghostSelectorHooks {
    axiom ghostSelectorHooks[to_bytes4(0x481fef8a)] == HOOK_DEPOSIT()  // depositCollateral(uint256,address)
        && ghostSelectorHooks[to_bytes4(0x18168da7)] == HOOK_DEPOSIT() // depositProtected(uint256,address)
        && ghostSelectorHooks[to_bytes4(0x38bcbf86)] == HOOK_DEPOSIT() // mintCollateral(uint256,address)
        && ghostSelectorHooks[to_bytes4(0xda8718f8)] == HOOK_DEPOSIT() // mintProtected(uint256,address)

        && ghostSelectorHooks[to_bytes4(0x72d46ac2)] == HOOK_WITHDRAW() // withdrawCollateral(uint256,address,address)
        && ghostSelectorHooks[to_bytes4(0x52a9cf70)] == HOOK_WITHDRAW() // withdrawProtected(uint256,address,address)
        && ghostSelectorHooks[to_bytes4(0xcd88c072)] == HOOK_WITHDRAW() // redeemCollateral(uint256,address,address)
        && ghostSelectorHooks[to_bytes4(0xf7218880)] == HOOK_WITHDRAW() // redeemProtected(uint256,address,address)

        && ghostSelectorHooks[to_bytes4(0x6e553f65)] == HOOK_DEPOSIT()  // deposit(uint256,address)
        && ghostSelectorHooks[to_bytes4(0x94bf804d)] == HOOK_DEPOSIT()  // mint(uint256,address)
        && ghostSelectorHooks[to_bytes4(0xb460af94)] == HOOK_WITHDRAW() // withdraw(uint256,address,address)
        && ghostSelectorHooks[to_bytes4(0xba087652)] == HOOK_WITHDRAW() // redeem(uint256,address,address)

        && ghostSelectorHooks[to_bytes4(0xd5164184)] == HOOK_BORROW()             // borrow(uint256,address,address)
        && ghostSelectorHooks[to_bytes4(0x889576f7)] == HOOK_BORROW()             // borrowShares(uint256,address,address)
        && ghostSelectorHooks[to_bytes4(0x7fe2c8b7)] == HOOK_BORROW_SAME_ASSET()  // borrowSameAsset(uint256,address,address)
        && ghostSelectorHooks[to_bytes4(0xacb70815)] == HOOK_REPAY()              // repay(uint256,address)
        && ghostSelectorHooks[to_bytes4(0xe36754eb)] == HOOK_REPAY()              // repayShares(uint256,address)

        && ghostSelectorHooks[to_bytes4(0xfa9b1c6a)] == HOOK_TRANSITION_COLLATERAL() // transitionCollateral(uint256,address,uint8)
        && ghostSelectorHooks[to_bytes4(0x4c090ce6)] == HOOK_TRANSITION_COLLATERAL() // transitionCollateralFromCollateral(uint256,address)
        && ghostSelectorHooks[to_bytes4(0xff82f27a)] == HOOK_TRANSITION_COLLATERAL() // transitionCollateralFromProtected(uint256,address)
        && ghostSelectorHooks[to_bytes4(0xa1ecef5c)] == HOOK_SWITCH_COLLATERAL()     // switchCollateralToThisSilo()

        && ghostSelectorHooks[to_bytes4(0x5cffe9de)] == HOOK_FLASH_LOAN() // flashLoan(address,address,uint256,bytes)

        && ghostSelectorHooks[to_bytes4(0xa6afed95)] == HOOK_NONE() // accrueInterest()
        && ghostSelectorHooks[to_bytes4(0x6e236614)] == HOOK_NONE() // accrueInterestForConfig(address,uint256,uint256)
        && ghostSelectorHooks[to_bytes4(0x476343ee)] == HOOK_NONE() // withdrawFees()
        && ghostSelectorHooks[to_bytes4(0xcad1aacf)] == HOOK_NONE() // updateHooks()
        && ghostSelectorHooks[to_bytes4(0x4624c6a7)] == HOOK_NONE() // callOnBehalfOfSilo(address,uint256,uint8,bytes)
        ;
}

//
// Storage ghosts
// 

// Ghost copy of `ShareTokenStorage.hookSetup.hooksBefore`

persistent ghost mapping (address => mathint) ghostShareTokenHooksBefore {
    init_state axiom forall address contract. ghostShareTokenHooksBefore[contract] == 0;
    axiom forall address contract. 
        ghostShareTokenHooksBefore[contract] >= 0 && ghostShareTokenHooksBefore[contract] <= max_uint24;
}

// Ghost copy of `ShareTokenStorage.hookSetup.hooksAfter`

persistent ghost mapping (address => mathint) ghostShareTokenHooksAfter {
    init_state axiom forall address contract. ghostShareTokenHooksAfter[contract] == 0;
    axiom forall address contract. 
        ghostShareTokenHooksAfter[contract] >= 0 && ghostShareTokenHooksAfter[contract] <= max_uint24;
}

// Ghost copy of `ShareTokenStorage.hookSetup.tokenType`

definition COLLATERAL_TOKEN() returns mathint = 2^11;
definition PROTECTED_TOKEN() returns mathint = 2^12;
definition DEBT_TOKEN() returns mathint = 2^13;

// Ghost copy of `ShareTokenStorage.transferWithChecks`

persistent ghost mapping (address => bool) ghostShareTokenTransferWithChecks {
    init_state axiom forall address contract. ghostShareTokenTransferWithChecks[contract] == true;
}

// Ghost copy of `IERC20RStorage._receiveAllowances` for Debt token only

persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostReceiveAllowances {
    init_state axiom forall address contract. forall address owner. forall address recipient. 
        ghostReceiveAllowances[contract][owner][recipient] == 0;
    axiom forall address contract. forall address owner. forall address recipient. 
        ghostReceiveAllowances[contract][owner][recipient] >= 0 
            && ghostReceiveAllowances[contract][owner][recipient] <= max_uint256;
    // Owner and spender cannot be zero
    axiom forall address contract. forall address owner. forall address recipient. owner == 0 || recipient == 0 
        => ghostReceiveAllowances[contract][owner][recipient] == 0;
}