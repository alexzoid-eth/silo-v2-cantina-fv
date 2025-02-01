// PartialLiquidation sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../invariants.spec";

rule sanity_liquidationCall_receiveSTokenTrue(env e, calldataarg args) {
    setupSilo(e);
    liquidationCall_receiveSTokenTrue(e, args);
    satisfy(true);
}

rule sanity_liquidationCall_receiveSTokenFalse(env e, calldataarg args) {
    setupSilo(e);
    liquidationCall_receiveSTokenTrue(e, args);
    satisfy(true);
}