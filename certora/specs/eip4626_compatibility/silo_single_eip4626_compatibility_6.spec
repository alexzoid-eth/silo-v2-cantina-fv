// Part 6. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626_compatibility.spec";

use rule withdrawIntegrity;
use rule withdrawFromOtherIntegrity;
use rule withdrawFromSelfIntegrity;
use rule withdrawMustRevertIfCannotWithdraw;

use rule maxRedeemNoHigherThanActual;
use rule maxRedeemZeroIfDisabled;
use rule maxRedeemMustNotRevert;

use rule previewRedeemNoMoreThanActualAssets;
use rule previewRedeemMustIgnoreLimits;
use rule previewRedeemMustNotDependOnCaller;
use rule previewRedeemMayRevertOnlyWithRedeemRevert;

use rule redeemIntegrity;
use rule redeemFromOtherIntegrity;
use rule redeemFromSelfIntegrity;
use rule redeemMustRevertIfCannotRedeem;