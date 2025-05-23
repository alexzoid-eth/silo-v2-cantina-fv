# List of rule names extracted from the provided ruleset
rule_names = [
    "eip4626_collateral_assetIntegrity",
    "eip4626_collateral_assetMustNotRevert",
    "eip4626_collateral_totalAssetsIntegrity",
    "eip4626_collateral_totalAssetsMustNotRevert",
    "eip4626_collateral_convertToSharesNotIncludeFeesInDeposit",
    "eip4626_collateral_convertToSharesNotIncludeFeesInWithdraw",
    "eip4626_collateral_convertToSharesMustNotDependOnCaller",
    "eip4626_collateral_convertToSharesMustNotRevert",
    "eip4626_collateral_convertToSharesRoundTripDoesNotExceed",
    "eip4626_collateral_convertToSharesNoSlippage",
    "eip4626_collateral_convertToAssetsNotIncludeFeesRedeem",
    "eip4626_collateral_convertToAssetsNotIncludeFeesMint",
    "eip4626_collateral_convertToAssetsMustNotDependOnCaller",
    "eip4626_collateral_convertToAssetsMustNotRevert",
    #"eip4626_collateral_convertToAssetsRoundTripDoesNotExceed", 
    "eip4626_collateral_convertToAssetsNoSlippage",
    "eip4626_collateral_maxDepositNoHigherThanActual",
    "eip4626_collateral_maxDepositDoesNotDependOnUserBalance",
    "eip4626_collateral_maxDepositUnlimitedReturnsMax",
    "eip4626_collateral_maxDepositMustNotRevert",
    "eip4626_collateral_previewDepositNoMoreThanActualShares",
    "eip4626_collateral_previewDepositMustIgnoreLimits",
    "eip4626_collateral_previewDepositMustIncludeFees",
    "eip4626_collateral_previewDepositMustNotDependOnCaller",
    "eip4626_collateral_previewDepositMayRevertOnlyWithDepositRevert",
    "eip4626_collateral_depositIntegrity",
    "eip4626_collateral_depositToSelfIntegrity",
    "eip4626_collateral_depositRespectsApproveTransfer",
    "eip4626_collateral_depositMustRevertIfCannotDeposit",
    "eip4626_collateral_depositPossibility",
    "eip4626_collateral_maxMintNoHigherThanActual",
    "eip4626_collateral_maxMintDoesNotDependOnUserBalance",
    "eip4626_collateral_maxMintZeroIfDisabled",
    "eip4626_collateral_maxMintUnlimitedReturnsMax",
    "eip4626_collateral_maxMintMustNotRevert",
    "eip4626_collateral_previewMintNoFewerThanActualAssets",
    "eip4626_collateral_previewMintMustIgnoreLimits",
    "eip4626_collateral_previewMintMustIncludeFees",
    "eip4626_collateral_previewMintMustNotDependOnCaller",
    "eip4626_collateral_previewMintMayRevertOnlyWithMintRevert",
    "eip4626_collateral_mintIntegrity",
    "eip4626_collateral_mintToSelfIntegrity",
    "eip4626_collateral_mintRespectsApproveTransfer",
    "eip4626_collateral_mintMustRevertIfCannotMint",
    "eip4626_collateral_mintPossibility",
    #"eip4626_collateral_maxWithdrawNoHigherThanActual",
    "eip4626_collateral_maxWithdrawWithdrawPossibility",
    #"eip4626_collateral_maxWithdrawZeroIfDisabled",
    "eip4626_collateral_maxWithdrawMustNotRevert",
    #"eip4626_collateral_previewWithdrawNoFewerThanActualShares",
    "eip4626_collateral_previewWithdrawMustIgnoreLimits",
    "eip4626_collateral_previewWithdrawMustNotDependOnCaller",
    "eip4626_collateral_previewWithdrawMayRevertOnlyWithWithdrawRevert",
    "eip4626_collateral_withdrawIntegrity",
    "eip4626_collateral_withdrawFromOtherIntegrity",
    "eip4626_collateral_withdrawFromSelfIntegrity",
    "eip4626_collateral_withdrawMustRevertIfCannotWithdraw",
    #"eip4626_collateral_maxRedeemNoHigherThanActual",
    "eip4626_collateral_maxRedeemMustNotRevert",
    #"eip4626_collateral_previewRedeemNoMoreThanActualAssets",
    "eip4626_collateral_previewRedeemMustIgnoreLimits",
    "eip4626_collateral_previewRedeemMustNotDependOnCaller",
    "eip4626_collateral_previewRedeemMayRevertOnlyWithRedeemRevert",
    "eip4626_collateral_redeemIntegrity",
    "eip4626_collateral_redeemFromOtherIntegrity",
    "eip4626_collateral_redeemFromSelfIntegrity",
    "eip4626_collateral_redeemMustRevertIfCannotRedeem"
]
