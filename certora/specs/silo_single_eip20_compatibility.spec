// Prove contract is compatible with EIP20 (https://eips.ethereum.org/EIPS/eip-20)

import "./setup/silo0/silo_0.spec";

using Silo0 as _ERC20;

// ERC20 viewers integrity

// Returns the total token supply
rule totalSupplyIntegrity(env e) {

    // Assume valid Silo0 state
    setupSilo(e);

    assert(_ERC20.totalSupply(e) == ghostERC20TotalSupply[currentContract]);
}

// Returns the account balance of another account
rule balanceOfIntegrity(env e, address account) {

    // Assume valid Silo0 state
    setupSilo(e);

    assert(_ERC20.balanceOf(e, account) == ghostERC20Balances[currentContract][account]);
}

// Returns the amount which `spender` is still allowed to withdraw from `owner`
rule allowanceIntegrity(env e, address owner, address spender) {

    // Assume valid Silo0 state
    setupSilo(e);

    assert(_ERC20.allowance(e, owner, spender) == ghostERC20Allowances[currentContract][owner][spender]);
}

// ERC20 transfer() integrity

// Transfers `amount` of tokens to address `to`
rule transferIntegrity(env e, address to, uint256 amount) {

    // Assume valid Silo0 state
    setupSilo(e);

    address other; 
    address any1;
    address any2;

    // Ensure 'other' is not involved in the transfer
    require(other != ghostCaller && other != to);

    // Capture pre-state
    mathint fromBalancePrev = ghostERC20Balances[currentContract][ghostCaller];
    mathint toBalancePrev = ghostERC20Balances[currentContract][to];
    mathint otherBalancePrev = ghostERC20Balances[currentContract][other];
    mathint totalSupplyPrev = ghostERC20TotalSupply[currentContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[currentContract][any1][any2];

    // Perform transfer
    _ERC20.transfer(e, to, amount);

    // Check updates
    assert(ghostCaller != to ? ghostERC20Balances[currentContract][ghostCaller] == fromBalancePrev - amount 
                      : ghostERC20Balances[currentContract][ghostCaller] == fromBalancePrev);

    assert(ghostCaller != to ? ghostERC20Balances[currentContract][to] == toBalancePrev   + amount 
                      : ghostERC20Balances[currentContract][to] == toBalancePrev);

    assert(ghostERC20Balances[currentContract][other] == otherBalancePrev);
    assert(ghostERC20TotalSupply[currentContract] == totalSupplyPrev);
    assert(ghostERC20Allowances[currentContract][any1][any2] == allowanceAny1Any2Prev);
}

// The function SHOULD throw if the message caller’s account balance does not have enough tokens to spend
rule transferMustRevert(env e, address to, uint256 amount) {

    // Assume valid Silo0 state
    setupSilo(e);

    // Snapshot the 'from' balance
    mathint fromBalancePrev = ghostERC20Balances[currentContract][ghostCaller];

    // Attempt transfer with revert path
    _ERC20.transfer@withrevert(e, to, amount);
    bool reverted = lastReverted;

    // Must revert if transferring from the zero address
    assert(ghostCaller == 0 => reverted);

    // Must revert if transferring to the zero address
    assert(to == 0 => reverted);

    // Must revert if 'from' does not have enough balance
    assert(fromBalancePrev < amount => reverted);
}

// Transfers of 0 values MUST be treated as normal transfers
rule transferSupportZeroAmount(env e, address to, uint256 amount) {

    // Perform transfer
    _ERC20.transfer(e, to, amount);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// ERC20 transferFrom() integrity

// Transfers `amount` of tokens from address `from` to address `to`
rule transferFromIntegrity(env e, address from, address to, uint256 amount) {

    // Assume valid Silo0 state
    setupSilo(e);

    address other; 
    address any1;
    address any2;
    require(any1 != from && any2 != to);

    // Ensure 'other' is not involved in the transferFrom call
    require(other != from && other != to);

    // Capture pre-state
    mathint fromBalancePrev = ghostERC20Balances[currentContract][from];
    mathint toBalancePrev   = ghostERC20Balances[currentContract][to];
    mathint otherBalancePrev = ghostERC20Balances[currentContract][other];
    mathint totalSupplyPrev  = ghostERC20TotalSupply[currentContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[currentContract][any1][any2];

    // Perform the transferFrom
    _ERC20.transferFrom(e, from, to, amount);

    // Check updates
    assert(
        from != to 
            ? ghostERC20Balances[currentContract][from] == fromBalancePrev - amount 
            : ghostERC20Balances[currentContract][from] == fromBalancePrev
    );

    assert(
        from != to
            ? ghostERC20Balances[currentContract][to] == toBalancePrev + amount
            : ghostERC20Balances[currentContract][to] == toBalancePrev
    );

    assert(ghostERC20Balances[currentContract][other] == otherBalancePrev);
    assert(ghostERC20TotalSupply[currentContract] == totalSupplyPrev);
    assert(ghostERC20Allowances[currentContract][any1][any2] == allowanceAny1Any2Prev);
}

// The function SHOULD throw unless the `from` account has deliberately authorized the 
//  sender of the message via some mechanism
rule transferFromMustRevert(env e, address from, address to, uint256 amount) {

    // Assume valid Silo0 state
    setupSilo(e);

    // Snapshot the 'from' balance and allowance
    mathint fromBalancePrev = ghostERC20Balances[currentContract][from];
    mathint allowancePrev   = ghostERC20Allowances[currentContract][from][ghostCaller];

    // Attempt the transferFrom with revert path
    _ERC20.transferFrom@withrevert(e, from, to, amount);
    bool reverted = lastReverted;

    // Must revert if `from` is the zero address
    assert(from == 0 => reverted);

    // Must revert if `to` is the zero address
    assert(to == 0 => reverted);

    // Must revert if `from` does not have enough balance
    assert(fromBalancePrev < amount => reverted);

    // Must revert if `ghostCaller` does not have enough allowance
    assert(allowancePrev < amount => reverted);
}

// Transfers of 0 values MUST be treated as normal transfers
rule transferFromSupportZeroAmount(env e, address to, address from, uint256 amount) {

    // Perform the transferFrom
    _ERC20.transferFrom(e, from, to, amount);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// ERC20 approve() integrity

// Allows `spender` to withdraw from your account multiple times, up to the `value` amount
rule approveIntegrity(env e, address spender, uint256 value) {

    // Assume valid Silo0 state
    setupSilo(e);

    address other;
    address any1;
    address any2;

    // Ensure 'other' is not involved in the approve call
    require(other != ghostCaller && other != spender);

    // Capture pre-state
    mathint ownerBalancePrev   = ghostERC20Balances[currentContract][ghostCaller];
    mathint spenderBalancePrev = ghostERC20Balances[currentContract][spender];
    mathint otherBalancePrev   = ghostERC20Balances[currentContract][other];
    mathint totalSupplyPrev    = ghostERC20TotalSupply[currentContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[currentContract][any1][any2];

    // Perform the approve
    _ERC20.approve(e, spender, value);

    // Check that balances remain unchanged
    assert(ghostERC20Balances[currentContract][ghostCaller]   == ownerBalancePrev);
    assert(ghostERC20Balances[currentContract][spender] == spenderBalancePrev);
    assert(ghostERC20Balances[currentContract][other]   == otherBalancePrev);

    // Total supply must be unchanged
    assert(ghostERC20TotalSupply[currentContract] == totalSupplyPrev);

    // Allowances: only the `(owner -> spender)` pair changes
    assert(any1 == ghostCaller && any2 == spender 
        ? ghostERC20Allowances[currentContract][ghostCaller][spender] == value
        : ghostERC20Allowances[currentContract][any1][any2] == allowanceAny1Any2Prev
    );
}

rule approveMustRevert(env e, address spender, uint256 value) {

    // Assume valid Silo0 state
    setupSilo(e);

    // Attempt the approve with revert path
    _ERC20.approve@withrevert(e, spender, value);
    bool reverted = lastReverted;

    // Must revert if the spender is the zero address
    assert(spender == 0 => reverted);

    // Must revert if the caller (ghostCaller) is the zero address
    assert(ghostCaller == 0 => reverted);
}