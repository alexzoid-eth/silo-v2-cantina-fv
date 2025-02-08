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

ghost mulDivRoundingApproxCVL(uint256, uint256, uint256, bool) returns uint256 {
    axiom forall uint256 X. forall uint256 Y. forall uint256 Z.
        // domain restriction: only meaningful for Z > 0
        Z > 0
        =>
        (
            // Rounding-up is either equal or exactly +1 from rounding-down
            (
                mulDivRoundingApproxCVL(X,Y,Z,true) == mulDivRoundingApproxCVL(X,Y,Z,false)
                || mulDivRoundingApproxCVL(X,Y,Z,true) - mulDivRoundingApproxCVL(X,Y,Z,false) == 1
            )
            &&
            // Multiplication symmetry:
            mulDivRoundingApproxCVL(X,Y,Z,false) == mulDivRoundingApproxCVL(Y,X,Z,false)
            &&
            mulDivRoundingApproxCVL(X,Y,Z,true) == mulDivRoundingApproxCVL(Y,X,Z,true)
            &&
            // For typical "shares <= totalShares" scenarios: if X <= Z, then (X * Y / Z) <= Y.
            (X <= Z => mulDivRoundingApproxCVL(X,Y,Z,false) <= Y)
            &&
            // Nominator-denominator cancellation (round-down):
            ((X == Z) => mulDivRoundingApproxCVL(X,Y,Z,false) == Y)
            &&
            ((Y == Z) => mulDivRoundingApproxCVL(X,Y,Z,false) == X)
            &&
            // Nominator-denominator cancellation (round-up); same exact result if no remainder
            ((X == Z) => mulDivRoundingApproxCVL(X,Y,Z,true) == Y)
            &&
            ((Y == Z) => mulDivRoundingApproxCVL(X,Y,Z,true) == X)
        );

    axiom forall uint256 x1. forall uint256 x2. forall uint256 Y. forall uint256 Z.
        // monotonicity checks for x1 <= x2, assuming Z>0
        (Z > 0 && x1 <= x2)
        =>
        (
            mulDivRoundingApproxCVL(x1,Y,Z,false) <= mulDivRoundingApproxCVL(x2,Y,Z,false)
            &&
            mulDivRoundingApproxCVL(x1,Y,Z,true)  <= mulDivRoundingApproxCVL(x2,Y,Z,true)
            &&
            // With denominator in last position: if x1 <= x2 => 1/x1 >= 1/x2 => ratio is bigger
            mulDivRoundingApproxCVL(Z,Y,x1,false) >= mulDivRoundingApproxCVL(Z,Y,x2,false)
        );

    axiom forall uint256 X. forall uint256 Y. forall uint256 Z.
        // "cannot give zero unless product < divisor"
        (Z > 0 && mulDivRoundingApproxCVL(X,Y,Z,false) == 0)
        =>
        (X == 0 || Y == 0 || (X * Y < Z))
        // if rounding UP and X>=1,Y>=1 => result >=1
        && ((X >= 1 && Y >=1 && Z >=1) => mulDivRoundingApproxCVL(X,Y,Z,true) >= 1);

    axiom forall uint256 X. forall uint256 Y1. forall uint256 Y2. forall uint256 Z. forall uint256 XQ. forall uint256 ZQ.
        // adding same difference to X and Z, and switching Y1->Y2 (with Y2>=Y1)
        // cannot decrease the result
        (
            X >= 1
            && Y1 >= 1
            && Y2 >= Y1
            && Z >= 1
            && XQ > X
            && (XQ - X == ZQ - Z)
        )
        =>
        (
            mulDivRoundingApproxCVL(XQ,Y2,ZQ,false) >= mulDivRoundingApproxCVL(X,Y1,Z,false)
            &&
            mulDivRoundingApproxCVL(XQ,Y2,ZQ,true)  >= mulDivRoundingApproxCVL(X,Y1,Z,true)
        );
}