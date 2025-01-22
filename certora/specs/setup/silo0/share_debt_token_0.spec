import "../silo/share_token.spec";
import "../erc20.spec";
import "../env.spec";

using ShareDebtToken0 as _ShareDebtToken0;

//
// ShareTokenStorage
//

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _ShareDebtToken0.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[_ShareDebtToken0]) == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[_ShareDebtToken0] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _ShareDebtToken0.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[_ShareDebtToken0]) == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[_ShareDebtToken0] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _ShareDebtToken0.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(DEBT_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _ShareDebtToken0.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[_ShareDebtToken0] == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[_ShareDebtToken0] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _ShareDebtToken0.erc20Storage._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_ShareDebtToken0, account));
    require(require_uint256(ghostERC20Balances[_ShareDebtToken0][account]) == val);
}

hook Sstore _ShareDebtToken0.erc20Storage._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_ShareDebtToken0, account));
    ghostERC20Balances[_ShareDebtToken0][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _ShareDebtToken0.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_ShareDebtToken0, owner) && ERC20_ACCOUNT_BOUNDS(_ShareDebtToken0, spender));
    require(require_uint256(ghostERC20Allowances[_ShareDebtToken0][owner][spender]) == val);
}

hook Sstore _ShareDebtToken0.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_ShareDebtToken0, owner) && ERC20_ACCOUNT_BOUNDS(_ShareDebtToken0, spender));
    ghostERC20Allowances[_ShareDebtToken0][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _ShareDebtToken0.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_ShareDebtToken0]) == val);
}

hook Sstore _ShareDebtToken0.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[_ShareDebtToken0] = val;
}