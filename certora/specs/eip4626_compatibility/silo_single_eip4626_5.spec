// Part 5. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626.spec";

use rule mintIntegrity;
use rule mintRespectsApproveTransfer; // @todo
use rule mintMustRevertIfCannotMint;
use rule mintPossibility;

use rule maxWithdrawNoHigherThanActual; // @todo halted
use rule withdrawPossibilityUnderMaxWithdraw;
use rule maxWithdrawDoesNotDependOnUserShares; // @todo halted
use rule maxWithdrawZeroIfDisabled; // @todo halted
use rule maxWithdrawMustNotRevert; // @todo

use rule previewWithdrawNoFewerThanActualShares; // @todo 
use rule previewWithdrawMustIgnoreLimits;
use rule previewWithdrawMustNotDependOnCaller;
use rule previewWithdrawMayRevertOnlyWithWithdrawRevert;