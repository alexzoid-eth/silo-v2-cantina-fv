// Prove that Silo is compatible with ERC20 (https://eips.ethereum.org/EIPS/eip-20)

import "setup/silo.spec";

// ERC20 viewers integrity

// Returns the total token supply
rule totalSupplyIntegrity() {
    assert(_Silo.totalSupply() == ghostERC20TotalSupply);
    satisfy(_Silo.totalSupply() == ghostERC20TotalSupply);
}

// Returns the account balance of another account
rule balanceOfIntegrity(address account) {
    assert(_Silo.balanceOf(account) == ghostERC20Balances[account]);
    satisfy(_Silo.balanceOf(account) == ghostERC20Balances[account]);
}

// Returns the amount which `spender` is still allowed to withdraw from `owner`
rule allowanceIntegrity(address owner, address spender) {
    assert(_Silo.allowance(owner, spender) == ghostERC20Allowances[owner][spender]);
    satisfy(_Silo.allowance(owner, spender) == ghostERC20Allowances[owner][spender]);
}

// ERC20 transfer() integrity

// Transfers `amount` of tokens to address `to`
rule transferIntegrity(env e, address to, uint256 amount) {
    
    // msg.sender not current contract
    requireValidEnv(e);

    address other; 
    address any1;
    address any2;

    // Ensure 'other' is not involved in the transfer
    require(other != ghostCaller && other != to);

    // Capture pre-state
    mathint fromBalancePrev = ghostERC20Balances[ghostCaller];
    mathint toBalancePrev = ghostERC20Balances[to];
    mathint otherBalancePrev = ghostERC20Balances[other];
    mathint totalSupplyPrev = ghostERC20TotalSupply;
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[any1][any2];

    // Perform transfer
    _Silo.transfer(e, to, amount);

    // Check updates
    assert(ghostCaller != to ? ghostERC20Balances[ghostCaller] == fromBalancePrev - amount 
                      : ghostERC20Balances[ghostCaller] == fromBalancePrev);
    satisfy(ghostERC20Balances[ghostCaller] == fromBalancePrev - amount);

    assert(ghostCaller != to ? ghostERC20Balances[to] == toBalancePrev   + amount 
                      : ghostERC20Balances[to] == toBalancePrev);
    satisfy(ghostERC20Balances[to] == toBalancePrev + amount);

    assert(ghostERC20Balances[other] == otherBalancePrev);
    assert(ghostERC20TotalSupply == totalSupplyPrev);
    assert(ghostERC20Allowances[any1][any2] == allowanceAny1Any2Prev);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// The function SHOULD throw if the message caller’s account balance does not have enough tokens to spend
rule transferMustRevert(env e, address to, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Snapshot the 'from' balance
    mathint fromBalancePrev = ghostERC20Balances[ghostCaller];

    // Attempt transfer with revert path
    _Silo.transfer@withrevert(e, to, amount);
    bool reverted = lastReverted;

    // Must revert if transferring from the zero address
    assert(ghostCaller == 0 => reverted);

    // Must revert if transferring to the zero address
    assert(to == 0 => reverted);

    // Must revert if 'from' does not have enough balance
    assert(fromBalancePrev < amount => reverted);
}

// ERC20 transferFrom() integrity

// Transfers `amount` of tokens from address `from` to address `to`
rule transferFromIntegrity(env e, address from, address to, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    address other; 
    address any1;
    address any2;

    // Ensure 'other' is not involved in the transferFrom call
    require(other != from && other != to);

    // Capture pre-state
    mathint fromBalancePrev = ghostERC20Balances[from];
    mathint toBalancePrev   = ghostERC20Balances[to];
    mathint otherBalancePrev = ghostERC20Balances[other];
    mathint totalSupplyPrev  = ghostERC20TotalSupply;
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[any1][any2];

    // Perform the transferFrom
    _Silo.transferFrom(e, from, to, amount);

    // Check updates
    assert(
        from != to 
            ? ghostERC20Balances[from] == fromBalancePrev - amount 
            : ghostERC20Balances[from] == fromBalancePrev
    );
    satisfy(ghostERC20Balances[from] == fromBalancePrev - amount);

    assert(
        from != to
            ? ghostERC20Balances[to] == toBalancePrev + amount
            : ghostERC20Balances[to] == toBalancePrev
    );
    satisfy(ghostERC20Balances[to] == toBalancePrev + amount);

    assert(ghostERC20Balances[other] == otherBalancePrev);
    assert(ghostERC20TotalSupply == totalSupplyPrev);
    assert(ghostERC20Allowances[any1][any2] == allowanceAny1Any2Prev);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// The function SHOULD throw unless the `from` account has deliberately authorized the 
//  sender of the message via some mechanism
rule transferFromMustRevert(env e, address from, address to, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Snapshot the 'from' balance and allowance
    mathint fromBalancePrev = ghostERC20Balances[from];
    mathint allowancePrev   = ghostERC20Allowances[from][ghostCaller];

    // Attempt the transferFrom with revert path
    _Silo.transferFrom@withrevert(e, from, to, amount);
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

// ERC20 approve() integrity

// Allows `spender` to withdraw from your account multiple times, up to the `value` amount
rule approveIntegrity(env e, address spender, uint256 value) {

    // msg.sender not current contract
    requireValidEnv(e);

    address other;
    address any1;
    address any2;

    // Ensure 'other' is not involved in the approve call
    require(other != ghostCaller && other != spender);

    // Capture pre-state
    mathint ownerBalancePrev   = ghostERC20Balances[ghostCaller];
    mathint spenderBalancePrev = ghostERC20Balances[spender];
    mathint otherBalancePrev   = ghostERC20Balances[other];
    mathint totalSupplyPrev    = ghostERC20TotalSupply;
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[any1][any2];

    // Perform the approve
    _Silo.approve(e, spender, value);

    // Check that balances remain unchanged
    assert(ghostERC20Balances[ghostCaller]   == ownerBalancePrev);
    assert(ghostERC20Balances[spender] == spenderBalancePrev);
    assert(ghostERC20Balances[other]   == otherBalancePrev);

    // Total supply must be unchanged
    assert(ghostERC20TotalSupply == totalSupplyPrev);

    // Allowances: only the `(owner -> spender)` pair changes
    assert(any1 == ghostCaller && any2 == spender 
        ? ghostERC20Allowances[ghostCaller][spender] == value
        : ghostERC20Allowances[any1][any2] == allowanceAny1Any2Prev
    );
}

rule approveMustRevert(env e, address spender, uint256 value) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Attempt the approve with revert path
    _Silo.approve@withrevert(e, spender, value);
    bool reverted = lastReverted;

    // Must revert if the spender is the zero address
    assert(spender == 0 => reverted);

    // Must revert if the caller (ghostCaller) is the zero address
    assert(ghostCaller == 0 => reverted);
}

// ERC20 mint() integrity

rule mintErc20Integrity(env e, address account, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    address other;
    address any1;
    address any2;

    // Ensure 'other' is not the same as 'account'
    require(other != account);

    // Capture pre-state
    mathint accountBalancePrev = ghostERC20Balances[account];
    mathint otherBalancePrev   = ghostERC20Balances[other];
    mathint totalSupplyPrev    = ghostERC20TotalSupply;
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[any1][any2];

    // Perform the mint
    _Silo.mint(e, account, amount);

    // Check that 'account' got credited by 'amount'
    assert(ghostERC20Balances[account] == accountBalancePrev + amount);

    // Check that 'other' was not affected
    assert(ghostERC20Balances[other] == otherBalancePrev);

    // Check total supply is increased by 'amount'
    assert(ghostERC20TotalSupply == totalSupplyPrev + amount);

    // Check no unrelated allowances were affected
    assert(ghostERC20Allowances[any1][any2] == allowanceAny1Any2Prev);
}

rule mintErc20MustRevert(env e, address account, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Attempt mint with revert path
    _Silo.mint@withrevert(e, account, amount);
    bool reverted = lastReverted;

    // Must revert if `account` is the zero address
    assert(account == 0 => reverted);
}

// ERC20 burn() integrity

rule burnIntegrity(env e, address account, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    address other;
    address any1;
    address any2;

    // Ensure 'other' is not the same as 'account'
    require(other != account);

    // Capture pre-state
    mathint accountBalancePrev = ghostERC20Balances[account];
    mathint otherBalancePrev   = ghostERC20Balances[other];
    mathint totalSupplyPrev    = ghostERC20TotalSupply;
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[any1][any2];

    // Perform the burn
    _Silo.burn(e, account, amount);

    // Check that 'account' lost 'amount' tokens
    assert(ghostERC20Balances[account] == accountBalancePrev - amount);

    // Check that 'other' was not affected
    assert(ghostERC20Balances[other] == otherBalancePrev);

    // Check total supply is decreased by 'amount'
    assert(ghostERC20TotalSupply == totalSupplyPrev - amount);

    // Check no unrelated allowances were affected
    assert(ghostERC20Allowances[any1][any2] == allowanceAny1Any2Prev);
}

rule burnMustRevert(env e, address account, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Snapshot the account’s balance
    mathint balancePrev = ghostERC20Balances[account];

    // Attempt burn with revert path
    _Silo.burn@withrevert(e, account, amount);
    bool reverted = lastReverted;

    // Must revert if `account` is the zero address
    assert(account == 0 => reverted);

    // Must revert if `account` does not have enough tokens
    assert(balancePrev < amount => reverted);
}
