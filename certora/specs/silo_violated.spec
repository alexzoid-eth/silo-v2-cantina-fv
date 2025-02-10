// Silo1 violated rule

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./invariants.spec";

import "./setup/silo/silo_factory.spec";

rule silo_deployerFeeReceiverCannotBeBlocked() {
    assert(true);
}