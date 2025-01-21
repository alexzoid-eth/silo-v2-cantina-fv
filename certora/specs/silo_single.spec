import "setup/silo0/silo_0.spec";

methods {
    // Remove this function from the scene in single Silo configuration 
    function _.accrueInterestForBothSilos() external 
        => NONDET DELETE;
}

// Sanity

use builtin rule sanity;