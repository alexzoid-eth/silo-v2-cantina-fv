// Common ERC20 ghosts for all contracts

methods {

    // ERC20/ERC20Upgradeable
    function _.decimals() external => DISPATCHER(true);
    function _.totalSupply() external => DISPATCHER(true);
    function _.balanceOf(address) external => DISPATCHER(true);
    function _.allowance(address,address) external => DISPATCHER(true);
    function _.approve(address,uint256) external => DISPATCHER(true);
    function _.transfer(address,uint256) external => DISPATCHER(true);
    function _.transferFrom(address,address,uint256) external => DISPATCHER(true);

    function _.name() external => NONDET DELETE;
    function _.symbol() external => NONDET DELETE;

    // ERC20PermitUpgradeable
    function _.nonces(address) external => NONDET DELETE;
    function _.permit(address, address, uint256, uint256, uint8, bytes32, bytes32) external => NONDET DELETE;
}

// Assume 10 different non-zero accounts
definition MAX_ERC20_USERS() returns mathint = 10;
persistent ghost ghostErc20Accounts(address, mathint) returns address {
    // All accounts in the range are different
    axiom forall address contract. forall mathint i. forall mathint j. 
        i >= 0 && i < MAX_ERC20_USERS() && j >= 0 && j < MAX_ERC20_USERS() && i != j
        => ghostErc20Accounts(contract, i) != ghostErc20Accounts(contract, j);
    // Set out of range accounts as zero
    axiom forall address contract. forall mathint i. i >= 0 && i < MAX_ERC20_USERS()
        ? ghostErc20Accounts(contract, i) != 0
        : ghostErc20Accounts(contract, i) == 0;
}

persistent ghost ghostErc20AccountsValues(address, address) returns bool {
    // Assume true when address is nonzero in ghostErc20Accounts()
    axiom forall address contract. forall mathint i.
        ghostErc20AccountsValues(contract, ghostErc20Accounts(contract, i)) 
            == (ghostErc20Accounts(contract, i) != 0);
}

// Return true when address is supported ERC20 account
definition ERC20_ACCOUNT_BOUNDS(address contract, address account) returns bool = 
    ghostErc20AccountsValues(contract, account);

// Balances ghost
persistent ghost mapping(address => mapping(address => mathint)) ghostERC20Balances {
    init_state axiom forall address contract. forall address account. 
        ghostERC20Balances[contract][account] == 0;
    axiom forall address contract. forall address account. 
        ghostERC20Balances[contract][account] >= 0 && ghostERC20Balances[contract][account] <= max_uint128;
}

// Allowances ghost  
persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostERC20Allowances {
    init_state axiom forall address contract. forall address owner. forall address spender. 
        ghostERC20Allowances[contract][owner][spender] == 0;
    axiom forall address contract. forall address owner. forall address spender. 
        ghostERC20Allowances[contract][owner][spender] >= 0 && ghostERC20Allowances[contract][owner][spender] <= max_uint128;
}

// Total supply ghost
persistent ghost mapping(address => mathint) ghostERC20TotalSupply {
    init_state axiom forall address contract. ghostERC20TotalSupply[contract] == 0;
    axiom forall address contract. 
        ghostERC20TotalSupply[contract] >= 0 && ghostERC20TotalSupply[contract] <= max_uint128;
}

invariant erc20TotalSupplySolvency()
    forall address contract. ghostERC20TotalSupply[contract] 
        == ghostERC20Balances[contract][ghostErc20Accounts(contract, 0)] 
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 1)] 
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 2)]
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 3)] 
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 4)]
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 5)]
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 6)]
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 7)]
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 8)]
        + ghostERC20Balances[contract][ghostErc20Accounts(contract, 9)];

function requireErc20ValidState() {
    requireInvariant erc20TotalSupplySolvency;
}