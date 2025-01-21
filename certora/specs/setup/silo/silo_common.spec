// Silo core, CVL storage ghosts and hooks

import "./silo_config.spec";

using EmptyHookReceiver as _EmptyHookReceiver;

methods {

    // Remove from the scene

    function _.callOnBehalfOfSilo(address, uint256, ISilo.CallType, bytes) external
        => NONDET DELETE;

    // Resolve external calls to `SiloFactory`

    function _.getFeeReceivers(address _silo) external
        => getFeeReceiversCVL(_silo) expect (address, address);

    // Resolve external calls to `Silo`

    function _.getTotalAssetsStorage(ISilo.AssetType _assetType) external
        => DISPATCHER(true);

    function _.getCollateralAndDebtTotalsStorage() external
        => DISPATCHER(true);
    
    function _.getCollateralAndProtectedTotalsStorage() external
        => DISPATCHER(true);

    // Resolve external call to `IHookReceiver`

    function _.hookReceiverConfig(address _silo) external
        => DISPATCHER(true);
    
    // Resolve external call in `IERC3156FlashBorrower`

    function _.onFlashLoan(address, address, uint256, uint256, bytes) external
        => NONDET;

    // Resolve external calls in `IInterestRateModel`

    function _.getCompoundInterestRateAndUpdate(
        uint256 _collateralAssets, uint256 _debtAssets, uint256 _interestRateTimestamp
    ) external => getCompoundInterestRateCVL(
        _collateralAssets, _debtAssets, _interestRateTimestamp
        ) expect (uint256);

    function _.getCompoundInterestRate(
        address _silo,
        uint256 _blockTimestamp
    ) external => getCompoundInterestRateForSiloCVL(_silo, _blockTimestamp) expect (uint256);

    // Resolve external calls in `ISiloOracle`

    function _.beforeQuote(address _baseToken) external
        => NONDET;

    function _.quote(uint256 _baseAmount, address _baseToken) external
        => NONDET;
}

//
// Methods summarizes
//

// `SiloFactory`

persistent ghost mapping(address => address) ghostDaoFeeReceiver; 
persistent ghost mapping(address => address) ghostDeployerFeeReceiver;
function getFeeReceiversCVL(address _silo) returns (address, address) {
    return (ghostDaoFeeReceiver[_silo], ghostDeployerFeeReceiver[_silo]);
}

// `IInterestRateModel`

ghost mapping(uint256 => mapping(uint256 => mapping(uint256 => uint256))) ghostInterest;
function getCompoundInterestRateCVL(
    uint256 _collateralAssets,
    uint256 _debtAssets,
    uint256 _interestRateTimestamp
) returns uint256 {
    return ghostInterest[_collateralAssets][_debtAssets][_interestRateTimestamp];
}

persistent ghost mapping(address => mapping(uint256 => uint256)) ghostInterestSilo;
function getCompoundInterestRateForSiloCVL(address _silo, uint256 _blockTimestamp) returns uint256 {
    return ghostInterestSilo[_silo][_blockTimestamp];
}

//
// Storage ghosts
//

// Ghost copy of `IERC20RStorage._receiveAllowances`

persistent ghost mapping(address => mapping(address => mapping(address => mathint))) ghostReceiveAllowances {
    init_state axiom forall address contract. forall address owner. forall address recipient. 
        ghostReceiveAllowances[contract][owner][recipient] == 0;
    axiom forall address contract. forall address owner. forall address recipient. 
        ghostReceiveAllowances[contract][owner][recipient] >= 0 
            && ghostReceiveAllowances[contract][owner][recipient] <= max_uint256;
}

// Ghost copy of `SiloStorage.daoAndDeployerRevenue`

persistent ghost mapping(address => mathint) ghostDaoAndDeployerRevenue {
    init_state axiom forall address contract. ghostDaoAndDeployerRevenue[contract] == 0;
    axiom forall address contract. 
        ghostDaoAndDeployerRevenue[contract] >= 0 && ghostDaoAndDeployerRevenue[contract] <= max_uint192;
}

// Ghost copy of `SiloStorage.interestRateTimestamp`

persistent ghost mapping(address => mathint) ghostInterestRateTimestamp {
    init_state axiom forall address contract. ghostInterestRateTimestamp[contract] == 0;
    axiom forall address contract. 
        ghostInterestRateTimestamp[contract] >= 0 && ghostInterestRateTimestamp[contract] <= max_uint64;
}

// Ghost copy of `SiloStorage.totalAssets`

persistent ghost mapping(address => mapping(mathint => mathint)) ghostTotalAssets {
    init_state axiom forall address contract. forall mathint assetType. ghostTotalAssets[contract][assetType] == 0;
    axiom forall address contract. forall mathint assetType. 
        ghostTotalAssets[contract][assetType] >= 0 && ghostTotalAssets[contract][assetType] <= max_uint256;
    // Support only 3 types of accounting 
    axiom forall address contract. forall mathint assetType. 
        assetType > 2 => ghostTotalAssets[contract][assetType] == 0; 
}
