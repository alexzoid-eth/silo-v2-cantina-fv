// Part 6. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626.spec";

use rule withdrawIntegrity;
use rule withdrawFromOtherIntegrity;
use rule withdrawFromSelfIntegrity; // @todo
use rule withdrawMustRevertIfCannotWithdraw; // @todo

use rule maxRedeemNoHigherThanActual; // @todo halted
use rule maxRedeemZeroIfDisabled; // @todo halted
use rule maxRedeemMustNotRevert; // @todo

use rule previewRedeemNoMoreThanActualAssets;
use rule previewRedeemMustIgnoreLimits;
use rule previewRedeemMustNotDependOnCaller;
use rule previewRedeemMayRevertOnlyWithRedeemRevert;

use rule redeemIntegrity; // @todo
use rule redeemFromOtherIntegrity;
use rule redeemFromSelfIntegrity;
use rule redeemMustRevertIfCannotRedeem; // @todo