// Common ERC20 ghosts for all contracts

// Assume 10 different users
persistent ghost mapping(address => address) ERC20_A_1 {
    axiom forall address contract. 
        ERC20_A_1[contract] != ERC20_A_2[contract] 
        && ERC20_A_1[contract] != ERC20_A_3[contract] 
        && ERC20_A_1[contract] != ERC20_A_4[contract] 
        && ERC20_A_1[contract] != ERC20_A_5[contract]
        && ERC20_A_1[contract] != ERC20_A_6[contract]
        && ERC20_A_1[contract] != ERC20_A_7[contract]
        && ERC20_A_1[contract] != ERC20_A_8[contract]
        && ERC20_A_1[contract] != ERC20_A_9[contract]
        && ERC20_A_1[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_2 {
    axiom forall address contract. 
        ERC20_A_2[contract] != ERC20_A_1[contract] 
        && ERC20_A_2[contract] != ERC20_A_3[contract] 
        && ERC20_A_2[contract] != ERC20_A_4[contract] 
        && ERC20_A_2[contract] != ERC20_A_5[contract]
        && ERC20_A_2[contract] != ERC20_A_6[contract]
        && ERC20_A_2[contract] != ERC20_A_7[contract]
        && ERC20_A_2[contract] != ERC20_A_8[contract]
        && ERC20_A_2[contract] != ERC20_A_9[contract]
        && ERC20_A_2[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_3 {
    axiom forall address contract. 
        ERC20_A_3[contract] != ERC20_A_1[contract] 
        && ERC20_A_3[contract] != ERC20_A_2[contract] 
        && ERC20_A_3[contract] != ERC20_A_4[contract] 
        && ERC20_A_3[contract] != ERC20_A_5[contract]
        && ERC20_A_3[contract] != ERC20_A_6[contract]
        && ERC20_A_3[contract] != ERC20_A_7[contract]
        && ERC20_A_3[contract] != ERC20_A_8[contract]
        && ERC20_A_3[contract] != ERC20_A_9[contract]
        && ERC20_A_3[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_4 {
    axiom forall address contract. 
        ERC20_A_4[contract] != ERC20_A_1[contract] 
        && ERC20_A_4[contract] != ERC20_A_2[contract] 
        && ERC20_A_4[contract] != ERC20_A_3[contract] 
        && ERC20_A_4[contract] != ERC20_A_5[contract]
        && ERC20_A_4[contract] != ERC20_A_6[contract]
        && ERC20_A_4[contract] != ERC20_A_7[contract]
        && ERC20_A_4[contract] != ERC20_A_8[contract]
        && ERC20_A_4[contract] != ERC20_A_9[contract]
        && ERC20_A_4[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_5 {
    axiom forall address contract. 
        ERC20_A_5[contract] != ERC20_A_1[contract] 
        && ERC20_A_5[contract] != ERC20_A_2[contract] 
        && ERC20_A_5[contract] != ERC20_A_3[contract] 
        && ERC20_A_5[contract] != ERC20_A_4[contract]
        && ERC20_A_5[contract] != ERC20_A_6[contract]
        && ERC20_A_5[contract] != ERC20_A_7[contract]
        && ERC20_A_5[contract] != ERC20_A_8[contract]
        && ERC20_A_5[contract] != ERC20_A_9[contract]
        && ERC20_A_5[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_6 {
    axiom forall address contract. 
        ERC20_A_6[contract] != ERC20_A_1[contract] 
        && ERC20_A_6[contract] != ERC20_A_2[contract] 
        && ERC20_A_6[contract] != ERC20_A_3[contract] 
        && ERC20_A_6[contract] != ERC20_A_4[contract]
        && ERC20_A_6[contract] != ERC20_A_5[contract]
        && ERC20_A_6[contract] != ERC20_A_7[contract]
        && ERC20_A_6[contract] != ERC20_A_8[contract]
        && ERC20_A_6[contract] != ERC20_A_9[contract]
        && ERC20_A_6[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_7 {
    axiom forall address contract. 
        ERC20_A_7[contract] != ERC20_A_1[contract] 
        && ERC20_A_7[contract] != ERC20_A_2[contract] 
        && ERC20_A_7[contract] != ERC20_A_3[contract] 
        && ERC20_A_7[contract] != ERC20_A_4[contract]
        && ERC20_A_7[contract] != ERC20_A_5[contract]
        && ERC20_A_7[contract] != ERC20_A_6[contract]
        && ERC20_A_7[contract] != ERC20_A_8[contract]
        && ERC20_A_7[contract] != ERC20_A_9[contract]
        && ERC20_A_7[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_8 {
    axiom forall address contract. 
        ERC20_A_8[contract] != ERC20_A_1[contract] 
        && ERC20_A_8[contract] != ERC20_A_2[contract] 
        && ERC20_A_8[contract] != ERC20_A_3[contract] 
        && ERC20_A_8[contract] != ERC20_A_4[contract]
        && ERC20_A_8[contract] != ERC20_A_5[contract]
        && ERC20_A_8[contract] != ERC20_A_6[contract]
        && ERC20_A_8[contract] != ERC20_A_7[contract]
        && ERC20_A_8[contract] != ERC20_A_9[contract]
        && ERC20_A_8[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_9 {
    axiom forall address contract. 
        ERC20_A_9[contract] != ERC20_A_1[contract] 
        && ERC20_A_9[contract] != ERC20_A_2[contract] 
        && ERC20_A_9[contract] != ERC20_A_3[contract] 
        && ERC20_A_9[contract] != ERC20_A_4[contract]
        && ERC20_A_9[contract] != ERC20_A_5[contract]
        && ERC20_A_9[contract] != ERC20_A_6[contract]
        && ERC20_A_9[contract] != ERC20_A_7[contract]
        && ERC20_A_9[contract] != ERC20_A_8[contract]
        && ERC20_A_9[contract] != ERC20_A_10[contract];
}
persistent ghost mapping(address => address) ERC20_A_10 {
    axiom forall address contract. 
        ERC20_A_10[contract] != ERC20_A_1[contract] 
        && ERC20_A_10[contract] != ERC20_A_2[contract] 
        && ERC20_A_10[contract] != ERC20_A_3[contract] 
        && ERC20_A_10[contract] != ERC20_A_4[contract]
        && ERC20_A_10[contract] != ERC20_A_5[contract]
        && ERC20_A_10[contract] != ERC20_A_6[contract]
        && ERC20_A_10[contract] != ERC20_A_7[contract]
        && ERC20_A_10[contract] != ERC20_A_8[contract]
        && ERC20_A_10[contract] != ERC20_A_9[contract];
}

definition ERC20_A_BOUNDS(address contract, address account) returns bool = 
    account == ERC20_A_1[contract] 
    || account == ERC20_A_2[contract] 
    || account == ERC20_A_3[contract] 
    || account == ERC20_A_4[contract] 
    || account == ERC20_A_5[contract] 
    || account == ERC20_A_6[contract] 
    || account == ERC20_A_7[contract] 
    || account == ERC20_A_8[contract] 
    || account == ERC20_A_9[contract] 
    || account == ERC20_A_10[contract];
    
// Balances ghost
persistent ghost mapping(address => mapping(address => mathint)) ghostERC20Balances {
    init_state axiom forall address contract. forall address account. 
        ghostERC20Balances[contract][account] == 0;
    axiom forall address contract. forall address account. ERC20_A_BOUNDS(contract, account)
        ? ghostERC20Balances[contract][account] >= 0 && ghostERC20Balances[contract][account] <= max_uint128
        : ghostERC20Balances[contract][account] == 0;
}

// Allowances ghost  
persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20Allowances {
    init_state axiom forall address contract. forall address owner. forall address spender. 
        ghostERC20Allowances[contract][owner][spender] == 0;
    axiom forall address contract. forall address owner. forall address spender. 
        ERC20_A_BOUNDS(contract, owner) && ERC20_A_BOUNDS(contract, spender)
        ? ghostERC20Allowances[contract][owner][spender] >= 0 
            && ghostERC20Allowances[contract][owner][spender] <= max_uint128
        : ghostERC20Allowances[contract][owner][spender] == 0;
}

// Total supply ghost
persistent ghost mapping(address => mathint) ghostERC20TotalSupply {
    init_state axiom forall address contract. ghostERC20TotalSupply[contract] == 0;
    axiom forall address contract. ghostERC20TotalSupply[contract] >= 0 && ghostERC20TotalSupply[contract] <= max_uint128 
        && ghostERC20TotalSupply[contract] == ghostERC20Balances[contract][ERC20_A_1[contract]] 
            + ghostERC20Balances[contract][ERC20_A_2[contract]] 
            + ghostERC20Balances[contract][ERC20_A_3[contract]]
            + ghostERC20Balances[contract][ERC20_A_4[contract]] 
            + ghostERC20Balances[contract][ERC20_A_5[contract]];
}