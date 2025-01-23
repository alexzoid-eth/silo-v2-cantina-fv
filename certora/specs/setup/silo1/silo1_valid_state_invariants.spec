// Silo config valid state invariants working both for Silo0

import "../silo/silo_valid_state_invariants.spec";

// Use it when env is not needed
function requireSilo0ValidState() {

    // Valid state invariants both for silo0 and silo1
    requireSiloValidState();

    // @todo add all invariants
}

// Use it when env matters
function requireSilo0ValidStateEnv(env e) {

    requireSilo0ValidState();

    // Valid state invariants both for silo0 and silo1
    requireSiloValidStateEnv(e);

    // @todo add all invariants
}

// @todo copy everything from `silo0_valid_state_invariants` changing silo0 to silo1