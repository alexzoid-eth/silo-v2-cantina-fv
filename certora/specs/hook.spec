// PartialLiquidation rules

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./invariants.spec";

rule hook_test() {
    assert(true);
}

strong invariant hook_test_inv() true;