// Common ShareTokenStorage ghosts for all contracts

methods {

    // External call to `IShareToken`
    
    function _.synchronizeHooks(uint24 _hooksBefore, uint24 _hooksAfter) external with (env e)
        => synchronizeHooksCVL(e, calledContract, _hooksBefore, _hooksAfter) expect void;

    function _.balanceOfAndTotalSupply(address _account) external with (env e)
        => balanceOfAndTotalSupplyCVL(e, calledContract, _account) expect (uint256, uint256);
    
    function _.mint(address _owner, address _spender, uint256 _amount) external with (env e)
        => mintCVL(e, calledContract, _owner, _spender, _amount) expect void;

    function _.burn(address _owner, address _spender, uint256 _amount) external with (env e)
        => burnCVL(e, calledContract, _owner, _spender, _amount) expect void;
}

//
// Methods summarize
//

function mintCVL(env e, address contract, address _owner, address _spender, uint256 _amount) {
    contract.mint(e, _owner, _spender, _amount);
}

function burnCVL(env e, address contract, address _owner, address _spender, uint256 _amount) {
    contract.burn(e, _owner, _spender, _amount);
}

// Ghost copy of `ShareTokenStorage.silo`

persistent ghost mapping (address => address) ghostShareTokenSilo;

// Ghost copy of `ShareTokenStorage.siloConfig`

persistent ghost address ghostShareTokenSiloConfig;

// Ghost copy of `ShareTokenStorage.hookSetup.hookReceiver`

persistent ghost address ghostShareTokenHookReceiver;

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

persistent ghost mapping (address => mathint) ghostShareTokenTokenType {
    axiom forall address contract. 
        ghostShareTokenTokenType[contract] >= 0 && ghostShareTokenTokenType[contract] <= max_uint24;
}

// Ghost copy of `ShareTokenStorage.transferWithChecks`

persistent ghost mapping (address => bool) ghostShareTokenTransferWithChecks {
    init_state axiom forall address contract. ghostShareTokenTransferWithChecks[contract] == false;
}