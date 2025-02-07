methods {
    function SiloSolvencyLib.calculateLtv(
        SiloSolvencyLib.LtvData memory _ltvData, address _collateralToken, address _debtAsset
        ) internal returns (uint256, uint256, uint256) 
        => calculateLtv(_ltvData, _collateralToken, _debtAsset);
}

definition _INFINITY() returns uint256 = max_uint256;

function calculateLtv(SiloSolvencyLib.LtvData _ltvData, address _collateralToken, address _debtAsset) 
    returns (uint256, uint256, uint256) {

    uint256 sumOfBorrowerCollateralValue = require_uint256(_ltvData.borrowerProtectedAssets 
        + _ltvData.borrowerCollateralAssets);
    uint256 totalBorrowerDebtValue = _ltvData.borrowerDebtAssets; 
    uint256 ltvInDp;

    if(sumOfBorrowerCollateralValue == 0 && totalBorrowerDebtValue == 0) {
        return (0, 0, 0);
    } else if(sumOfBorrowerCollateralValue == 0) {
        return (0, 0, _INFINITY());
    } else {
        return (
            sumOfBorrowerCollateralValue, 
            totalBorrowerDebtValue, 
            mulDivRoundingCVL(totalBorrowerDebtValue, PRECISION_DECIMALS(), sumOfBorrowerCollateralValue, true)
            );
    }
}
