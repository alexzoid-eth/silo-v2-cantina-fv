// Common ERC20 ghosts for all contracts

methods {
    function _.decimals() external => PER_CALLEE_CONSTANT;
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    function _.name() external => PER_CALLEE_CONSTANT DELETE;
    function _.symbol() external => PER_CALLEE_CONSTANT DELETE;
}

// Assume 20 different users
definition MAX_ERC20_USERS() returns mathint = 20;
persistent ghost mapping(address => mapping(mathint => address)) ghostErc20Accounts {
    axiom forall address contract. forall mathint i. forall mathint j. 
        i >= 0 && i < MAX_ERC20_USERS() && j >= 0 && j < MAX_ERC20_USERS() && i != j
            => ghostErc20Accounts[contract][i] != ghostErc20Accounts[contract][j];
}

definition ERC20_A_BOUNDS(address contract, address account) returns bool = 
    ghostErc20Accounts[contract][0] == account
    || ghostErc20Accounts[contract][1] == account
    || ghostErc20Accounts[contract][2] == account
    || ghostErc20Accounts[contract][3] == account
    || ghostErc20Accounts[contract][4] == account
    || ghostErc20Accounts[contract][5] == account
    || ghostErc20Accounts[contract][6] == account
    || ghostErc20Accounts[contract][7] == account
    || ghostErc20Accounts[contract][8] == account
    || ghostErc20Accounts[contract][9] == account
    || ghostErc20Accounts[contract][10] == account
    || ghostErc20Accounts[contract][11] == account
    || ghostErc20Accounts[contract][12] == account
    || ghostErc20Accounts[contract][13] == account
    || ghostErc20Accounts[contract][14] == account
    || ghostErc20Accounts[contract][15] == account
    || ghostErc20Accounts[contract][16] == account
    || ghostErc20Accounts[contract][17] == account
    || ghostErc20Accounts[contract][18] == account
    || ghostErc20Accounts[contract][19] == account; 

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
    axiom forall address contract. ghostERC20TotalSupply[contract] >= 0 
        && ghostERC20TotalSupply[contract] <= max_uint128; 
    axiom forall address contract. ghostERC20TotalSupply[contract] 
        == ghostERC20Balances[contract][ghostErc20Accounts[contract][0]] 
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][1]] 
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][2]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][3]] 
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][4]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][5]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][6]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][7]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][8]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][9]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][10]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][11]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][12]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][13]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][14]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][15]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][16]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][17]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][18]]
            + ghostERC20Balances[contract][ghostErc20Accounts[contract][19]]
            ;
}