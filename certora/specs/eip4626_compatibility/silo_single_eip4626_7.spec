// Part 7. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626.spec";

using HavocState as _HavocState;

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule convertToSharesNoSlippage(env e1, env e2, uint256 assets) {

    // Assume valid Silo0 state
    requireValidSilo0E(e1);

    // Another way: if totalAssets and totalSupply remain the same between two calls, convertToShares 
    //  MUST return the same value

    mathint totalAssets1 = _ERC4626.totalAssets(e1);
    mathint totalSupply1 = _ERC4626.totalSupply(e1);
    mathint shares1 = _ERC4626.convertToShares(e1, assets);

    // Havoc storage
    _HavocState.makeUnresolvedCall(e1);

    // Assume valid Silo0 state with another environment
    requireValidSilo0E(e2);

    mathint totalAssets2 = _ERC4626.totalAssets(e2);
    mathint totalSupply2 = _ERC4626.totalSupply(e2);
    mathint shares2 = _ERC4626.convertToShares(e2, assets);

    // if totalAssets() and totalSupply() remain unchanged, the result must be identical
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => shares1 == shares2
        );
    satisfy(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2);
}

// MUST NOT reflect slippage or other on-chain conditions, when performing the actual exchange
rule convertToAssetsNoSlippage(env e1, env e2, uint256 shares) {

    // Assume valid Silo0 state
    requireValidSilo0E(e1);

    // Snapshot totalAssets() and totalSupply() before first call
    mathint totalAssets1  = _ERC4626.totalAssets(e1);
    mathint totalSupply1  = _ERC4626.totalSupply(e1);
    mathint assets1 = _ERC4626.convertToAssets(e1, shares);

    // Havoc storage
    _HavocState.makeUnresolvedCall(e1);

    // Assume valid Silo0 state with another environment
    requireValidSilo0E(e2);

    // Snapshot again
    mathint totalAssets2 = _ERC4626.totalAssets(e2);
    mathint totalSupply2 = _ERC4626.totalSupply(e2);
    mathint assets2 = _ERC4626.convertToAssets(e2, shares);

    // If totalAssets() and totalSupply() are unchanged, the output must match
    assert(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2 
        => assets1 == assets2
    );
    satisfy(totalAssets1 == totalAssets2 && totalSupply1 == totalSupply2);
}
