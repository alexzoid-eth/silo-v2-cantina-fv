import "../silo/share_token.spec";
import "../erc20.spec";
import "../env.spec";

using Silo1 as _CollateralShareToken1;

methods {
    function _CollateralShareToken1.totalSupply() external returns (uint256) envfree;
    function _CollateralShareToken1.balanceOf(address account) external returns (uint256) envfree;
    function _CollateralShareToken1.allowance(address owner, address spender) external returns (uint256) envfree;

    function _CollateralShareToken1.name() external returns (string) => NONDET DELETE;
    function _CollateralShareToken1.symbol() external returns (string) => NONDET DELETE;
}

//
// ShareTokenStorage
//

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _CollateralShareToken1.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[executingContract]) == val);
}

hook Sstore _CollateralShareToken1.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[executingContract] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _CollateralShareToken1.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[executingContract]) == val);
}

hook Sstore _CollateralShareToken1.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[executingContract] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _CollateralShareToken1.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(COLLATERAL_TOKEN()) == val);
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _CollateralShareToken1.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[executingContract] == val);
}

hook Sstore _CollateralShareToken1.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[executingContract] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _CollateralShareToken1.erc20Storage._balances[KEY address account] {
    require(require_uint256(ghostERC20Balances[executingContract][account]) == val);
}

hook Sstore _CollateralShareToken1.erc20Storage._balances[KEY address account] uint256 val {
    ghostERC20Balances[executingContract][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _CollateralShareToken1.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(require_uint256(ghostERC20Allowances[executingContract][owner][spender]) == val);
}

hook Sstore _CollateralShareToken1.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    ghostERC20Allowances[executingContract][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _CollateralShareToken1.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[executingContract]) == val);
}

hook Sstore _CollateralShareToken1.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[executingContract] = val;
}