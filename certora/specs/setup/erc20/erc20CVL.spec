// ERC20 ghosts implemented in CVL

// Assume 10 different non-zero accounts
definition MAX_ERC20CVL_USERS() returns mathint = 10;
persistent ghost ghostErc20CVLAccounts(address, mathint) returns address {
    // All accounts in the range are different
    axiom forall address token. forall mathint i. forall mathint j. 
        i >= 0 && i < MAX_ERC20CVL_USERS() && j >= 0 && j < MAX_ERC20CVL_USERS() && i != j
        => ghostErc20CVLAccounts(token, i) != ghostErc20CVLAccounts(token, j);
    // Set out of range accounts as zero
    axiom forall address token. forall mathint i. i >= 0 && i < MAX_ERC20CVL_USERS()
        ? ghostErc20CVLAccounts(token, i) != 0
        : ghostErc20CVLAccounts(token, i) == 0;
}

persistent ghost ghostErc20CVLAccountsValues(address, address) returns bool {
    // Assume true when address is nonzero in ghostErc20CVLAccounts()
    axiom forall address token. forall mathint i.
        ghostErc20CVLAccountsValues(token, ghostErc20CVLAccounts(token, i)) 
            == (ghostErc20CVLAccounts(token, i) != 0);
}

// Return true when address is supported ERC20 account
definition ERC20CVL_ACCOUNT_BOUNDS(address token, address account) returns bool = 
    ghostErc20CVLAccountsValues(token, account);
    
// Viewers summaries

function totalSupplyCVL(address token) returns uint256 {
    return require_uint256(ghostERC20CVLTotalSupply[token]);
}

function balanceOfCVL(address token, address owner) returns uint256 {
    require(ERC20CVL_ACCOUNT_BOUNDS(token, owner));
    return require_uint256(ghostERC20CVLBalances[token][owner]);
}

function allowanceCVL(address token, address owner, address spender) returns uint256 {
    require(ERC20CVL_ACCOUNT_BOUNDS(token, owner) && ERC20CVL_ACCOUNT_BOUNDS(token, spender));
    return require_uint256(ghostERC20CVLAllowances[token][owner][spender]);
}

// Total supply

persistent ghost mapping (address => mathint) ghostERC20CVLTotalSupply {
    init_state axiom forall address token. ghostERC20CVLTotalSupply[token] == 0;
    axiom forall address token. ghostERC20TotalSupply[token] 
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
}

// Transfers

persistent ghost mapping(address => mapping(address => mathint)) ghostERC20CVLBalances {
    init_state axiom forall address token. forall address owner. ghostERC20CVLBalances[token][owner] == 0;
    axiom forall address token. forall address owner. 
        ghostERC20CVLBalances[token][owner] >= 0 && ghostERC20CVLBalances[token][owner] <= max_uint128;
}

function transferFromCVL(
    env e, address token, address from, address to, mathint amount, bool transferFrom
    ) returns bool {
    
    // Only specific tokens are supported
    require(VALID_ERC20CVL_ADDRESS(token));

    // Only specific accounts are supported
    require(ERC20CVL_ACCOUNT_BOUNDS(token, from));
    require(ERC20CVL_ACCOUNT_BOUNDS(token, to));

    // Safe assumptions about transferFrom()
    require(from != to);

    // Revert on zero address
    ASSERT(from != 0 && to != 0);

    if(transferFrom) {
        ASSERT(ghostERC20CVLAllowances[token][from][to] >= amount);
        ghostERC20CVLAllowances[token][from][to] 
            = require_uint256(ghostERC20CVLAllowances[token][from][to] - amount);
    }

    ASSERT(ghostERC20CVLBalances[token][from] >= amount);
    ghostERC20CVLBalances[token][from] = require_uint256(ghostERC20CVLBalances[token][from] - amount);
    ghostERC20CVLBalances[token][to] = require_uint256(ghostERC20CVLBalances[token][to] + amount);

    return true;
}

function safeTransferFromCVL(env e, address token, address from, address to, uint256 amount, bool transferFrom) {
    ASSERT(transferFromCVL(e, token, from, to, amount, transferFrom));
}

// Allowances

persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20CVLAllowances {
    init_state axiom forall address token. forall address owner. forall address spender. 
        ghostERC20CVLAllowances[token][owner][spender] == 0;
    axiom forall address token. forall address owner. forall address spender. 
        ghostERC20CVLAllowances[token][owner][spender] >= 0 && ghostERC20CVLAllowances[token][owner][spender] <= max_uint128;
}

function approveCVL(env e, address token, address owner, address spender, mathint value) returns bool {

    // Only specific tokens are supported
    require(VALID_ERC20CVL_ADDRESS(token));

    // Only specific accounts are supported
    require(ERC20CVL_ACCOUNT_BOUNDS(token, owner) && ERC20CVL_ACCOUNT_BOUNDS(token, spender));

    ghostERC20CVLAllowances[token][owner][spender] = value;

    return true;
}