// Mathematical simplifications

methods {
    function _.mulDiv(uint256 x, uint256 y, uint256 denominator) internal 
        => mulDivCVL(x, y, denominator) expect uint256;
}

function mulDivCVL(uint256 x, uint256 y, uint256 denominator) returns uint {
    require(denominator != 0);
    return require_uint256(x * y / denominator);
}
