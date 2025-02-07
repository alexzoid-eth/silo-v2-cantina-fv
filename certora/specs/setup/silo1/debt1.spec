import "../silo/share_token.spec";

using Debt1 as _Debt1;

//
// ShareTokenStorage
//

// Hooks for addresses viewers

hook Sload address val _Debt1.shareTokenStorage.silo {
    require(_Silo1 == val);
}

hook Sload address val _Debt1.shareTokenStorage.hookSetup.hookReceiver {
    require(ghostHookReceiver == val);
}

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _Debt1.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[_Debt1]) == val);
}

hook Sstore _Debt1.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[_Debt1] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _Debt1.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[_Debt1]) == val);
}

hook Sstore _Debt1.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[_Debt1] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _Debt1.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(DEBT_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _Debt1.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[_Debt1] == val);
}

hook Sstore _Debt1.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[_Debt1] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _Debt1.erc20Storage._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_Debt1, account));
    require(require_uint256(ghostERC20Balances[_Debt1][account]) == val);
}

hook Sstore _Debt1.erc20Storage._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Debt1, account));
    ghostERC20Balances[_Debt1][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _Debt1.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_Debt1, owner) && ERC20_ACCOUNT_BOUNDS(_Debt1, spender));
    require(require_uint256(ghostERC20Allowances[_Debt1][owner][spender]) == val);
}

hook Sstore _Debt1.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Debt1, owner) && ERC20_ACCOUNT_BOUNDS(_Debt1, spender));
    ghostERC20Allowances[_Debt1][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _Debt1.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_Debt1]) == val);
}

hook Sstore _Debt1.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[_Debt1] = val;
}

//
// IERC20R
//

hook Sload uint256 val _Debt1.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] {
    require(require_uint256(ghostReceiveAllowances[_Debt1][owner][recipient]) == val);
}

hook Sstore _Debt1.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] uint256 val {
    ghostReceiveAllowances[_Debt1][owner][recipient] = val;
}
