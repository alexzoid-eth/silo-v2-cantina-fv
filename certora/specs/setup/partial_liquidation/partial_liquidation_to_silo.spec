import "./partial_liquidation_lib.spec";

using Hook as _HookSender;
using PartialLiquidation as _PartialLiquidation;

// UNSAFE: everything extremely simplified
// collateral - silo0
// debt - silo1
// 1-to-1 conversion

methods {

    function _HookSender.liquidationCallValidFlexible(
        address _borrower,
        uint256 _maxDebtToCover,
        bool _receiveSToken,
        bool _bypassInterest,
        bool _ignoreProtectedShares,
        bool _ignoreCollateralShares
    ) internal returns (uint256, uint256) with (env e)
        => liquidationCallValidFlexibleCVL(
            e, _borrower, _maxDebtToCover, _receiveSToken, _bypassInterest, _ignoreProtectedShares, _ignoreCollateralShares
        );

    function SiloSolvencyLib.isSolvent(
        ISiloConfig.ConfigData memory,
        ISiloConfig.ConfigData memory,
        address _borrower,
        ISilo.AccrueInterestInMemory
    ) internal returns bool
        => ghostUserSolvent[_borrower];

    function PartialLiquidationExecLib.getExactLiquidationAmounts(
        ISiloConfig.ConfigData _collateralConfig,
        ISiloConfig.ConfigData _debtConfig,
        address _user,
        uint256 _maxDebtToCover,
        uint256 _liquidationFee
    ) external returns (
        uint256,
        uint256,
        uint256,
        bytes4
    ) => getExactLiquidationAmountsCVL(
        _user,
        _maxDebtToCover,
        _liquidationFee
    );

    function SiloMathLib.convertToAssets(
        uint256 _shares, uint256 _totalAssets, uint256 _totalShares, Math.Rounding _rounding, ISilo.AssetType _assetType
    ) internal returns (uint256) 
        => convertToAssetsCVL(_shares); 

    function SiloMathLib.convertToShares(
        uint256 _assets, uint256 _totalAssets, uint256 _totalShares, Math.Rounding _rounding, ISilo.AssetType _assetType
    ) internal returns (uint256) 
        => convertToSharesCVL(_assets); 

    function _.forwardTransferFromNoChecks(address _from, address _to, uint256 _amount) external
        => forwardTransferFromNoChecksCVL(calledContract, _from, _to, _amount, true) expect void;
    /*
    function _.repay(uint256 _assets, address _borrower) external with (env e)
        => repayCVL(e, calledContract, _assets, _borrower) expect uint256;

    function _.redeem(uint256 _shares, address _receiver, address _owner, ISilo.CollateralType _collateralType) external with (env e)
        => redeemCVL(e, calledContract, _shares, _receiver, _owner, _collateralType) expect uint256;

    function _.previewRedeem(uint256 _shares, ISilo.CollateralType _collateralType) external
        => previewRedeemCVL(calledContract, _shares, _collateralType) expect uint256;
    */
}

definition _DUST() returns mathint = 100;

function borrowerReadyToLiquidate(address borrower) returns bool {

    return borrower != 0 
        && ghostConfigBorrowerCollateralSilo[borrower] == _Silo0
        && ghostERC20Balances[_Collateral0][borrower] + ghostERC20Balances[_Protected0][borrower] > _DUST()
        && ghostERC20Balances[_Debt1][borrower] > _DUST()
        && ghostUserSolvent[borrower] == false
        ;
}

persistent ghost address ghostBorrower;
persistent ghost uint256 ghostMaxDebtToCover;
persistent ghost bool ghostReceiveSToken;
persistent ghost bool ghostIgnoreProtectedShares;
persistent ghost bool ghostIgnoreCollateralShares;

function liquidationCallValidFlexibleCVL(
    env e,
    address _borrower,
    uint256 _maxDebtToCover,
    bool _receiveSToken,
    bool _bypassInterest,
    bool _ignoreProtectedShares,
    bool _ignoreCollateralShares
) returns (uint256, uint256) {

    require(ghostBorrower == _borrower);
    require(ghostMaxDebtToCover == _maxDebtToCover);
    require(ghostReceiveSToken == _receiveSToken);
    require(ghostIgnoreProtectedShares == _ignoreProtectedShares);
    require(ghostIgnoreCollateralShares == _ignoreCollateralShares);

    require(e.msg.sender == _HookSender);

    setupSilo(e);

    if(_bypassInterest) {
        require(ghostInterestRateTimestamp[_Silo0] == e.block.timestamp);
        require(ghostInterestRateTimestamp[_Silo1] == e.block.timestamp);
    }

    require(!_ignoreProtectedShares || !_ignoreCollateralShares);

    if(_ignoreProtectedShares) {
        require(ghostERC20Balances[_Protected0][_borrower] == 0);
        require(ghostERC20Balances[_Protected1][_borrower] == 0);
    } else {
        require(ghostERC20Balances[_Collateral0][_borrower] == 0);
        require(ghostERC20Balances[_Collateral1][_borrower] == 0);
    }

    uint256 withdrawCollateral; 
    uint256 repayDebtAssets;
    withdrawCollateral, repayDebtAssets = _PartialLiquidation.liquidationCall(
        e,
        ghostToken0,    // Silo0 - collateral
        ghostToken1,    // Silo1 - debt
        _borrower,
        _maxDebtToCover,
        _receiveSToken
    );

    return (withdrawCollateral, repayDebtAssets);
}

persistent ghost mapping(address => bool) ghostUserSolvent {
    init_state axiom forall address user. ghostUserSolvent[user] == false;
}

function getExactLiquidationAmountsCVL(
    address _user,
    uint256 _maxDebtToCover,
    uint256 _liquidationFee
    ) returns (uint256, uint256, uint256, bytes4)
{
    uint256 withdrawAssetsFromCollateral;
    uint256 withdrawAssetsFromProtected;
    uint256 repayDebtAssets;
    bytes4 customError;

    if(borrowerReadyToLiquidate(_user) == false) {
        return (0, 0, 0, customError);
    } else {
        if(ghostIgnoreProtectedShares) {
            require(ghostERC20Balances[_Protected0][_user] == 0);
            require(withdrawAssetsFromCollateral > _DUST() && withdrawAssetsFromCollateral <= ghostERC20Balances[_Collateral0][_user]);
            require(withdrawAssetsFromProtected == 0);
            require(repayDebtAssets == withdrawAssetsFromCollateral);
        } else {
            require(ghostERC20Balances[_Collateral0][_user] == 0);
            require(withdrawAssetsFromCollateral == 0);
            require(withdrawAssetsFromProtected > _DUST() && withdrawAssetsFromProtected <= ghostERC20Balances[_Protected0][_user]);
            require(repayDebtAssets == withdrawAssetsFromProtected);
        }

        return (withdrawAssetsFromCollateral, withdrawAssetsFromProtected, repayDebtAssets, to_bytes4(0));
    }
}

function convertToAssetsCVL(uint256 _shares) returns uint256 {
    return _shares;
}

function convertToSharesCVL(uint256 _assets) returns uint256 {
    return _assets;
}

persistent ghost mathint ghostConfiscatedCollateralShares;
function forwardTransferFromNoChecksCVL(address token, address _from, address _to, uint256 _amount, bool transferFrom) {

    // Borrower must have a debt in Silo1 with collateral in Silo0
    assert(ghostERC20Balances[_Debt1][_from] != 0);
    assert(ghostConfigBorrowerCollateralSilo[_from] == _Silo0);

    // Selected collateral shares
    if(ghostIgnoreProtectedShares) {
        assert(token == _Collateral0);
    } else {
        assert(token == _Protected0);
    }

    // From borrower
    assert(_from == ghostBorrower);

    // To msg.sender or current contract 
    if(ghostReceiveSToken) {
        assert(_to == _HookSender);
    } else {
        assert(_to == _PartialLiquidation);
    }

    // Don't send zero shares
    assert(_amount != 0);
    ghostConfiscatedCollateralShares = _amount;

    transferFromCVL(token, _from, _to, _amount, transferFrom);
}

function repayCVL(env e, address silo, uint256 _assets, address _borrower)
    returns uint256
{
    uint256 shares = _assets;
    
    assert(silo == _Silo1); // Debt silo based on liquidationCallValidFlexibleCVL()
    assert(ghostMaxDebtToCover != 0);
    require(_assets != 0 && _assets <= ghostMaxDebtToCover);
    require(_borrower != 0 && _borrower == ghostBorrower);

    // Debt tokens (Token1) were transferred earlier from _HookSender
    assert(ghostERC20Balances[ghostToken1][_PartialLiquidation] >= _assets);

    // Allowance must be set before transferFrom()
    assert(ghostERC20Allowances[ghostToken1][_PartialLiquidation][_Silo1] >= _assets);

    // Borrower's shares decrease
    assert(ghostERC20Balances[_Debt1][_borrower] >= shares); 
    ghostERC20Balances[_Debt1][_borrower] = ghostERC20Balances[_Debt1][_borrower] - shares;
    
    // Total debt assets decrease
    require(ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] >= _assets);
    ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] = ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] - _assets;

    // Debt tokens: _PartialLiquidation -> Silo1
    transferFromCVL(ghostToken1, _PartialLiquidation, _Silo1, _assets, true);
    
    return shares;
}

function redeemCVL(
    env e,
    address silo, 
    uint256 _shares,
    address _receiver,
    address _owner,
    ISilo.CollateralType _collateralType
)
    returns uint256
{
    uint256 assets = _shares;
    
    // Based on PartialLiquidation.sol
    assert(silo == _Silo0);
    assert(_shares == ghostConfiscatedCollateralShares);
    assert(_receiver == _HookSender);       // msg.sender 
    assert(_owner == _PartialLiquidation);  // this
    if(ghostIgnoreProtectedShares) {
        assert(_collateralType == ISilo.CollateralType.Collateral);
    } else {
        assert(_collateralType == ISilo.CollateralType.Protected);
    }

    if (_collateralType == ISilo.CollateralType.Collateral) {
        // Burn collateral shares
        assert(ghostERC20Balances[_Collateral0][_PartialLiquidation] >= _shares);
        ghostERC20Balances[_Collateral0][_PartialLiquidation] = ghostERC20Balances[_Collateral0][_PartialLiquidation] - _shares;

        // Decrease total tracked Collateral assets in Silo
        require(ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] >= assets);
        ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] = ghostTotalAssets[_Silo0][ASSET_TYPE_COLLATERAL()] - assets;
    } else {
        // Burn protected collateral shares
        assert(ghostERC20Balances[_Protected0][_PartialLiquidation] >= _shares);
        ghostERC20Balances[_Protected0][_PartialLiquidation] = ghostERC20Balances[_Protected0][_PartialLiquidation] - _shares;

        // Decrease total tracked Collateral assets in Silo
        require(ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] >= assets);
        ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] = ghostTotalAssets[_Silo0][ASSET_TYPE_PROTECTED()] - assets;
    }
    
    // Send underlying assets Token0 from Silo to HookSender
    require(ghostERC20Balances[ghostToken0][_Silo0] >= assets);
    ghostERC20Balances[ghostToken0][_Silo0] = ghostERC20Balances[ghostToken0][_Silo0] - assets;
    ghostERC20Balances[ghostToken0][_HookSender] = ghostERC20Balances[ghostToken0][_HookSender] + assets;

    return assets;
}

function previewRedeemCVL(address silo, uint256 _shares, ISilo.CollateralType _collateralType) returns uint256
{
    uint256 assets = _shares;
    
    assert(ghostReceiveSToken == true);
    assert(silo == _Silo0); // Collateral silo based on liquidationCallValidFlexibleCVL()
    assert(_shares != 0);
    
    // Check sender receive shares
    if(ghostIgnoreProtectedShares) {
        assert(_collateralType == ISilo.CollateralType.Collateral);
        assert(ghostERC20Balances[_Collateral0][_HookSender] >= ghostConfiscatedCollateralShares);

    } else {
        assert(_collateralType == ISilo.CollateralType.Protected);
        assert(ghostERC20Balances[_Protected0][_HookSender] >= ghostConfiscatedCollateralShares);
    }

    return assets;
}
