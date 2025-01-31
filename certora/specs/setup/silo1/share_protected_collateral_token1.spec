import "../silo/share_token.spec";

using Protected1 as _ShareProtectedCollateralToken1;

//
// Storage hooks
//

// Hooks for addresses viewers

hook Sload address val _ShareProtectedCollateralToken1.shareTokenStorage.silo {
    require(ghostConfigSilo0 == val);
}

hook Sload address val _ShareProtectedCollateralToken1.shareTokenStorage.siloConfig {
    require(ghostSiloConfig == val);
}

hook Sload address val _ShareProtectedCollateralToken1.shareTokenStorage.hookSetup.hookReceiver {
    require(ghostConfigHookReceiver == val);
}

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _ShareProtectedCollateralToken1.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[_ShareProtectedCollateralToken1]) == val);
}

hook Sstore _ShareProtectedCollateralToken1.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[_ShareProtectedCollateralToken1] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _ShareProtectedCollateralToken1.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[_ShareProtectedCollateralToken1]) == val);
}

hook Sstore _ShareProtectedCollateralToken1.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[_ShareProtectedCollateralToken1] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _ShareProtectedCollateralToken1.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(PROTECTED_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _ShareProtectedCollateralToken1.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[_ShareProtectedCollateralToken1] == val);
}

hook Sstore _ShareProtectedCollateralToken1.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[_ShareProtectedCollateralToken1] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _ShareProtectedCollateralToken1.erc20Storage._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_ShareProtectedCollateralToken1, account));
    require(require_uint256(ghostERC20Balances[_ShareProtectedCollateralToken1][account]) == val);
}

hook Sstore _ShareProtectedCollateralToken1.erc20Storage._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_ShareProtectedCollateralToken1, account));
    ghostERC20Balances[_ShareProtectedCollateralToken1][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _ShareProtectedCollateralToken1.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_ShareProtectedCollateralToken1, owner) && ERC20_ACCOUNT_BOUNDS(_ShareProtectedCollateralToken1, spender));
    require(require_uint256(ghostERC20Allowances[_ShareProtectedCollateralToken1][owner][spender]) == val);
}

hook Sstore _ShareProtectedCollateralToken1.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_ShareProtectedCollateralToken1, owner) && ERC20_ACCOUNT_BOUNDS(_ShareProtectedCollateralToken1, spender));
    ghostERC20Allowances[_ShareProtectedCollateralToken1][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _ShareProtectedCollateralToken1.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_ShareProtectedCollateralToken1]) == val);
}

hook Sstore _ShareProtectedCollateralToken1.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[_ShareProtectedCollateralToken1] = val;
}