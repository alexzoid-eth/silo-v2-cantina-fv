// PartialLiquidation sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../invariants.spec";

rule sanity_liquidationCall(env e, calldataarg args) {
    setupSilo(e);
    liquidationCall(e, args);
    satisfy(true);
}

rule sanity_beforeAction(env e, calldataarg args) {
    setupSilo(e);
    beforeAction(e, args);
    satisfy(true);
}

rule sanity_afterAction(env e, calldataarg args) {
    setupSilo(e);
    afterAction(e, args);
    satisfy(true);
}