import "./partial_liquidation_lib.spec";

using PartialLiquidation as _PartialLiquidation;

// UNSAFE: everything extremely simplified
methods {
    function SiloSolvencyLib.isSolvent(
        ISiloConfig.ConfigData memory _collateralConfig,
        ISiloConfig.ConfigData memory _debtConfig,
        address _borrower,
        ISilo.AccrueInterestInMemory _accrueInMemory
    ) internal returns bool
    => ghostUserSolvent[_borrower];

    function _.repay(uint256 _assets, address _borrower) external with (env e)
        => repayCVL(e, _assets, _borrower) expect uint256;

    function _.redeem(uint256 _shares, address _receiver, address _owner, ISilo.CollateralType _collateralType) external with (env e)
        => redeemCVL(e, _shares, _receiver, _owner, _collateralType) expect uint256;
}

persistent ghost mapping(address => bool) ghostUserSolvent {
    init_state axiom forall address user. ghostUserSolvent[user] == false;
}

function repayCVL(env e, uint256 _assets, address _borrower) returns uint256 {
    mathint shares;
    
    // Borrower's shares decrease
    require(ghostERC20Balances[_Debt1][_borrower] >= shares);
    ghostERC20Balances[_Debt1][_borrower] = ghostERC20Balances[_Debt1][_borrower] - shares;
    
    // Total debt assets decrease
    require(ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] >= _assets);
    ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] = ghostTotalAssets[_Silo1][ASSET_TYPE_DEBT()] - _assets;

    // Repayer assets decrease, Silo assets increase
    require(ghostERC20Balances[_Token1][e.msg.sender] >= _assets);
    ghostERC20Balances[_Token1][e.msg.sender] = ghostERC20Balances[_Token1][e.msg.sender] - _assets;
    ghostERC20Balances[_Token1][_Silo1] = ghostERC20Balances[_Token1][_Silo1] + _assets;

    return shares;
}

function redeemCVL(env e, uint256 _shares, address _receiver, address _owner, mathint _collateralType) returns uint256 {
    mathint assets;

    assert(_receiver == e.msg.sender);
    assert(_owner == _PartialLiquidation);

    // Owner's shares decrease
    require(ghostERC20Balances[_Collateral1][_owner] >= _shares);
    ghostERC20Balances[_Collateral1][_owner] = ghostERC20Balances[_Collateral1][_owner] - _shares;

    // Total collateral assets decrease
    require(ghostTotalAssets[_Silo1][ASSET_TYPE_COLLATERAL()] >= _shares);
    ghostTotalAssets[_Silo1][ASSET_TYPE_COLLATERAL()] = ghostTotalAssets[_Silo1][ASSET_TYPE_COLLATERAL()] - _shares;

    // Owner receives assets
    require(ghostERC20Balances[_Token1][_Silo1] >= _shares);
    ghostERC20Balances[_Token1][_Silo1] = ghostERC20Balances[_Token1][_Silo1] - _shares;
    ghostERC20Balances[_Token1][_owner] = ghostERC20Balances[_Token1][_owner] + _shares;

    return assets;
}