// Prove that ERC4626 is compatible with https://eips.ethereum.org/EIPS/eip-4626

methods {
    // Mark as `envfree` all functions which don't involve environments calls (msg.sender, block.timestamp etc)
    function asset() external returns (address) envfree;
    function totalAssets() external returns (uint256) envfree;
}

//
// asset()
//

// MUST be an EIP-20 token contract
rule assetIntegrity() {

    address asset = asset();

    assert(asset == ghostERC20CVLToken[0]);
}

// MUST NOT revert
rule assetMustNotRevert() {

    asset@withrevert();
    
    assert(lastReverted == false);
}

//
// totalAssets()
//

// SHOULD include any compounding that occurs from yield
rule totalAssetsIntegrity() {

    mathint totalAssets = totalAssets();

    assert(totalAssets == ghostERC20CVLBalances[asset()][currentContract]);
}

// MUST NOT revert
rule totalAssetsMustNotRevert() {

    totalAssets@withrevert();
    
    assert(lastReverted == false);
}

//
// convertToShares()
//

// MUST NOT be inclusive of any fees that are charged against assets in the Vault
rule convertToSharesNotIncludeFees(env e, uint256 assets) {

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Another way: previewDeposit() factors in deposit fees, so it will return fewer shares 
    //  if a fee is charged, previewWithdraw() includes withdrawal fees, so you typically have 
    //  to burn more shares to net the same assets

    assert(previewDeposit(e, assets) <= convertToShares(e, assets));
    satisfy(previewDeposit(e, assets) <= convertToShares(e, assets));

    assert(previewWithdraw(e, assets) >= convertToShares(e, assets));
    satisfy(previewWithdraw(e, assets) >= convertToShares(e, assets));
}

// MUST NOT show any variations depending on the caller
rule convertToSharesMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    mathint shares1 = convertToShares(e1, assets);
    mathint shares2 = convertToShares(e2, assets);

    assert(shares1 == shares2);
    satisfy(shares1 == shares2);
}

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule convertToSharesNoSlippage(env e1, env e2, uint256 assets) {

    // Another way: if totalAssets and totalSupply remain the same between two calls, convertToShares 
    //  MUST return the same value

    mathint totalAssets1 = totalAssets();
    mathint totalSupply1 = totalSupply();
    mathint shares1 = convertToShares(e1, assets);

    // Havoc storage
    method f;
    env e;
    calldataarg args;
    f(e, args);

    mathint totalAssets2 = totalAssets();
    mathint totalSupply2 = totalSupply();
    mathint shares2 = convertToShares(e2, assets);

    // if totalAssets() and totalSupply() remain unchanged, the result must be identical
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => shares1 == shares2
        );
    satisfy(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 && shares1 == shares2);
}

// MUST NOT revert unless due to integer overflow caused by an unreasonably large input
rule convertToSharesMustNotRevert(env e, uint256 assets) {
    
    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);
    
    convertToShares@withrevert(e, assets);
    bool reverted = lastReverted;

    assert(reverted == false);
}

// MUST round down towards 0
rule convertToSharesRoundTripDoesNotExceed(env e, uint256 assets) {

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Indirectly prove that each function is rounding down. Going one way and then back will 
    //  produce no more than the original value

    uint256 shares = convertToShares(e, assets);
    mathint assets2 = convertToAssets(e, shares);

    // assets2 must be <= assets, proving that convertToShares didn’t round up
    assert(assets2 <= assets);
    satisfy(assets2 <= assets);
}

//
// convertToAssets()
//

// MUST NOT be inclusive of any fees that are charged against assets in the Vault
rule convertToAssetsNotIncludeFees(env e, uint256 shares) {

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    // Typically, previewMint() includes deposit fees -> requires more assets to mint the same shares
    // previewRedeem() includes withdrawal fees -> yields fewer assets for the same shares
    // Therefore, the "ideal scenario" convertToAssets() is >= previewRedeem() and <= previewMint()

    assert(previewRedeem(e, shares) <= convertToAssets(e, shares));
    satisfy(previewRedeem(e, shares) <= convertToAssets(e, shares));

    assert(previewMint(e, shares) >= convertToAssets(e, shares));
    satisfy(previewMint(e, shares) >= convertToAssets(e, shares));
}

// MUST NOT show any variations depending on the caller
rule convertToAssetsMustNotDependOnCaller(env e1, env e2, uint256 shares) {
    mathint assets1 = convertToAssets(e1, shares);
    mathint assets2 = convertToAssets(e2, shares);

    // If no state changed, the result should be identical regardless of the caller
    assert(assets1 == assets2);
    satisfy(assets1 == assets2);
}

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule convertToAssetsNoSlippage(env e1, env e2, uint256 shares) {

    // Snapshot totalAssets() and totalSupply() before first call
    mathint totalAssets1  = totalAssets();
    mathint totalSupply1  = totalSupply();
    mathint assets1 = convertToAssets(e1, shares);

    // "Havoc" the contract by calling an arbitrary method (f), but if it does not affect 
    // totalAssets/totalSupply, then convertToAssets must remain the same
    method f;
    env e;
    calldataarg args;
    f(e, args);

    // Snapshot again
    mathint totalAssets2 = totalAssets();
    mathint totalSupply2 = totalSupply();
    mathint assets2 = convertToAssets(e2, shares);

    // If totalAssets() and totalSupply() are unchanged, the output must match
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => assets1 == assets2
    );
    satisfy(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 && assets1 == assets2);
}

// MUST NOT revert unless due to integer overflow caused by an unreasonably large input
rule convertToAssetsMustNotRevert(env e, uint256 shares) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    convertToAssets@withrevert(e, shares);
    assert(lastReverted == false);
}

// MUST round down towards 0
rule convertToAssetsRoundTripDoesNotExceed(env e, uint256 shares) {

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    // Indirectly prove rounding down. If we convert to assets and back, 
    // we can't exceed the original shares.

    uint256 assets = convertToAssets(e, shares);
    mathint shares2 = convertToShares(e, assets);

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
    // Query the reported limit
    mathint limit = maxDeposit(e, receiver);

    // Attempt deposit any assets
    deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // Because the spec says “it should *not* be higher than the true limit”
    assert(limit != max_uint256 && limit < assets => reverted);
    satisfy(limit == max_uint256 => !reverted);
} 

// MUST NOT rely on balanceOf of asset
rule maxDepositDoesNotDependOnUserBalance(env e1, env e2, address receiver) {

    mathint limit1 = maxDeposit(e1, receiver);

    // The vault must not factor the user's actual underlying asset balance
    havoc ghostERC20CVLBalances assuming ghostERC20CVLBalances@new[asset()][receiver] 
        != ghostERC20CVLBalances@old[asset()][receiver];

    mathint limit2 = maxDeposit(e2, receiver);

    // The spec says they SHOULD match if all else is the same (global state).
    // If deposit is truly disabled or unlimited, they must match, etc.
    assert(limit1 == limit2);
    satisfy(limit1 == limit2);
}

// MUST factor in both global and user-specific limits, like if deposits are entirely 
//  disabled (even temporarily) it MUST return 0
rule maxDepositZeroIfDisabled(env e, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    mathint limit = maxDeposit(e, receiver);

    // Attempt depositing 1
    deposit@withrevert(e, 1, receiver);
    bool reverted = lastReverted;

    // If deposit(1) reverts, then EIP-4626 says maxDeposit *must* be 0
    assert(reverted => limit == 0);

    // Not reachable when maxDeposit() returns `type(uint256).max`
}

// MUST return 2 ** 256 - 1 if there is no limit on the maximum amount of assets that may be deposited
rule maxDepositUnlimitedReturnsMax(env e, uint256 assets, address receiver) {
    
    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    mathint limit = maxDeposit(e, receiver);

    // If deposit(e, anyLargeNumber, receiver) DOES NOT revert,
    // that means the vault truly imposes no limit. Then maxDeposit MUST be 2^256-1.
    deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // If deposit did NOT revert at a very large number, we interpret that as "no limit".
    assert(reverted == false => limit == max_uint256);

    // At least one flow when mint doesn't revert with "unlimited" limits
    satisfy(limit == max_uint256 => !reverted);
}

// MUST NOT revert
rule maxDepositMustNotRevert(env e, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    maxDeposit@withrevert(e, receiver);

    assert(!lastReverted);
}

//
// previewDeposit()
//

// MUST return as close to and no more than the exact amount of Vault shares that would 
//  be minted in a deposit call in the same transaction
rule previewDepositNoMoreThanActualShares(env e, uint256 assets, address receiver) {

    mathint previewedShares = previewDeposit(e, assets);
    mathint sharesDeposited = deposit(e, assets, receiver);

    // The returned real minted shares must be at least as many as the “previewed” shares
    assert(sharesDeposited >= previewedShares);
    satisfy(sharesDeposited >= previewedShares);
}

// MUST NOT account for deposit limits like those returned from maxDeposit and should 
//  always act as though the deposit would be accepted, regardless if the user has enough 
//  tokens approved, etc.
rule previewDepositMustIgnoreLimits(env e, uint256 assets) {

    // Set ghost caller
    requireValidEnv(e);

    bool enoughAllowance = ghostERC20CVLAllowances[asset()][ghostCaller][currentContract] >= assets;
    mathint limit = maxDeposit(e, ghostCaller);

    mathint shares = previewDeposit(e, assets);

    // Preview deposit even when user don't have "enough tokens approved"
    satisfy(enoughAllowance == false => shares != 0);

    // Preview deposit even when user "maxDeposit" limit is exceeded 
    satisfy(limit < assets => shares != 0);
}

// MUST be inclusive of deposit fees. Integrators should be aware of the existence of deposit fees.
rule previewDepositMustIncludeFees(env e, uint256 assets) {

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64); 

    mathint previewed = previewDeposit(e, assets);
    mathint idealNoFee = convertToShares(e, assets);

    // Because deposit fees reduce the minted shares, previewDeposit <= convertToShares
    assert(previewed <= idealNoFee);
    satisfy(previewed <= idealNoFee);
}

// MUST NOT revert due to vault specific user/global limits
rule previewDepositMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    // Like convertToShares or convertToAssets, previewDeposit(assets) must not change based on msg.sender
    mathint pd1 = previewDeposit(e1, assets);
    mathint pd2 = previewDeposit(e2, assets);

    assert(pd1 == pd2);
    satisfy(pd1 == pd2);
}

// MAY revert due to other conditions that would also cause deposit to revert
rule previewDepositMayRevertOnlyWithDepositRevert(env e, uint256 assets, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    // Save current storage 
    storage init = lastStorage;

    deposit@withrevert(e, assets, receiver) at init;
    bool depositReverted = lastReverted;

    previewDeposit@withrevert(e, assets) at init;
    bool previewReverted = lastReverted;

    // previewDeposit() may revert only when deposit() reverts
    assert(previewReverted => depositReverted);
}

//
// deposit()
//

// Mints shares Vault shares to receiver by depositing exactly assets of underlying tokens
rule depositIntegrity(env e, uint256 assets, address receiver) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Pre-state checks
    mathint vaultAssetsPrev    = ghostERC20CVLBalances[asset()][currentContract];
    mathint callerBalancePrev  = ghostERC20CVLBalances[asset()][ghostCaller];
    mathint receiverSharesPrev = ghostERC20Balances[receiver];
    mathint vaultSharesSupplyPrev = ghostERC20TotalSupply;

    // Attempt deposit
    mathint shares = deposit(e, assets, receiver);

    // Post-state checks

    // The vault's asset balance must have increased by exactly `assets`
    mathint vaultAssetsPost = ghostERC20CVLBalances[asset()][currentContract];
    assert(vaultAssetsPost == vaultAssetsPrev + assets);

    // The caller's asset balance must have decreased by exactly `assets`
    mathint callerBalancePost = ghostERC20CVLBalances[asset()][ghostCaller];
    assert(callerBalancePost == callerBalancePrev - assets);

    // The receiver's share balance must have increased by `shares`
    mathint receiverSharesPost = ghostERC20Balances[receiver];
    assert(receiverSharesPost == receiverSharesPrev + shares);

    // The vault's total supply of shares must have increased by `shares`
    mathint vaultSharesSupplyPost = ghostERC20TotalSupply;
    assert(vaultSharesSupplyPost == vaultSharesSupplyPrev + shares);

    // At least one non-reverted path where `receiver` is caller
    satisfy(receiver == ghostCaller);
}

// MUST support EIP-20 approve / transferFrom on asset as a deposit flow
rule depositRespectsApproveTransfer(env e, uint256 assets, address receiver) {

    // Avoid reverting due non-zero msg.value, msg.sender not current contract
    requireValidEnv(e);

    mathint allowanceBefore = ghostERC20CVLAllowances[asset()][ghostCaller][currentContract];

    deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // Checks that the deposit logic is actually pulling tokens via “approve + transferFrom.”
    assert(allowanceBefore != max_uint256 && allowanceBefore < assets => reverted);
    satisfy(allowanceBefore >= assets && !reverted);
}

// MUST revert if all of assets cannot be deposited (due to deposit limit being reached, slippage, the 
//  user not approving enough underlying tokens to the Vault contract, etc).
rule depositMustRevertIfCannotDeposit(env e, uint256 assets, address receiver) {

    // Avoid reverting due non-zero msg.value, msg.sender not current contract
    requireValidEnv(e);

    mathint balanceBefore = ghostERC20CVLBalances[asset()][currentContract];

    deposit@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    mathint balanceAfter = ghostERC20CVLBalances[asset()][currentContract];

    // Must revert if contract doesn't receive all tokens
    assert(balanceAfter != balanceBefore + assets => reverted);

    // At least one path when balance changed correctly and not reverted
    satisfy(balanceAfter == balanceBefore + assets && !reverted);
}

//
// maxMint()
//

// MUST return the maximum amount of shares mint would allow to be deposited to receiver 
//  and not cause a revert, which MUST NOT be higher than the actual maximum that would be accepted
rule maxMintNoHigherThanActual(env e, uint256 shares, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    // Query the reported limit
    mathint limit = maxMint(e, receiver);

    // Attempt mint any shares
    mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // MUST NOT exceed the “true” maximum
    assert(limit != max_uint256 && limit < shares => reverted);
}

// MUST NOT rely on balanceOf of asset
rule maxMintDoesNotDependOnUserBalance(env e1, env e2, address receiver) {

    mathint limit1 = maxMint(e1, receiver);

    // The vault must not factor the user's actual underlying asset balance
    havoc ghostERC20CVLBalances assuming ghostERC20CVLBalances@new[asset()][receiver] 
        != ghostERC20CVLBalances@old[asset()][receiver];

    mathint limit2 = maxMint(e2, receiver);

    // If global state is the same, the two calls must return the same
    assert(limit1 == limit2);
    satisfy(limit1 == limit2);
}

// MUST return 0 if mints are entirely disabled (even temporarily)
rule maxMintZeroIfDisabled(env e, uint256 shares, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    mathint limit = maxMint(e, receiver);

    // Try minting any shares
    mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // Always reverted with zero limit
    assert(limit == 0 => reverted);
    satisfy(limit != 0 && !reverted);
}

// MUST return `2 ** 256 - 1` if there is no limit on the maximum amount of shares that may be minted
rule maxMintUnlimitedReturnsMax(env e, uint256 shares, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    mathint limit = maxMint(e, receiver);

    // Attempt mint
    mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // If mint did NOT revert at a large number, we interpret that as “no limit.”
    // Then EIP-4626 says maxMint must be 2^256-1
    assert(!reverted => limit == max_uint256);
}

// MUST NOT revert
rule maxMintMustNotRevert(env e, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    maxMint@withrevert(e, receiver);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewMint()
//

// MUST return as close to and no fewer than the exact amount of assets that would be 
//  deposited in a mint call in the same transaction
rule previewMintNoFewerThanActualAssets(env e, uint256 shares, address receiver) {
    
    mathint previewedAssets = previewMint(e, shares);

    mathint actualAssets = mint(e, shares, receiver);

    // EIP-4626 says: mint(...) >= previewMint(...) in terms of assets used
    // "no fewer than the exact amount"
    assert(actualAssets >= previewedAssets);
    satisfy(actualAssets >= previewedAssets);
}

// MUST NOT account for mint limits like those returned from maxMint and should 
//  always act as though the mint would be accepted
rule previewMintMustIgnoreLimits(env e, uint256 shares) {

    // Set ghost caller
    requireValidEnv(e);

    mathint allowance = ghostERC20CVLAllowances[asset()][ghostCaller][currentContract];
    mathint sharesLimit = maxMint(e, ghostCaller);

    mathint assets = previewMint(e, shares);

    // Preview mint even when user don't have "enough tokens approved"
    satisfy(allowance == 0 => assets != 0);

    // Preview mint even when user "maxMint" limit is exceeded 
    satisfy(sharesLimit < shares => assets != 0);
}

// MUST be inclusive of deposit fees. Integrators should be aware of the existence of deposit fees
rule previewMintMustIncludeFees(env e, uint256 shares) {

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64); 

    mathint pm = previewMint(e, shares);
    mathint cta = convertToAssets(e, shares);

    // Because deposit fees => user needs more assets => pm >= cta
    // If no fees, pm == cta. But never < cta.
    assert(pm >= cta);
    satisfy(pm >= cta);
}

// MUST NOT revert due to vault specific user/global limits 
//  (i.e. MUST NOT show any variations depending on the caller)
rule previewMintMustNotDependOnCaller(env e1, env e2, uint256 shares) {

    mathint pm1 = previewMint(e1, shares);
    mathint pm2 = previewMint(e2, shares);

    // If the vault state is identical, the results must match
    assert(pm1 == pm2);
    satisfy(pm1 == pm2);
}

// MAY revert due to other conditions that would also cause `mint` to revert
rule previewMintMayRevertOnlyWithMintRevert(env e, uint256 shares, address receiver) {

    // Avoid reverting due non-zero msg.value
    requireValidEnv(e);

    // Save current storage
    storage init = lastStorage;

    // Attempt the real mint
    mint@withrevert(e, shares, receiver) at init;
    bool mintReverted = lastReverted;

    // Attempt previewMint
    previewMint@withrevert(e, shares) at init;
    bool previewReverted = lastReverted;

    // previewMint may revert only if mint also reverts (e.g. overflow)
    assert(previewReverted => mintReverted);
}

//
// mint()
//

// Mints exactly `shares` Vault shares to `receiver` by depositing assets of underlying tokens
rule mintIntegrity(env e, uint256 shares, address receiver) {

    // msg.sender not current contract
    requireValidEnv(e);

    // Capture pre-state
    mathint vaultAssetsPrev         = ghostERC20CVLBalances[asset()][currentContract];
    mathint callerAssetBalancePrev  = ghostERC20CVLBalances[asset()][ghostCaller];
    mathint receiverSharesPrev      = ghostERC20Balances[receiver];
    mathint vaultShareSupplyPrev    = ghostERC20TotalSupply;

    // Perform the mint
    mathint actualAssetsUsed = mint(e, shares, receiver);

    // Capture post-state
    mathint vaultAssetsPost         = ghostERC20CVLBalances[asset()][currentContract];
    mathint callerAssetBalancePost  = ghostERC20CVLBalances[asset()][ghostCaller];
    mathint receiverSharesPost      = ghostERC20Balances[receiver];
    mathint vaultShareSupplyPost    = ghostERC20TotalSupply;

    // The vault’s asset balance must have increased by exactly `actualAssetsUsed`
    assert(vaultAssetsPost == vaultAssetsPrev + actualAssetsUsed);

    // The caller’s asset balance must have decreased by exactly that same `actualAssetsUsed`
    assert(callerAssetBalancePost == callerAssetBalancePrev - actualAssetsUsed);

    // The receiver’s share balance must have increased by `shares`
    assert(receiverSharesPost == receiverSharesPrev + shares);

    // The vault’s total share supply must have increased by `shares`
    assert(vaultShareSupplyPost == vaultShareSupplyPrev + shares);

    // At least one non-reverted path where `receiver` is caller
    satisfy(receiver == ghostCaller);
}

// MUST support EIP-20 approve / transferFrom on asset as a mint flow
rule mintRespectsApproveTransfer(env e, uint256 shares, address receiver) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    // Snapshot the caller’s allowance and needed assets prior to calling mint
    mathint allowanceBefore = ghostERC20CVLAllowances[asset()][ghostCaller][currentContract];
    mathint neededAssets = previewMint(e, shares);

    // Select code flow where user doesn't allow unlimited allowance to the Vault
    require(allowanceBefore != max_uint256);

    // Attempt the mint
    mint@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // Checks that the mint logic is actually pulling tokens via “approve + transferFrom.”
    assert(allowanceBefore < neededAssets => reverted);
    satisfy(allowanceBefore >= neededAssets && !reverted);
}

// MUST revert if all of `shares` cannot be minted (due to limit reached, user not approving enough tokens, etc.)
rule mintMustRevertIfCannotMint(env e, uint256 shares, address receiver) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    mathint receiverSharesBefore = ghostERC20Balances[receiver];

    // Attempt the mint
    mint@withrevert(e, shares, receiver);
    bool mintReverted = lastReverted;

    mathint receiverSharesAfter = ghostERC20Balances[receiver];

    // If the receiver's share balance did not increase by the required amount for these shares,
    //    EIP-4626 says it MUST revert
    assert(receiverSharesAfter != receiverSharesBefore + shares => mintReverted);
    assert(!mintReverted => receiverSharesAfter == receiverSharesBefore + shares);

    // At least one path when balance changed correctly and not reverted
    satisfy(receiverSharesAfter == receiverSharesBefore + shares && !mintReverted);
}

//
// maxWithdraw()
//

// MUST NOT be higher than the actual maximum that would be accepted 
rule maxWithdrawNoHigherThanActual(env e, uint256 assets, address owner, address receiver) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    // Query the reported limit
    mathint limit = maxWithdraw(e, owner);

    // Attempt a withdraw any assets amount
    withdraw@withrevert(e, assets, receiver, owner);
    bool reverted = lastReverted;

    // Always revert when withdraw over the limit
    assert(assets > limit => reverted);

    // At least one path when withdraw is possible inside limits
    satisfy(assets <= limit && !reverted);
}

// MUST factor in both global and user-specific limits
rule maxWithdrawDoesNotDependOnUserShares(env e1, env e2, address owner) {

    // Query the limit first time
    mathint limit1 = maxWithdraw(e1, owner);

    // Havoc the user’s share balance in the vault
    havoc ghostERC20Balances assuming
        ghostERC20Balances@new[owner] != ghostERC20Balances@old[owner];

    // Query the limit again in a second environment
    mathint limit2 = maxWithdraw(e2, owner);

    // If global state is otherwise the same, the two calls must return the same
    assert(limit1 == limit2);
}

// MUST return 0 if withdrawals are entirely disabled
rule maxWithdrawZeroIfDisabled(env e, address owner, uint256 assets, address receiver) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    mathint limit = maxWithdraw(e, owner);

    // Attempt withdrawing any assets
    withdraw@withrevert(e, assets, receiver, owner);
    bool reverted = lastReverted;

    // Always reverted with zero limit
    assert(limit == 0 => (reverted || assets == 0));
    satisfy(limit != 0 && !reverted);
}

// MUST NOT revert
rule maxWithdrawMustNotRevert(env e, address owner) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    maxWithdraw@withrevert(e, owner);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewWithdraw()
//

// MUST return as close to and no fewer than the exact amount of Vault shares that would be 
//  burned in a `withdraw` call in the same transaction
rule previewWithdrawNoFewerThanActualShares(env e, uint256 assets, address receiver, address owner) {

    // Compare the previewed shares vs. the actual shares burned by withdraw.
    mathint previewedShares = previewWithdraw(e, assets);

    mathint sharesBurned = withdraw(e, assets, receiver, owner);

    // The spec says: "withdraw should return the same or fewer shares as previewWithdraw."
    // => sharesBurned <= previewedShares
    assert(sharesBurned <= previewedShares);
    satisfy(sharesBurned <= previewedShares);
}

// MUST NOT account for withdrawal limits like those returned from `maxWithdraw` and should always act as 
//  though the withdrawal would be accepted, regardless if the user has enough shares, etc.
rule previewWithdrawMustIgnoreLimits(env e, uint256 assets, address receiver, address owner) {

    // Set ghost caller
    requireValidEnv(e);

    mathint assetsLimit = maxWithdraw(e, ghostCaller);
    mathint userShares = ghostERC20Balances[ghostCaller];

    mathint previewShares = previewWithdraw(e, assets);

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

    mathint pw1 = previewWithdraw(e1, assets);
    mathint pw2 = previewWithdraw(e2, assets);

    // If the vault state didn't change, the result must be identical
    assert(pw1 == pw2);
    satisfy(pw1 == pw2);
}

// MAY revert due to other conditions that would also cause `withdraw` to revert
rule previewWithdrawMayRevertOnlyWithWithdrawRevert(env e, uint256 assets, address receiver, address owner) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    // Save current storage so that the same state is tested for both calls
    storage init = lastStorage;

    // Attempt withdraw in that snapshot
    withdraw@withrevert(e, assets, receiver, owner) at init;
    bool withdrawReverted = lastReverted;

    // Attempt previewWithdraw in the same snapshot
    previewWithdraw@withrevert(e, assets) at init;
    bool previewReverted = lastReverted;

    // If previewWithdraw reverts, that can only happen if withdraw also reverts
    assert(previewReverted => withdrawReverted);
}

//
// withdraw()
//

// Burns shares from owner and sends exactly assets of underlying tokens to receiver
rule withdrawIntegrity(env e, uint256 assets, address receiver, address owner) {

    // Ensure valid environment: no msg.value, valid msg.sender, etc.
    requireValidEnv(e);

    // Pre-state snapshots
    mathint ownerSharesBefore    = ghostERC20Balances[owner];                       // The owner's share balance
    mathint vaultSharesSupplyBefore = ghostERC20TotalSupply;                        // The vault’s total share supply
    mathint vaultAssetsBefore    = ghostERC20CVLBalances[asset()][currentContract]; // The vault’s asset balance
    mathint receiverAssetsBefore = ghostERC20CVLBalances[asset()][receiver];        // The receiver’s asset balance
    mathint ownerAllowancesBefore= ghostERC20Allowances[owner][ghostCaller];

    // Perform the withdraw
    mathint sharesBurned = withdraw(e, assets, receiver, owner);

    // Post-state snapshots
    mathint ownerSharesAfter    = ghostERC20Balances[owner];
    mathint vaultSharesSupplyAfter = ghostERC20TotalSupply;
    mathint vaultAssetsAfter    = ghostERC20CVLBalances[asset()][currentContract];
    mathint receiverAssetsAfter = ghostERC20CVLBalances[asset()][receiver];
    mathint ownerAllowancesAfter= ghostERC20Allowances[owner][ghostCaller];

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

    // MUST support a withdraw flow where the shares are burned from owner directly where msg.sender has 
    //  EIP-20 approval over the shares of owner.
    satisfy(owner != ghostCaller);

    // SHOULD check msg.sender can spend owner funds, assets needs to be converted to shares and shares 
    //  should be checked for allowance
    assert(owner != ghostCaller => 
        ownerAllowancesAfter == ownerAllowancesBefore - sharesBurned
        );
}

// MUST support a `withdraw` flow where the shares are burned from owner directly where owner is msg.sender
rule withdrawOwnerIsCaller(env e, uint256 assets, address receiver, address owner) {

    // Ensure valid environment: no msg.value, valid msg.sender, etc.
    requireValidEnv(e);

    withdraw(e, assets, receiver, owner);

    satisfy(owner == ghostCaller);
}

// MUST revert if all of assets cannot be withdrawn
rule withdrawMustRevertIfCannotWithdraw(env e, uint256 assets, address receiver, address owner) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    mathint vaultAssetsBefore = ghostERC20CVLBalances[asset()][currentContract];
    mathint receiverAssetsBefore = ghostERC20CVLBalances[asset()][receiver];

    withdraw@withrevert(e, assets, receiver, owner);
    bool reverted = lastReverted;

    mathint vaultAssetsAfter = ghostERC20CVLBalances[asset()][currentContract];
    mathint receiverAssetsAfter = ghostERC20CVLBalances[asset()][receiver];

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
    requireValidEnv(e);

    // Query the reported limit
    mathint maxShares = maxRedeem(e, owner);

    // Attempt redeeming `shares`
    redeem@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    // Going above that limit must revert
    assert(shares > maxShares => reverted);
    assert(!reverted => shares <= maxShares);
}

// MUST return 0 if redemption is entirely disabled
rule maxRedeemZeroIfDisabled(env e, uint256 shares, address owner, address receiver) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    mathint maxShares = maxRedeem(e, owner);

    mathint assets = redeem@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    // Redemption is entirely disabled when `maxRedeem` returns zero
    assert(maxShares == 0 => (assets == 0 || reverted));
}

// MUST NOT revert
rule maxRedeemMustNotRevert(env e, address owner) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    maxRedeem@withrevert(e, owner);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewRedeem()
//

// MUST return as close to and no more than the exact amount of `assets` that would
//  be withdrawn in a `redeem` call in the same transaction.
rule previewRedeemNoMoreThanActualAssets(env e, uint256 shares, address receiver, address owner) {

    // Compute the “previewed” assets
    mathint previewedAssets = previewRedeem(e, shares);

    // Perform the actual redeem
    mathint actualAssets = redeem(e, shares, receiver, owner);

    // EIP-4626: "redeem should return the same or MORE assets as previewRedeem"
    assert(actualAssets >= previewedAssets);
    satisfy(actualAssets >= previewedAssets);
}

// MUST NOT account for redemption limits like those returned from `maxRedeem`, and should always 
//  act as though the redemption would be accepted, regardless if the user has enough shares, etc.
rule previewRedeemMustIgnoreLimits(env e, uint256 shares, address receiver, address owner) {

    // Set ghost caller
    requireValidEnv(e);

    mathint sharesLimit = maxRedeem(e, ghostCaller);
    mathint userShares = ghostERC20Balances[ghostCaller];

    mathint previewAssets = previewRedeem(e, shares);

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

    mathint pr1 = previewRedeem(e1, shares);
    mathint pr2 = previewRedeem(e2, shares);

    // If the vault state didn’t change, results must match
    assert(pr1 == pr2);
    satisfy(pr1 == pr2);
}

// MAY revert due to other conditions that would also cause `redeem` to revert
rule previewRedeemMayRevertOnlyWithRedeemRevert(env e, uint256 shares, address receiver, address owner) {

    // Avoid reverting for non-zero msg.value and invalid msg.sender
    requireValidEnv(e);

    // Save the state
    storage init = lastStorage;

    // Attempt the real redeem in that snapshot
    redeem@withrevert(e, shares, receiver, owner) at init;
    bool redeemReverted = lastReverted;

    // Attempt previewRedeem in the same snapshot
    previewRedeem@withrevert(e, shares) at init;
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
    requireValidEnv(e);

    // Pre-state snapshots
    mathint ownerSharesBefore       = ghostERC20Balances[owner];                       
    mathint vaultSharesSupplyBefore = ghostERC20TotalSupply;                         
    mathint vaultAssetsBefore       = ghostERC20CVLBalances[asset()][currentContract];
    mathint receiverAssetsBefore    = ghostERC20CVLBalances[asset()][receiver];
    mathint ownerAllowancesBefore   = ghostERC20Allowances[owner][ghostCaller];

    // Perform redeem
    mathint assetsOut = redeem(e, shares, receiver, owner);

    // Post-state snapshots
    mathint ownerSharesAfter       = ghostERC20Balances[owner];
    mathint vaultSharesSupplyAfter = ghostERC20TotalSupply;
    mathint vaultAssetsAfter       = ghostERC20CVLBalances[asset()][currentContract];
    mathint receiverAssetsAfter    = ghostERC20CVLBalances[asset()][receiver];
    mathint ownerAllowancesAfter   = ghostERC20Allowances[owner][ghostCaller];

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
rule redeemOwnerIsCaller(env e, uint256 shares, address receiver, address owner) {

    // Valid environment (no msg.value, msg.sender != 0/currentContract, etc.)
    requireValidEnv(e);

    redeem(e, shares, receiver, owner);

    // This path must succeed if `owner == msg.sender`
    satisfy(owner == ghostCaller);
}

// MUST revert if all of shares cannot be redeemed
rule redeemMustRevertIfCannotRedeem(env e, uint256 shares, address receiver, address owner) {

    // Valid environment (no msg.value, msg.sender != 0/currentContract, etc.)
    requireValidEnv(e);

    mathint vaultAssetsBefore    = ghostERC20CVLBalances[asset()][currentContract];
    mathint receiverAssetsBefore = ghostERC20CVLBalances[asset()][receiver];

    mathint assetsOut = redeem@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    mathint vaultAssetsAfter    = ghostERC20CVLBalances[asset()][currentContract];
    mathint vaultAssetsChange   = vaultAssetsBefore - vaultAssetsAfter;

    mathint receiverAssetsAfter = ghostERC20CVLBalances[asset()][receiver];
    mathint receiverAssetsChange= receiverAssetsAfter - receiverAssetsBefore;

    // If partial redemption happened, must revert
    assert(vaultAssetsChange != receiverAssetsChange || vaultAssetsChange != assetsOut
        => reverted
    );
}
