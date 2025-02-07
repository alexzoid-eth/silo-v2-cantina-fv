// Silo core, CVL storage ghosts and hooks


import "../erc20.spec";
import "../math.spec";

import "./helper.spec";
import "./silo_config.spec";
import "./interest_rate_model.spec";

import "./silo_solvency_lib.spec";
import "./silo_math_lib.spec";
import "./partial_liquidation_lib.spec";

methods {

    // Decimals

    function ShareTokenLib.decimals() external returns (uint8)
        => shareTokenLibDecimalsCVL(calledContract);

    // Resolve external calls to `SiloFactory`

    function _.getFeeReceivers(address _silo) external
        => getFeeReceiversCVL() expect (address, address);
        
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

    function _.accrueInterestForConfig(address _interestRateModel, uint256 _daoFee, uint256 _deployerFee) external
        => DISPATCHER(true);

    function _.config() external
        => DISPATCHER(true);

    // Resolve external call in `IERC3156FlashBorrower`

    function _.onFlashLoan(address _initiator, address _token, uint256 _amount, uint256 _fee, bytes _data) external
        => onFlashLoanCVL(calledContract) expect bytes32;

    // Resolve external calls in `IHookReceiver`

    function _.beforeAction(address _silo, uint256 _action, bytes _input) external
        => NONDET; // not in use

    function _.afterAction(address _silo, uint256 _action, bytes _inputAndOutput) external
        => NONDET; // not in use

    function _.hookReceiverConfig(address _silo) external
        => NONDET; // not in use

    // Resolve external calls in `ISiloOracle`

    function _.quote(uint256 _baseAmount, address _baseToken) external
        => NONDET;

    function _.beforeQuote(address) external 
        => NONDET;

    // Remove from the scene 
    
    function _.callOnBehalfOfSilo(address, uint256, ISilo.CallType, bytes) external
        => NONDET DELETE;

    function _.initialize(address _config) external
        => NONDET DELETE;

    function _.DOMAIN_SEPARATOR() external
        => NONDET DELETE;

    function _.eip712Domain() external
        => NONDET DELETE;
}

//
// Assume valid state for all Silo contracts
//

persistent ghost address ghostCaller;

persistent ghost mathint ghostTokensSupply {
    axiom ghostTokensSupply > 10 && ghostTokensSupply < 1000;
}

function setupSilo(env e) {

    // SAFE: To make further computations in the Silo secure require DAO and deployer 
    //  fees to be less than 100% (from SiloConfig's constructor)
    require(ghostConfigDaoFee + ghostConfigDeployerFee < 10^18);

    // SAFE: assume realistic initial amount of accumulated fee to avoid overflow in
    //  `unchecked { $.daoAndDeployerRevenue += uint192(totalFees); }`
    require(forall address silo. ghostDaoAndDeployerRevenue[silo] < max_uint96);

    // SAFE: Avoid reverting due non-zero msg.value
    require(e.msg.value == 0);

    // SAFE: Valid msg.sender
    require(e.msg.sender != 0);
    require(ghostCaller == e.msg.sender);

    // SAFE: Valid time
    require(e.block.timestamp != 0);
    require(e.block.number != 0);

    // SAFE: Common valid state invariants working both for Silo0 and Silo1
    requireValidStateInvariants(e);

    // SAFE: Assume realistic assets total supply
    require(ghostERC20TotalSupply[ghostToken0] == ghostTokensSupply * 10^ghostDecimals0);
    require(ghostERC20TotalSupply[ghostToken1] == ghostTokensSupply * 10^ghostDecimals1);

    // UNSAFE: zero assets <=> zero shares (based on `SiloMathLib._commonConvertTo()`)
    require(ghostTotalAssets[ghostSilo0][ASSET_TYPE_PROTECTED()] == 0 <=> ghostERC20TotalSupply[ghostProtectedToken0] == 0);
    require(ghostTotalAssets[ghostSilo1][ASSET_TYPE_PROTECTED()] == 0 <=> ghostERC20TotalSupply[ghostProtectedToken1] == 0);
    require(ghostTotalAssets[ghostSilo0][ASSET_TYPE_COLLATERAL()] == 0 <=> ghostERC20TotalSupply[ghostCollateralToken0] == 0);
    require(ghostTotalAssets[ghostSilo1][ASSET_TYPE_COLLATERAL()] == 0 <=> ghostERC20TotalSupply[ghostCollateralToken1] == 0);
    require(ghostTotalAssets[ghostSilo0][ASSET_TYPE_DEBT()] == 0 <=> ghostERC20TotalSupply[ghostDebtToken0] == 0);
    require(ghostTotalAssets[ghostSilo1][ASSET_TYPE_DEBT()] == 0 <=> ghostERC20TotalSupply[ghostDebtToken1] == 0);

    // UNSAFE: non-zero shares total supply => non-zero tracked assets (based on `SiloMathLib._commonConvertTo()`)
    require(ghostERC20TotalSupply[ghostProtectedToken0] != 0 => ghostTotalAssets[ghostSilo0][ASSET_TYPE_PROTECTED()] != 0);    
    require(ghostERC20TotalSupply[ghostProtectedToken1] != 0 => ghostTotalAssets[ghostSilo1][ASSET_TYPE_PROTECTED()] != 0);    
    require(ghostERC20TotalSupply[ghostCollateralToken0] != 0 => ghostTotalAssets[ghostSilo0][ASSET_TYPE_COLLATERAL()] != 0);
    require(ghostERC20TotalSupply[ghostCollateralToken1] != 0 => ghostTotalAssets[ghostSilo1][ASSET_TYPE_COLLATERAL()] != 0);
    require(ghostERC20TotalSupply[ghostDebtToken0] != 0 => ghostTotalAssets[ghostSilo0][ASSET_TYPE_DEBT()] != 0);
    require(ghostERC20TotalSupply[ghostDebtToken1] != 0 => ghostTotalAssets[ghostSilo1][ASSET_TYPE_DEBT()] != 0);

    // UNSAFE: Disabling oracles
    require(ghostConfigSolvencyOracle0 == 0 && ghostConfigMaxLtvOracle0 == 0);
    require(ghostConfigSolvencyOracle1 == 0 && ghostConfigMaxLtvOracle1 == 0);

    // UNSAFE: set `true` to use static config based on `silo-core/deploy/input/mainnet/FULL_CONFIG_TEST.json`
    require(ghostUseStaticConfig == true);
    require(ghostUseStaticConfig => (
        // Fees
        ghostConfigDaoFee == 1500 * BP2DP_NORMALIZATION()
        && ghostConfigDeployerFee == 1000 * BP2DP_NORMALIZATION()

        // Silo0
        && ghostConfigMaxLtv0 == 7500 * BP2DP_NORMALIZATION()
        && ghostConfigLt0 == 8500 * BP2DP_NORMALIZATION()
        && ghostConfigLiquidationTargetLtv0 == 7650 * BP2DP_NORMALIZATION()
        && ghostConfigLiquidationFee0 == 500 * BP2DP_NORMALIZATION()
        && ghostConfigFlashloanFee0 == 100 * BP2DP_NORMALIZATION()
        && ghostConfigCallBeforeQuote0 == false

        // Silo1
        && ghostConfigMaxLtv1 == 8500 * BP2DP_NORMALIZATION()
        && ghostConfigLt1 == 9500 * BP2DP_NORMALIZATION()
        && ghostConfigLiquidationTargetLtv1 == 8550 * BP2DP_NORMALIZATION()
        && ghostConfigLiquidationFee1 == 250 * BP2DP_NORMALIZATION()
        && ghostConfigFlashloanFee1 == 100 * BP2DP_NORMALIZATION()
        && ghostConfigCallBeforeQuote1 == false
        ));
    }

function requireSameEnv(env e1, env e2) {
    require(e1.block.number == e2.block.number);
    require(e1.block.timestamp == e2.block.timestamp);
    require(e1.msg.sender == e2.msg.sender);
    require(e1.msg.value == e2.msg.value);
}

//
// Definitions
//

definition ASSET_TYPE_PROTECTED() returns mathint = to_mathint(ISilo.AssetType.Protected);
definition ASSET_TYPE_COLLATERAL() returns mathint = to_mathint(ISilo.AssetType.Collateral);
definition ASSET_TYPE_DEBT() returns mathint = to_mathint(ISilo.AssetType.Debt);

definition ADDRESS_NOT_CONTRACT_IN_SCENE(address a) returns bool 
    = a != ghostSiloConfig
        && a != ghostSilo0
        && a != ghostToken0
        && a != ghostProtectedToken0
        && a != ghostCollateralToken0
        && a != ghostDebtToken0
        && a != ghostConfigSolvencyOracle0
        && a != ghostConfigMaxLtvOracle0
        && a != ghostConfigInterestRateModel0
        && a != ghostSilo1
        && a != ghostToken1
        && a != ghostProtectedToken1
        && a != ghostCollateralToken1
        && a != ghostDebtToken1
        && a != ghostConfigSolvencyOracle1
        && a != ghostConfigMaxLtvOracle1
        && a != ghostConfigInterestRateModel1
        && a != ghostConfigHookReceiver;

definition IS_MODE_SINGLE() returns bool
    = _SiloConfig._SILO_MODE() == ghostSilo0;

definition IS_MODE_HOOK() returns bool
    = _SiloConfig._SILO_MODE() != ghostSilo0 && _SiloConfig._SILO_MODE() != ghostSilo1;

//
// Methods summarizes
//

// `ShareTokenLib.decimals`

persistent ghost uint8 ghostDecimals0 {
    axiom ghostDecimals0 == 0 || (ghostDecimals0 >= 6 && ghostDecimals0 <= 18);
}
persistent ghost uint8 ghostDecimals1 {
    axiom ghostDecimals1 == 0 || (ghostDecimals1 >= 6 && ghostDecimals1 <= 18);
}
function shareTokenLibDecimalsCVL(address token) returns uint8 {
    // Different decimals for Token0 and Token1
    return (silo0contractsAddress(token) ? ghostDecimals0 : ghostDecimals1);
}

// `SiloFactory`

persistent ghost address ghostDaoFeeReceiver {
    axiom ghostDaoFeeReceiver != ghostDeployerFeeReceiver
        && ghostDaoFeeReceiver != 0
        && ADDRESS_NOT_CONTRACT_IN_SCENE(ghostDaoFeeReceiver);
}
persistent ghost address ghostDeployerFeeReceiver {
    axiom ghostDeployerFeeReceiver != ghostDaoFeeReceiver
        && ADDRESS_NOT_CONTRACT_IN_SCENE(ghostDeployerFeeReceiver);
}
function getFeeReceiversCVL() returns (address, address) {
    return (ghostDaoFeeReceiver, ghostDeployerFeeReceiver);
}

// `IERC3156FlashBorrower`

function onFlashLoanCVL(address _receiver) returns bytes32 {
    // SAFE: Receiver cannot be Silo due revert in `onFlashLoan()` call
    require(_receiver != ghostSilo0 && _receiver != ghostSilo1);

    bytes32 result;
    return result;
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
    // Assume realistic assets amount to void overflow in unchecked blocks
    axiom forall address contract. forall mathint assetType. 
        ghostTotalAssets[contract][assetType] >= 0 && ghostTotalAssets[contract][assetType] <= max_uint128;
    // Support only 3 types of accounting 
    axiom forall address contract. forall mathint assetType. 
        assetType > ASSET_TYPE_DEBT() => ghostTotalAssets[contract][assetType] == 0; 
}
