// Mathematical simplifications for `@openzeppelin/contracts/utils/math/Math.sol`

methods {
    function Math.mulDiv(uint256 x, uint256 y, uint256 denominator) internal returns (uint256)
        => mulDivCVL(x, y, denominator);
    function Math.mulDiv(uint256 x, uint256 y, uint256 denominator, Math.Rounding rounding) internal returns (uint256)
        // Math.Rounding.Ceil or Math.Rounding.Expand => rounds up 
        => mulDivRoundingCVL(x, y, denominator, to_mathint(rounding) == 1 || to_mathint(rounding) == 3);
}

definition PRECISION_DECIMALS() returns uint256 = 10^18;

definition CMP_EQUAL_UP_TO(mathint a, mathint b, mathint tot) returns bool = 
    a > b ? a - b <= tot : b - a <= tot;

definition CMP_NOT_EQUAL_UP_TO(mathint a, mathint b, mathint tot) returns bool = 
    a > b ? a - b > tot : b - a > tot;

function mulDivCVL(
    mathint numerator,
    mathint multiplier,
    mathint denominator
) returns uint256 {

    require(denominator != 0);

    mathint product = require_uint256(numerator * multiplier);
    return require_uint256(product / denominator);
}

function mulDivRoundingCVL(
    mathint numerator,
    mathint multiplier,
    mathint denominator,
    bool roundingUp
) returns uint256 {

    require(denominator != 0);

    mathint product = require_uint256(numerator * multiplier);
    mathint result = product / denominator;

    if (roundingUp && (product % denominator != 0)) {
        return require_uint256(result + 1);
    } else {
        return require_uint256(result);
    }
}