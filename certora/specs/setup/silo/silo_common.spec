// Silo core, CVL storage ghosts and hooks

import "./silo_config.spec";
import "./silo_common_valid_state.spec";

// From initial contest's setup
import "./initial/SiloMathLib_SAFE.spec";
import "./initial/SimplifiedGetCompoundInterestRateAndUpdate_SAFE.spec";
import "./initial/priceOracle_UNSAFE.spec";

using EmptyHookReceiver as _EmptyHookReceiver;

methods {

    // Remove from the scene as it as admin specific with unlimited rights
    function _.callOnBehalfOfSilo(address, uint256, ISilo.CallType, bytes) external
        => NONDET DELETE;

    // Remove from the scene in order to support single Silo configuration 
    function _.accrueInterestForBothSilos() external 
        => NONDET DELETE;

    // Assume decimals via `ShareTokenLib.decimals()` summarization

    function ShareTokenLib.decimals() external returns (uint8)
        => decimalsCVL(calledContract);

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
}

//
// Methods summarizes
//

// `ShareTokenLib.decimals()`

persistent ghost uint8 ghostDecimals0 {
    axiom ghostDecimals0 == 0 || (ghostDecimals0 >= 6 && ghostDecimals0 <= 18);
}
persistent ghost uint8 ghostDecimals1 {
    axiom ghostDecimals0 == 0 || (ghostDecimals1 >= 6 && ghostDecimals1 <= 18);
}
function decimalsCVL(address contract) returns uint8 {
    // Different decimals for Token0 and Token1
    bool isSilo0 = (contract == _CollateralShareToken0 
        || contract == _ShareDebtToken0 
        || contract == _ShareProtectedCollateralToken0
        || contract == _Token0
        ); 
    return (isSilo0 ? ghostDecimals0 : ghostDecimals1);
}

// `SiloFactory`

persistent ghost mapping(address => address) ghostDaoFeeReceiver; 
persistent ghost mapping(address => address) ghostDeployerFeeReceiver;
function getFeeReceiversCVL(address _silo) returns (address, address) {
    return (ghostDaoFeeReceiver[_silo], ghostDeployerFeeReceiver[_silo]);
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
