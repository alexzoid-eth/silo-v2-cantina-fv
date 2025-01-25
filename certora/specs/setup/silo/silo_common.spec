// Silo core, CVL storage ghosts and hooks

import "./silo_config.spec";
import "./hook_receiver.spec";
import "../../valid_state/silo_valid_state_invariants.spec";

import "../erc20.spec";
import "../env.spec";

// From initial contest's setup
import "./initial/SiloMathLib_SAFE.spec";
import "./initial/SimplifiedGetCompoundInterestRateAndUpdate_SAFE.spec";
import "./initial/priceOracle_UNSAFE.spec";

methods {

    // Decimals

    function ShareTokenLib.decimals() external returns (uint8)
        => shareTokenLibDecimalsCVL(calledContract);

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
    
    function _.getLiquidity() external 
        => DISPATCHER(true);

    function _.accrueInterest() external
        => DISPATCHER(true);

    function _.repay(uint256 _assets, address _borrower) external
        => DISPATCHER(true);

    function _.redeem(uint256 _shares, address _receiver, address _owner) external
        => DISPATCHER(true);

    function _.redeem(uint256 _shares, address _receiver, address _owner, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);

    function _.previewRedeem(uint256 _shares) external
        => DISPATCHER(true);

    function _.previewRedeem(uint256 _shares, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);

    // Resolve external call in `IERC3156FlashBorrower`

    function _.onFlashLoan(address, address, uint256, uint256, bytes) external
        => NONDET;

    // Remove from the scene 
    
    function _.callOnBehalfOfSilo(address, uint256, ISilo.CallType, bytes) external
        => NONDET DELETE;

    function _.accrueInterestForBothSilos() external 
        => NONDET DELETE;

    function _.initialize(address _config) external
        => NONDET DELETE;
}

//
// Silo constants
//

definition ASSET_TYPE_PROTECTED() returns mathint = to_mathint(ISilo.AssetType.Protected);
definition ASSET_TYPE_COLLATERAL() returns mathint = to_mathint(ISilo.AssetType.Collateral);
definition ASSET_TYPE_DEBT() returns mathint = to_mathint(ISilo.AssetType.Debt);

//
// Valid state common for Silo and Silo1
//

function requireValidSiloCommon() {
    // Common valid state invariants working both for Silo0 and Silo1
    requireSiloValidStateCommon();
}

function requireValidSiloCommonE(env e) {
    requireValidSiloCommon();

    // Common environment for all tested contracts
    requireValidEnv(e);

    // Common valid state invariants working both for Silo0 and Silo1
    requireSiloValidStateCommonE(e);

    // Common environment both Silo0 and Silo1
    require(e.msg.sender != _SiloConfig);
}

//
// Methods summarizes
//

// `ShareTokenLib.decimals`

persistent ghost uint8 ghostDecimals0 {
    axiom ghostDecimals0 == 0 || (ghostDecimals0 >= 6 && ghostDecimals0 <= 18);
}
persistent ghost uint8 ghostDecimals1 {
    axiom ghostDecimals0 == 0 || (ghostDecimals1 >= 6 && ghostDecimals1 <= 18);
}
function shareTokenLibDecimalsCVL(address token) returns uint8 {
    // Different decimals for Token0 and Token1
    bool isSilo0 = (token == _CollateralShareToken0 
        || token == _ShareDebtToken0 
        || token == _ShareProtectedCollateralToken0
        || token == _Token0
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
        assetType > ASSET_TYPE_DEBT() => ghostTotalAssets[contract][assetType] == 0; 
}
