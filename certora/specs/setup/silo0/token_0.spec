import "../erc20.spec";
import "../env.spec";

using Token0 as _Token0;

// Balances hooks

hook Sload uint256 val _Token0._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_Token0, account));
    require(require_uint256(ghostERC20Balances[_Token0][account]) == val);
}

hook Sstore _Token0._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Token0, account));
    ghostERC20Balances[_Token0][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _Token0._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_Token0, owner) && ERC20_ACCOUNT_BOUNDS(_Token0, spender));
    require(require_uint256(ghostERC20Allowances[_Token0][owner][spender]) == val);
}

hook Sstore _Token0._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Token0, owner) && ERC20_ACCOUNT_BOUNDS(_Token0, spender));
    ghostERC20Allowances[_Token0][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _Token0._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_Token0]) == val);
}

hook Sstore _Token0._totalSupply uint256 val {
    ghostERC20TotalSupply[_Token0] = val;
}