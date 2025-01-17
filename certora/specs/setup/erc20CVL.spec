// All ERC20 tokens implemented in CVL

methods {

    function _.decimals() external
        => require_uint8(ghostERC20CVLDecimals[calledContract]) expect uint8;

    function _.totalSupply() external
        => require_uint256(ghostERC20CVLTotalSupply[calledContract]) expect uint256;

    function _.balanceOf(address owner) external
        => require_uint256(ghostERC20CVLBalances[calledContract][owner]) expect uint256;

    function _.allowance(address owner, address spender) external
        => require_uint256(ghostERC20CVLAllowances[calledContract][owner][spender]) expect uint256;

    function _.approve(address spender, uint256 value) external with (env e)
        => approveCVL(calledContract, e.msg.sender, spender, value) expect bool;

    function _.transfer(address to, uint256 value) external with (env e)
        => transferFromCVL(calledContract, e.msg.sender, to, value, false) expect bool;

    function _.transferFrom(address from, address to, uint256 value) external with (env e)
        => transferFromCVL(calledContract, e.msg.sender, to, value, true) expect bool;

    function _.safeTransfer(address token, address to, uint256 value) internal
        => safeTransferFromCVL(token, calledContract, to, value, false) expect void;

    function _.safeTransferFrom(address token, address from, address to, uint256 value) internal
        => safeTransferFromCVL(token, from, to, value, true) expect void;

    function _.mint(address account, uint256 value) external
        => mintCVL(calledContract, account, value) expect void;

    function _.burn(address account, uint256 value) external
        => burnCVL(calledContract, account, value) expect void;
}

// Assume 5 different users
persistent ghost address ERC20CVL_ACCOUNT_1 {
    axiom ERC20CVL_ACCOUNT_1 != ERC20CVL_ACCOUNT_2 
        && ERC20CVL_ACCOUNT_1 != ERC20CVL_ACCOUNT_3 
        && ERC20CVL_ACCOUNT_1 != ERC20CVL_ACCOUNT_4 
        && ERC20CVL_ACCOUNT_1 != ERC20CVL_ACCOUNT_5;
}
persistent ghost address ERC20CVL_ACCOUNT_2 {
    axiom ERC20CVL_ACCOUNT_2 != ERC20CVL_ACCOUNT_1 
        && ERC20CVL_ACCOUNT_2 != ERC20CVL_ACCOUNT_3 
        && ERC20CVL_ACCOUNT_2 != ERC20CVL_ACCOUNT_4 
        && ERC20CVL_ACCOUNT_2 != ERC20CVL_ACCOUNT_5;
}
persistent ghost address ERC20CVL_ACCOUNT_3 {
    axiom ERC20CVL_ACCOUNT_3 != ERC20CVL_ACCOUNT_1 
        && ERC20CVL_ACCOUNT_3 != ERC20CVL_ACCOUNT_2 
        && ERC20CVL_ACCOUNT_3 != ERC20CVL_ACCOUNT_4 
        && ERC20CVL_ACCOUNT_3 != ERC20CVL_ACCOUNT_5;
}
persistent ghost address ERC20CVL_ACCOUNT_4 {
    axiom ERC20CVL_ACCOUNT_4 != ERC20CVL_ACCOUNT_1 
        && ERC20CVL_ACCOUNT_4 != ERC20CVL_ACCOUNT_2 
        && ERC20CVL_ACCOUNT_4 != ERC20CVL_ACCOUNT_3 
        && ERC20CVL_ACCOUNT_4 != ERC20CVL_ACCOUNT_5;
}
persistent ghost address ERC20CVL_ACCOUNT_5 {
    axiom ERC20CVL_ACCOUNT_5 != ERC20CVL_ACCOUNT_1 
        && ERC20CVL_ACCOUNT_5 != ERC20CVL_ACCOUNT_2 
        && ERC20CVL_ACCOUNT_5 != ERC20CVL_ACCOUNT_3 
        && ERC20CVL_ACCOUNT_5 != ERC20CVL_ACCOUNT_4;
}

definition ERC20CVL_ACCOUNT_BOUNDS(address account) returns bool = 
    account == ERC20CVL_ACCOUNT_1 
    || account == ERC20CVL_ACCOUNT_2 
    || account == ERC20CVL_ACCOUNT_3 
    || account == ERC20CVL_ACCOUNT_4 
    || account == ERC20CVL_ACCOUNT_5;

// Supported ERC20CVL tokens (up to 3)

persistent ghost mapping (mathint => address) ghostERC20CVLToken {    
    axiom ghostERC20CVLToken[0] != 0 
        && ghostERC20CVLToken[0] < ghostERC20CVLToken[1]
        && ghostERC20CVLToken[1] < ghostERC20CVLToken[2];    
}

definition VALID_TOKEN_ADDRESS(address token) returns bool
    = token == ghostERC20CVLToken[0] 
        || token == ghostERC20CVLToken[1] 
        || token == ghostERC20CVLToken[2];
    
// Decimals

persistent ghost mapping(address => mathint) ghostERC20CVLDecimals {
    axiom forall address token. VALID_TOKEN_ADDRESS(token)
        ? ghostERC20CVLDecimals[token] >= 6 && ghostERC20CVLDecimals[token] <= 18
        : ghostERC20CVLDecimals[token] == 0;
}

// Total supply

persistent ghost mapping (address => mathint) ghostERC20CVLTotalSupply {
    init_state axiom forall address token. ghostERC20CVLTotalSupply[token] == 0;
    axiom forall address token. VALID_TOKEN_ADDRESS(token) 
        ? ghostERC20CVLTotalSupply[token] == (
            ghostERC20CVLBalances[token][ERC20CVL_ACCOUNT_1] 
            + ghostERC20CVLBalances[token][ERC20CVL_ACCOUNT_2] 
            + ghostERC20CVLBalances[token][ERC20CVL_ACCOUNT_3]
            + ghostERC20CVLBalances[token][ERC20CVL_ACCOUNT_4] 
            + ghostERC20CVLBalances[token][ERC20CVL_ACCOUNT_5]
        ) : ghostERC20CVLTotalSupply[token] == 0;
}

// Transfers

persistent ghost mapping(address => mapping(address => mathint)) ghostERC20CVLBalances {
    init_state axiom forall address token. forall address owner. ghostERC20CVLBalances[token][owner] == 0;
    axiom forall address token. forall address owner. VALID_TOKEN_ADDRESS(token) && ERC20CVL_ACCOUNT_BOUNDS(owner)
        ? ghostERC20CVLBalances[token][owner] >= 0 && ghostERC20CVLBalances[token][owner] <= max_uint128
        : ghostERC20CVLBalances[token][owner] == 0;
}

function transferFromCVL(address token, address from, address to, mathint amount, bool transferFrom) returns bool {

    // Only specific tokens are supported
    require(VALID_TOKEN_ADDRESS(token));

    // Only specific accounts are supported
    require(ERC20CVL_ACCOUNT_BOUNDS(from));
    require(ERC20CVL_ACCOUNT_BOUNDS(to));

    // Safe assumptions about transferFrom()
    require(from != to);

    // Revert on zero address
    ASSERT(from != 0 && to != 0);

    if(transferFrom) {
        ASSERT(ghostERC20CVLAllowances[token][from][to] >= amount);
        ghostERC20CVLAllowances[token][from][to] = require_uint256(ghostERC20CVLAllowances[token][from][to] - amount);
    }

    ASSERT(ghostERC20CVLBalances[token][from] >= amount);
    ghostERC20CVLBalances[token][from] = require_uint256(ghostERC20CVLBalances[token][from] - amount);
    ghostERC20CVLBalances[token][to] = require_uint256(ghostERC20CVLBalances[token][to] + amount);

    return true;
}

function safeTransferFromCVL(address token, address from, address to, uint256 amount, bool transferFrom) {
    ASSERT(transferFromCVL(token, from, to, amount, transferFrom));
}

// Allowances

persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20CVLAllowances {
    init_state axiom forall address token. forall address owner. forall address spender. 
        ghostERC20CVLAllowances[token][owner][spender] == 0;
    axiom forall address token. forall address owner. forall address spender. 
        VALID_TOKEN_ADDRESS(token) && ERC20CVL_ACCOUNT_BOUNDS(owner) && ERC20CVL_ACCOUNT_BOUNDS(spender)
        ? ghostERC20CVLAllowances[token][owner][spender] >= 0 
            && ghostERC20CVLAllowances[token][owner][spender] <= max_uint128
        : ghostERC20CVLAllowances[token][owner][spender] == 0;
}

function approveCVL(address token, address owner, address spender, mathint value) returns bool {

    // Only specific tokens are supported
    require(VALID_TOKEN_ADDRESS(token));

    // Only specific accounts are supported
    require(ERC20CVL_ACCOUNT_BOUNDS(owner));
    require(ERC20CVL_ACCOUNT_BOUNDS(spender));

    ghostERC20CVLAllowances[token][owner][spender] = value;

    return true;
}

// Mint and burn

function mintCVL(address token, address account, mathint value) {

    // Only specific tokens are supported
    require(VALID_TOKEN_ADDRESS(token));

    // Only specific accounts are supported
    require(ERC20CVL_ACCOUNT_BOUNDS(account));

    // Revert on zero address
    ASSERT(account != 0);

    ghostERC20CVLTotalSupply[token] = require_uint256(ghostERC20CVLTotalSupply[token] + value);
    ghostERC20CVLBalances[token][account] = require_uint256(ghostERC20CVLBalances[token][account] + value);
}

function burnCVL(address token, address account, mathint value) {

    // Only specific tokens are supported
    require(VALID_TOKEN_ADDRESS(token));

    // Only specific accounts are supported
    require(ERC20CVL_ACCOUNT_BOUNDS(account));

    // Revert on zero address
    ASSERT(account != 0);

    ghostERC20CVLTotalSupply[token] = assert_uint256(ghostERC20CVLTotalSupply[token] - value);
    ghostERC20CVLBalances[token][account] = assert_uint256(ghostERC20CVLBalances[token][account] - value);
}