methods {
    
    function SiloMathLib.convertToAssets(
        uint256 _shares, uint256 _totalAssets, uint256 _totalShares, Math.Rounding _rounding, ISilo.AssetType _assetType
    ) internal returns (uint256) 
        => convertToAssetsCVL(
            _shares, _totalAssets, _totalShares, to_mathint(_rounding) == 1, _assetType == ISilo.AssetType.Debt
            );

    function SiloMathLib.convertToShares(
        uint256 _assets, uint256 _totalAssets, uint256 _totalShares, Math.Rounding _rounding, ISilo.AssetType _assetType
    ) internal returns (uint256) 
        => convertToSharesCVL(
            _assets, _totalAssets, _totalShares, to_mathint(_rounding) == 1, _assetType == ISilo.AssetType.Debt
            ); 
}

definition _DECIMALS_OFFSET_POW() returns mathint = 10^3;

function _commonConvertToCVL(uint256 _totalAssets, uint256 _totalShares, bool debt) returns (uint256, uint256) {
    if(debt) {
        return (_totalShares, _totalShares == 0 ? 0 : _totalAssets);
    } else {
        return (
            require_uint256(_totalShares + _DECIMALS_OFFSET_POW()), 
            _totalShares == 0 ? 1 : require_uint256(_totalAssets + 1)
            );
    }
}

function convertToAssetsCVL(uint256 _shares, uint256 _totalAssets, uint256 _totalShares, bool roundingUp, bool debt) returns uint256 {
    uint256 totalShares; uint256 totalAssets; 
    totalShares, totalAssets = _commonConvertToCVL(_totalAssets, _totalShares, debt);
    if(totalShares == 0) {
        return _shares;
    } else {
        return mulDivRoundingCVL(_shares, totalAssets, totalShares, roundingUp);
    }
}

function convertToSharesCVL(uint256 _assets, uint256 _totalAssets, uint256 _totalShares, bool roundingUp, bool debt) returns uint256 {
    uint256 totalShares; uint256 totalAssets; 
    totalShares, totalAssets = _commonConvertToCVL(_totalAssets, _totalShares, debt);
    if(totalShares == 0) {
        return _assets;
    } else {
        return mulDivRoundingCVL(_assets, totalShares, totalAssets, roundingUp);
    }
}   
