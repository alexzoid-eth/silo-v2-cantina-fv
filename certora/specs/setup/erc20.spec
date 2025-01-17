// Common ERC20 ghosts for all contracts

// Assume 5 different users
persistent ghost mapping(address => address) ERC20_ACCOUNT_1 {
    axiom forall address contract. 
        ERC20_ACCOUNT_1[contract] != ERC20_ACCOUNT_2[contract] 
        && ERC20_ACCOUNT_1[contract] != ERC20_ACCOUNT_3[contract] 
        && ERC20_ACCOUNT_1[contract] != ERC20_ACCOUNT_4[contract] 
        && ERC20_ACCOUNT_1[contract] != ERC20_ACCOUNT_5[contract];
}
persistent ghost mapping(address => address) ERC20_ACCOUNT_2 {
    axiom forall address contract.
        ERC20_ACCOUNT_2[contract] != ERC20_ACCOUNT_1[contract] 
        && ERC20_ACCOUNT_2[contract] != ERC20_ACCOUNT_3[contract] 
        && ERC20_ACCOUNT_2[contract] != ERC20_ACCOUNT_4[contract] 
        && ERC20_ACCOUNT_2[contract] != ERC20_ACCOUNT_5[contract];
}
persistent ghost mapping(address => address) ERC20_ACCOUNT_3 {
    axiom forall address contract.
        ERC20_ACCOUNT_3[contract] != ERC20_ACCOUNT_1[contract] 
        && ERC20_ACCOUNT_3[contract] != ERC20_ACCOUNT_2[contract] 
        && ERC20_ACCOUNT_3[contract] != ERC20_ACCOUNT_4[contract] 
        && ERC20_ACCOUNT_3[contract] != ERC20_ACCOUNT_5[contract];
}
persistent ghost mapping(address => address) ERC20_ACCOUNT_4 {
    axiom forall address contract.
        ERC20_ACCOUNT_4[contract] != ERC20_ACCOUNT_1[contract] 
        && ERC20_ACCOUNT_4[contract] != ERC20_ACCOUNT_2[contract] 
        && ERC20_ACCOUNT_4[contract] != ERC20_ACCOUNT_3[contract] 
        && ERC20_ACCOUNT_4[contract] != ERC20_ACCOUNT_5[contract];
}
persistent ghost mapping(address => address) ERC20_ACCOUNT_5 {
    axiom forall address contract.
        ERC20_ACCOUNT_5[contract] != ERC20_ACCOUNT_1[contract] 
        && ERC20_ACCOUNT_5[contract] != ERC20_ACCOUNT_2[contract] 
        && ERC20_ACCOUNT_5[contract] != ERC20_ACCOUNT_3[contract] 
        && ERC20_ACCOUNT_5[contract] != ERC20_ACCOUNT_4[contract];
}

definition ERC20_ACCOUNT_BOUNDS(address contract, address account) returns bool = 
    account == ERC20_ACCOUNT_1[contract] 
    || account == ERC20_ACCOUNT_2[contract] 
    || account == ERC20_ACCOUNT_3[contract] 
    || account == ERC20_ACCOUNT_4[contract] 
    || account == ERC20_ACCOUNT_5[contract];

// Balances ghost
persistent ghost mapping(address => mapping(address => mathint)) ghostERC20Balances {
    init_state axiom forall address contract. forall address account. 
        ghostERC20Balances[contract][account] == 0;
    axiom forall address contract. forall address account. ERC20_ACCOUNT_BOUNDS(contract, account)
        ? ghostERC20Balances[contract][account] >= 0 && ghostERC20Balances[contract][account] <= max_uint128
        : ghostERC20Balances[contract][account] == 0;
}

// Allowances ghost  
persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20Allowances {
    init_state axiom forall address contract. forall address owner. forall address spender. 
        ghostERC20Allowances[contract][owner][spender] == 0;
    axiom forall address contract. forall address owner. forall address spender. 
        ERC20_ACCOUNT_BOUNDS(contract, owner) && ERC20_ACCOUNT_BOUNDS(contract, spender)
        ? ghostERC20Allowances[contract][owner][spender] >= 0 
            && ghostERC20Allowances[contract][owner][spender] <= max_uint128
        : ghostERC20Allowances[contract][owner][spender] == 0;
}

// Total supply ghost
persistent ghost mapping(address => mathint) ghostERC20TotalSupply {
    init_state axiom forall address contract. ghostERC20TotalSupply[contract] == 0;
    axiom forall address contract. ghostERC20TotalSupply[contract] >= 0 && ghostERC20TotalSupply[contract] <= max_uint128 
        && ghostERC20TotalSupply[contract] == ghostERC20Balances[contract][ERC20_ACCOUNT_1[contract]] 
            + ghostERC20Balances[contract][ERC20_ACCOUNT_2[contract]] 
            + ghostERC20Balances[contract][ERC20_ACCOUNT_3[contract]]
            + ghostERC20Balances[contract][ERC20_ACCOUNT_4[contract]] 
            + ghostERC20Balances[contract][ERC20_ACCOUNT_5[contract]];
}