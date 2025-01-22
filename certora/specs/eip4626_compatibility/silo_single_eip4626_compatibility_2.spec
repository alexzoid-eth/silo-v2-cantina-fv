// Part 2. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626_compatibility.spec";

use rule maxDepositNoHigherThanActual;
use rule maxDepositDoesNotDependOnUserBalance;
use rule maxDepositZeroIfDisabled;
use rule maxDepositUnlimitedReturnsMax;
use rule maxDepositMustNotRevert;

use rule previewDepositNoMoreThanActualShares;
use rule previewDepositMustIgnoreLimits;
use rule previewDepositMustIncludeFees;
use rule previewDepositMustNotDependOnCaller;
use rule previewDepositMayRevertOnlyWithDepositRevert;