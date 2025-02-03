// PartialLiquidation sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../invariants.spec";

rule sanity_liquidationCall_noSToken_noBypass_protectedAllowed(env e, calldataarg args) {
    setupSilo(e);
    liquidationCall_noSToken_noBypass_protectedAllowed(e, args);
    satisfy(true);
}

rule sanity_liquidationCall_receiveSToken_bypassInterest_protectedAllowed(env e, calldataarg args) {
    setupSilo(e);
    liquidationCall_receiveSToken_bypassInterest_protectedAllowed(e, args);
    satisfy(true);
}

rule sanity_liquidationCall_noSToken_bypassInterest_collateralAllowed(env e, calldataarg args) {
    setupSilo(e);
    liquidationCall_noSToken_bypassInterest_collateralAllowed(e, args);
    satisfy(true);
}

rule sanity_liquidationCall_receiveSToken_bypassInterest_collateralAllowed(env e, calldataarg args) {
    setupSilo(e);
    liquidationCall_receiveSToken_bypassInterest_collateralAllowed(e, args);
    satisfy(true);
}