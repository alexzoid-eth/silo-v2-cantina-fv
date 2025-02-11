// Silo sanity for full silo configuration 

import "../setup/silo/silo_valid_state.spec";
import "../setup/silo/hard_methods.spec";
import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";

rule sanity_all(method f, env e, calldataarg args) {
    setupSilo(e);
    f(e, args);
    satisfy(true);
}