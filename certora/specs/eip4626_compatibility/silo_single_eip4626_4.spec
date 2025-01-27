// Part 4. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626.spec";

use rule depositIntegrity;
use rule depositToSelfIntegrity;
use rule depositRespectsApproveTransfer;
use rule depositMustRevertIfCannotDeposit;
use rule depositPossibility;

use rule maxMintNoHigherThanActual;
use rule maxMintDoesNotDependOnUserBalance;
use rule maxMintZeroIfDisabled;
use rule maxMintUnlimitedReturnsMax;
use rule maxMintMustNotRevert;

use rule previewMintNoFewerThanActualAssets; // @todo valid state for shares
use rule previewMintMustIgnoreLimits;
use rule previewMintMustIncludeFees;
use rule previewMintMustNotDependOnCaller;
use rule previewMintMayRevertOnlyWithMintRevert;