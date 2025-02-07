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

ghost mulDivRoundingCVL(uint256, uint256, uint256, bool) returns uint256 {
    axiom forall uint256 X. forall uint256 Y. forall uint256 Z.
        // domain restriction: only meaningful for Z > 0
        Z > 0
        =>
        (
            // Rounding-up is either equal or exactly +1 from rounding-down
            (
                mulDivRoundingCVL(X,Y,Z,true) == mulDivRoundingCVL(X,Y,Z,false)
                || mulDivRoundingCVL(X,Y,Z,true) - mulDivRoundingCVL(X,Y,Z,false) == 1
            )
            &&
            // Multiplication symmetry:
            mulDivRoundingCVL(X,Y,Z,false) == mulDivRoundingCVL(Y,X,Z,false)
            &&
            mulDivRoundingCVL(X,Y,Z,true) == mulDivRoundingCVL(Y,X,Z,true)
            &&
            // For typical "shares <= totalShares" scenarios: if X <= Z, then (X * Y / Z) <= Y.
            (X <= Z => mulDivRoundingCVL(X,Y,Z,false) <= Y)
            &&
            // Nominator-denominator cancellation (round-down):
            ((X == Z) => mulDivRoundingCVL(X,Y,Z,false) == Y)
            &&
            ((Y == Z) => mulDivRoundingCVL(X,Y,Z,false) == X)
            &&
            // Nominator-denominator cancellation (round-up); same exact result if no remainder
            ((X == Z) => mulDivRoundingCVL(X,Y,Z,true) == Y)
            &&
            ((Y == Z) => mulDivRoundingCVL(X,Y,Z,true) == X)
        );

    axiom forall uint256 x1. forall uint256 x2. forall uint256 Y. forall uint256 Z.
        // monotonicity checks for x1 <= x2, assuming Z>0
        (Z > 0 && x1 <= x2)
        =>
        (
            mulDivRoundingCVL(x1,Y,Z,false) <= mulDivRoundingCVL(x2,Y,Z,false)
            &&
            mulDivRoundingCVL(x1,Y,Z,true)  <= mulDivRoundingCVL(x2,Y,Z,true)
            &&
            // With denominator in last position: if x1 <= x2 => 1/x1 >= 1/x2 => ratio is bigger
            mulDivRoundingCVL(Z,Y,x1,false) >= mulDivRoundingCVL(Z,Y,x2,false)
        );

    axiom forall uint256 X. forall uint256 Y. forall uint256 Z.
        // "cannot give zero unless product < divisor"
        (Z > 0 && mulDivRoundingCVL(X,Y,Z,false) == 0)
        =>
        (X == 0 || Y == 0 || (X * Y < Z))
        // if rounding UP and X>=1,Y>=1 => result >=1
        && ((X >= 1 && Y >=1 && Z >=1) => mulDivRoundingCVL(X,Y,Z,true) >= 1);

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
            mulDivRoundingCVL(XQ,Y2,ZQ,false) >= mulDivRoundingCVL(X,Y1,Z,false)
            &&
            mulDivRoundingCVL(XQ,Y2,ZQ,true)  >= mulDivRoundingCVL(X,Y1,Z,true)
        );
}