// Import this file in full Silo configuration

import "silo0/silo_0.spec";
import "silo1/silo_1.spec";

function requireValidSiloFull() {
    requireValidSilo0();    
    requireValidSilo1();    
}

function requireValidSiloFullEnv(env e) {
    requireValidSilo0E(e);    
    requireValidSilo1E(e);    
}
