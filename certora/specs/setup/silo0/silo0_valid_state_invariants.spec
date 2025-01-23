// Silo config valid state invariants working both for Silo0

import "../silo/silo_valid_state_invariants.spec";

// Use it when env is not needed
function requireSilo0ValidState() {

    // Valid state invariants both for silo0 and silo1
    requireSiloValidState();

    requireInvariant silo0AssetBalanceNotBelowDaoAndDeployerRevenue;
}

// Use it when env matters
function requireSilo0ValidStateEnv(env e) {

    // Valid state invariants both for silo0 and silo1
    requireSiloValidStateEnv(e);

    requireSilo0ValidState();
}

// VS- The silo’s underlying asset balance must always be at least the daoAndDeployerRevenue
strong invariant silo0AssetBalanceNotBelowDaoAndDeployerRevenue()
    ghostERC20Balances[_Token0][_Silo0] >= ghostDaoAndDeployerRevenue[_Silo0];