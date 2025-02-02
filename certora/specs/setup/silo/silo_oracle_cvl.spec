// Price oracle setup
methods {
    function _.quote(
        uint256 _baseAmount,
        address _baseToken
    ) external with (env e)
        => calculateTokenValue(calledContract, _baseToken, _baseAmount, e.block.timestamp) expect uint256;

    function _.beforeQuote(address) external 
        => NONDET;
}

definition VALUE1() returns uint256 = 1;
definition VALUE2() returns uint256 = 2;
definition VALUE3() returns uint256 = 6;
definition PRECISION() returns uint256 = 2;

function calculateTokenValue(
    address oracle,
    address token,
    uint256 baseAmount,
    uint256 time
) returns uint256 {
    return require_uint256(
        (priceOracle(oracle, token, time) * baseAmount + 1) / PRECISION()
    );
}

persistent ghost priceOracle(address, address, uint256) returns uint256 {
    axiom forall address oracle.
        forall address token.
            forall uint256 timestamp. (
                priceOracle(oracle, token, timestamp) == VALUE1() ||
                priceOracle(oracle, token, timestamp) == VALUE2() ||
                priceOracle(oracle, token, timestamp) == VALUE3()
            );
}
