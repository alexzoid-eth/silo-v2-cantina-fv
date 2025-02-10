// Version of `silo.spec` with support of `ALL_SSTORE`. Keep it in a separate spec because 
//  storage view is not available with `enableStorageSplitting false` option enabled

import "./silo.spec";

persistent ghost bool ghostProtectedStorageAccess;
persistent ghost bool ghostCollateralStorageAccess;
persistent ghost bool ghostDebtStorageAccess;

hook ALL_SSTORE(uint256 slot, uint256 val)  {
    if(executingContract == _Protected1) {
        ghostProtectedStorageAccess = true;
    } else if(executingContract == _Collateral1) {
        ghostCollateralStorageAccess = true;
    } else if(executingContract == _Debt1) {
        ghostDebtStorageAccess = true;
    }
}

hook ALL_SLOAD(uint256 slot) uint256 val {
    if(executingContract == _Protected1) {
        ghostProtectedStorageAccess = true;
    } else if(executingContract == _Collateral1) {
        ghostCollateralStorageAccess = true;
    } else if(executingContract == _Debt1) {
        ghostDebtStorageAccess = true;
    }
}

// @todo https://prover.certora.com/output/52567/bfcb202d793f4c48826df25eb6facb6f?anonymousKey=7a1f69bd5060b641ed409220d5d53ff4afd39ce7
// Collateral harness must not touch protected/debt storage
rule silo_collateralFunctionsNoAccessOtherVaults(env e, method f, calldataarg args)
    filtered { f -> COLLATERAL_HARNESS_FUNCTIONS(f) } 
{
    setupSilo(e);

    require(!ghostProtectedStorageAccess && !ghostDebtStorageAccess);

    // Call harness
    f(e, args);

    assert(!ghostProtectedStorageAccess && !ghostDebtStorageAccess);
}

// @todo https://prover.certora.com/output/52567/e4180377f43d4b549ae68db78b3e4aa3?anonymousKey=a101b10ccf7ba950b8490e0cc6d308fb1f2cab26
// Protected harness must not touch debt (access collateral contract as Silo)
rule silo_protectedFunctionsNoAccessOtherVaults(env e, method f, calldataarg args)
    filtered { f -> PROTECTED_HARNESS_FUNCTIONS(f) } 
{
    setupSilo(e);

    require(!ghostDebtStorageAccess);

    // Call harness
    f(e, args);

    assert(!ghostDebtStorageAccess);
}

// @todo https://prover.certora.com/output/52567/c1b02adf07414990a83411f3b7865d96?anonymousKey=c52c9ac4b0956d1e8ab4f73a26d7a316fc17ebc7
// Possibility of collateral vault read/write its own storage
rule silo_collateralFunctionsAccessOwnStorage(env e, method f, calldataarg args)
    filtered { f -> COLLATERAL_HARNESS_FUNCTIONS(f) }
{
    setupSilo(e);

    require(!ghostCollateralStorageAccess);

    f(e, args);

    // These functions return constants
    bool stateLessFunctions = (
        f.selector != sig:maxMintCollateral(address).selector
        || f.selector != sig:maxDepositCollateral(address).selector
    );

    satisfy(!stateLessFunctions
        => ghostCollateralStorageAccess
        );
}