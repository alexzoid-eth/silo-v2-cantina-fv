import "setup/silo0/silo_0.spec";

// Sanity

use builtin rule sanity;

// Valid state

use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;
