import "setup/silo0/silo_0.spec";

// Silo config

use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;

// Share token

use invariant shareTokenHooksSynchronization;

// Silo 

use invariant interestRateTimestampNotInFuture;

// Silo0

use invariant protectedAssetsNotExceedBalance;
use invariant totalDebtNotExceedCollateral;