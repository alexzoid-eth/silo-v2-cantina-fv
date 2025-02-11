// Prove collateral vault is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "../setup/silo/silo_valid_state.spec";
import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../setup/silo/hard_methods.spec";

/*
    Excluded (violated):
    - eip4626_collateral_convertToAssetsRoundTripDoesNotExceed
    - eip4626_collateral_previewRedeemNoMoreThanActualAssets
    - eip4626_collateral_previewWithdrawNoFewerThanActualShares

    Excluded (timeout):
    - eip4626_collateral_maxRedeemNoHigherThanActual
    - eip4626_collateral_maxWithdrawNoHigherThanActual
    - eip4626_collateral_maxWithdrawZeroIfDisabled
*/

//
// Asset
//

// MUST be an EIP-20 token contract
rule eip4626_collateral_assetIntegrity(env e) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    address asset = asset(e);

    assert(asset == ghostToken1);
}

// MUST NOT revert
rule eip4626_collateral_assetMustNotRevert(env e) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    asset@withrevert(e);
    
    assert(lastReverted == false);
}

//
// totalAssets()
//

// SHOULD include any compounding that occurs from yield
rule eip4626_collateral_totalAssetsIntegrity(env e) {

    // SAFE: Assume valid Silo state
    setupSilo(e);
    
    // Total available assets including compounding
    mathint expectedTotalAssets = getTotalCollateralAssetsWithInterestCVL(e, _Silo1);

    mathint totalAssets = totalAssets(e);

    assert(expectedTotalAssets == totalAssets);
}

// MUST NOT revert
rule eip4626_collateral_totalAssetsMustNotRevert(env e) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    totalAssets@withrevert(e);
    
    assert(lastReverted == false);
}

//
// convertToShares()
//

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check deposit)
rule eip4626_collateral_convertToSharesNotIncludeFeesInDeposit(env e, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Another way: previewDeposit() factors in deposit fees, so it will return fewer shares 
    //  if a fee is charged

    assert(previewDepositCollateral(e, assets) <= convertToSharesCollateral(e, assets));
}

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check withdrawal)
rule eip4626_collateral_convertToSharesNotIncludeFeesInWithdraw(env e, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Another way: previewWithdraw() includes withdrawal fees, so you typically have 
    //  to burn more shares to net the same assets

    assert(previewWithdrawCollateral(e, assets) >= convertToSharesCollateral(e, assets));
}

// MUST NOT show any variations depending on the caller
rule eip4626_collateral_convertToSharesMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    // Same storage state for both calls
    storage init = lastStorage;
    mathint shares1 = convertToSharesCollateral(e1, assets) at init;
    mathint shares2 = convertToSharesCollateral(e2, assets) at init;

    // If the function is truly caller-agnostic, the results must match
    assert(shares1 == shares2);
}

// MUST NOT revert unless due to integer overflow caused by an unreasonably large input
rule eip4626_collateral_convertToSharesMustNotRevert(env e, uint256 assets) {
    
    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);
    
    convertToSharesCollateral@withrevert(e, assets);
    bool reverted = lastReverted;

    assert(reverted == false);
}

// MUST round down towards 0
rule eip4626_collateral_convertToSharesRoundTripDoesNotExceed(env e, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64);

    // Indirectly prove that each function is rounding down. Going one way and then back will 
    //  produce no more than the original value

    uint256 shares = convertToSharesCollateral(e, assets); 
    mathint assets2 = convertToAssetsCollateral(e, shares);

    // assets2 must be <= assets, proving that convertToShares didn’t round up
    assert(assets2 <= assets);
}

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule eip4626_collateral_convertToSharesNoSlippage(env e1, env e2, uint256 assets) {

    // Assume valid Silo state
    setupSilo(e1);

    // Another way: if totalAssets and totalSupply remain the same between two calls, convertToShares 
    //  MUST return the same value

    mathint totalAssets1 = totalAssets(e1);
    mathint totalSupply1 = totalSupply(e1);
    mathint shares1 = convertToSharesCollateral(e1, assets);

    // Havoc storage
    _HelperCVL.makeUnresolvedCall(e1);

    // Assume valid Silo state with another environment
    setupSilo(e2);

    mathint totalAssets2 = totalAssets(e2);
    mathint totalSupply2 = totalSupply(e2);
    mathint shares2 = convertToSharesCollateral(e2, assets);

    // if totalAssets() and totalSupply() remain unchanged, the result must be identical
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => shares1 == shares2
        );
    satisfy(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2);
}

//
// convertToAssets()
//

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check redeem)
rule eip4626_collateral_convertToAssetsNotIncludeFeesRedeem(env e, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    // Typically, previewMint() includes deposit fees -> requires more assets to mint the same shares
    // Therefore, the "ideal scenario" convertToAssets() is >= previewRedeem() and <= previewMint()
    assert(previewRedeemCollateral(e, shares) <= convertToAssetsCollateral(e, shares));
}

// MUST NOT be inclusive of any fees that are charged against assets in the Vault (check mint)
rule eip4626_collateral_convertToAssetsNotIncludeFeesMint(env e, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    // Typically previewRedeem() includes withdrawal fees -> yields fewer assets for the same shares
    // Therefore, the "ideal scenario" convertToAssets() is >= previewRedeem() and <= previewMint()
    assert(previewMintCollateral(e, shares) >= convertToAssetsCollateral(e, shares));
}

// MUST NOT show any variations depending on the caller
rule eip4626_collateral_convertToAssetsMustNotDependOnCaller(env e1, env e2, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint assets1 = convertToAssetsCollateral(e1, shares) at init;
    mathint assets2 = convertToAssetsCollateral(e2, shares) at init;

    // If no state changed, the result should be identical regardless of the caller
    assert(assets1 == assets2);
}

// MUST NOT revert unless due to integer overflow caused by an unreasonably large input
rule eip4626_collateral_convertToAssetsMustNotRevert(env e, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64);

    convertToAssetsCollateral@withrevert(e, shares);
    assert(lastReverted == false);
}

// MUST round down towards 0
rule eip4626_collateral_convertToAssetsRoundTripDoesNotExceed(env e, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // UNSAFE: assume ERC20 total share not zero
    require(ghostERC20TotalSupply[currentContract] != 0);

    // Indirectly prove rounding down. If we convert to assets and back, 
    // we can't exceed the original shares.

    uint256 assets = convertToAssetsCollateral(e, shares);
    mathint shares2 = convertToSharesCollateral(e, assets);

    // shares2 must be <= shares, proving convertToAssets didn't round up
    assert(shares2 <= shares);
}

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule eip4626_collateral_convertToAssetsNoSlippage(env e1, env e2, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);

    // Snapshot totalAssets() and totalSupply() before first call
    mathint totalAssets1  = totalAssets(e1);
    mathint totalSupply1  = totalSupply(e1);
    mathint assets1 = convertToAssetsCollateral(e1, shares);

    // Havoc storage
    _HelperCVL.makeUnresolvedCall(e1);

    // Assume valid Silo state with another environment
    setupSilo(e2);

    // Snapshot again
    mathint totalAssets2 = totalAssets(e2);
    mathint totalSupply2 = totalSupply(e2);
    mathint assets2 = convertToAssetsCollateral(e2, shares);

    // If totalAssets() and totalSupply() are unchanged, the output must match
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => assets1 == assets2
    );
}

//
// maxDeposit()
// 

// MUST return the maximum amount of assets deposit would allow to be deposited for receiver

// MUST NOT be higher than the actual maximum that would be accepted
rule eip4626_collateral_maxDepositNoHigherThanActual(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Query the reported limit
    mathint limit = maxDepositCollateral(e, receiver);

    // Attempt deposit any assets
    depositCollateral@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // Because the spec says “it should *not* be higher than the true limit”
    assert(limit != max_uint256 && limit < assets => reverted);
} 

// MUST NOT rely on balanceOf of asset
rule eip4626_collateral_maxDepositDoesNotDependOnUserBalance(env e1, env e2, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    mathint limit1 = maxDepositCollateral(e1, receiver);

    // The vault must not factor the user's actual underlying asset balance
    havoc ghostERC20Balances assuming ghostERC20Balances@new[ghostToken1][receiver] 
        != ghostERC20Balances@old[ghostToken1][receiver];

    mathint limit2 = maxDepositCollateral(e2, receiver);

    // The spec says they SHOULD match if all else is the same (global state).
    // If deposit is truly disabled or unlimited, they must match, etc.
    assert(limit1 == limit2);
}

// MUST factor in both global and user-specific limits, like if deposits are entirely 
//  disabled (even temporarily) it MUST return 0

// MUST return 2 ** 256 - 1 if there is no limit on the maximum amount of assets that may be deposited
rule eip4626_collateral_maxDepositUnlimitedReturnsMax(env e, uint256 assets, address receiver) {
    
    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint limit = maxDepositCollateral(e, receiver);

    // If deposit(e, anyLargeNumber, receiver) DOES NOT revert,
    // that means the vault truly imposes no limit. Then maxDeposit MUST be 2^256-1.
    depositCollateral@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // If deposit did NOT revert at a very large number, we interpret that as "no limit".
    assert(reverted == false => limit == max_uint256);

    // At least one flow when mint doesn't revert with "unlimited" limits
    satisfy(limit == max_uint256 => !reverted);
}

// MUST NOT revert
rule eip4626_collateral_maxDepositMustNotRevert(env e, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    maxDepositCollateral@withrevert(e, receiver);

    assert(!lastReverted);
}

//
// previewDeposit()
//

// MUST return as close to and no more than the exact amount of Vault shares that would 
//  be minted in a deposit call in the same transaction
rule eip4626_collateral_previewDepositNoMoreThanActualShares(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint previewedShares = previewDepositCollateral(e, assets);
    mathint sharesDeposited = depositCollateral(e, assets, receiver);

    // The returned real minted shares must be at least as many as the “previewed” shares
    assert(sharesDeposited >= previewedShares);
}

// MUST NOT account for deposit limits like those returned from maxDeposit and should 
//  always act as though the deposit would be accepted, regardless if the user has enough 
//  tokens approved, etc.
rule eip4626_collateral_previewDepositMustIgnoreLimits(env e, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    bool enoughAllowance = ghostERC20Allowances[ghostToken1][ghostCaller][currentContract] >= assets;
    mathint limit = maxDepositCollateral(e, ghostCaller);

    mathint shares = previewDepositCollateral(e, assets);

    // Preview deposit even when user don't have "enough tokens approved"
    satisfy(enoughAllowance == false => shares != 0);

    // Preview deposit even when user "maxDeposit" limit is exceeded 
    satisfy(limit < assets => shares != 0);
}

// MUST be inclusive of deposit fees. Integrators should be aware of the existence of deposit fees.
rule eip4626_collateral_previewDepositMustIncludeFees(env e, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(assets < max_uint64); 

    mathint previewed = previewDepositCollateral(e, assets);
    mathint idealNoFee = convertToSharesCollateral(e, assets);

    // Because deposit fees reduce the minted shares, previewDeposit <= convertToShares
    assert(previewed <= idealNoFee);
}

// MUST NOT revert due to vault specific user/global limits
rule eip4626_collateral_previewDepositMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    // Like convertToShares or convertToAssets, previewDeposit(assets) must not change based on msg.sender
    storage init = lastStorage;
    mathint pd1 = previewDepositCollateral(e1, assets) at init;
    mathint pd2 = previewDepositCollateral(e2, assets) at init;

    assert(pd1 == pd2);
}

// MAY revert due to other conditions that would also cause deposit to revert
rule eip4626_collateral_previewDepositMayRevertOnlyWithDepositRevert(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Save current storage 
    storage init = lastStorage;

    depositCollateral@withrevert(e, assets, receiver) at init;
    bool depositReverted = lastReverted;

    previewDepositCollateral@withrevert(e, assets) at init;
    bool previewReverted = lastReverted;

    // previewDeposit() may revert only when deposit() reverts
    assert(previewReverted => depositReverted);
}

//
// deposit()
//

// Mints shares Vault shares to receiver by depositing exactly assets of underlying tokens
rule eip4626_collateral_depositIntegrity(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Pre-state checks
    mathint vaultAssetsPrev    = ghostERC20Balances[ghostToken1][currentContract];
    mathint callerBalancePrev  = ghostERC20Balances[ghostToken1][ghostCaller];
    mathint receiverSharesPrev = ghostERC20Balances[currentContract][receiver];
    mathint vaultSharesSupplyPrev = ghostERC20TotalSupply[currentContract];

    // Attempt deposit
    mathint shares = depositCollateral(e, assets, receiver);

    // Post-state checks

    // The vault's asset balance must have increased by exactly `assets`
    mathint vaultAssetsPost = ghostERC20Balances[ghostToken1][currentContract];
    assert(vaultAssetsPost == vaultAssetsPrev + assets);

    // The caller's asset balance must have decreased by exactly `assets`
    mathint callerBalancePost = ghostERC20Balances[ghostToken1][ghostCaller];
    assert(callerBalancePost == callerBalancePrev - assets);

    // The receiver's share balance must have increased by `shares`
    mathint receiverSharesPost = ghostERC20Balances[currentContract][receiver];
    assert(receiverSharesPost == receiverSharesPrev + shares);

    // The vault's total supply of shares must have increased by `shares`
    mathint vaultSharesSupplyPost = ghostERC20TotalSupply[currentContract];
    assert(vaultSharesSupplyPost == vaultSharesSupplyPrev + shares);
}

rule eip4626_collateral_depositToSelfIntegrity(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Attempt deposit
    mathint shares = depositCollateral(e, assets, receiver);

    // At least one non-reverted path where `receiver` is caller
    satisfy(shares != 0 && receiver == ghostCaller);
}

// MUST support EIP-20 approve / transferFrom on asset as a deposit flow
rule eip4626_collateral_depositRespectsApproveTransfer(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint allowanceBefore = ghostERC20Allowances[ghostToken1][ghostCaller][currentContract];

    depositCollateral@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    // Checks that the deposit logic is actually pulling tokens via “approve + transferFrom.”
    assert(allowanceBefore != max_uint256 && allowanceBefore < assets => reverted);
}

// MUST revert if all of assets cannot be deposited (due to deposit limit being reached, slippage, the 
//  user not approving enough underlying tokens to the Vault contract, etc).
rule eip4626_collateral_depositMustRevertIfCannotDeposit(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint balanceBefore = ghostERC20Balances[ghostToken1][currentContract];

    depositCollateral@withrevert(e, assets, receiver);
    bool reverted = lastReverted;

    mathint balanceAfter = ghostERC20Balances[ghostToken1][currentContract];

    // Must revert if contract doesn't receive all tokens
    assert(balanceAfter != balanceBefore + assets => reverted);
}

rule eip4626_collateral_depositPossibility(env e, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint balanceBefore = ghostERC20Balances[ghostToken1][currentContract];

    depositCollateral(e, assets, receiver);

    mathint balanceAfter = ghostERC20Balances[ghostToken1][currentContract];

    // At least one path when balance increased correctly
    satisfy(assets != 0 && balanceAfter == balanceBefore + assets);
}

//
// maxMint()
//

// MUST return the maximum amount of shares mint would allow to be deposited to receiver 
//  and not cause a revert, which MUST NOT be higher than the actual maximum that would be accepted
rule eip4626_collateral_maxMintNoHigherThanActual(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Query the reported limit
    mathint limit = maxMintCollateral(e, receiver);

    // Attempt mint any shares
    mintCollateral@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // MUST NOT exceed the “true” maximum
    assert(limit != max_uint256 && limit < shares => reverted);
}

// MUST NOT rely on balanceOf of asset
rule eip4626_collateral_maxMintDoesNotDependOnUserBalance(env e1, env e2, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    mathint limit1 = maxMintCollateral(e1, receiver);

    // The vault must not factor the user's actual underlying asset balance
    havoc ghostERC20Balances assuming ghostERC20Balances@new[ghostToken1][receiver] 
        != ghostERC20Balances@old[ghostToken1][receiver];

    mathint limit2 = maxMintCollateral(e2, receiver);

    // If global state is the same, the two calls must return the same
    assert(limit1 == limit2);
}

// MUST return 0 if mints are entirely disabled (even temporarily)
rule eip4626_collateral_maxMintZeroIfDisabled(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint limit = maxMintCollateral(e, receiver);

    // Try minting any shares
    mintCollateral@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // Always reverted with zero limit
    assert(limit == 0 => reverted);
}

// MUST return `2 ** 256 - 1` if there is no limit on the maximum amount of shares that may be minted
rule eip4626_collateral_maxMintUnlimitedReturnsMax(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint limit = maxMintCollateral(e, receiver);

    // Attempt mint
    mintCollateral@withrevert(e, shares, receiver);
    bool reverted = lastReverted;

    // If mint did NOT revert at a large number, we interpret that as “no limit.”
    // Then EIP-4626 says maxMint must be 2^256-1
    assert(!reverted => limit == max_uint256);
}

// MUST NOT revert
rule eip4626_collateral_maxMintMustNotRevert(env e, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    maxMintCollateral@withrevert(e, receiver);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewMint()
//

// MUST return as close to and no fewer than the exact amount of assets that would be 
//  deposited in a mint call in the same transaction
rule eip4626_collateral_previewMintNoFewerThanActualAssets(env e, uint256 shares, address receiver) {
    
    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint previewedAssets = previewMintCollateral(e, shares);
    mathint actualAssets = mintCollateral(e, shares, receiver);

    assert(actualAssets <= previewedAssets);
}

// MUST NOT account for mint limits like those returned from maxMint and should 
//  always act as though the mint would be accepted
rule eip4626_collateral_previewMintMustIgnoreLimits(env e, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint allowance = ghostERC20Allowances[ghostToken1][ghostCaller][currentContract];
    mathint sharesLimit = maxMintCollateral(e, ghostCaller);

    mathint assets = previewMintCollateral(e, shares);

    // Preview mint even when user don't have "enough tokens approved"
    satisfy(allowance == 0 => assets != 0);

    // Preview mint even when user "maxMint" limit is exceeded 
    satisfy(sharesLimit < shares => assets != 0);
}

// MUST be inclusive of deposit fees. Integrators should be aware of the existence of deposit fees
rule eip4626_collateral_previewMintMustIncludeFees(env e, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Solve complexity, avoiding unreasonably large input
    require(shares < max_uint64); 

    mathint pm = previewMintCollateral(e, shares);
    mathint cta = convertToAssetsCollateral(e, shares);

    // Because deposit fees => user needs more assets => pm >= cta
    // If no fees, pm == cta. But never < cta.
    assert(pm >= cta);
}

// MUST NOT revert due to vault specific user/global limits 
//  (i.e. MUST NOT show any variations depending on the caller)
rule eip4626_collateral_previewMintMustNotDependOnCaller(env e1, env e2, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint pm1 = previewMintCollateral(e1, shares) at init;
    mathint pm2 = previewMintCollateral(e2, shares) at init;

    // If the vault state is identical, the results must match
    assert(pm1 == pm2);
}

// MAY revert due to other conditions that would also cause `mint` to revert
rule eip4626_collateral_previewMintMayRevertOnlyWithMintRevert(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Save current storage
    storage init = lastStorage;

    mintCollateral@withrevert(e, shares, receiver) at init;
    bool mintReverted = lastReverted;

    previewMintCollateral@withrevert(e, shares) at init;
    bool previewReverted = lastReverted;

    // previewMint may revert only if mint also reverts (e.g. overflow)
    assert(previewReverted => mintReverted);
}

//
// mint()
//

// Mints exactly `shares` Vault shares to `receiver` by depositing assets of underlying tokens
rule eip4626_collateral_mintIntegrity(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Capture pre-state
    mathint vaultAssetsPrev         = ghostERC20Balances[ghostToken1][currentContract];
    mathint callerAssetBalancePrev  = ghostERC20Balances[ghostToken1][ghostCaller];
    mathint receiverSharesPrev      = ghostERC20Balances[currentContract][receiver];
    mathint vaultShareSupplyPrev    = ghostERC20TotalSupply[currentContract];

    // Perform the mint
    mathint actualAssetsUsed = mintCollateral(e, shares, receiver);

    // Capture post-state
    mathint vaultAssetsPost         = ghostERC20Balances[ghostToken1][currentContract];
    mathint callerAssetBalancePost  = ghostERC20Balances[ghostToken1][ghostCaller];
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

rule eip4626_collateral_mintToSelfIntegrity(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Perform the mint
    mintCollateral(e, shares, receiver);

    // At least one non-reverted path where `receiver` is caller
    satisfy(shares != 0 && receiver == ghostCaller);
}

// MUST support EIP-20 approve / transferFrom on asset as a mint flow
rule eip4626_collateral_mintRespectsApproveTransfer(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Snapshot the caller’s allowance and needed assets prior to calling mint
    mathint allowanceBefore = ghostERC20Allowances[ghostToken1][ghostCaller][currentContract];

    // Select code flow where user doesn't allow unlimited allowance to the Vault
    require(allowanceBefore != max_uint256);

    // Attempt the mint
    mathint assets = mintCollateral(e, shares, receiver);

    mathint allowanceAfter = ghostERC20Allowances[ghostToken1][ghostCaller][currentContract];

    // Checks that the mint logic is actually pulling tokens via “approve + transferFrom.”
    assert(allowanceBefore != max_uint256
        => allowanceBefore - allowanceAfter == assets
        );
}

// MUST revert if all of `shares` cannot be minted (due to limit reached, user not approving enough tokens, etc.)
rule eip4626_collateral_mintMustRevertIfCannotMint(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint receiverSharesBefore = ghostERC20Balances[currentContract][receiver];

    // Attempt the mint
    mintCollateral@withrevert(e, shares, receiver);
    bool mintReverted = lastReverted;

    mathint receiverSharesAfter = ghostERC20Balances[currentContract][receiver];

    // If the receiver's share balance did not increase by the required amount for these shares,
    //    EIP-4626 says it MUST revert
    assert(receiverSharesAfter != receiverSharesBefore + shares => mintReverted);
    assert(!mintReverted => receiverSharesAfter == receiverSharesBefore + shares);

}

rule eip4626_collateral_mintPossibility(env e, uint256 shares, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint receiverSharesBefore = ghostERC20Balances[currentContract][receiver];

    mintCollateral(e, shares, receiver);

    mathint receiverSharesAfter = ghostERC20Balances[currentContract][receiver];

    // At least one path when balance changed correctly and not reverted
    satisfy(shares != 0 && receiverSharesAfter == receiverSharesBefore + shares);
}

//
// maxWithdraw()
//

// MUST NOT be higher than the actual maximum that would be accepted 
rule eip4626_collateral_maxWithdrawNoHigherThanActual(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    storage init = lastStorage;

    // Query the reported limit
    mathint limit = maxWithdrawCollateral(e, owner) at init;

    // Attempt a withdraw any assets amount
    withdrawCollateral@withrevert(e, assets, receiver, owner) at init;
    bool reverted = lastReverted;

    // Always revert when withdraw over the limit
    assert(assets > limit => reverted);
}

rule eip4626_collateral_maxWithdrawWithdrawPossibility(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    storage init = lastStorage;

    // Query the reported limit
    mathint assetsLimit = maxWithdrawCollateral(e, owner) at init;

    // Attempt a withdraw any assets amount
    withdrawCollateral(e, assets, receiver, owner) at init;

    // At least one path when withdraw is possible inside limits
    satisfy(assets != 0 && assets <= assetsLimit);
}

// MUST factor in both global and user-specific limits

// MUST return 0 if withdrawals are entirely disabled
rule eip4626_collateral_maxWithdrawZeroIfDisabled(env e, address owner, uint256 assets, address receiver) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    storage init = lastStorage;

    mathint limit = maxWithdrawCollateral(e, owner) at init;

    // Attempt withdrawing any assets
    withdrawCollateral@withrevert(e, assets, receiver, owner) at init;
    bool reverted = lastReverted;

    // Always reverted with zero limit
    assert(limit == 0 => (reverted || assets == 0));
}

// MUST NOT revert
rule eip4626_collateral_maxWithdrawMustNotRevert(env e, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    maxWithdrawCollateral@withrevert(e, owner);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewWithdraw()
//

// MUST return as close to and no fewer than the exact amount of Vault shares that would be 
//  burned in a `withdraw` call in the same transaction
rule eip4626_collateral_previewWithdrawNoFewerThanActualShares(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Compare the previewed shares vs. the actual shares burned by withdraw.
    mathint previewedShares = previewWithdrawCollateral(e, assets);
    mathint sharesBurned = withdrawCollateral(e, assets, receiver, owner);

    // The spec says: "withdraw should return the same or fewer shares as previewWithdraw."
    // => sharesBurned <= previewedShares 
    assert(sharesBurned <= previewedShares);
}

// MUST NOT account for withdrawal limits like those returned from `maxWithdraw` and should always act as 
//  though the withdrawal would be accepted, regardless if the user has enough shares, etc.
rule eip4626_collateral_previewWithdrawMustIgnoreLimits(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint assetsLimit = maxWithdrawCollateral(e, ghostCaller);
    mathint userShares = ghostERC20Balances[currentContract][ghostCaller];

    mathint previewShares = previewWithdrawCollateral(e, assets);

    // Preview withdraw even when user "maxWithdraw" limit is exceeded 
    satisfy(assetsLimit < assets => previewShares != 0);

    // Preview withdraw "regardless of user shares"
    satisfy(userShares == 0 => previewShares != 0);
}

// MUST be inclusive of withdrawal fees
// Similar check already exists in `convertToSharesNotIncludeFees()` rule

// MUST NOT revert due to vault-specific user/global limits
//  (i.e. MUST NOT vary by the caller if the state is the same).
rule eip4626_collateral_previewWithdrawMustNotDependOnCaller(env e1, env e2, uint256 assets) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint pw1 = previewWithdrawCollateral(e1, assets) at init;
    mathint pw2 = previewWithdrawCollateral(e2, assets) at init;

    // If the vault state didn't change, the result must be identical
    assert(pw1 == pw2);
}

// MAY revert due to other conditions that would also cause `withdraw` to revert
rule eip4626_collateral_previewWithdrawMayRevertOnlyWithWithdrawRevert(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Save current storage so that the same state is tested for both calls
    storage init = lastStorage;

    withdrawCollateral@withrevert(e, assets, receiver, owner) at init;
    bool withdrawReverted = lastReverted;

    previewWithdrawCollateral@withrevert(e, assets) at init;
    bool previewReverted = lastReverted;

    // If previewWithdraw reverts, that can only happen if withdraw also reverts
    assert(previewReverted => withdrawReverted);
}

//
// withdrawCollateral()
//

// Burns shares from owner and sends exactly assets of underlying tokens to receiver
rule eip4626_collateral_withdrawIntegrity(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);
    
    // Pre-state snapshots
    mathint ownerSharesBefore    = ghostERC20Balances[currentContract][owner];
    mathint vaultSharesSupplyBefore = ghostERC20TotalSupply[currentContract];
    mathint vaultAssetsBefore    = ghostERC20Balances[ghostToken1][currentContract];
    mathint receiverAssetsBefore = ghostERC20Balances[ghostToken1][receiver];    
    
    // Perform the withdraw
    mathint sharesBurned = withdrawCollateral(e, assets, receiver, owner);
    
    // Post-state snapshots
    mathint ownerSharesAfter    = ghostERC20Balances[currentContract][owner];
    mathint vaultSharesSupplyAfter = ghostERC20TotalSupply[currentContract];
    mathint vaultAssetsAfter    = ghostERC20Balances[ghostToken1][currentContract];
    mathint receiverAssetsAfter = ghostERC20Balances[ghostToken1][receiver];

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
}

// MUST support a withdraw flow where the shares are burned from owner directly where msg.sender has 
//  EIP-20 approval over the shares of owner
rule eip4626_collateral_withdrawFromOtherIntegrity(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint ownerAllowancesBefore= ghostERC20Allowances[currentContract][owner][ghostCaller];

    // Perform the withdraw
    mathint sharesBurned = withdrawCollateral(e, assets, receiver, owner);

    mathint ownerAllowancesAfter= ghostERC20Allowances[currentContract][owner][ghostCaller];

    // SHOULD check msg.sender can spend owner funds, assets needs to be converted to shares and shares 
    //  should be checked for allowance
    assert(owner != ghostCaller => 
        ownerAllowancesAfter == ownerAllowancesBefore - sharesBurned
        );

    satisfy(sharesBurned != 0 && owner != ghostCaller);
}

// MUST support a `withdraw` flow where the shares are burned from owner directly where owner is msg.sender
rule eip4626_collateral_withdrawFromSelfIntegrity(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint sharesBurned = withdrawCollateral(e, assets, receiver, owner);

    satisfy(sharesBurned != 0 && owner == ghostCaller);
}

// MUST revert if all of assets cannot be withdrawn
rule eip4626_collateral_withdrawMustRevertIfCannotWithdraw(env e, uint256 assets, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // SAFE: Assume receiver is not current contract
    require(receiver != currentContract);

    mathint vaultAssetsBefore = ghostERC20Balances[ghostToken1][currentContract];
    mathint receiverAssetsBefore = ghostERC20Balances[ghostToken1][receiver];

    withdrawCollateral@withrevert(e, assets, receiver, owner);
    bool reverted = lastReverted;

    mathint vaultAssetsAfter = ghostERC20Balances[ghostToken1][currentContract];
    mathint receiverAssetsAfter = ghostERC20Balances[ghostToken1][receiver];

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
rule eip4626_collateral_maxRedeemNoHigherThanActual(env e, uint256 shares, address owner, address receiver) {

    // SAFE: Avoid reverting for non-zero msg.value and invalid msg.sender
    setupSilo(e);

    // Query the reported limit
    mathint maxShares = maxRedeemCollateral(e, owner);

    // Attempt redeeming `shares`
    redeemCollateral@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    // Going above that limit must revert, 2 wei rounding acceptance
    assert(shares > maxShares => reverted);
    assert(!reverted => shares <= maxShares + UNDERESTIMATION());
}

// MUST return 0 if redemption is entirely disabled
// Don't use such functional

// MUST NOT revert
rule eip4626_collateral_maxRedeemMustNotRevert(env e, address owner) {

    // SAFE: Avoid reverting for non-zero msg.value and invalid msg.sender
    setupSilo(e);

    maxRedeemCollateral@withrevert(e, owner);
    bool reverted = lastReverted;

    assert(!reverted);
}

//
// previewRedeem()
//

// MUST return as close to and no more than the exact amount of `assets` that would
//  be withdrawn in a `redeem` call in the same transaction.
rule eip4626_collateral_previewRedeemNoMoreThanActualAssets(env e, uint256 shares, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    // Compute the “previewed” assets
    mathint previewedAssets = previewRedeemCollateral(e, shares);

    // Perform the actual redeem
    mathint actualAssets = redeemCollateral(e, shares, receiver, owner);

    // EIP-4626: "redeem should return the same or MORE assets as previewRedeem"
    assert(actualAssets >= previewedAssets);
}

// MUST NOT account for redemption limits like those returned from `maxRedeem`, and should always 
//  act as though the redemption would be accepted, regardless if the user has enough shares, etc.
rule eip4626_collateral_previewRedeemMustIgnoreLimits(env e, uint256 shares, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint sharesLimit = maxRedeemCollateral(e, ghostCaller);
    mathint userShares = ghostERC20Balances[currentContract][ghostCaller];

    mathint previewAssets = previewRedeemCollateral(e, shares);

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
rule eip4626_collateral_previewRedeemMustNotDependOnCaller(env e1, env e2, uint256 shares) {

    // SAFE: Assume valid Silo state
    setupSilo(e1);
    setupSilo(e2);

    // Same timestamp, but different callers
    require(e1.block.timestamp == e2.block.timestamp);

    storage init = lastStorage;
    mathint pr1 = previewRedeemCollateral(e1, shares) at init;
    mathint pr2 = previewRedeemCollateral(e2, shares) at init;

    // If the vault state didn’t change, results must match
    assert(pr1 == pr2);
}

// MAY revert due to other conditions that would also cause `redeem` to revert
rule eip4626_collateral_previewRedeemMayRevertOnlyWithRedeemRevert(env e, uint256 shares, address receiver, address owner) {

    // SAFE: Avoid reverting for non-zero msg.value and invalid msg.sender
    setupSilo(e);

    // Save the state
    storage init = lastStorage;

    // Attempt the real redeem in that snapshot
    redeemCollateral@withrevert(e, shares, receiver, owner) at init;
    bool redeemReverted = lastReverted;

    // Attempt previewRedeem
    previewRedeemCollateral@withrevert(e, shares) at init;
    bool previewReverted = lastReverted;

    // previewRedeem may revert only if redeem also reverts
    assert(previewReverted => redeemReverted);
}

//
// redeemCollateral()
//

// Burns exactly shares from owner and sends assets of underlying tokens to receiver
rule eip4626_collateral_redeemIntegrity(env e, uint256 shares, address receiver, address owner) {

    // SAFE: Valid environment (no msg.value, msg.sender != 0/currentContract, etc.)
    setupSilo(e);

    // Pre-state snapshots
    mathint ownerSharesBefore       = ghostERC20Balances[currentContract][owner];                       
    mathint vaultSharesSupplyBefore = ghostERC20TotalSupply[currentContract];                         
    mathint vaultAssetsBefore       = ghostERC20Balances[ghostToken1][currentContract];
    mathint receiverAssetsBefore    = ghostERC20Balances[ghostToken1][receiver];

    // Perform redeem
    mathint assetsOut = redeemCollateral(e, shares, receiver, owner);

    // Post-state snapshots
    mathint ownerSharesAfter       = ghostERC20Balances[currentContract][owner];
    mathint vaultSharesSupplyAfter = ghostERC20TotalSupply[currentContract];
    mathint vaultAssetsAfter       = ghostERC20Balances[ghostToken1][currentContract];
    mathint receiverAssetsAfter    = ghostERC20Balances[ghostToken1][receiver];

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
}

// MUST support a redeem flow where the shares are burned from owner directly where msg.sender 
// has EIP-20 approval over the shares of owner.
rule eip4626_collateral_redeemFromOtherIntegrity(env e, uint256 shares, address receiver, address owner) {

    // SAFE: Assume receiver is not current contract
    require(receiver != currentContract);

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint ownerAllowancesBefore = ghostERC20Allowances[currentContract][owner][ghostCaller];

    mathint sharesBurned = redeemCollateral(e, shares, receiver, owner);

    mathint ownerAllowancesAfter = ghostERC20Allowances[currentContract][owner][ghostCaller];

    // SHOULD check msg.sender can spend owner’s funds
    // => if `owner != msg.sender`, the allowance should be reduced by `shares`

    // 1 wei rounding acceptance
    assert(owner != ghostCaller 
        => CMP_EQUAL_UP_TO(ownerAllowancesAfter, ownerAllowancesBefore - shares, 1)
    );

    // This path must succeed if `owner != msg.sender`
    satisfy(sharesBurned != 0 && owner != ghostCaller);
}

// MUST support a redeem flow where the shares are burned from owner directly where owner is msg.sender
rule eip4626_collateral_redeemFromSelfIntegrity(env e, uint256 shares, address receiver, address owner) {

    // SAFE: Assume valid Silo state
    setupSilo(e);

    mathint assetsOut = redeemCollateral(e, shares, receiver, owner);

    // This path must succeed if `owner == msg.sender`
    satisfy(assetsOut != 0 && owner == ghostCaller);
}

// MUST revert if all of shares cannot be redeemed
rule eip4626_collateral_redeemMustRevertIfCannotRedeem(env e, uint256 shares, address receiver, address owner) {

    // SAFE: Valid environment (no msg.value, msg.sender != 0/currentContract, etc.)
    setupSilo(e);

    mathint vaultAssetsBefore = ghostERC20Balances[ghostToken1][currentContract];
    mathint receiverAssetsBefore = ghostERC20Balances[ghostToken1][receiver];

    mathint assetsOut = redeemCollateral@withrevert(e, shares, receiver, owner);
    bool reverted = lastReverted;

    mathint vaultAssetsAfter = ghostERC20Balances[ghostToken1][currentContract];
    mathint vaultAssetsChange = vaultAssetsBefore - vaultAssetsAfter;

    mathint receiverAssetsAfter = ghostERC20Balances[ghostToken1][receiver];
    mathint receiverAssetsChange= receiverAssetsAfter - receiverAssetsBefore;

    // If partial redemption happened, must revert
    assert(vaultAssetsChange != receiverAssetsChange || vaultAssetsChange != assetsOut
        => reverted
    );
}
