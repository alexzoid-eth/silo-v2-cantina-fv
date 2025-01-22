// Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "../setup/silo0/silo_0.spec";

using Silo0 as _ERC4626;

// @todo change to ghostToken0
using Token0 as _Asset;

//
// _Asset
//

// MUST be an EIP-20 token contract
rule assetIntegrity(env e) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    address asset = _ERC4626.asset(e);

    assert(asset == _Asset);
}

// MUST NOT revert
rule assetMustNotRevert(env e) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    _ERC4626.asset@withrevert(e);
    
    assert(lastReverted == false);
}

//
// totalAssets()
//

// SHOULD include any compounding that occurs from yield
rule totalAssetsIntegrity(env e) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint totalAssets = _ERC4626.totalAssets(e);

    assert(totalAssets == ghostERC20Balances[_Asset][currentContract]);
}

// MUST NOT revert
rule totalAssetsMustNotRevert(env e) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    _ERC4626.totalAssets@withrevert(e);
    
    assert(lastReverted == false);
}

//
// convertToShares()
//

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check deposit)
rule convertToSharesNotIncludeFeesInDeposit(env e, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Another way: previewDeposit() factors in deposit fees, so it will return fewer shares 
    //  if a fee is charged

    assert(_ERC4626.previewDeposit(e, assets) <= _ERC4626.convertToShares(e, assets));
    satisfy(_ERC4626.previewDeposit(e, assets) <= _ERC4626.convertToShares(e, assets));
}

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check withdrawal)
rule convertToSharesNotIncludeFeesInWithdraw(env e, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Another way: previewWithdraw() includes withdrawal fees, so you typically have 
    //  to burn more shares to net the same assets

    assert(_ERC4626.previewWithdraw(e, assets) >= _ERC4626.convertToShares(e, assets));
    satisfy(_ERC4626.previewWithdraw(e, assets) >= _ERC4626.convertToShares(e, assets));
}

// MUST NOT show any variations depending on the caller
rule convertToSharesMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint shares1 = _ERC4626.convertToShares(e1, assets) at init;
    mathint shares2 = _ERC4626.convertToShares(e2, assets) at init;

    assert(shares1 == shares2);
}

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule convertToSharesNoSlippage(env e1, env e2, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Another way: if totalAssets and totalSupply remain the same between two calls, convertToShares 
    //  MUST return the same value

    mathint totalAssets1 = _ERC4626.totalAssets(e1);
    mathint totalSupply1 = _ERC4626.totalSupply(e1);
    mathint shares1 = _ERC4626.convertToShares(e1, assets);

    // Havoc storage
    method f;
    env e;
    calldataarg args;
    _ERC4626.f(e, args);

    mathint totalAssets2 = _ERC4626.totalAssets(e2);
    mathint totalSupply2 = _ERC4626.totalSupply(e2);
    mathint shares2 = _ERC4626.convertToShares(e2, assets);

    // if totalAssets() and totalSupply() remain unchanged, the result must be identical
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => shares1 == shares2
        );
    satisfy(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 && shares1 == shares2);
}

// MUST NOT revert unless due to integer overflow caused by an unreasonably large input
rule convertToSharesMustNotRevert(env e, uint256 assets) {
    
    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);
    
    _ERC4626.convertToShares@withrevert(e, assets);
    bool reverted = lastReverted;

    assert(reverted == false);
}

// MUST round down towards 0
rule convertToSharesRoundTripDoesNotExceed(env e, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Indirectly prove that each function is rounding down. Going one way and then back will 
    //  produce no more than the original value

    uint256 shares = _ERC4626.convertToShares(e, assets);
    mathint assets2 = _ERC4626.convertToAssets(e, shares);

    // assets2 must be <= assets, proving that convertToShares didn’t round up
    assert(assets2 <= assets);
    satisfy(assets2 <= assets);
}

//
// convertToAssets()
//

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check redeem)
rule convertToAssetsNotIncludeFeesRedeem(env e, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    // Typically, previewMint() includes deposit fees -> requires more assets to mint the same shares
    // Therefore, the "ideal scenario" convertToAssets() is >= previewRedeem() and <= previewMint()
    assert(_ERC4626.previewRedeem(e, shares) <= _ERC4626.convertToAssets(e, shares));
    satisfy(_ERC4626.previewRedeem(e, shares) <= _ERC4626.convertToAssets(e, shares));
}

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check mint)
rule convertToAssetsNotIncludeFeesMint(env e, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    // Typically previewRedeem() includes withdrawal fees -> yields fewer assets for the same shares
    // Therefore, the "ideal scenario" convertToAssets() is >= previewRedeem() and <= previewMint()
    assert(_ERC4626.previewMint(e, shares) >= _ERC4626.convertToAssets(e, shares));
    satisfy(_ERC4626.previewMint(e, shares) >= _ERC4626.convertToAssets(e, shares));
}

// MUST NOT show any variations depending on the caller
rule convertToAssetsMustNotDependOnCaller(env e1, env e2, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint assets1 = _ERC4626.convertToAssets(e1, shares) at init;
    mathint assets2 = _ERC4626.convertToAssets(e2, shares) at init;

    // If no state changed, the result should be identical regardless of the caller
    assert(assets1 == assets2);
    satisfy(assets1 == assets2);
}

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule convertToAssetsNoSlippage(env e1, env e2, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Snapshot totalAssets() and totalSupply() before first call
    mathint totalAssets1  = _ERC4626.totalAssets(e1);
    mathint totalSupply1  = _ERC4626.totalSupply(e1);
    mathint assets1 = _ERC4626.convertToAssets(e1, shares);

    // "Havoc" the contract by calling an arbitrary method (f), but if it does not affect 
    // totalAssets/totalSupply, then convertToAssets must remain the same
    method f;
    env e;
    calldataarg args;
    _ERC4626.f(e, args);

    // Snapshot again
    mathint totalAssets2 = _ERC4626.totalAssets(e2);
    mathint totalSupply2 = _ERC4626.totalSupply(e2);
    mathint assets2 = _ERC4626.convertToAssets(e2, shares);

    // If totalAssets() and totalSupply() are unchanged, the output must match
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => assets1 == assets2
    );
    satisfy(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 && assets1 == assets2);
}

// MUST NOT revert unless due to integer overflow caused by an unreasonably large input
rule convertToAssetsMustNotRevert(env e, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    _ERC4626.convertToAssets@withrevert(e, shares);
    assert(lastReverted == false);
}

// MUST round down towards 0
rule convertToAssetsRoundTripDoesNotExceed(env e, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    // Indirectly prove rounding down. If we convert to assets and back, 
    // we can't exceed the original shares.

    uint256 assets = _ERC4626.convertToAssets(e, shares);
    mathint shares2 = _ERC4626.convertToShares(e, assets);

    // shares2 must be <= shares, proving convertToAssets didn't round up
    assert(shares2 <= shares);
    satisfy(shares2 <= shares);
}

//
// maxDeposit()
// 

// MUST return the maximum amount of assets deposit would allow to be deposited for receiver

// MUST NOT be higher than the actual maximum that would be accepted
rule maxDepositNoHigherThanActual(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Query the reported limit
    mathint limit = _ERC4626.maxDeposit(e, receiver);

    // Attempt deposit any assets
    _ERC4626.deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // Because the spec says “it should *not* be higher than the true limit”
    assert(limit != max_uint256 && limit < assets => reverted);
} 

// MUST NOT rely on balanceOf of asset
rule maxDepositDoesNotDependOnUserBalance(env e1, env e2, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    mathint limit1 = _ERC4626.maxDeposit(e1, receiver);

    // The vault must not factor the user's actual underlying asset balance
    havoc ghostERC20Balances assuming ghostERC20Balances@new[_Asset][receiver] 
        != ghostERC20Balances@old[_Asset][receiver];

    mathint limit2 = _ERC4626.maxDeposit(e2, receiver);

    // The spec says they SHOULD match if all else is the same (global state).
    // If deposit is truly disabled or unlimited, they must match, etc.
    assert(limit1 == limit2);
}

// MUST factor in both global and user-specific limits, like if deposits are entirely 
//  disabled (even temporarily) it MUST return 0
rule maxDepositZeroIfDisabled(env e, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint limit = _ERC4626.maxDeposit(e, receiver);

    // Attempt depositing 1
    _ERC4626.deposit@withrevert(e, 1, receiver);
    bool reverted = lastReverted;

    // If deposit(1) reverts, then EIP-4626 says maxDeposit *must* be 0
    assert(reverted => limit == 0);

    // Not reachable when maxDeposit() returns `type(uint256).max`
}

// MUST return 2 ** 256 - 1 if there is no limit on the maximum amount of assets that may be deposited
rule maxDepositUnlimitedReturnsMax(env e, uint256 assets, address receiver) {
    
    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint limit = _ERC4626.maxDeposit(e, receiver);

    // If deposit(e, anyLargeNumber, receiver) DOES NOT revert,
    // that means the vault truly imposes no limit. Then maxDeposit MUST be 2^256-1.
    _ERC4626.deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // If deposit did NOT revert at a very large number, we interpret that as "no limit".
    assert(reverted == false => limit == max_uint256);

    // At least one flow when mint doesn't revert with "unlimited" limits
    satisfy(limit == max_uint256 => !reverted);
}

// MUST NOT revert
rule maxDepositMustNotRevert(env e, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    _ERC4626.maxDeposit@withrevert(e, receiver);

    assert(!lastReverted);
}

//
// previewDeposit()
//

// MUST return as close to and no more than the exact amount of Vault shares that would 
//  be minted in a deposit call in the same transaction
rule previewDepositNoMoreThanActualShares(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint previewedShares = _ERC4626.previewDeposit(e, assets);
    mathint sharesDeposited = _ERC4626.deposit(e, assets, receiver);

    // The returned real minted shares must be at least as many as the “previewed” shares
    assert(sharesDeposited >= previewedShares);
    satisfy(sharesDeposited >= previewedShares);
}

// MUST NOT account for deposit limits like those returned from maxDeposit and should 
//  always act as though the deposit would be accepted, regardless if the user has enough 
//  tokens approved, etc.
rule previewDepositMustIgnoreLimits(env e, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    bool enoughAllowance = ghostERC20Allowances[_Asset][ghostCaller][currentContract] >= assets;
    mathint limit = _ERC4626.maxDeposit(e, ghostCaller);

    mathint shares = _ERC4626.previewDeposit(e, assets);

    // Preview deposit even when user don't have "enough tokens approved"
    satisfy(enoughAllowance == false => shares != 0);

    // Preview deposit even when user "maxDeposit" limit is exceeded 
    satisfy(limit < assets => shares != 0);
}

// MUST be inclusive of deposit fees. Integrators should be aware of the existence of deposit fees.
rule previewDepositMustIncludeFees(env e, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64); 

    mathint previewed = _ERC4626.previewDeposit(e, assets);
    mathint idealNoFee = _ERC4626.convertToShares(e, assets);

    // Because deposit fees reduce the minted shares, previewDeposit <= convertToShares
    assert(previewed <= idealNoFee);
    satisfy(previewed <= idealNoFee);
}

// MUST NOT revert due to vault specific user/global limits
rule previewDepositMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    // Like convertToShares or convertToAssets, previewDeposit(assets) must not change based on msg.sender
    storage init = lastStorage;
    mathint pd1 = _ERC4626.previewDeposit(e1, assets) at init;
    mathint pd2 = _ERC4626.previewDeposit(e2, assets) at init;

    assert(pd1 == pd2);
    satisfy(pd1 == pd2);
}

// MAY revert due to other conditions that would also cause deposit to revert
rule previewDepositMayRevertOnlyWithDepositRevert(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Save current storage 
    storage init = lastStorage;

    _ERC4626.deposit@withrevert(e, assets, receiver) at init;
    bool depositReverted = lastReverted;

    _ERC4626.previewDeposit@withrevert(e, assets) at init;
    bool previewReverted = lastReverted;

    // previewDeposit() may revert only when deposit() reverts
    assert(previewReverted => depositReverted);
}

//
// deposit()
//

// Mints shares Vault shares to receiver by depositing exactly assets of underlying tokens
rule depositIntegrity(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Pre-state checks
    mathint vaultAssetsPrev    = ghostERC20Balances[_Asset][currentContract];
    mathint callerBalancePrev  = ghostERC20Balances[_Asset][ghostCaller];
    mathint receiverSharesPrev = ghostERC20Balances[currentContract][receiver];
    mathint vaultSharesSupplyPrev = ghostERC20TotalSupply[currentContract];

    // Attempt deposit
    mathint shares = _ERC4626.deposit(e, assets, receiver);

    // Post-state checks

    // The vault's asset balance must have increased by exactly `assets`
    mathint vaultAssetsPost = ghostERC20Balances[_Asset][currentContract];
    assert(vaultAssetsPost == vaultAssetsPrev + assets);

    // The caller's asset balance must have decreased by exactly `assets`
    mathint callerBalancePost = ghostERC20Balances[_Asset][ghostCaller];
    assert(callerBalancePost == callerBalancePrev - assets);

    // The receiver's share balance must have increased by `shares`
    mathint receiverSharesPost = ghostERC20Balances[currentContract][receiver];
    assert(receiverSharesPost == receiverSharesPrev + shares);

    // The vault's total supply of shares must have increased by `shares`
    mathint vaultSharesSupplyPost = ghostERC20TotalSupply[currentContract];
    assert(vaultSharesSupplyPost == vaultSharesSupplyPrev + shares);
}

rule depositToSelfIntegrity(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Attempt deposit
    mathint shares = _ERC4626.deposit(e, assets, receiver);

    // At least one non-reverted path where `receiver` is caller
    satisfy(shares != 0 && receiver == ghostCaller);
}

// MUST support EIP-20 approve / transferFrom on asset as a deposit flow
rule depositRespectsApproveTransfer(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint allowanceBefore = ghostERC20Allowances[_Asset][ghostCaller][currentContract];

    _ERC4626.deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // Checks that the deposit logic is actually pulling tokens via “approve + transferFrom.”
    assert(allowanceBefore != max_uint256 && allowanceBefore < assets => reverted);
}

// MUST revert if all of assets cannot be deposited (due to deposit limit being reached, slippage, the 
//  user not approving enough underlying tokens to the Vault contract, etc).
rule depositMustRevertIfCannotDeposit(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint balanceBefore = ghostERC20Balances[_Asset][currentContract];

    _ERC4626.deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    mathint balanceAfter = ghostERC20Balances[_Asset][currentContract];

    // Must revert if contract doesn't receive all tokens
    assert(balanceAfter != balanceBefore + assets => reverted);

    // At least one path when balance changed correctly and not reverted
    satisfy(balanceAfter == balanceBefore + assets && !reverted);
}

rule depositPossibility(env e, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint balanceBefore = ghostERC20Balances[_Asset][currentContract];

    _ERC4626.deposit(e, assets, receiver);

    mathint balanceAfter = ghostERC20Balances[_Asset][currentContract];

    // At least one path when balance increased correctly
    satisfy(assets != 0 && balanceAfter == balanceBefore + assets);
}

//
// maxMint()
//

// MUST return the maximum amount of shares mint would allow to be deposited to receiver 
//  and not cause a revert, which MUST NOT be higher than the actual maximum that would be accepted
rule maxMintNoHigherThanActual(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Query the reported limit
    mathint limit = _ERC4626.maxMint(e, receiver);

    // Attempt mint any shares
    _ERC4626.mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // MUST NOT exceed the “true” maximum
    assert(limit != max_uint256 && limit < shares => reverted);
}

// MUST NOT rely on balanceOf of asset
rule maxMintDoesNotDependOnUserBalance(env e1, env e2, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    mathint limit1 = _ERC4626.maxMint(e1, receiver);

    // The vault must not factor the user's actual underlying asset balance
    havoc ghostERC20Balances assuming ghostERC20Balances@new[_Asset][receiver] 
        != ghostERC20Balances@old[_Asset][receiver];

    mathint limit2 = _ERC4626.maxMint(e2, receiver);

    // If global state is the same, the two calls must return the same
    assert(limit1 == limit2);
    satisfy(limit1 == limit2);
}

// MUST return 0 if mints are entirely disabled (even temporarily)
rule maxMintZeroIfDisabled(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint limit = _ERC4626.maxMint(e, receiver);

    // Try minting any shares
    mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // Always reverted with zero limit
    assert(limit == 0 => reverted);
}

// MUST return `2 ** 256 - 1` if there is no limit on the maximum amount of shares that may be minted
rule maxMintUnlimitedReturnsMax(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint limit = _ERC4626.maxMint(e, receiver);

    // Attempt mint
    _ERC4626.mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // If mint did NOT revert at a large number, we interpret that as “no limit.”
    // Then EIP-4626 says maxMint must be 2^256-1
    assert(!reverted => limit == max_uint256);
}

// MUST NOT revert
rule maxMintMustNotRevert(env e, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    _ERC4626.maxMint@withrevert(e, receiver);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewMint()
//

// MUST return as close to and no fewer than the exact amount of assets that would be 
//  deposited in a mint call in the same transaction
rule previewMintNoFewerThanActualAssets(env e, uint256 shares, address receiver) {
    
    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint previewedAssets = _ERC4626.previewMint(e, shares);

    mathint actualAssets = _ERC4626.mint(e, shares, receiver);

    // EIP-4626 says: mint(...) >= previewMint(...) in terms of assets used
    // "no fewer than the exact amount"
    assert(actualAssets >= previewedAssets);
    satisfy(actualAssets >= previewedAssets);
}

// MUST NOT account for mint limits like those returned from maxMint and should 
//  always act as though the mint would be accepted
rule previewMintMustIgnoreLimits(env e, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint allowance = ghostERC20Allowances[_Asset][ghostCaller][currentContract];
    mathint sharesLimit = _ERC4626.maxMint(e, ghostCaller);

    mathint assets = _ERC4626.previewMint(e, shares);

    // Preview mint even when user don't have "enough tokens approved"
    satisfy(allowance == 0 => assets != 0);

    // Preview mint even when user "maxMint" limit is exceeded 
    satisfy(sharesLimit < shares => assets != 0);
}

// MUST be inclusive of deposit fees. Integrators should be aware of the existence of deposit fees
rule previewMintMustIncludeFees(env e, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64); 

    mathint pm = _ERC4626.previewMint(e, shares);
    mathint cta = _ERC4626.convertToAssets(e, shares);

    // Because deposit fees => user needs more assets => pm >= cta
    // If no fees, pm == cta. But never < cta.
    assert(pm >= cta);
    satisfy(pm >= cta);
}

// MUST NOT revert due to vault specific user/global limits 
//  (i.e. MUST NOT show any variations depending on the caller)
rule previewMintMustNotDependOnCaller(env e1, env e2, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint pm1 = _ERC4626.previewMint(e1, shares) at init;
    mathint pm2 = _ERC4626.previewMint(e2, shares) at init;

    // If the vault state is identical, the results must match
    assert(pm1 == pm2);
    satisfy(pm1 == pm2);
}

// MAY revert due to other conditions that would also cause `mint` to revert
rule previewMintMayRevertOnlyWithMintRevert(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Save current storage
    storage init = lastStorage;

    // Attempt the real mint
    _ERC4626.mint@withrevert(e, shares, receiver) at init;
    bool mintReverted = lastReverted;

    // Attempt previewMint
    _ERC4626.previewMint@withrevert(e, shares) at init;
    bool previewReverted = lastReverted;

    // previewMint may revert only if mint also reverts (e.g. overflow)
    assert(previewReverted => mintReverted);
}

//
// mint()
//

// Mints exactly `shares` Vault shares to `receiver` by depositing assets of underlying tokens
rule mintIntegrity(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Capture pre-state
    mathint vaultAssetsPrev         = ghostERC20Balances[_Asset][currentContract];
    mathint callerAssetBalancePrev  = ghostERC20Balances[_Asset][ghostCaller];
    mathint receiverSharesPrev      = ghostERC20Balances[currentContract][receiver];
    mathint vaultShareSupplyPrev    = ghostERC20TotalSupply[currentContract];

    // Perform the mint
    mathint actualAssetsUsed = _ERC4626.mint(e, shares, receiver);

    // Capture post-state
    mathint vaultAssetsPost         = ghostERC20Balances[_Asset][currentContract];
    mathint callerAssetBalancePost  = ghostERC20Balances[_Asset][ghostCaller];
    mathint receiverSharesPost      = ghostERC20Balances[currentContract][receiver];
    mathint vaultShareSupplyPost    = ghostERC20TotalSupply[currentContract];

    // The vault’s asset balance must have increased by exactly `actualAssetsUsed`
    assert(vaultAssetsPost == vaultAssetsPrev + actualAssetsUsed);

    // The caller’s asset balance must have decreased by exactly that same `actualAssetsUsed`
    assert(callerAssetBalancePost == callerAssetBalancePrev - actualAssetsUsed);

    // The receiver’s share balance must have increased by `shares`
    assert(receiverSharesPost == receiverSharesPrev + shares);

    // The vault’s total share supply must have increased by `shares`
    assert(vaultShareSupplyPost == vaultShareSupplyPrev + shares);
}

rule mintToSelfIntegrity(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Perform the mint
    _ERC4626.mint(e, shares, receiver);

    // At least one non-reverted path where `receiver` is caller
    satisfy(shares != 0 && receiver == ghostCaller);
}

// MUST support EIP-20 approve / transferFrom on asset as a mint flow
rule mintRespectsApproveTransfer(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Snapshot the caller’s allowance and needed assets prior to calling mint
    mathint allowanceBefore = ghostERC20Allowances[_Asset][ghostCaller][currentContract];
    mathint neededAssets = _ERC4626.previewMint(e, shares);

    // Select code flow where user doesn't allow unlimited allowance to the Vault
    require(allowanceBefore != max_uint256);

    // Attempt the mint
    _ERC4626.mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // Checks that the mint logic is actually pulling tokens via “approve + transferFrom.”
    assert(allowanceBefore < neededAssets => reverted);
}

// MUST revert if all of `shares` cannot be minted (due to limit reached, user not approving enough tokens, etc.)
rule mintMustRevertIfCannotMint(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint receiverSharesBefore = ghostERC20Balances[currentContract][receiver];

    // Attempt the mint
    _ERC4626.mint@withrevert(e, shares, receiver);
    bool mintReverted = lastReverted;

    mathint receiverSharesAfter = ghostERC20Balances[currentContract][receiver];

    // If the receiver's share balance did not increase by the required amount for these shares,
    //    EIP-4626 says it MUST revert
    assert(receiverSharesAfter != receiverSharesBefore + shares => mintReverted);
    assert(!mintReverted => receiverSharesAfter == receiverSharesBefore + shares);

}

rule mintPossibility(env e, uint256 shares, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint receiverSharesBefore = ghostERC20Balances[currentContract][receiver];

    _ERC4626.mint(e, shares, receiver);

    mathint receiverSharesAfter = ghostERC20Balances[currentContract][receiver];

    // At least one path when balance changed correctly and not reverted
    satisfy(shares != 0 && receiverSharesAfter == receiverSharesBefore + shares);
}

//
// maxWithdraw()
//

// MUST NOT be higher than the actual maximum that would be accepted 
rule maxWithdrawNoHigherThanActual(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Query the reported limit
    mathint limit = _ERC4626.maxWithdraw(e, owner);

    // Attempt a withdraw any assets amount
    _ERC4626.withdraw@withrevert(e, assets, receiver, owner);
    bool reverted = lastReverted;

    // Always revert when withdraw over the limit
    assert(assets > limit => reverted);
}

rule withdrawPossibilityUnderMaxWithdraw(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Query the reported limit
    mathint assetsLimit = _ERC4626.maxWithdraw(e, owner);

    // Attempt a withdraw any assets amount
    _ERC4626.withdraw(e, assets, receiver, owner);

    // At least one path when withdraw is possible inside limits
    satisfy(assets != 0 && assets <= assetsLimit);
}

// MUST factor in both global and user-specific limits
rule maxWithdrawDoesNotDependOnUserShares(env e1, env e2, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Query the limit first time
    mathint limit1 = _ERC4626.maxWithdraw(e1, owner);

    // Havoc the user’s share balance in the vault
    havoc ghostERC20Balances assuming
        ghostERC20Balances@new[currentContract][owner] != ghostERC20Balances@old[currentContract][owner];

    // Query the limit again in a second environment
    mathint limit2 = _ERC4626.maxWithdraw(e2, owner);

    // If global state is otherwise the same, the two calls must return the same
    assert(limit1 == limit2);
}

// MUST return 0 if withdrawals are entirely disabled
rule maxWithdrawZeroIfDisabled(env e, address owner, uint256 assets, address receiver) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint limit = _ERC4626.maxWithdraw(e, owner);

    // Attempt withdrawing any assets
    _ERC4626.withdraw@withrevert(e, assets, receiver, owner);
    bool reverted = lastReverted;

    // Always reverted with zero limit
    assert(limit == 0 => (reverted || assets == 0));
}

// MUST NOT revert
rule maxWithdrawMustNotRevert(env e, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    _ERC4626.maxWithdraw@withrevert(e, owner);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewWithdraw()
//

// MUST return as close to and no fewer than the exact amount of Vault shares that would be 
//  burned in a `withdraw` call in the same transaction
rule previewWithdrawNoFewerThanActualShares(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Compare the previewed shares vs. the actual shares burned by withdraw.
    mathint previewedShares = _ERC4626.previewWithdraw(e, assets);

    mathint sharesBurned = _ERC4626.withdraw(e, assets, receiver, owner);

    // The spec says: "withdraw should return the same or fewer shares as previewWithdraw."
    // => sharesBurned <= previewedShares
    assert(sharesBurned <= previewedShares);
    satisfy(sharesBurned <= previewedShares);
}

// MUST NOT account for withdrawal limits like those returned from `maxWithdraw` and should always act as 
//  though the withdrawal would be accepted, regardless if the user has enough shares, etc.
rule previewWithdrawMustIgnoreLimits(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint assetsLimit = _ERC4626.maxWithdraw(e, ghostCaller);
    mathint userShares = ghostERC20Balances[currentContract][ghostCaller];

    mathint previewShares = _ERC4626.previewWithdraw(e, assets);

    // Preview withdraw even when user "maxWithdraw" limit is exceeded 
    satisfy(assetsLimit < assets => previewShares != 0);

    // Preview withdraw "regardless of user shares"
    satisfy(userShares == 0 => previewShares != 0);
}

// MUST be inclusive of withdrawal fees
// Similar check already exists in `convertToSharesNotIncludeFees()` rule

// MUST NOT revert due to vault-specific user/global limits
//  (i.e. MUST NOT vary by the caller if the state is the same).
rule previewWithdrawMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint pw1 = _ERC4626.previewWithdraw(e1, assets) at init;
    mathint pw2 = _ERC4626.previewWithdraw(e2, assets) at init;

    // If the vault state didn't change, the result must be identical
    assert(pw1 == pw2);
    satisfy(pw1 == pw2);
}

// MAY revert due to other conditions that would also cause `withdraw` to revert
rule previewWithdrawMayRevertOnlyWithWithdrawRevert(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Save current storage so that the same state is tested for both calls
    storage init = lastStorage;

    // Attempt withdraw in that snapshot
    _ERC4626.withdraw@withrevert(e, assets, receiver, owner) at init;
    bool withdrawReverted = lastReverted;

    // Attempt previewWithdraw in the same snapshot
    _ERC4626.previewWithdraw@withrevert(e, assets) at init;
    bool previewReverted = lastReverted;

    // If previewWithdraw reverts, that can only happen if withdraw also reverts
    assert(previewReverted => withdrawReverted);
}

//
// withdraw()
//

// Burns shares from owner and sends exactly assets of underlying tokens to receiver
rule withdrawIntegrity(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Pre-state snapshots
    mathint ownerSharesBefore    = ghostERC20Balances[currentContract][owner];                       // The owner's share balance
    mathint vaultSharesSupplyBefore = ghostERC20TotalSupply[currentContract];                        // The vault’s total share supply
    mathint vaultAssetsBefore    = ghostERC20Balances[_Asset][currentContract]; // The vault’s asset balance
    mathint receiverAssetsBefore = ghostERC20Balances[_Asset][receiver];        // The receiver’s asset balance
    mathint ownerAllowancesBefore= ghostERC20Allowances[currentContract][owner][ghostCaller];

    // Perform the withdraw
    mathint sharesBurned = _ERC4626.withdraw(e, assets, receiver, owner);

    // Post-state snapshots
    mathint ownerSharesAfter    = ghostERC20Balances[currentContract][owner];
    mathint vaultSharesSupplyAfter = ghostERC20TotalSupply[currentContract];
    mathint vaultAssetsAfter    = ghostERC20Balances[_Asset][currentContract];
    mathint receiverAssetsAfter = ghostERC20Balances[_Asset][receiver];
    mathint ownerAllowancesAfter= ghostERC20Allowances[currentContract][owner][ghostCaller];

    // The `owner`’s share balance must have decreased by exactly `sharesBurned`
    assert(ownerSharesAfter == ownerSharesBefore - sharesBurned);

    // The vault’s total share supply must have decreased by `sharesBurned`
    assert(vaultSharesSupplyAfter == vaultSharesSupplyBefore - sharesBurned);

    // The vault’s asset balance must have decreased by `assets`
    assert(vaultAssetsAfter == vaultAssetsBefore - assets);

    // The `receiver`’s asset balance must have increased by `assets`
    //  unless `receiver` == vault, in which case it might remain unchanged
    assert(receiver != currentContract
        ? receiverAssetsAfter == receiverAssetsBefore + assets
        : receiverAssetsAfter == receiverAssetsBefore
        );

    // SHOULD check msg.sender can spend owner funds, assets needs to be converted to shares and shares 
    //  should be checked for allowance
    assert(owner != ghostCaller => 
        ownerAllowancesAfter == ownerAllowancesBefore - sharesBurned
        );
}

// MUST support a withdraw flow where the shares are burned from owner directly where msg.sender has 
//  EIP-20 approval over the shares of owner
rule withdrawFromOtherIntegrity(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Perform the withdraw
    mathint sharesBurned = _ERC4626.withdraw(e, assets, receiver, owner);

    satisfy(sharesBurned != 0 && owner != ghostCaller);
}

// MUST support a `withdraw` flow where the shares are burned from owner directly where owner is msg.sender
rule withdrawFromSelfIntegrity(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint sharesBurned = _ERC4626.withdraw(e, assets, receiver, owner);

    satisfy(sharesBurned != 0 && owner == ghostCaller);
}

// MUST revert if all of assets cannot be withdrawn
rule withdrawMustRevertIfCannotWithdraw(env e, uint256 assets, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    mathint vaultAssetsBefore = ghostERC20Balances[_Asset][currentContract];
    mathint receiverAssetsBefore = ghostERC20Balances[_Asset][receiver];

    _ERC4626.withdraw@withrevert(e, assets, receiver, owner);
    bool reverted = lastReverted;

    mathint vaultAssetsAfter = ghostERC20Balances[_Asset][currentContract];
    mathint receiverAssetsAfter = ghostERC20Balances[_Asset][receiver];

    // If a withdraw happened partially => revert 
    assert(vaultAssetsBefore - assets != vaultAssetsAfter
        => reverted
    );
    assert(receiverAssetsBefore + assets != receiverAssetsAfter
        => reverted
    );
}

//
// maxRedeem()
//

// MUST return the maximum amount of shares that could be transferred from owner through `redeem`
rule maxRedeemNoHigherThanActual(env e, uint256 shares, address owner, address receiver) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidSilo0Env(e);

    // Query the reported limit
    mathint maxShares = _ERC4626.maxRedeem(e, owner);

    // Attempt redeeming `shares`
    _ERC4626.redeem@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    // Going above that limit must revert
    assert(shares > maxShares => reverted);
    assert(!reverted => shares <= maxShares);
}

// MUST return 0 if redemption is entirely disabled
rule maxRedeemZeroIfDisabled(env e, uint256 shares, address owner, address receiver) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidSilo0Env(e);

    mathint maxShares = _ERC4626.maxRedeem(e, owner);

    mathint assets = _ERC4626.redeem@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    // Redemption is entirely disabled when `maxRedeem` returns zero
    assert(maxShares == 0 => (assets == 0 || reverted));
}

// MUST NOT revert
rule maxRedeemMustNotRevert(env e, address owner) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidSilo0Env(e);

    _ERC4626.maxRedeem@withrevert(e, owner);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewRedeem()
//

// MUST return as close to and no more than the exact amount of `assets` that would
//  be withdrawn in a `redeem` call in the same transaction.
rule previewRedeemNoMoreThanActualAssets(env e, uint256 shares, address receiver, address owner) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e);

    // Compute the “previewed” assets
    mathint previewedAssets = _ERC4626.previewRedeem(e, shares);

    // Perform the actual redeem
    mathint actualAssets = _ERC4626.redeem(e, shares, receiver, owner);

    // EIP-4626: "redeem should return the same or MORE assets as previewRedeem"
    assert(actualAssets >= previewedAssets);
    satisfy(actualAssets >= previewedAssets);
}

// MUST NOT account for redemption limits like those returned from `maxRedeem`, and should always 
//  act as though the redemption would be accepted, regardless if the user has enough shares, etc.
rule previewRedeemMustIgnoreLimits(env e, uint256 shares, address receiver, address owner) {

    // Set ghost caller
    requireValidSilo0Env(e);

    mathint sharesLimit = _ERC4626.maxRedeem(e, ghostCaller);
    mathint userShares = ghostERC20Balances[currentContract][ghostCaller];

    mathint previewAssets = _ERC4626.previewRedeem(e, shares);

    // Preview redeem even when user "maxRedeem" limit is exceeded 
    satisfy(sharesLimit < shares => previewAssets != 0);

    // Preview redeem "regardless if the user has enough shares"
    satisfy(userShares == 0 => previewAssets != 0);
}

// MUST be inclusive of withdrawal fees. Integrators should be aware of existence of withdrawal fees.
//  Typically, if there's a withdrawal fee, the user receives fewer assets than the "no-fee" scenario.
//  So: previewRedeem(shares) <= convertToAssets(shares). Implemented in `convertToAssetsNotIncludeFees() rule`

// MUST NOT revert due to vault-specific user/global limits
//  (i.e. MUST NOT vary by the caller if the state is unchanged).
rule previewRedeemMustNotDependOnCaller(env e1, env e2, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0Env(e1);
    requireValidSilo0Env(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint pr1 = _ERC4626.previewRedeem(e1, shares) at init;
    mathint pr2 = _ERC4626.previewRedeem(e2, shares) at init;

    // If the vault state didn’t change, results must match
    assert(pr1 == pr2);
    satisfy(pr1 == pr2);
}

// MAY revert due to other conditions that would also cause `redeem` to revert
rule previewRedeemMayRevertOnlyWithRedeemRevert(env e, uint256 shares, address receiver, address owner) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidSilo0Env(e);

    // Save the state
    storage init = lastStorage;

    // Attempt the real redeem in that snapshot
    _ERC4626.redeem@withrevert(e, shares, receiver, owner) at init;
    bool redeemReverted = lastReverted;

    // Attempt previewRedeem in the same snapshot
    _ERC4626.previewRedeem@withrevert(e, shares) at init;
    bool previewReverted = lastReverted;

    // If previewRedeem reverts, that can only happen if redeem also reverts
    assert(previewReverted => redeemReverted);
}

//
// redeem()
//

// Burns exactly shares from owner and sends assets of underlying tokens to receiver
rule redeemIntegrity(env e, uint256 shares, address receiver, address owner) {

    // Valid environment (no msg.value, msg.sender != 0/currentContract, etc.)
    requireValidSilo0Env(e);

    // Pre-state snapshots
    mathint ownerSharesBefore       = ghostERC20Balances[currentContract][owner];                       
    mathint vaultSharesSupplyBefore = ghostERC20TotalSupply[currentContract];                         
    mathint vaultAssetsBefore       = ghostERC20Balances[_Asset][currentContract];
    mathint receiverAssetsBefore    = ghostERC20Balances[_Asset][receiver];
    mathint ownerAllowancesBefore   = ghostERC20Allowances[currentContract][owner][ghostCaller];

    // Perform redeem
    mathint assetsOut = _ERC4626.redeem(e, shares, receiver, owner);

    // Post-state snapshots
    mathint ownerSharesAfter       = ghostERC20Balances[currentContract][owner];
    mathint vaultSharesSupplyAfter = ghostERC20TotalSupply[currentContract];
    mathint vaultAssetsAfter       = ghostERC20Balances[_Asset][currentContract];
    mathint receiverAssetsAfter    = ghostERC20Balances[_Asset][receiver];
    mathint ownerAllowancesAfter   = ghostERC20Allowances[currentContract][owner][ghostCaller];

    // The `owner`’s share balance must decrease by exactly `shares`
    assert(ownerSharesAfter == ownerSharesBefore - shares);

    // The vault’s total share supply must decrease by `shares`
    assert(vaultSharesSupplyAfter == vaultSharesSupplyBefore - shares);

    // The vault’s asset balance must decrease by `assetsOut`
    assert(vaultAssetsAfter == vaultAssetsBefore - assetsOut);

    // The `receiver`’s asset balance must increase by `assetsOut`
    //  (unless `receiver == vault`, in which case it might remain unchanged)
    assert(
        receiver != currentContract
            ? receiverAssetsAfter == receiverAssetsBefore + assetsOut
            : receiverAssetsAfter == receiverAssetsBefore
    );

    // MUST support a redeem flow where the shares are burned from owner
    // directly where msg.sender has EIP-20 approval over the shares of owner.
    // i.e. if `owner != msg.sender`, we rely on allowance for shares.
    satisfy(owner != ghostCaller);

    // SHOULD check msg.sender can spend owner’s funds
    // => if `owner != msg.sender`, the allowance should be reduced by `shares`
    assert(
        owner != ghostCaller => ownerAllowancesAfter == ownerAllowancesBefore - shares
    );
}

// MUST support a redeem flow where the shares are burned from owner directly where owner is msg.sender
rule redeemFromOtherIntegrity(env e, uint256 shares, address receiver, address owner) {

    // Set ghost caller
    requireValidSilo0Env(e);

    mathint assetsOut = _ERC4626.redeem(e, shares, receiver, owner);

    // This path must succeed if `owner == msg.sender`
    satisfy(assetsOut != 0 && owner != ghostCaller);
}

// MUST support a redeem flow where the shares are burned from owner directly where owner is msg.sender
rule redeemFromSelfIntegrity(env e, uint256 shares, address receiver, address owner) {

    // Set ghost caller
    requireValidSilo0Env(e);

    mathint assetsOut = _ERC4626.redeem(e, shares, receiver, owner);

    // This path must succeed if `owner == msg.sender`
    satisfy(assetsOut != 0 && owner == ghostCaller);
}

// MUST revert if all of shares cannot be redeemed
rule redeemMustRevertIfCannotRedeem(env e, uint256 shares, address receiver, address owner) {

    // Valid environment (no msg.value, msg.sender != 0/currentContract, etc.)
    requireValidSilo0Env(e);

    mathint vaultAssetsBefore    = ghostERC20Balances[_Asset][currentContract];
    mathint receiverAssetsBefore = ghostERC20Balances[_Asset][receiver];

    mathint assetsOut = _ERC4626.redeem@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    mathint vaultAssetsAfter    = ghostERC20Balances[_Asset][currentContract];
    mathint vaultAssetsChange   = vaultAssetsBefore - vaultAssetsAfter;

    mathint receiverAssetsAfter = ghostERC20Balances[_Asset][receiver];
    mathint receiverAssetsChange= receiverAssetsAfter - receiverAssetsBefore;

    // If partial redemption happened, must revert
    assert(vaultAssetsChange != receiverAssetsChange || vaultAssetsChange != assetsOut
        => reverted
    );
}
