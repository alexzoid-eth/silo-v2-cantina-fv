rule_names = [
    # ERC20
    "inv_eip20_totalSupplySolvency",

    # SiloConfig
    "inv_crossReentrancyGuardOpenedOnExit",
    "inv_crossReentrancyProtectionNoDoubleCall",

    # Silo
    "inv_transferWithChecksAlwaysEnabled",
    "inv_interestRateTimestampNotInFuture",
    "inv_onlyOneDebtPerBorrower",
    "inv_borrowerCollateralSiloMustMatchDebt",

    # SiloX
    "inv_liquiditySolvency0", "inv_liquiditySolvency1",
    "inv_collateralPlusFeesCoverDebt0", "inv_collateralPlusFeesCoverDebt1",
    "inv_borrowerCannotHaveDebtWithoutCollateral0", "inv_borrowerCannotHaveDebtWithoutCollateral1",
    "inv_siloMustNotHaveUserAllowances0", "inv_siloMustNotHaveUserAllowances1",
    "inv_protectedCollateralAlwaysLiquid0", "inv_protectedCollateralAlwaysLiquid1",
    "inv_zeroCollateralMeansZeroDebt0", "inv_zeroCollateralMeansZeroDebt1",

    "inv_debtAssetsGteShares0", "inv_debtAssetsGteShares1",

    "inv_protectedZeroAssetsMustZeroShares0", "inv_protectedZeroAssetsMustZeroShares1",
    "inv_collateralZeroAssetsMustZeroShares0", "inv_collateralZeroAssetsMustZeroShares1",
    "inv_debtZeroAssetsMustZeroShares0", "inv_debtZeroAssetsMustZeroShares1",

    "inv_protectedNonZeroSharesMustNonZeroAssets0", "inv_protectedNonZeroSharesMustNonZeroAssets1",
    "inv_collateralNonZeroSharesMustNonZeroAssets0", "inv_collateralNonZeroSharesMustNonZeroAssets1",
    "inv_debtNonZeroSharesMustNonZeroAssets0", "inv_debtNonZeroSharesMustNonZeroAssets1",
];
