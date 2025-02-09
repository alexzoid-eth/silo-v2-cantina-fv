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

// @todo https://prover.certora.com/output/52567/fd2e1930193e4d30b33cc13b58a3e91c?anonymousKey=810711b72840036209925ed32bba9874fcd32893
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

// @todo https://prover.certora.com/output/52567/aef1d0e36c2843b3a86be170873a452c?anonymousKey=0b22b51d7749995e05163292a882d4067c1e0d9d
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

// @todo https://prover.certora.com/output/52567/c614655c74e94edb94f2c629e3eff909?anonymousKey=9cfc4bddaf5ff09e317d1517b631ec9bd51edb9a
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