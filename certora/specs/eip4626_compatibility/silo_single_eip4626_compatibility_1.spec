// Part 1. Prove contract is compatible with EIP4626 (https://eips.ethereum.org/EIPS/eip-4626)

import "./silo_single_eip4626_compatibility.spec";

use rule assetIntegrity;
use rule assetMustNotRevert;

use rule totalAssetsIntegrity;
use rule totalAssetsMustNotRevert;

use rule convertToSharesNotIncludeFeesInDeposit;
use rule convertToSharesNotIncludeFeesInWithdraw;
use rule convertToSharesMustNotDependOnCaller;
use rule convertToSharesNoSlippage;
use rule convertToSharesMustNotRevert;
use rule convertToSharesRoundTripDoesNotExceed;

use rule convertToAssetsNotIncludeFeesRedeem;
use rule convertToAssetsNotIncludeFeesMint;
use rule convertToAssetsMustNotDependOnCaller;
use rule convertToAssetsNoSlippage;
use rule convertToAssetsMustNotRevert;
use rule convertToAssetsRoundTripDoesNotExceed;
