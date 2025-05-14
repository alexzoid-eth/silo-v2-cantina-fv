import "../silo/silo_math_lib.spec";

using Hook as _HookSender;
using PartialLiquidation as _PartialLiquidation;

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
            e, 
            _borrower, 
            _maxDebtToCover, 
            _receiveSToken, 
            _bypassInterest, 
            _ignoreProtectedShares, 
            _ignoreCollateralShares
        );
    
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
    
    function SiloSolvencyLib.isSolvent(
        ISiloConfig.ConfigData memory,
        ISiloConfig.ConfigData memory,
        address _borrower,
        ISilo.AccrueInterestInMemory
    ) internal returns bool
        => ghostUserSolvent[_borrower];

    function _.forwardTransferFromNoChecks(address _from, address _to, uint256 _amount) external
        => DISPATCHER(true);

    function _.repay(uint256 _assets, address _borrower) external
        => DISPATCHER(true);

    function _.redeem(uint256 _shares, address _receiver, address _owner, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);

    function _.previewRedeem(uint256 _shares, ISilo.CollateralType _collateralType) external
        => NONDET;
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
            require(withdrawAssetsFromCollateral > _DUST() && withdrawAssetsFromCollateral 
                <= ghostERC20Balances[_Collateral0][_user]);
            require(withdrawAssetsFromProtected == 0);
        } else {
            require(ghostERC20Balances[_Collateral0][_user] == 0);
            require(withdrawAssetsFromCollateral == 0);
            require(withdrawAssetsFromProtected > _DUST() && withdrawAssetsFromProtected 
                <= ghostERC20Balances[_Protected0][_user]);
        }
        require(repayDebtAssets != 0);
        
        return (withdrawAssetsFromCollateral, withdrawAssetsFromProtected, repayDebtAssets, to_bytes4(0));
    }
}

persistent ghost mapping(address => bool) ghostUserSolvent {
    init_state axiom forall address user. ghostUserSolvent[user] == false;
}