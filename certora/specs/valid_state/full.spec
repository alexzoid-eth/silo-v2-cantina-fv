// Silo valid state invariants for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";

// ERC20
use invariant erc20TotalSupplySolvency;

// Silo config
use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;

// Silo
use invariant interestRateTimestampNotInFuture;
use invariant zeroCollateralMeansZeroDebt;
use invariant onlyOneDebtPerBorrower;
use invariant borrowerCollateralSiloMustMatchDebt;
use invariant zeroDebtMeansNoCollateralSilo;
use invariant protectedCollateralAlwaysLiquid;
use invariant liquiditySolvency;
use invariant totalTrackedAssetsNotExceedERC20TokenSupply; // @todo 
use invariant protectedSharesMustBeBackedWithAssets; // @todo 
use invariant collateralSharesMustBeBackedWithAssets; // @todo 
use invariant debtSharesMustBeBackedWithAssets; // @todo 
use invariant siloMustNotHaveUserAllowances;