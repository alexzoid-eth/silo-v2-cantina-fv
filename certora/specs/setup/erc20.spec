import "./env.spec";

// Assume 5 different users
persistent ghost address ERC20_ACCOUNT_1 {
    axiom ERC20_ACCOUNT_1 != ERC20_ACCOUNT_2 
        && ERC20_ACCOUNT_1 != ERC20_ACCOUNT_3 
        && ERC20_ACCOUNT_1 != ERC20_ACCOUNT_4 
        && ERC20_ACCOUNT_1 != ERC20_ACCOUNT_5;
}
persistent ghost address ERC20_ACCOUNT_2 {
    axiom ERC20_ACCOUNT_2 != ERC20_ACCOUNT_1 
        && ERC20_ACCOUNT_2 != ERC20_ACCOUNT_3 
        && ERC20_ACCOUNT_2 != ERC20_ACCOUNT_4 
        && ERC20_ACCOUNT_2 != ERC20_ACCOUNT_5;
}
persistent ghost address ERC20_ACCOUNT_3 {
    axiom ERC20_ACCOUNT_3 != ERC20_ACCOUNT_1 
        && ERC20_ACCOUNT_3 != ERC20_ACCOUNT_2 
        && ERC20_ACCOUNT_3 != ERC20_ACCOUNT_4 
        && ERC20_ACCOUNT_3 != ERC20_ACCOUNT_5;
}
persistent ghost address ERC20_ACCOUNT_4 {
    axiom ERC20_ACCOUNT_4 != ERC20_ACCOUNT_1 
        && ERC20_ACCOUNT_4 != ERC20_ACCOUNT_2 
        && ERC20_ACCOUNT_4 != ERC20_ACCOUNT_3 
        && ERC20_ACCOUNT_4 != ERC20_ACCOUNT_5;
}
persistent ghost address ERC20_ACCOUNT_5 {
    axiom ERC20_ACCOUNT_5 != ERC20_ACCOUNT_1 
        && ERC20_ACCOUNT_5 != ERC20_ACCOUNT_2 
        && ERC20_ACCOUNT_5 != ERC20_ACCOUNT_3 
        && ERC20_ACCOUNT_5 != ERC20_ACCOUNT_4;
}

definition ERC20_ACCOUNT_BOUNDS(address account) returns bool = 
    account == ERC20_ACCOUNT_1 
    || account == ERC20_ACCOUNT_2 
    || account == ERC20_ACCOUNT_3 
    || account == ERC20_ACCOUNT_4 
    || account == ERC20_ACCOUNT_5;

// Balances hooks
persistent ghost mapping(address => mathint) ghostERC20Balances {
    init_state axiom forall address account. ghostERC20Balances[account] == 0;
    axiom forall address account. ERC20_ACCOUNT_BOUNDS(account)
        ? ghostERC20Balances[account] >= 0 && ghostERC20Balances[account] <= max_uint128
        : ghostERC20Balances[account] == 0;
    // Zero account balance always zero
    axiom ghostERC20Balances[0] == 0;
}

hook Sload uint256 val _Silo.erc20Storage._balances[KEY address account] {
    require(require_uint256(ghostERC20Balances[account]) == val);
}

hook Sstore _Silo.erc20Storage._balances[KEY address account] uint256 val {
    ghostERC20Balances[account] = val;
}

// Allowances hooks  
persistent ghost mapping(address => mapping(address => mathint)) ghostERC20Allowances {
    init_state axiom forall address owner. forall address spender. ghostERC20Allowances[owner][spender] == 0;
    axiom forall address owner. forall address spender. ERC20_ACCOUNT_BOUNDS(owner) && ERC20_ACCOUNT_BOUNDS(spender)
        ? ghostERC20Allowances[owner][spender] >= 0 && ghostERC20Allowances[owner][spender] <= max_uint128
        : ghostERC20Allowances[owner][spender] == 0;
    // Zero account allowance always zero
    axiom forall address spender. ghostERC20Allowances[0][spender] == 0;
    axiom forall address owner. ghostERC20Allowances[owner][0] == 0;
}

hook Sload uint256 val _Silo.erc20Storage._allowances[KEY address owner][KEY address spender] {
    require(require_uint256(ghostERC20Allowances[owner][spender]) == val);
}

hook Sstore _Silo.erc20Storage._allowances[KEY address owner][KEY address spender] uint256 val {
    ghostERC20Allowances[owner][spender] = val;
}

// Total supply hooks
persistent ghost mathint ghostERC20TotalSupply {
    init_state axiom ghostERC20TotalSupply == 0;
    axiom ghostERC20TotalSupply >= 0 && ghostERC20TotalSupply <= max_uint128 && ghostERC20TotalSupply == 
        ghostERC20Balances[ERC20_ACCOUNT_1] 
        + ghostERC20Balances[ERC20_ACCOUNT_2] 
        + ghostERC20Balances[ERC20_ACCOUNT_3]
        + ghostERC20Balances[ERC20_ACCOUNT_4] 
        + ghostERC20Balances[ERC20_ACCOUNT_5];
}

hook Sload uint256 val _Silo.erc20Storage._totalSupply {
    require(require_uint256(ghostERC20TotalSupply) == val);
}

hook Sstore _Silo.erc20Storage._totalSupply uint256 val {
    ghostERC20TotalSupply = val;
}