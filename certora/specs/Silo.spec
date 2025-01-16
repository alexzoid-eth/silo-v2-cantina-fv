import "./ERC20Integrity.spec";
import "./ERC4626Integrity.spec";

// Sanity

// use builtin rule sanity;

// Valid State

invariant crossReentrancyGuardOpenedOnExit()
    ghostCrossReentrantStatus == _NOT_ENTERED();

// ERC20 integrity

use rule totalSupplyIntegrity;
use rule balanceOfIntegrity;
use rule allowanceIntegrity;
use rule transferIntegrity;
use rule transferMustRevert;
use rule transferFromIntegrity;
use rule transferFromMustRevert;
use rule approveIntegrity;
use rule approveMustRevert;

// ERC4626 integrity

use rule assetIntegrity;
use rule assetMustNotRevert;

use rule totalAssetsIntegrity;
use rule totalAssetsMustNotRevert;

use rule convertToSharesNotIncludeFees;
use rule convertToSharesMustNotDependOnCaller;
use rule convertToSharesNoSlippage;
use rule convertToSharesMustNotRevert;
use rule convertToSharesRoundTripDoesNotExceed;

use rule convertToAssetsNotIncludeFees;
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
use rule depositRespectsApproveTransfer;
use rule depositMustRevertIfCannotDeposit;

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

use rule maxWithdrawNoHigherThanActual;
use rule maxWithdrawDoesNotDependOnUserShares;
use rule maxWithdrawZeroIfDisabled;
use rule maxWithdrawMustNotRevert;

use rule previewWithdrawNoFewerThanActualShares;
use rule previewWithdrawMustIgnoreLimits;
use rule previewWithdrawMustNotDependOnCaller;
use rule previewWithdrawMayRevertOnlyWithWithdrawRevert;

use rule withdrawIntegrity;
use rule withdrawOwnerIsCaller;
use rule withdrawMustRevertIfCannotWithdraw;

use rule maxRedeemNoHigherThanActual;
use rule maxRedeemZeroIfDisabled;
use rule maxRedeemMustNotRevert;

use rule previewRedeemNoMoreThanActualAssets;
use rule previewRedeemMustIgnoreLimits;
use rule previewRedeemMustNotDependOnCaller;
use rule previewRedeemMayRevertOnlyWithRedeemRevert;

use rule redeemIntegrity;
use rule redeemOwnerIsCaller;
use rule redeemMustRevertIfCannotRedeem;