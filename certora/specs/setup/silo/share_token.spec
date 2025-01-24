// Common ShareTokenStorage ghosts for all contracts

methods {

    // External calls to `IShareToken`
    
    function _.synchronizeHooks(uint24 _hooksBefore, uint24 _hooksAfter) external
        => DISPATCHER(true);
    
    function _.mint(address _owner, address _spender, uint256 _amount) external
        => DISPATCHER(true);
        
    function _.burn(address _owner, address _spender, uint256 _amount) external
        => DISPATCHER(true);

    function _.forwardTransferFromNoChecks(address _from, address _to, uint256 _amount) external
        => DISPATCHER(true);

    function _.balanceOfAndTotalSupply(address _account) external with (env e)
        => balanceOfAndTotalSupplyCVL(e, calledContract, _account) expect (uint256, uint256);
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

// Ghost copy of `IERC20RStorage._receiveAllowances`

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