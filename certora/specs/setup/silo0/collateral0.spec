import "../silo/share_token.spec";

using Silo0 as _Collateral0;

//
// ShareTokenStorage
//

// Hooks for addresses viewers

hook Sload address val _Collateral0.shareTokenStorage.silo {
    require(_Silo0 == val);
}

hook Sload address val _Collateral0.shareTokenStorage.siloConfig {
    require(ghostConfig == val);
}

hook Sload address val _Collateral0.shareTokenStorage.hookSetup.hookReceiver {
    require(ghostHookReceiver == val);
}

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _Collateral0.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[_Collateral0]) == val);
}

hook Sstore _Collateral0.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[_Collateral0] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _Collateral0.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[_Collateral0]) == val);
}

hook Sstore _Collateral0.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[_Collateral0] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _Collateral0.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(COLLATERAL_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _Collateral0.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[_Collateral0] == val);
}

hook Sstore _Collateral0.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[_Collateral0] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _Collateral0.erc20Storage._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_Collateral0, account));
    require(require_uint256(ghostERC20Balances[_Collateral0][account]) == val);
}

hook Sstore _Collateral0.erc20Storage._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Collateral0, account));
    ghostERC20Balances[_Collateral0][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _Collateral0.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_Collateral0, owner) && ERC20_ACCOUNT_BOUNDS(_Collateral0, spender));
    require(require_uint256(ghostERC20Allowances[_Collateral0][owner][spender]) == val);
}

hook Sstore _Collateral0.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Collateral0, owner) && ERC20_ACCOUNT_BOUNDS(_Collateral0, spender));
    ghostERC20Allowances[_Collateral0][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _Collateral0.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_Collateral0]) == val);
}

hook Sstore _Collateral0.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[_Collateral0] = val;
}