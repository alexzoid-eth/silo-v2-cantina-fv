// Silo config valid state invariants working for Silo1

import "./silo_valid_state_invariants.spec";

// Use it when env is not needed
function requireSilo1ValidState() {

    // Valid state invariants both for silo0 and silo1
    requireValidSiloCommon();

}

// Use it when env matters
function requireSilo1ValidStateE(env e) {
    requireSilo1ValidState();

    // Valid state invariants both for silo0 and silo1
    requireValidSiloCommonE(e);

}

// @todo copy everything from `silo0_valid_state_invariants` changing silo0 to silo1