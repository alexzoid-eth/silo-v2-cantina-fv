// ERC20 ghosts for storage hooks

methods {

    // ERC20/ERC20Upgradeable
    function _.decimals() external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    // Remove from the scene
    function _.name() external => NONDET DELETE;
    function _.symbol() external => NONDET DELETE;
    function _.nonces(address) external => NONDET DELETE;
    function _.permit(address, address, uint256, uint256, uint8, bytes32, bytes32) external => NONDET DELETE;
}

// Assume 10 different accounts

definition MAX_ERC20_USERS() returns mathint = 10;
persistent ghost ghostErc20Accounts(address, mathint) returns address {
    // All accounts in the range are different
    axiom forall address token. forall mathint i. forall mathint j. 
        i >= 0 && i < MAX_ERC20_USERS() && j >= 0 && j < MAX_ERC20_USERS() && i != j
        => ghostErc20Accounts(token, i) != ghostErc20Accounts(token, j);
}

persistent ghost mapping (address => mapping (mathint => address)) ghostErc20AccountsValues {
    // All addresses are different
    axiom forall address token. forall mathint i. 
        ghostErc20AccountsValues[token][i] == ghostErc20Accounts(token, i);
    // All addresses are not zero
    axiom forall address token. forall mathint i. 
        ghostErc20AccountsValues[token][i] != 0;
}

// Return true when address is existence ERC20 account
definition ERC20_ACCOUNT_BOUNDS(address token, address account) returns bool = 
    ghostErc20AccountsValues[token][0] == account
    || ghostErc20AccountsValues[token][1] == account
    || ghostErc20AccountsValues[token][2] == account
    || ghostErc20AccountsValues[token][3] == account
    || ghostErc20AccountsValues[token][4] == account
    || ghostErc20AccountsValues[token][5] == account
    || ghostErc20AccountsValues[token][6] == account
    || ghostErc20AccountsValues[token][7] == account
    || ghostErc20AccountsValues[token][8] == account
    || ghostErc20AccountsValues[token][9] == account
    ;

// Balances ghost
persistent ghost mapping(address => mapping(address => mathint)) ghostERC20Balances {
    init_state axiom forall address token. forall address account. 
        ghostERC20Balances[token][account] == 0;
    axiom forall address token. forall address account. ERC20_ACCOUNT_BOUNDS(token, account)
        ? ghostERC20Balances[token][account] >= 0 && ghostERC20Balances[token][account] <= max_uint128
        : ghostERC20Balances[token][account] == 0;
}

// Allowances ghost  
persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20Allowances {
    init_state axiom forall address token. forall address owner. forall address spender. 
        ghostERC20Allowances[token][owner][spender] == 0;
    axiom forall address token. forall address owner. forall address spender. 
        ERC20_ACCOUNT_BOUNDS(token, owner) || ERC20_ACCOUNT_BOUNDS(token, spender)
        ? ghostERC20Allowances[token][owner][spender] >= 0 && ghostERC20Allowances[token][owner][spender] <= max_uint128
        : ghostERC20Allowances[token][owner][spender] == 0;
}

// Total supply ghost
persistent ghost mapping(address => mathint) ghostERC20TotalSupply {
    init_state axiom forall address token. ghostERC20TotalSupply[token] == 0;
    axiom forall address token. 
        ghostERC20TotalSupply[token] >= 0 && ghostERC20TotalSupply[token] <= max_uint128;
}

invariant erc20TotalSupplySolvency()
    forall address token. ghostERC20TotalSupply[token] 
        == ghostERC20Balances[token][ghostErc20AccountsValues[token][0]] 
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][1]] 
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][2]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][3]] 
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][4]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][5]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][6]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][7]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][8]]
        + ghostERC20Balances[token][ghostErc20AccountsValues[token][9]]
        ;

function requireErc20ValidState() {
    requireInvariant erc20TotalSupplySolvency;
}