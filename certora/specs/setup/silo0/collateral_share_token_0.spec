import "../silo/share_token.spec";

using Silo0 as _CollateralShareToken0;

//
// ShareTokenStorage
//

// Hooks for addresses viewers

hook Sload address val _CollateralShareToken0.shareTokenStorage.silo {
    require(ghostConfigSilo0 == val);
}

hook Sload address val _CollateralShareToken0.shareTokenStorage.siloConfig {
    require(_SiloConfig == val);
}

hook Sload address val _CollateralShareToken0.shareTokenStorage.hookSetup.hookReceiver {
    require(ghostConfigHookReceiver == val);
}

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _CollateralShareToken0.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[_CollateralShareToken0]) == val);
}

hook Sstore _CollateralShareToken0.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[_CollateralShareToken0] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _CollateralShareToken0.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[_CollateralShareToken0]) == val);
}

hook Sstore _CollateralShareToken0.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[_CollateralShareToken0] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _CollateralShareToken0.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(COLLATERAL_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _CollateralShareToken0.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[_CollateralShareToken0] == val);
}

hook Sstore _CollateralShareToken0.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[_CollateralShareToken0] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _CollateralShareToken0.erc20Storage._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken0, account));
    require(require_uint256(ghostERC20Balances[_CollateralShareToken0][account]) == val);
}

hook Sstore _CollateralShareToken0.erc20Storage._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken0, account));
    ghostERC20Balances[_CollateralShareToken0][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _CollateralShareToken0.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken0, owner) && ERC20_ACCOUNT_BOUNDS(_CollateralShareToken0, spender));
    require(require_uint256(ghostERC20Allowances[_CollateralShareToken0][owner][spender]) == val);
}

hook Sstore _CollateralShareToken0.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_CollateralShareToken0, owner) && ERC20_ACCOUNT_BOUNDS(_CollateralShareToken0, spender));
    ghostERC20Allowances[_CollateralShareToken0][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _CollateralShareToken0.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_CollateralShareToken0]) == val);
}

hook Sstore _CollateralShareToken0.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[_CollateralShareToken0] = val;
}