// Prove contract is compatible with ERC20 (https://eips.ethereum.org/EIPS/eip-20)

import "./setup/env.spec";

// ERC20 viewers integrity

// Returns the total token supply
rule totalSupplyIntegrity() {
    assert(_ERC20.totalSupply() == ghostERC20TotalSupply[ghostContract]);
}

// Returns the account balance of another account
rule balanceOfIntegrity(address account) {
    assert(_ERC20.balanceOf(account) == ghostERC20Balances[ghostContract][account]);
}

// Returns the amount which `spender` is still allowed to withdraw from `owner`
rule allowanceIntegrity(address owner, address spender) {
    assert(_ERC20.allowance(owner, spender) == ghostERC20Allowances[ghostContract][owner][spender]);
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
    mathint fromBalancePrev = ghostERC20Balances[ghostContract][ghostCaller];
    mathint toBalancePrev = ghostERC20Balances[ghostContract][to];
    mathint otherBalancePrev = ghostERC20Balances[ghostContract][other];
    mathint totalSupplyPrev = ghostERC20TotalSupply[ghostContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[ghostContract][any1][any2];

    // Perform transfer
    _ERC20.transfer(e, to, amount);

    // Check updates
    assert(ghostCaller != to ? ghostERC20Balances[ghostContract][ghostCaller] == fromBalancePrev - amount 
                      : ghostERC20Balances[ghostContract][ghostCaller] == fromBalancePrev);

    assert(ghostCaller != to ? ghostERC20Balances[ghostContract][to] == toBalancePrev   + amount 
                      : ghostERC20Balances[ghostContract][to] == toBalancePrev);

    assert(ghostERC20Balances[ghostContract][other] == otherBalancePrev);
    assert(ghostERC20TotalSupply[ghostContract] == totalSupplyPrev);
    assert(ghostERC20Allowances[ghostContract][any1][any2] == allowanceAny1Any2Prev);
}

// Transfers of 0 values MUST be treated as normal transfers
rule transferSupportZeroAmount(env e, address to, uint256 amount) {

    // Perform transfer
    _ERC20.transfer(e, to, amount);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// The function SHOULD throw if the message caller’s account balance does not have enough tokens to spend
rule transferMustRevert(env e, address to, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Snapshot the 'from' balance
    mathint fromBalancePrev = ghostERC20Balances[ghostContract][ghostCaller];

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
    mathint fromBalancePrev = ghostERC20Balances[ghostContract][from];
    mathint toBalancePrev   = ghostERC20Balances[ghostContract][to];
    mathint otherBalancePrev = ghostERC20Balances[ghostContract][other];
    mathint totalSupplyPrev  = ghostERC20TotalSupply[ghostContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[ghostContract][any1][any2];

    // Perform the transferFrom
    _ERC20.transferFrom(e, from, to, amount);

    // Check updates
    assert(
        from != to 
            ? ghostERC20Balances[ghostContract][from] == fromBalancePrev - amount 
            : ghostERC20Balances[ghostContract][from] == fromBalancePrev
    );
    satisfy(ghostERC20Balances[ghostContract][from] == fromBalancePrev - amount);

    assert(
        from != to
            ? ghostERC20Balances[ghostContract][to] == toBalancePrev + amount
            : ghostERC20Balances[ghostContract][to] == toBalancePrev
    );
    satisfy(ghostERC20Balances[ghostContract][to] == toBalancePrev + amount);

    assert(ghostERC20Balances[ghostContract][other] == otherBalancePrev);
    assert(ghostERC20TotalSupply[ghostContract] == totalSupplyPrev);
    assert(ghostERC20Allowances[ghostContract][any1][any2] == allowanceAny1Any2Prev);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// Transfers of 0 values MUST be treated as normal transfers
rule transferFromSupportZeroAmount(env e, address to, address from, uint256 amount) {

    // Perform the transferFrom
    _ERC20.transferFrom(e, from, to, amount);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// The function SHOULD throw unless the `from` account has deliberately authorized the 
//  sender of the message via some mechanism
rule transferFromMustRevert(env e, address from, address to, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Snapshot the 'from' balance and allowance
    mathint fromBalancePrev = ghostERC20Balances[ghostContract][from];
    mathint allowancePrev   = ghostERC20Allowances[ghostContract][from][ghostCaller];

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
    mathint ownerBalancePrev   = ghostERC20Balances[ghostContract][ghostCaller];
    mathint spenderBalancePrev = ghostERC20Balances[ghostContract][spender];
    mathint otherBalancePrev   = ghostERC20Balances[ghostContract][other];
    mathint totalSupplyPrev    = ghostERC20TotalSupply[ghostContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[ghostContract][any1][any2];

    // Perform the approve
    _ERC20.approve(e, spender, value);

    // Check that balances remain unchanged
    assert(ghostERC20Balances[ghostContract][ghostCaller]   == ownerBalancePrev);
    assert(ghostERC20Balances[ghostContract][spender] == spenderBalancePrev);
    assert(ghostERC20Balances[ghostContract][other]   == otherBalancePrev);

    // Total supply must be unchanged
    assert(ghostERC20TotalSupply[ghostContract] == totalSupplyPrev);

    // Allowances: only the `(owner -> spender)` pair changes
    assert(any1 == ghostCaller && any2 == spender 
        ? ghostERC20Allowances[ghostContract][ghostCaller][spender] == value
        : ghostERC20Allowances[ghostContract][any1][any2] == allowanceAny1Any2Prev
    );
}

rule approveMustRevert(env e, address spender, uint256 value) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Attempt the approve with revert path
    _ERC20.approve@withrevert(e, spender, value);
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
    mathint accountBalancePrev = ghostERC20Balances[ghostContract][account];
    mathint otherBalancePrev   = ghostERC20Balances[ghostContract][other];
    mathint totalSupplyPrev    = ghostERC20TotalSupply[ghostContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[ghostContract][any1][any2];

    // Perform the mint
    _ERC20.mint(e, account, amount);

    // Check that 'account' got credited by 'amount'
    assert(ghostERC20Balances[ghostContract][account] == accountBalancePrev + amount);

    // Check that 'other' was not affected
    assert(ghostERC20Balances[ghostContract][other] == otherBalancePrev);

    // Check total supply is increased by 'amount'
    assert(ghostERC20TotalSupply[ghostContract] == totalSupplyPrev + amount);

    // Check no unrelated allowances were affected
    assert(ghostERC20Allowances[ghostContract][any1][any2] == allowanceAny1Any2Prev);
}

rule mintErc20MustRevert(env e, address account, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Attempt mint with revert path
    _ERC20.mint@withrevert(e, account, amount);
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
    mathint accountBalancePrev = ghostERC20Balances[ghostContract][account];
    mathint otherBalancePrev   = ghostERC20Balances[ghostContract][other];
    mathint totalSupplyPrev    = ghostERC20TotalSupply[ghostContract];
    mathint allowanceAny1Any2Prev = ghostERC20Allowances[ghostContract][any1][any2];

    // Perform the burn
    _ERC20.burn(e, account, amount);

    // Check that 'account' lost 'amount' tokens
    assert(ghostERC20Balances[ghostContract][account] == accountBalancePrev - amount);

    // Check that 'other' was not affected
    assert(ghostERC20Balances[ghostContract][other] == otherBalancePrev);

    // Check total supply is decreased by 'amount'
    assert(ghostERC20TotalSupply[ghostContract] == totalSupplyPrev - amount);

    // Check no unrelated allowances were affected
    assert(ghostERC20Allowances[ghostContract][any1][any2] == allowanceAny1Any2Prev);
}

rule burnMustRevert(env e, address account, uint256 amount) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Snapshot the account’s balance
    mathint balancePrev = ghostERC20Balances[ghostContract][account];

    // Attempt burn with revert path
    _ERC20.burn@withrevert(e, account, amount);
    bool reverted = lastReverted;

    // Must revert if `account` is the zero address
    assert(account == 0 => reverted);

    // Must revert if `account` does not have enough tokens
    assert(balancePrev < amount => reverted);
}
