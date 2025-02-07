methods {

    function PartialLiquidationLib.maxLiquidation(
        uint256 _sumOfCollateralAssets,
        uint256 _sumOfCollateralValue,
        uint256 _borrowerDebtAssets,
        uint256 _borrowerDebtValue,
        uint256 _liquidationTargetLTV,
        uint256 _liquidationFee
    ) internal returns (uint256, uint256)
    => maxLiquidationCVL(
        _sumOfCollateralAssets,
        _sumOfCollateralValue,
        _borrowerDebtAssets,
        _borrowerDebtValue,
        _liquidationTargetLTV,
        _liquidationFee
    );

    function PartialLiquidationLib.liquidationPreview(
        uint256 _ltvBefore,
        uint256 _sumOfCollateralAssets,
        uint256 _sumOfCollateralValue,
        uint256 _borrowerDebtAssets,
        uint256 _borrowerDebtValue,
        PartialLiquidationLib.LiquidationPreviewParams memory _params
    ) 
        internal
        returns (uint256, uint256, uint256)
    => liquidationPreviewCVL(
        _ltvBefore,
        _sumOfCollateralAssets,
        _sumOfCollateralValue,
        _borrowerDebtAssets,
        _borrowerDebtValue,
        _params.maxDebtToCover,
        _params.liquidationFee,
        _params.liquidationTargetLtv
    );

    function PartialLiquidationLib.valueToAssetsByRatio(
        uint256 _value,
        uint256 _totalAssets,
        uint256 _totalValue
    ) 
        internal 
        returns (uint256)
    => mulDivCVL(_value, _totalAssets, _totalValue);

    function PartialLiquidationLib.maxLiquidationPreview(
        uint256 _totalBorrowerCollateralValue,
        uint256 _totalBorrowerDebtValue,
        uint256 _ltvAfterLiquidation,
        uint256 _liquidationFee
    ) internal returns (uint256, uint256)
    => maxLiquidationPreviewCVL(
        _totalBorrowerCollateralValue,
        _totalBorrowerDebtValue,
        _ltvAfterLiquidation,
        _liquidationFee
    );

    function PartialLiquidationLib.calculateCollateralToLiquidate(
        uint256 _maxDebtToCover, 
        uint256 _sumOfCollateral, 
        uint256 _liquidationFee
        ) internal returns (uint256)
    => calculateCollateralToLiquidateCVL(
        _maxDebtToCover,
        _sumOfCollateral,
        _liquidationFee
    );

    function PartialLiquidationLib.estimateMaxRepayValue(
        uint256 _totalBorrowerDebtValue,
        uint256 _totalBorrowerCollateralValue,
        uint256 _ltvAfterLiquidation,
        uint256 _liquidationFee
    ) internal returns (uint256) 
    => estimateMaxRepayValueCVL(
        _totalBorrowerDebtValue,
        _totalBorrowerCollateralValue,
        _ltvAfterLiquidation,
        _liquidationFee
    );

    function PartialLiquidationLib.splitReceiveCollateralToLiquidate(
        uint256 _collateralToLiquidate, 
        uint256 _borrowerProtectedAssets
    ) 
        internal
        returns (uint256, uint256)
    => splitReceiveCollateralToLiquidateCVL(
        _collateralToLiquidate,
        _borrowerProtectedAssets
    );
}

definition _DEBT_DUST_LEVEL() returns mathint = 90 * 10^17;  // 90%
definition _PRECISION_DECIMALS() returns uint256 = 10^18;
definition _BAD_DEBT() returns mathint = 10^18;             // 1e18
definition _UNDERESTIMATION() returns mathint = 2;          // "2 wei"

function maxLiquidationCVL(
    mathint paramSumOfCollateralAssets,
    mathint paramSumOfCollateralValue,
    mathint paramBorrowerDebtAssets,
    mathint paramBorrowerDebtValue,
    mathint paramLiquidationTargetLTV,
    mathint paramLiquidationFee
) returns (uint256, uint256) {

    mathint localCollateralValueToLiquidate;
    mathint localRepayValue;
    (localCollateralValueToLiquidate, localRepayValue) = maxLiquidationPreviewCVL(
        paramSumOfCollateralValue,
        paramBorrowerDebtValue,
        paramLiquidationTargetLTV,
        paramLiquidationFee
    );

    mathint localCollateralToLiquidateVal = mulDivCVL(
        localCollateralValueToLiquidate,
        paramSumOfCollateralAssets,
        paramSumOfCollateralValue
    );

    mathint finalCollateralAssets;
    if (localCollateralToLiquidateVal > _UNDERESTIMATION()) {
        mathint minusCandidate = require_uint256(
            localCollateralToLiquidateVal - _UNDERESTIMATION()
        );
        finalCollateralAssets = require_uint256(minusCandidate);
    } else {
        finalCollateralAssets = 0;
    }

    mathint localDebtToRepayVal = mulDivCVL(
        localRepayValue,
        paramBorrowerDebtAssets,
        paramBorrowerDebtValue
    );

    return (
        require_uint256(finalCollateralAssets),
        require_uint256(localDebtToRepayVal)
    );
}

function liquidationPreviewCVL(
    mathint paramLTVBefore,
    mathint paramSumOfCollateralAssets,
    mathint paramSumOfCollateralValue,
    mathint paramBorrowerDebtAssets,
    mathint paramBorrowerDebtValue,
    mathint paramMaxDebtToCover,
    mathint paramLiquidationFee,
    mathint paramLiquidationTargetLtv
) returns (uint256, uint256, uint256) {

    // CASE 1: If _ltvBefore >= _BAD_DEBT => "bad debt" scenario
    if (paramLTVBefore >= _BAD_DEBT()) {
        // debtToRepay = min(maxDebtToCover, borrowerDebtAssets)
        mathint debtToRepayCandidate;
        if (paramMaxDebtToCover > paramBorrowerDebtAssets) {
            debtToRepayCandidate = paramBorrowerDebtAssets;
        } else {
            debtToRepayCandidate = paramMaxDebtToCover;
        }
        mathint localDebtToRepay = require_uint256(debtToRepayCandidate);

        mathint localDebtValueToRepay = mulDivCVL(
            localDebtToRepay,
            paramBorrowerDebtValue,
            paramBorrowerDebtAssets
        );

        mathint localCollValueToLiquidate = calculateCollateralToLiquidateCVL(
            localDebtValueToRepay,
            paramSumOfCollateralValue,
            paramLiquidationFee
        );

        mathint localCollateralToLiquidate = mulDivCVL(
            localCollValueToLiquidate,
            paramSumOfCollateralAssets,
            paramSumOfCollateralValue
        );

        mathint localLtvAfter = _calculateLtvAfterCVL(
            paramSumOfCollateralValue,
            paramBorrowerDebtValue,
            localCollValueToLiquidate,
            localDebtValueToRepay
        );

        return (
            require_uint256(localCollateralToLiquidate),
            require_uint256(localDebtToRepay),
            require_uint256(localLtvAfter)
        );
    }
    // CASE 2: normal scenario
    else {
        mathint localMaxRepayValue = estimateMaxRepayValueCVL(
            paramBorrowerDebtValue,
            paramSumOfCollateralValue,
            paramLiquidationTargetLtv,
            paramLiquidationFee
        );

        if (localMaxRepayValue == paramBorrowerDebtValue) {
            mathint localDebtToRepayFull = require_uint256(paramBorrowerDebtAssets);
            mathint localDebtValueToRepayFull = require_uint256(paramBorrowerDebtValue);

            mathint localCollValueToLiquidateFull = calculateCollateralToLiquidateCVL(
                localDebtValueToRepayFull,
                paramSumOfCollateralValue,
                paramLiquidationFee
            );

            mathint localCollateralToLiquidateFull = mulDivCVL(
                localCollValueToLiquidateFull,
                paramSumOfCollateralAssets,
                paramSumOfCollateralValue
            );

            mathint localLtvAfterFull = _calculateLtvAfterCVL(
                paramSumOfCollateralValue,
                paramBorrowerDebtValue,
                localCollValueToLiquidateFull,
                localDebtValueToRepayFull
            );

            return (
                require_uint256(localCollateralToLiquidateFull),
                require_uint256(localDebtToRepayFull),
                require_uint256(localLtvAfterFull)
            );
        }
        // partial liquidation
        else {
            mathint localMaxDebtToRepay = mulDivCVL(
                localMaxRepayValue,
                paramBorrowerDebtAssets,
                paramBorrowerDebtValue
            );

            mathint partialDebtToRepayCandidate;
            if (paramMaxDebtToCover > localMaxDebtToRepay) {
                partialDebtToRepayCandidate = localMaxDebtToRepay;
            } else {
                partialDebtToRepayCandidate = paramMaxDebtToCover;
            }
            mathint localDebtToRepayPartial = require_uint256(partialDebtToRepayCandidate);

            mathint localDebtValueToRepayPartial = mulDivCVL(
                localDebtToRepayPartial,
                paramBorrowerDebtValue,
                paramBorrowerDebtAssets
            );

            mathint localCollValueToLiquidatePartial = calculateCollateralToLiquidateCVL(
                localDebtValueToRepayPartial,
                paramSumOfCollateralValue,
                paramLiquidationFee
            );

            mathint localCollateralToLiquidatePartial = mulDivCVL(
                localCollValueToLiquidatePartial,
                paramSumOfCollateralAssets,
                paramSumOfCollateralValue
            );

            mathint localLtvAfterPartial = _calculateLtvAfterCVL(
                paramSumOfCollateralValue,
                paramBorrowerDebtValue,
                localCollValueToLiquidatePartial,
                localDebtValueToRepayPartial
            );

            return (
                require_uint256(localCollateralToLiquidatePartial),
                require_uint256(localDebtToRepayPartial),
                require_uint256(localLtvAfterPartial)
            );
        }
    }
}

function maxLiquidationPreviewCVL(
    mathint paramTotalBorrowerCollateralValue,
    mathint paramTotalBorrowerDebtValue,
    mathint paramLtvAfterLiquidation,
    mathint paramLiquidationFee
) returns (uint256, uint256) {
    
    mathint localRepayValue = estimateMaxRepayValueCVL(
        paramTotalBorrowerDebtValue,
        paramTotalBorrowerCollateralValue,
        paramLtvAfterLiquidation,
        paramLiquidationFee
    );

    mathint localCollateralValueToLiquidate = calculateCollateralToLiquidateCVL(
        localRepayValue,
        paramTotalBorrowerCollateralValue,
        paramLiquidationFee
    );

    return (
        require_uint256(localCollateralValueToLiquidate),
        require_uint256(localRepayValue)
    );
}

function calculateCollateralToLiquidateCVL(
    mathint paramMaxDebtToCover,
    mathint paramSumOfCollateral,
    mathint paramFee
) returns uint256 {

    mathint feeMul = require_uint256(paramMaxDebtToCover * paramFee);
    mathint fee = require_uint256(feeMul / _PRECISION_DECIMALS());
    mathint toLiquidateVal = require_uint256(paramMaxDebtToCover + fee);

    if (toLiquidateVal > paramSumOfCollateral) {
        return require_uint256(paramSumOfCollateral);
    } else {
        return require_uint256(toLiquidateVal);
    }
}

function estimateMaxRepayValueCVL(
    mathint paramDebtValue,
    mathint paramCollValue,
    mathint paramLTV,
    mathint paramFee
) returns uint256 {

    if (paramDebtValue == 0) {
        return 0;
    }

    if (paramFee >= _PRECISION_DECIMALS()) {
        return 0;
    }

    if (paramDebtValue >= paramCollValue) {
        return require_uint256(paramDebtValue);
    }

    if (paramLTV == 0) {
        return require_uint256(paramDebtValue);
    }

    mathint ltCv = require_uint256(paramLTV * paramCollValue);

    mathint scaledDebtValue = require_uint256(paramDebtValue * _PRECISION_DECIMALS());

    if (ltCv >= scaledDebtValue) {
        return 0;
    }

    mathint repayNumerator = require_uint256(scaledDebtValue - ltCv);

    mathint ltvTimesFee = require_uint256(paramLTV * paramFee);
    mathint ltvTimesFeeScaled = require_uint256(ltvTimesFee / _PRECISION_DECIMALS());
    mathint dividerR = require_uint256(paramLTV + ltvTimesFeeScaled);

    if (dividerR >= _PRECISION_DECIMALS()) {
        return require_uint256(paramDebtValue);
    }

    mathint leftover = require_uint256(_PRECISION_DECIMALS() - dividerR);

    mathint repayValue = require_uint256(repayNumerator / leftover);

    if (repayValue > paramDebtValue) {
        return require_uint256(paramDebtValue);
    }

    mathint scaledRepayValue = require_uint256(repayValue * _PRECISION_DECIMALS());
    mathint dustCheck        = require_uint256(scaledRepayValue / paramDebtValue);

    if (dustCheck > _DEBT_DUST_LEVEL()) {
        return require_uint256(paramDebtValue);
    }

    return require_uint256(repayValue);
}

function splitReceiveCollateralToLiquidateCVL(
    mathint paramCollateralToLiquidate,
    mathint paramBorrowerProtectedAssets
) returns (uint256, uint256) {

    if (paramCollateralToLiquidate == 0) {
        return (0, 0);
    }

    if (paramCollateralToLiquidate > paramBorrowerProtectedAssets) {
        mathint withdrawFromCollateral = require_uint256(
            paramCollateralToLiquidate - paramBorrowerProtectedAssets
        );
        return (
            require_uint256(withdrawFromCollateral),
            require_uint256(paramBorrowerProtectedAssets)
        );
    }
    else {
        return (
            0,
            require_uint256(paramCollateralToLiquidate)
        );
    }
}

function _calculateLtvAfterCVL(
    mathint paramSumCollValue,
    mathint paramTotalDebtValue,
    mathint paramCollValueLiquidate,
    mathint paramDebtValueCover
) returns uint256 {

    if (
        (paramSumCollValue <= paramCollValueLiquidate)
        || (paramTotalDebtValue <= paramDebtValueCover)
    ) {
        return 0;
    }

    mathint leftoverCollateral = require_uint256(paramSumCollValue - paramCollValueLiquidate);
    mathint leftoverDebt = require_uint256(paramTotalDebtValue - paramDebtValueCover);

    mathint product = require_uint256(leftoverDebt * _PRECISION_DECIMALS());
    mathint ltv = ceilDivCVL(product, leftoverCollateral);

    return require_uint256(ltv);
}

function ceilDivCVL(
    mathint numerator,
    mathint denominator
) returns uint256 {
    
    require(denominator != 0);

    mathint denomMinusOne = require_uint256(denominator - 1);
    mathint adjustedSum   = require_uint256(numerator + denomMinusOne);
    mathint result        = require_uint256(adjustedSum / denominator);

    return require_uint256(result);
}
