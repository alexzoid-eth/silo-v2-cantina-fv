import "setup/silo_full.spec";

// Sanity

use builtin rule sanity;

// Valid state

use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;