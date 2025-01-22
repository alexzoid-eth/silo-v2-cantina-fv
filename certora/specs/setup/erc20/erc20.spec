// ERC20 ghosts for storage hooks

methods {
    // Remove from the scene
    function _.name() external => NONDET DELETE;
    function _.symbol() external => NONDET DELETE;
    function _.nonces(address) external => NONDET DELETE;
    function _.permit(address, address, uint256, uint256, uint8, bytes32, bytes32) external => NONDET DELETE;
}

// Assume 10 different non-zero accounts
definition MAX_ERC20_USERS() returns mathint = 10;
persistent ghost ghostErc20Accounts(address, mathint) returns address {
    // All accounts in the range are different
    axiom forall address token. forall mathint i. forall mathint j. 
        i >= 0 && i < MAX_ERC20_USERS() && j >= 0 && j < MAX_ERC20_USERS() && i != j
        => ghostErc20Accounts(token, i) != ghostErc20Accounts(token, j);
    // Set out of range accounts as zero
    axiom forall address token. forall mathint i. i >= 0 && i < MAX_ERC20_USERS()
        ? ghostErc20Accounts(token, i) != 0
        : ghostErc20Accounts(token, i) == 0;
}

persistent ghost ghostErc20AccountsValues(address, address) returns bool {
    // Assume true when address is nonzero in ghostErc20Accounts()
    axiom forall address token. forall mathint i.
        ghostErc20AccountsValues(token, ghostErc20Accounts(token, i)) 
            == (ghostErc20Accounts(token, i) != 0);
}

// Return true when address is supported ERC20 account
definition ERC20_ACCOUNT_BOUNDS(address token, address account) returns bool = 
    ghostErc20AccountsValues(token, account);

// Balances ghost
persistent ghost mapping(address => mapping(address => mathint)) ghostERC20Balances {
    init_state axiom forall address token. forall address account. 
        ghostERC20Balances[token][account] == 0;
    axiom forall address token. forall address account. 
        ghostERC20Balances[token][account] >= 0 && ghostERC20Balances[token][account] <= max_uint128;
}

// Allowances ghost  
persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20Allowances {
    init_state axiom forall address token. forall address owner. forall address spender. 
        ghostERC20Allowances[token][owner][spender] == 0;
    axiom forall address token. forall address owner. forall address spender. 
        ghostERC20Allowances[token][owner][spender] >= 0 && ghostERC20Allowances[token][owner][spender] <= max_uint128;
}

// Total supply ghost
persistent ghost mapping(address => mathint) ghostERC20TotalSupply {
    init_state axiom forall address token. ghostERC20TotalSupply[token] == 0;
    axiom forall address token. 
        ghostERC20TotalSupply[token] >= 0 && ghostERC20TotalSupply[token] <= max_uint128;
}

invariant erc20TotalSupplySolvency()
    forall address token. ghostERC20TotalSupply[token] 
        == ghostERC20Balances[token][ghostErc20Accounts(token, 0)] 
        + ghostERC20Balances[token][ghostErc20Accounts(token, 1)] 
        + ghostERC20Balances[token][ghostErc20Accounts(token, 2)]
        + ghostERC20Balances[token][ghostErc20Accounts(token, 3)] 
        + ghostERC20Balances[token][ghostErc20Accounts(token, 4)]
        + ghostERC20Balances[token][ghostErc20Accounts(token, 5)]
        + ghostERC20Balances[token][ghostErc20Accounts(token, 6)]
        + ghostERC20Balances[token][ghostErc20Accounts(token, 7)]
        + ghostERC20Balances[token][ghostErc20Accounts(token, 8)]
        + ghostERC20Balances[token][ghostErc20Accounts(token, 9)];

function requireErc20ValidState() {
    requireInvariant erc20TotalSupplySolvency;
}