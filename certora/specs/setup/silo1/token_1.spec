import "../erc20.spec";
import "../env.spec";

using Token1 as _Token1;

// Balances hooks

hook Sload uint256 val _Token1._balances[KEY address account] {
    require(require_uint256(ghostERC20Balances[executingContract][account]) == val);
}

hook Sstore _Token1._balances[KEY address account] uint256 val {
    ghostERC20Balances[executingContract][account] = val;
}

// Allowances hooks  

hook Sload uint256 val _Token1._allowances[KEY address owner][KEY address spender] {
    require(require_uint256(ghostERC20Allowances[executingContract][owner][spender]) == val);
}

hook Sstore _Token1._allowances[KEY address owner][KEY address spender] uint256 val {
    ghostERC20Allowances[executingContract][owner][spender] = val;
}

// Total supply hooks

hook Sload uint256 val _Token1._totalSupply {
    require(require_uint256(ghostERC20TotalSupply[executingContract]) == val);
}

hook Sstore _Token1._totalSupply uint256 val {
    ghostERC20TotalSupply[executingContract] = val;
}