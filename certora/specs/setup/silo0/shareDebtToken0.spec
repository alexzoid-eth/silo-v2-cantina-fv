import "../shareToken.spec";
import "../erc20.spec";

using ShareDebtToken0 as _ShareDebtToken0;

methods {
    function _ShareDebtToken0.totalSupply() external returns (uint256) envfree;
    function _ShareDebtToken0.balanceOf(address account) external returns (uint256) envfree;
    function _ShareDebtToken0.allowance(address owner, address spender) external returns (uint256) envfree;

    function _ShareDebtToken0.name() external returns (string) => NONDET DELETE;
    function _ShareDebtToken0.symbol() external returns (string) => NONDET DELETE;
}

//
// ShareTokenStorage
//

// Hooks for `ShareTokenStorage.silo`

hook Sload address val _ShareDebtToken0.shareTokenStorage.silo {
    require(ghostShareTokenSilo[executingContract] == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.silo address val {
    ghostShareTokenSilo[executingContract] = val;
}

// Hooks for `ShareTokenStorage.siloConfig`

hook Sload address val _ShareDebtToken0.shareTokenStorage.siloConfig {
    require(ghostShareTokenSiloConfig == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.siloConfig address val {
    ghostShareTokenSiloConfig = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hookReceiver`

hook Sload address val _ShareDebtToken0.shareTokenStorage.hookSetup.hookReceiver {
    require(ghostShareTokenHookReceiver[executingContract] == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.hookSetup.hookReceiver address val {
    ghostShareTokenHookReceiver[executingContract] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksBefore`

hook Sload uint24 val _ShareDebtToken0.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore[executingContract]) == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore[executingContract] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.hooksAfter`

hook Sload uint24 val _ShareDebtToken0.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter[executingContract]) == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter[executingContract] = val;
}

// Hooks for `ShareTokenStorage.hookSetup.tokenType`

hook Sload uint24 val _ShareDebtToken0.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(ghostShareTokenTokenType[executingContract]) == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.hookSetup.tokenType uint24 val {
    ghostShareTokenTokenType[executingContract] = val;
}

// Hooks for `ShareTokenStorage.transferWithChecks`

hook Sload bool val _ShareDebtToken0.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks[executingContract] == val);
}

hook Sstore _ShareDebtToken0.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks[executingContract] = val;
}

//
// ERC20
//

// Balances hooks

hook Sload uint256 val _ShareDebtToken0.erc20Storage._balances[KEY address account] {
    require(require_uint256(ghostERC20Balances[executingContract][account]) == val);
}

hook Sstore _ShareDebtToken0.erc20Storage._balances[KEY address account] uint256 val {
    ghostERC20Balances[executingContract][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _ShareDebtToken0.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(require_uint256(ghostERC20Allowances[executingContract][owner][spender]) == val);
}

hook Sstore _ShareDebtToken0.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    ghostERC20Allowances[executingContract][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _ShareDebtToken0.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[executingContract]) == val);
}

hook Sstore _ShareDebtToken0.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply[executingContract] = val;
}