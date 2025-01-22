import "setup/silo_full.spec";

// Valid state

use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;