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
use invariant onlyOneDebtPerBorrower;
use invariant borrowerCollateralSiloMustMatchDebt;
use invariant zeroDebtMeansNoCollateralSilo;

// Silo0

use invariant silo0ProtectedCollateralAlwaysLiquid;
use invariant silo0LiquiditySolvency;
use invariant silo0TotalTrackedAssetsNotExceedERC20TokenSupply; // @todo 

use invariant silo0ProtectedSharesMustBeBackedWithAssets; // @todo 
use invariant silo0CollateralSharesMustBeBackedWithAssets; // @todo 
use invariant silo0DebtSharesMustBeBackedWithAssets; // @todo 

use invariant silo0AllProtectedSharesAlwaysWithdrawable; // @todo 

// Sanity 

rule sanitySilo0ValidState(method f, env e, calldataarg args) {

    // SAFE: Assume valid Silo0 state
    requireValidSilo0E(e);
    
    f(e, args);
    
    // Check all external methods are reachable with valid state
    satisfy(true);
}   
