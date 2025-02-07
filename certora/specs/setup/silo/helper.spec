using Silo0 as _HelperCVL;

methods {
    // Link separate HelperCVL contract with helper solidity functions
    function _HelperCVL.assertOnFalse(bool b) external envfree;    
}

function ASSERT(bool expression) {
    _HelperCVL.assertOnFalse(expression);
} 

//
// CVL helpers for `SiloMathLib.getCollateralAmountsWithInterest()`
//

// Return collateral + accrued interest - fees
function getTotalCollateralAssetsWithInterestCVL(env e, address silo) returns mathint {

    mathint collateralAssets = ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()];
    mathint debtAssets = ghostTotalAssets[silo][ASSET_TYPE_DEBT()];
    mathint rcomp = getCompoundInterestRateCVL(silo, e.block.timestamp);

    mathint totalCollateralAssetsWithInterest = collateralAssets;
    mathint debtAssetsWithInterest = debtAssets;
    mathint daoAndDeployerRevenue = 0;
    mathint accruedInterest = 0;

    if(rcomp != 0 && debtAssets != 0) {
        (totalCollateralAssetsWithInterest, debtAssetsWithInterest, daoAndDeployerRevenue, accruedInterest) 
            = _HelperCVL.getCollateralAmountsWithInterestHarness(
                e, 
                require_uint256(collateralAssets), 
                require_uint256(debtAssets), 
                require_uint256(rcomp), 
                require_uint256(ghostConfigDaoFee), 
                require_uint256(ghostConfigDeployerFee)
                );
    }

    return totalCollateralAssetsWithInterest;
}

// Return debt + accrued interest
function getDebtAssetsWithInterestCVL(env e, address silo) returns mathint {

    mathint collateralAssets = ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()];
    mathint debtAssets = ghostTotalAssets[silo][ASSET_TYPE_DEBT()];
    mathint rcomp = getCompoundInterestRateCVL(silo, e.block.timestamp);

    mathint totalCollateralAssetsWithInterest = collateralAssets;
    mathint debtAssetsWithInterest = debtAssets;
    mathint daoAndDeployerRevenue = 0;
    mathint accruedInterest = 0;

    if(rcomp != 0 && debtAssets != 0) {
        (totalCollateralAssetsWithInterest, debtAssetsWithInterest, daoAndDeployerRevenue, accruedInterest) 
            = _HelperCVL.getCollateralAmountsWithInterestHarness(
                e, 
                require_uint256(collateralAssets), 
                require_uint256(debtAssets), 
                require_uint256(rcomp), 
                require_uint256(ghostConfigDaoFee), 
                require_uint256(ghostConfigDeployerFee)
                );
    }

    return debtAssetsWithInterest;
}

// Return fees from accrued interest
function getDaoAndDeployerRevenueCVL(env e, address silo) returns mathint {

    mathint collateralAssets = ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()];
    mathint debtAssets = ghostTotalAssets[silo][ASSET_TYPE_DEBT()];
    mathint rcomp = getCompoundInterestRateCVL(silo, e.block.timestamp);

    mathint totalCollateralAssetsWithInterest = collateralAssets;
    mathint debtAssetsWithInterest = debtAssets;
    mathint daoAndDeployerRevenue = 0;
    mathint accruedInterest = 0;

    if(rcomp != 0 && debtAssets != 0) {
        (totalCollateralAssetsWithInterest, debtAssetsWithInterest, daoAndDeployerRevenue, accruedInterest) 
            = _HelperCVL.getCollateralAmountsWithInterestHarness(
                e, 
                require_uint256(collateralAssets), 
                require_uint256(debtAssets), 
                require_uint256(rcomp), 
                require_uint256(ghostConfigDaoFee), 
                require_uint256(ghostConfigDeployerFee)
                );
    }

    return daoAndDeployerRevenue;
}

// Return accrued interest from debt
function getAccruedInterestCVL(env e, address silo) returns mathint {

    mathint collateralAssets = ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()];
    mathint debtAssets = ghostTotalAssets[silo][ASSET_TYPE_DEBT()];
    mathint rcomp = getCompoundInterestRateCVL(silo, e.block.timestamp);

    mathint totalCollateralAssetsWithInterest = collateralAssets;
    mathint debtAssetsWithInterest = debtAssets;
    mathint daoAndDeployerRevenue = 0;
    mathint accruedInterest = 0;

    if(rcomp != 0 && debtAssets != 0) {
        (totalCollateralAssetsWithInterest, debtAssetsWithInterest, daoAndDeployerRevenue, accruedInterest) 
            = _HelperCVL.getCollateralAmountsWithInterestHarness(
                e, 
                require_uint256(collateralAssets), 
                require_uint256(debtAssets), 
                require_uint256(rcomp), 
                require_uint256(ghostConfigDaoFee), 
                require_uint256(ghostConfigDeployerFee)
                );
    }

    return accruedInterest;
}


