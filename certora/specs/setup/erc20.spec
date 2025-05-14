// ERC20 support

methods {

    // For assets only
    function _.decimals() external 
        => DISPATCHER(true);
    function _.allowance(address,address) external 
        => DISPATCHER(true);
    function _.approve(address,uint256) external 
        => DISPATCHER(true);
    function _.transfer(address,uint256) external 
        => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external 
        => DISPATCHER(true);

    // Both for shares and assets
    function _.totalSupply() external 
        => totalSupplyCVL(calledContract) expect uint256;

    function _.balanceOf(address account) external with (env e) 
        => balanceOfCVL(e, calledContract, account) expect uint256;

    // For Assets only
    function SafeERC20.safeTransfer(address token, address to, uint256 value) internal
        => safeTransferFromCVL(token, currentContract, to, value, false);
    function SafeERC20.safeTransferFrom(address token, address from, address to, uint256 value) internal
        => safeTransferFromCVL(token, from, to, value, true);
    function SafeERC20.safeIncreaseAllowance(address token, address spender, uint256 value) internal
        => safeIncreaseAllowanceCVL(token, currentContract, spender, value);

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
    axiom forall address token. forall address account. 
        ghostERC20Balances[token][account] >= 0 
        // UNSAFE: Reduce max amount to reduce complexity 
        && ghostERC20Balances[token][account] <= ghostWeiUpperLimit;
}

// Allowances ghost  
persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20Allowances {
    init_state axiom forall address token. forall address owner. forall address spender. 
        ghostERC20Allowances[token][owner][spender] == 0;
    axiom forall address token. forall address owner. forall address spender. 
        ghostERC20Allowances[token][owner][spender] >= 0 
        // UNSAFE: Reduce max amount to reduce complexity
        && ghostERC20Allowances[token][owner][spender] <= max_uint128;
}

// Total supply ghost
persistent ghost mapping(address => mathint) ghostERC20TotalSupply {
    init_state axiom forall address token. ghostERC20TotalSupply[token] == 0;
    axiom forall address token. ghostERC20TotalSupply[token] >= 0 
        // UNSAFE: Reduce max amount to reduce complexity
        && ghostERC20TotalSupply[token] <= max_uint128;
}

// Total supply

function totalSupplyCVL(address token) returns uint256 {
    return require_uint256(ghostERC20TotalSupply[token]);
}

// User balances

function balanceOfCVL(env e, address token, address account) returns uint256 {
    require(ERC20_ACCOUNT_BOUNDS(token, account));
    return require_uint256(ghostERC20Balances[token][account]);
}

// Safe transfer lib summaries

function transferFromCVL(address token, address from, address to, uint256 amount, bool transferFrom) returns bool {

    require(ERC20_ACCOUNT_BOUNDS(token, from) && ERC20_ACCOUNT_BOUNDS(token, to));

    ASSERT(from != to);

    if(transferFrom) {
        ASSERT(ghostERC20Allowances[token][from][to] == max_uint256 || ghostERC20Allowances[token][from][to] >= amount);
        ghostERC20Allowances[token][from][to] = require_uint256(ghostERC20Allowances[token][from][to] - amount);
    }

    ASSERT(ghostERC20Balances[token][from] >= amount);
    ghostERC20Balances[token][from] = require_uint256(ghostERC20Balances[token][from] - amount);
    ghostERC20Balances[token][to] = require_uint256(ghostERC20Balances[token][to] + amount);

    return true;
}

function safeTransferFromCVL(address token, address from, address to, uint256 amount, bool transferFrom) {
    ASSERT(transferFromCVL(token, from, to, amount, transferFrom));
}

// Safe increase allowance

function increaseAllowanceCVL(address token, address owner, address spender, uint256 amount) returns bool {

    require(ERC20_ACCOUNT_BOUNDS(token, owner) && ERC20_ACCOUNT_BOUNDS(token, spender));

    ghostERC20Allowances[token][owner][spender] = require_uint256(
        ghostERC20Allowances[token][owner][spender] + amount
    );

    return true;
}

function safeIncreaseAllowanceCVL(address token, address owner, address spender, uint256 amount) {
    ASSERT(increaseAllowanceCVL(token, owner, spender, amount));
}