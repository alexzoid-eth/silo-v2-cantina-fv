// Interest rate model setup
methods {
    function _.getCompoundInterestRateAndUpdate(
        uint256 _collateralAssets,
        uint256 _debtAssets,
        uint256 _interestRateTimestamp
    ) external with (env e)
        => compoundInterestRate(require_uint256(e.block.timestamp - _interestRateTimestamp)) expect uint256;

    function _.getCompoundInterestRate(
        address _silo,
        uint256 _blockTimestamp
    ) external
        => getCompoundInterestRateCVL(_silo, _blockTimestamp) expect uint256;
}

definition RCOMP_MAX() returns uint256 = 2^16 * 10^18;

ghost compoundInterestRate(uint256) returns uint256 {
    axiom forall uint256 timestampDiff0. forall uint256 timestampDiff1. (
        timestampDiff1 >= timestampDiff0 =>
        compoundInterestRate(timestampDiff1) >= compoundInterestRate(timestampDiff0)
    );
    axiom forall uint256 timestampDiff. compoundInterestRate(timestampDiff) <= RCOMP_MAX();
    axiom compoundInterestRate(0) == 0;
}

function getCompoundInterestRateCVL(address _silo, uint256 _blockTimestamp) returns uint256 {
    require(_blockTimestamp >= ghostInterestRateTimestamp[_silo]);
    mathint timestampDiff = _blockTimestamp - ghostInterestRateTimestamp[_silo];
    return compoundInterestRate(require_uint256(timestampDiff));
}
