using Token1 as _Token1;

// Balances hooks

hook Sload uint256 val _Token1._balances[KEY address account] {
    require(ERC20_ACCOUNT_BOUNDS(_Token1, account));
    require(require_uint256(ghostERC20Balances[_Token1][account]) == val);
}

hook Sstore _Token1._balances[KEY address account] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Token1, account));
    ghostERC20Balances[_Token1][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _Token1._allowances[KEY address owner][KEY address spender] {
    require(ERC20_ACCOUNT_BOUNDS(_Token1, owner) && ERC20_ACCOUNT_BOUNDS(_Token1, spender));
    require(require_uint256(ghostERC20Allowances[_Token1][owner][spender]) == val);
}

hook Sstore _Token1._allowances[KEY address owner][KEY address spender] uint256 val {
    require(ERC20_ACCOUNT_BOUNDS(_Token1, owner) && ERC20_ACCOUNT_BOUNDS(_Token1, spender));
    ghostERC20Allowances[_Token1][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _Token1._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[_Token1]) == val);
}

hook Sstore _Token1._totalSupply uint256 val {
    ghostERC20TotalSupply[_Token1] = val;
}