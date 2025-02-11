// PartialLiquidation rules

import "./setup/silo/silo_valid_state.spec";
import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";

import "./setup/partial_liquidation/partial_liquidation.spec";

rule hook_test(address borrower) {
    setupBorrower(borrower);
    assert(true);
}

strong invariant hook_test_inv() true;