# List of rule names extracted from the provided ruleset
rule_names = [
    "eip4626_protected_assetIntegrity",
    "eip4626_protected_assetMustNotRevert",
    "eip4626_protected_totalAssetsIntegrity",
    "eip4626_protected_totalAssetsMustNotRevert",
    "eip4626_protected_convertToSharesNotIncludeFeesInDeposit",
    "eip4626_protected_convertToSharesNotIncludeFeesInWithdraw",
    "eip4626_protected_convertToSharesMustNotDependOnCaller",
    "eip4626_protected_convertToSharesMustNotRevert",
    "eip4626_protected_convertToSharesRoundTripDoesNotExceed",
    "eip4626_protected_convertToSharesNoSlippage",
    "eip4626_protected_convertToAssetsNotIncludeFeesRedeem",
    "eip4626_protected_convertToAssetsNotIncludeFeesMint",
    "eip4626_protected_convertToAssetsMustNotDependOnCaller",
    "eip4626_protected_convertToAssetsMustNotRevert",
    #"eip4626_protected_convertToAssetsRoundTripDoesNotExceed",
    "eip4626_protected_convertToAssetsNoSlippage",
    "eip4626_protected_maxDepositNoHigherThanActual",
    "eip4626_protected_maxDepositDoesNotDependOnUserBalance",
    "eip4626_protected_maxDepositUnlimitedReturnsMax",
    "eip4626_protected_maxDepositMustNotRevert",
    "eip4626_protected_previewDepositNoMoreThanActualShares",
    "eip4626_protected_previewDepositMustIgnoreLimits",
    "eip4626_protected_previewDepositMustIncludeFees",
    "eip4626_protected_previewDepositMustNotDependOnCaller",
    "eip4626_protected_previewDepositMayRevertOnlyWithDepositRevert",
    "eip4626_protected_depositIntegrity",
    "eip4626_protected_depositToSelfIntegrity",
    "eip4626_protected_depositRespectsApproveTransfer",
    "eip4626_protected_depositMustRevertIfCannotDeposit",
    "eip4626_protected_depositPossibility",
    "eip4626_protected_maxMintNoHigherThanActual",
    "eip4626_protected_maxMintDoesNotDependOnUserBalance",
    "eip4626_protected_maxMintZeroIfDisabled",
    "eip4626_protected_maxMintUnlimitedReturnsMax",
    "eip4626_protected_maxMintMustNotRevert",
    "eip4626_protected_previewMintNoFewerThanActualAssets",
    "eip4626_protected_previewMintMustIgnoreLimits",
    "eip4626_protected_previewMintMustIncludeFees",
    "eip4626_protected_previewMintMustNotDependOnCaller",
    "eip4626_protected_previewMintMayRevertOnlyWithMintRevert",
    "eip4626_protected_mintIntegrity",
    "eip4626_protected_mintToSelfIntegrity",
    "eip4626_protected_mintRespectsApproveTransfer",
    "eip4626_protected_mintMustRevertIfCannotMint",
    "eip4626_protected_mintPossibility",
    #"eip4626_protected_maxWithdrawNoHigherThanActual",
    "eip4626_protected_maxWithdrawWithdrawPossibility",
    #"eip4626_protected_maxWithdrawZeroIfDisabled",
    "eip4626_protected_maxWithdrawMustNotRevert",
    "eip4626_protected_previewWithdrawNoFewerThanActualShares",
    "eip4626_protected_previewWithdrawMustIgnoreLimits",
    "eip4626_protected_previewWithdrawMustNotDependOnCaller",
    "eip4626_protected_previewWithdrawMayRevertOnlyWithWithdrawRevert",
    "eip4626_protected_withdrawIntegrity",
    "eip4626_protected_withdrawFromOtherIntegrity",
    "eip4626_protected_withdrawFromSelfIntegrity",
    "eip4626_protected_withdrawMustRevertIfCannotWithdraw",
    #"eip4626_protected_maxRedeemNoHigherThanActual",
    "eip4626_protected_maxRedeemMustNotRevert",
    "eip4626_protected_previewRedeemNoMoreThanActualAssets",
    "eip4626_protected_previewRedeemMustIgnoreLimits",
    "eip4626_protected_previewRedeemMustNotDependOnCaller",
    "eip4626_protected_previewRedeemMayRevertOnlyWithRedeemRevert",
    "eip4626_protected_redeemIntegrity",
    "eip4626_protected_redeemFromOtherIntegrity",
    "eip4626_protected_redeemFromSelfIntegrity",
    "eip4626_protected_redeemMustRevertIfCannotRedeem"
]
