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

// @todo https://prover.certora.com/output/52567/972dc20e06614cbf8debe06cd71e5bba?anonymousKey=d18ddb60f2d14af1ed796054dc48375118b51663
// Collateral harness must not touch protected/debt storage, protected harness must not touch collateral/debt
rule silo_noCrossStorageAccess(env e, method f, calldataarg args)
    filtered { f -> COLLATERAL_HARNESS_FUNCTIONS(f) || PROTECTED_HARNESS_FUNCTIONS(f) } 
{
    setupSilo(e);

    require(!ghostCollateralStorageAccess && !ghostProtectedStorageAccess && !ghostDebtStorageAccess);

    // Call harness
    f(e, args);

    assert(COLLATERAL_HARNESS_FUNCTIONS(f)
        => !ghostProtectedStorageAccess && !ghostDebtStorageAccess
        );

    assert(PROTECTED_HARNESS_FUNCTIONS(f)
        => !ghostCollateralStorageAccess && !ghostDebtStorageAccess
        );
}

// @todo https://prover.certora.com/output/52567/ba67b4b7bdf84e48923a2d97cef1c5af?anonymousKey=e50cf201346909a1f15fc7e6d0fc23a4dc545ca3
// Harness may read/write its own vault
rule silo_possibilityAccessOwnStorage(env e, method f, calldataarg args)
    filtered { f -> COLLATERAL_HARNESS_FUNCTIONS(f) || PROTECTED_HARNESS_FUNCTIONS(f) }
{
    setupSilo(e);

    require(!ghostCollateralStorageAccess && !ghostProtectedStorageAccess);

    f(e, args);

    satisfy(COLLATERAL_HARNESS_FUNCTIONS(f)
        => ghostCollateralStorageAccess
    );

    satisfy(PROTECTED_HARNESS_FUNCTIONS(f)
        => ghostProtectedStorageAccess
    );
}
