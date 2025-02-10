rule_names = [
    # ERC20
    "inv_eip20_totalSupplySolvency",

    # SiloConfig
    "inv_crossReentrancyGuardOpenedOnExit",

    # Silo
    "inv_transferWithChecksAlwaysEnabled",
    "inv_interestRateTimestampNotInFuture",
    "inv_borrowerCannotHaveTwoDebts",
    "inv_borrowerCannotHaveDebtWithoutCollateralSet",

    # SiloX
    "inv_liquiditySolvency0", 
    "inv_liquiditySolvency1",
    
    "inv_collateralPlusFeesCoverDebt0", 
    "inv_collateralPlusFeesCoverDebt1",
    
    "inv_siloMustNotHaveUserAllowances0", 
    "inv_siloMustNotHaveUserAllowances1",
    
    "inv_protectedCollateralAlwaysLiquid0", 
    "inv_protectedCollateralAlwaysLiquid1",
    
    "inv_zeroCollateralMeansZeroDebt0", 
    "inv_zeroCollateralMeansZeroDebt1",
    
    "inv_debtAssetsGteShares0", 
    "inv_debtAssetsGteShares1",
];
