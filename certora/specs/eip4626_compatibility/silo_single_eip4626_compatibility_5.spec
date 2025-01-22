// Part 5. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626_compatibility.spec";

use rule mintIntegrity;
use rule mintRespectsApproveTransfer;
use rule mintMustRevertIfCannotMint;
use rule mintPossibility;

use rule maxWithdrawNoHigherThanActual;
use rule withdrawPossibilityUnderMaxWithdraw;
use rule maxWithdrawDoesNotDependOnUserShares;
use rule maxWithdrawZeroIfDisabled;
use rule maxWithdrawMustNotRevert;

use rule previewWithdrawNoFewerThanActualShares;
use rule previewWithdrawMustIgnoreLimits;
use rule previewWithdrawMustNotDependOnCaller;
use rule previewWithdrawMayRevertOnlyWithWithdrawRevert;