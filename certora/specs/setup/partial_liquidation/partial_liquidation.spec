import "./partial_liquidation_lib.spec";

using Hook as _HookSender;
using PartialLiquidation as _PartialLiquidation;

// UNSAFE: everything extremely simplified
// collateral - silo0
// debt - silo1
// 1-to-1 conversion

methods {

    function _.liquidationCallValidFlexible(
        address _borrower,
        uint256 _maxDebtToCover,
        bool _receiveSToken,
        bool _bypassInterest,
        bool _ignoreProtectedShares,
        bool _ignoreCollateralShares
    ) external with (env e)
        => liquidationCallValidFlexibleCVL(
            e, _borrower, _maxDebtToCover, _receiveSToken, _bypassInterest, _ignoreProtectedShares, _ignoreCollateralShares
        ) expect (uint256, uint256);

    function SiloSolvencyLib.isSolvent(
        ISiloConfig.ConfigData memory,
        ISiloConfig.ConfigData memory,
        address _borrower,
        ISilo.AccrueInterestInMemory
    ) internal returns bool
        => ghostUserSolvent[_borrower];

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

    function _.repay(uint256 _assets, address _borrower) external with (env e)
        => repayCVL(e, calledContract, _assets, _borrower) expect uint256;

    function _.redeem(uint256 _shares, address _receiver, address _owner, ISilo.CollateralType _collateralType) external with (env e)
        => redeemCVL(e, calledContract, _shares, _receiver, _owner, _collateralType) expect uint256;

    function _.previewRedeem(uint256 _shares, ISilo.CollateralType _collateralType) external
        => previewRedeemCVL(calledContract, _shares, _collateralType) expect uint256;
}

definition _DUST() returns mathint = 100;

function setupValidBorrowerWithDebtCollateral(address borrower) {

    require(borrower != 0);

    // Has collateral in Silo0
    require(ghostConfigBorrowerCollateralSilo[borrower] == _Silo0
        && ghostERC20Balances[_Collateral0][borrower] + ghostERC20Balances[_Protected0][borrower] > _DUST()
    );

    // Has debt in Silo1
    require(ghostERC20Balances[_Debt1][borrower] > _DUST());
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

    ghostBorrower = _borrower;
    ghostMaxDebtToCover = _maxDebtToCover;
    ghostReceiveSToken = _receiveSToken;
    ghostIgnoreProtectedShares = _ignoreProtectedShares;
    ghostIgnoreCollateralShares = _ignoreCollateralShares;

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

function convertToAssetsCVL(uint256 _shares) returns uint256 {
    return _shares;
}

function convertToSharesCVL(uint256 _assets) returns uint256 {
    return _assets;
}

function getTotalAssetsStorageCVL(address silo, mathint assetType) returns uint256 {

    // Collateral Silo
    assert(silo == _Silo0);

    // Selected collateral shares
    if(ghostIgnoreProtectedShares) {
        assert(assetType == ASSET_TYPE_COLLATERAL());
    } else {
        assert(assetType == ASSET_TYPE_PROTECTED());
    }

    return require_uint256(ghostTotalAssets[silo][assetType]);
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
    // For harness only, treat 1 underlying asset = 1 debt share
    uint256 shares = _assets;
    
    assert(silo == _Silo1); // Debt silo based on liquidationCallValidFlexibleCVL()
    assert(ghostMaxDebtToCover != 0);
    assert(_assets != 0 && _assets <= ghostMaxDebtToCover);
    assert(_borrower != 0 && _borrower == ghostBorrower);

    // Debt tokens (Token1) were transferred earlier from _HookSender
    assert(ghostERC20Balances[ghostToken1][_PartialLiquidation] >= _assets);

    // Allowance must be set before transferFrom()
    assert(ghostERC20Allowances[ghostToken1][_PartialLiquidation][_Silo1] >= _assets);

    // Borrower's shares decrease
    require(ghostERC20Balances[_Debt1][_borrower] >= shares); // @todo assert?
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
    assert(silo == _Silo0); // Collateral silo based on liquidationCallValidFlexibleCVL()
    assert(_shares != 0);
    assert(_receiver == _HookSender);       // msg.sender 
    assert(_owner == _PartialLiquidation);  // this
    if(ghostIgnoreProtectedShares) {
        assert(_collateralType == ISilo.CollateralType.Collateral);
    } else {
        assert(_collateralType == ISilo.CollateralType.Protected);
    }

    if (_collateralType == ISilo.CollateralType.Collateral) {
        // Check the owner has enough "collateral share" balance
        require(ghostERC20Balances[silo][_owner] >= _shares);
        ghostERC20Balances[silo][_owner] = ghostERC20Balances[silo][_owner] - _shares;

        // Decrease total tracked Collateral assets in Silo
        require(ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()] >= _shares);
        ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()] = ghostTotalAssets[silo][ASSET_TYPE_COLLATERAL()] - _shares;

        // Send underlying assets from Silo to `_owner` (or `_receiver`, but here `_receiver == _owner`)
        require(ghostERC20Balances[ghostToken1][_Silo1] >= _shares);
        ghostERC20Balances[ghostToken1][_Silo1] = ghostERC20Balances[ghostToken1][_Silo1] - _shares;
        ghostERC20Balances[ghostToken1][_owner] = ghostERC20Balances[ghostToken1][_owner] + _shares;

    } else {
        // Check the owner has enough "protected share" balance
        require(ghostERC20Balances[_Protected1][_owner] >= _shares);
        ghostERC20Balances[_Protected1][_owner] = ghostERC20Balances[_Protected1][_owner] - _shares;

        // Decrease total tracked Protected assets in Silo
        require(ghostTotalAssets[_Silo1][ASSET_TYPE_PROTECTED()] >= _shares);
        ghostTotalAssets[_Silo1][ASSET_TYPE_PROTECTED()] = ghostTotalAssets[_Silo1][ASSET_TYPE_PROTECTED()] - _shares;

        // Send underlying assets from Silo to `_owner`
        require(ghostERC20Balances[ghostToken1][_Silo1] >= _shares);
        ghostERC20Balances[ghostToken1][_Silo1] = ghostERC20Balances[ghostToken1][_Silo1] - _shares;
        ghostERC20Balances[ghostToken1][_owner] = ghostERC20Balances[ghostToken1][_owner] + _shares;
    }
    
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
