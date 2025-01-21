import "../silo/share_token.spec";
import "../erc20.spec";
import "../env.spec";

using ShareProtectedCollateralToken0 as _ShareProtectedCollateralToken0;

methods {
    function _ShareProtectedCollateralToken0.totalSupply() external returns (uint256) envfree;
    function _ShareProtectedCollateralToken0.balanceOf(address account) external returns (uint256) envfree;
    function _ShareProtectedCollateralToken0.allowance(address owner, address spender) external returns (uint256) envfree;

    function _ShareProtectedCollateralToken0.name() external returns (string) => NONDET DELETE;
    function _ShareProtectedCollateralToken0.symbol() external returns (string) => NONDET DELETE;
}

//
// Storage hooks
//

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _ShareProtectedCollateralToken0.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[executingContract]) == val);
}

hook Sstore _ShareProtectedCollateralToken0.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[executingContract] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _ShareProtectedCollateralToken0.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[executingContract]) == val);
}

hook Sstore _ShareProtectedCollateralToken0.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[executingContract] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _ShareProtectedCollateralToken0.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(PROTECTED_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _ShareProtectedCollateralToken0.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[executingContract] == val);
}

hook Sstore _ShareProtectedCollateralToken0.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[executingContract] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _ShareProtectedCollateralToken0.erc20Storage._balances[KEY address account] {
    require(require_uint256(ghostERC20Balances[executingContract][account]) == val);
}

hook Sstore _ShareProtectedCollateralToken0.erc20Storage._balances[KEY address account] uint256 val {
    ghostERC20Balances[executingContract][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _ShareProtectedCollateralToken0.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(require_uint256(ghostERC20Allowances[executingContract][owner][spender]) == val);
}

hook Sstore _ShareProtectedCollateralToken0.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    ghostERC20Allowances[executingContract][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _ShareProtectedCollateralToken0.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[executingContract]) == val);
}

hook Sstore _ShareProtectedCollateralToken0.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[executingContract] = val;
}