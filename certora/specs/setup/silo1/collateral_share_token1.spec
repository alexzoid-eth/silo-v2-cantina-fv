import "../silo/share_token.spec";

using Silo1 as _CollateralShareToken1;

//
// ShareTokenStorage
//

// Hooks for addresses viewers

hook Sload address val _CollateralShareToken1.shareTokenStorage.silo {
    require(ghostConfigSilo1 == val);
}

hook Sload address val _CollateralShareToken1.shareTokenStorage.siloConfig {
    require(ghostSiloConfig == val);
}

hook Sload address val _CollateralShareToken1.shareTokenStorage.hookSetup.hookReceiver {
    require(ghostConfigHookReceiver == val);
}

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _CollateralShareToken1.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[_CollateralShareToken1]) == val);
}

hook Sstore _CollateralShareToken1.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[_CollateralShareToken1] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _CollateralShareToken1.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[_CollateralShareToken1]) == val);
}

hook Sstore _CollateralShareToken1.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[_CollateralShareToken1] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _CollateralShareToken1.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(COLLATERAL_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _CollateralShareToken1.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[_CollateralShareToken1] == val);
}

hook Sstore _CollateralShareToken1.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[_CollateralShareToken1] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _CollateralShareToken1.erc20Storage._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken1, account));
    require(require_uint256(ghostERC20Balances[_CollateralShareToken1][account]) == val);
}

hook Sstore _CollateralShareToken1.erc20Storage._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken1, account));
    ghostERC20Balances[_CollateralShareToken1][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _CollateralShareToken1.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken1, owner) && ERC20_ACCOUNT_BOUNDS(_CollateralShareToken1, spender));
    require(require_uint256(ghostERC20Allowances[_CollateralShareToken1][owner][spender]) == val);
}

hook Sstore _CollateralShareToken1.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken1, owner) && ERC20_ACCOUNT_BOUNDS(_CollateralShareToken1, spender));
    ghostERC20Allowances[_CollateralShareToken1][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _CollateralShareToken1.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_CollateralShareToken1]) == val);
}

hook Sstore _CollateralShareToken1.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[_CollateralShareToken1] = val;
}