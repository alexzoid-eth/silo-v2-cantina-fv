import "./partial_liquidation_lib.spec";

using Hook as _HookSender;
using PartialLiquidation as _PartialLiquidation;

// UNSAFE: everything extremely simplified (1-to-1 conversion)
methods {
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

    function _.repay(uint256 _assets, address _borrower) external with (env e)
        => repayCVL(e, _assets, _borrower) expect uint256;

    function _.redeem(uint256 _shares, address _receiver, address _owner, ISilo.CollateralType _collateralType) external with (env e)
        => redeemCVL(e, _shares, _receiver, _owner, to_mathint(_collateralType)) expect uint256;

    function _.previewRedeem(uint256 _shares, ISilo.CollateralType _collateralType) external
        => previewRedeemCVL(_shares, to_mathint(_collateralType)) expect uint256;
}

definition _DUST() returns mathint = 100;

function setupBorrower(address borrower) {

    require(borrower != 0);

    // Has collateral set in config
    require(isConfigBorrowerCollateralSiloValid(borrower));

    // Has collateral shares
    require(ghostConfigBorrowerCollateralSilo[borrower] == _Silo0
        ? ghostERC20Balances[_Collateral0][borrower] + ghostERC20Balances[_Protected0][borrower] > _DUST()
        : ghostERC20Balances[_Collateral1][borrower] + ghostERC20Balances[_Protected1][borrower] > _DUST()
    );

    // Has debt
    require(ghostERC20Balances[_Debt0][borrower] > _DUST()
        || ghostERC20Balances[_Debt1][borrower] > _DUST()
        );
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

function repayCVL(env e, uint256 _assets, address _borrower)
    returns uint256
{
    // For harness only, treat 1 underlying asset = 1 debt share
    uint256 shares = _assets;

    assert(_assets != 0);
    assert(_borrower != 0);

    // Borrower's shares decrease
    require(ghostERC20Balances[_Debt1][_borrower] >= shares);
    ghostERC20Balances[_Debt1][_borrower] = ghostERC20Balances[_Debt1][_borrower] - shares;
    
    // Total debt assets decrease
    require(ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] >= _assets);
    ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] = ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] - _assets;

    // Repayer's underlying tokens decrease, Silo's token balance increases
    require(ghostERC20Balances[ghostToken1][_PartialLiquidation] >= _assets);
    ghostERC20Balances[ghostToken1][_PartialLiquidation] = ghostERC20Balances[ghostToken1][_PartialLiquidation] - _assets;
    ghostERC20Balances[ghostToken1][_Silo1] = ghostERC20Balances[ghostToken1][_Silo1] + _assets;

    return shares;
}

persistent ghost mathint ghostRedeemType;
function redeemCVL(
    env e,
    uint256 _shares,
    address _receiver,
    address _owner,
    mathint _collateralType
)
    returns uint256
{
    uint256 assets = _shares;

    // Based on PartialLiquidation.sol
    assert(_receiver == _HookSender);       // msg.sender 
    assert(_owner == _PartialLiquidation);  // this

    ghostRedeemType = _collateralType;

    if (_collateralType == ASSET_TYPE_COLLATERAL()) {
        // Check the owner has enough "collateral share" balance
        require(ghostERC20Balances[_Silo1][_owner] >= _shares);
        ghostERC20Balances[_Silo1][_owner] = ghostERC20Balances[_Silo1][_owner] - _shares;

        // Decrease total tracked Collateral assets in Silo
        require(ghostTotalAssets[_Silo1][ASSET_TYPE_COLLATERAL()] >= _shares);
        ghostTotalAssets[_Silo1][ASSET_TYPE_COLLATERAL()] = ghostTotalAssets[_Silo1][ASSET_TYPE_COLLATERAL()] - _shares;

        // Send underlying assets from Silo to `_owner` (or `_receiver`, but here `_receiver == _owner`)
        require(ghostERC20Balances[ghostToken1][_Silo1] >= _shares);
        ghostERC20Balances[ghostToken1][_Silo1] = ghostERC20Balances[ghostToken1][_Silo1] - _shares;
        ghostERC20Balances[ghostToken1][_owner] = ghostERC20Balances[ghostToken1][_owner] + _shares;

    } else if (_collateralType == ASSET_TYPE_PROTECTED()) {
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

    } else {
        assert(false, "Unknown collateralType");
    }

    return assets;
}

persistent ghost mathint ghostPreviewRedeemType;
function previewRedeemCVL(uint256 _shares, mathint _collateralType) returns uint256
{
    assert(_shares != 0);
    assert(_collateralType == ASSET_TYPE_COLLATERAL() 
        || _collateralType == ASSET_TYPE_PROTECTED());

    ghostPreviewRedeemType = _collateralType;

    return _shares;
}
