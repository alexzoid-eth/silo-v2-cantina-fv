import "setup/silo0/silo_0.spec";

// ERC20

use invariant erc20TotalSupplySolvency; // filtered { f -> f.selector == sig:transfer(address, uint256).selector }

// Silo config

use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;

// Share token

use invariant shareTokenHooksSynchronization;

// Silo 

use invariant interestRateTimestampNotInFuture;

// Silo0

use invariant silo0ProtectedCollateralAlwaysLiquid;
use invariant silo0TotalDebtNotExceedCollateral;