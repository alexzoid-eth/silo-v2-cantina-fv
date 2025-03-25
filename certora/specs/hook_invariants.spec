// Hook valid state invariants working for all Silo contracts 

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./setup/silo/silo_valid_state.spec";

import "./setup/partial_liquidation/partial_liquidation.spec";

use invariant inv_eip20_totalSupplySolvency;

use invariant inv_crossReentrancyGuardOpenedOnExit;

use invariant inv_transferWithChecksAlwaysEnabled;
use invariant inv_interestRateTimestampNotInFuture;
use invariant inv_borrowerCannotHaveTwoDebts;
use invariant inv_borrowerCannotHaveDebtWithoutCollateralSet;

use invariant inv_liquiditySolvency0;
use invariant inv_liquiditySolvency1;

use invariant inv_siloMustNotHaveUserAllowances0;
use invariant inv_siloMustNotHaveUserAllowances1;

use invariant inv_protectedCollateralAlwaysLiquid0;
use invariant inv_protectedCollateralAlwaysLiquid1;

use invariant inv_zeroCollateralMeansZeroDebt0;
use invariant inv_zeroCollateralMeansZeroDebt1;