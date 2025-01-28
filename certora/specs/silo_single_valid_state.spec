import "setup/silo0/silo_0.spec";

// ERC20

use invariant erc20TotalSupplySolvency;

// Silo config

use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;

// Share token

use invariant shareTokenHooksSynchronization;

// Silo

use invariant interestRateTimestampNotInFuture;
use invariant zeroCollateralMeansZeroDebt;

// Silo0

use invariant silo0ProtectedCollateralAlwaysLiquid;
use invariant silo0LiquiditySolvency;
use invariant silo0TotalTrackedAssetsNotExceedERC20TokenSupply; // @todo 

use invariant silo0ProtectedSharesMustBeBackedWithAssets;
use invariant silo0CollateralSharesMustBeBackedWithAssets;
use invariant silo0DebtSharesMustBeBackedWithAssets;
use invariant silo0ProtectedSharesAlwaysWithdrawable;