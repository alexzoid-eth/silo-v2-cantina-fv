// Mathematical simplifications

methods {
    function _.mulDiv(uint256 x, uint256 y, uint256 denominator) internal 
        => mulDivCVL(x, y, denominator) expect uint256;
}

definition CMP_EQUAL_UP_TO_1(mathint a, mathint b) returns bool = 
    a > b ? a - b <= 1 : b - a <= 1;

definition CMP_NOT_EQUAL_UP_TO_1(mathint a, mathint b) returns bool = 
    a > b ? a - b > 1 : b - a > 1;

function mulDivCVL(uint256 x, uint256 y, uint256 denominator) returns uint {
    require(denominator != 0);
    return require_uint256(x * y / denominator);
}
