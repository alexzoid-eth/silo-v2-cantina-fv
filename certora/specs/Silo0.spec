import "setup/silo0/silo0.spec";

import "./ValidState.spec";
import "./ERC20Integrity.spec";
import "./ERC4626Integrity.spec";

methods {

    // Remove this function from the scene in single Silo configuration 
    function _.accrueInterestForBothSilos() external 
        => NONDET DELETE;
}

// Sanity

use builtin rule sanity;

/*
// Valid State

use invariant crossReentrancyGuardOpenedOnExit;
use invariant crossReentrancyProtectionNoDoubleCall;

// ERC20 integrity

use rule totalSupplyIntegrity;
use rule balanceOfIntegrity;
use rule allowanceIntegrity;
use rule transferIntegrity;
use rule transferSupportZeroAmount;
use rule transferMustRevert;
use rule transferFromIntegrity;
use rule transferFromSupportZeroAmount;
use rule transferFromMustRevert;
use rule approveIntegrity;
use rule approveMustRevert;

// ERC4626 integrity

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
*/