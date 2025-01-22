// Part 3. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626_compatibility.spec";

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

use rule previewMintNoFewerThanActualAssets;
use rule previewMintMustIgnoreLimits;
use rule previewMintMustIncludeFees;
use rule previewMintMustNotDependOnCaller;
use rule previewMintMayRevertOnlyWithMintRevert;