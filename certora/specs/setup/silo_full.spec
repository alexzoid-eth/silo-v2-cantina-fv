// Import this file in full Silo configuration

import "silo0/silo_0.spec";
import "silo1/silo_1.spec";

function requireValidSiloFullEnv(env e) {
    requireValidSilo0Env(e);    
    requireValidSilo1Env(e);    
}
