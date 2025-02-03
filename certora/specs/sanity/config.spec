// SiloConfig sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";
import "../invariants.spec";

rule sanity_others(method f, env e, calldataarg args) filtered { f->
    // Don't assume valid state as it requires disabled reentrancy protection
    f.selector != sig:turnOffReentrancyProtection().selector
} {
    setupSilo(e);
    f(e, args);
    satisfy(true);
}
