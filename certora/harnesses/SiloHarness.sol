// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { Silo } from "silo-core/contracts/Silo.sol";
import { ISiloFactory } from "silo-core/contracts/interfaces/ISiloFactory.sol";
import { SafeERC20 } from "openzeppelin5/token/ERC20/utils/SafeERC20.sol";

import { ISilo } from "silo-core/contracts/interfaces/ISilo.sol";
import { IShareToken } from "silo-core/contracts/interfaces/IShareToken.sol";
import { IERC20R } from "silo-core/contracts/interfaces/IERC20R.sol";
import { ERC20Upgradeable } from "openzeppelin5-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import { NoncesUpgradeable } from "openzeppelin5-upgradeable/utils/NoncesUpgradeable.sol";
import { EIP712Upgradeable } from "openzeppelin5-upgradeable/utils/cryptography/EIP712Upgradeable.sol";
import { Initializable } from "@openzeppelin/contracts/proxy/utils/Initializable.sol";
import { Actions } from "silo-core/contracts/lib/Actions.sol";
import { SiloERC4626Lib } from "silo-core/contracts/lib/SiloERC4626Lib.sol";
import { SiloMathLib } from "silo-core/contracts/lib/SiloMathLib.sol";

import { HelperCVL, IUnresolvedCall } from "./HelperCVL.sol";
import { SiloStorage } from "./SiloStorage.sol";

abstract contract SiloHarness is Silo, SiloStorage, HelperCVL {
    constructor(ISiloFactory _siloFactory) Silo(_siloFactory) { }

    // Linked with Silo1 or Hook. Solidity compiler will not accept unreferenced immutable
    address private immutable _SILO_MODE;
    
    function viewSiloMode() external pure returns (address) {
        return _SILO_MODE;
    }

    // Split Collateral and Protected collateral EIP-4626 functions

    function convertToSharesCollateral(uint256 _assets) external view virtual returns (uint256 shares) {
        shares = _convertToShares(_assets, AssetType.Collateral);
    }

    function convertToSharesProtected(uint256 _assets) external view virtual returns (uint256 shares) {
        shares = _convertToShares(_assets, AssetType.Protected);
    }

    function convertToAssetsCollateral(uint256 _shares) external view virtual returns (uint256 assets) {
        assets = _convertToAssets(_shares, AssetType.Collateral);
    }

    function convertToAssetsProtected(uint256 _shares) external view virtual returns (uint256 assets) {
        assets = _convertToAssets(_shares, AssetType.Protected);
    }

    function previewDepositCollateral(uint256 _assets)
        external
        view
        virtual
        returns (uint256 shares)
    {
        return _previewDeposit(_assets, CollateralType.Collateral);
    }

    function previewDepositProtected(uint256 _assets)
        external
        view
        virtual
        returns (uint256 shares)
    {
        return _previewDeposit(_assets, CollateralType.Protected);
    }

    function depositCollateral(uint256 _assets, address _receiver)
        external
        virtual
        returns (uint256 shares)
    {
        (, shares) = _deposit(_assets, 0, _receiver, CollateralType.Collateral);
    }

    function depositProtected(uint256 _assets, address _receiver)
        external
        virtual
        returns (uint256 shares)
    {
        (, shares) = _deposit(_assets, 0, _receiver, CollateralType.Protected);
    }

    function previewMintCollateral(uint256 _shares) external view virtual returns (uint256 assets) {
        return _previewMint(_shares, CollateralType.Collateral);
    }

    function previewMintProtected(uint256 _shares) external view virtual returns (uint256 assets) {
        return _previewMint(_shares, CollateralType.Protected);
    }

    function mintCollateral(uint256 _shares, address _receiver)
        external
        virtual
        returns (uint256 assets)
    {
        (assets,) = _deposit(0, _shares, _receiver, CollateralType.Collateral);
    }

    function mintProtected(uint256 _shares, address _receiver)
        external
        virtual
        returns (uint256 assets)
    {
        (assets,) = _deposit(0, _shares, _receiver, CollateralType.Protected);
    }

    function maxWithdrawCollateral(address _owner) external view virtual returns (uint256 maxAssets) {
        (maxAssets,) = _maxWithdraw(_owner, CollateralType.Collateral);
    }

    function maxWithdrawProtected(address _owner) external view virtual returns (uint256 maxAssets) {
        (maxAssets,) = _maxWithdraw(_owner, CollateralType.Protected);
    }

    function previewWithdrawCollateral(uint256 _assets) external view virtual returns (uint256 shares) {
        return _previewWithdraw(_assets, CollateralType.Collateral);
    }

    function previewWithdrawProtected(uint256 _assets) external view virtual returns (uint256 shares) {
        return _previewWithdraw(_assets, CollateralType.Protected);
    }

    function withdrawCollateral(
        uint256 _assets,
        address _receiver,
        address _owner
    )
        external
        virtual
        returns (uint256 shares)
    {
        (, shares) = _withdraw({
            _assets: _assets,
            _shares: 0,
            _receiver: _receiver,
            _owner: _owner,
            _spender: msg.sender,
            _collateralType: CollateralType.Collateral
        });
    }

    function withdrawProtected(
        uint256 _assets,
        address _receiver,
        address _owner
    )
        external
        virtual
        returns (uint256 shares)
    {
        (, shares) = _withdraw({
            _assets: _assets,
            _shares: 0,
            _receiver: _receiver,
            _owner: _owner,
            _spender: msg.sender,
            _collateralType: CollateralType.Protected
        });
    }

    function maxRedeemCollateral(address _owner) external view virtual returns (uint256 maxShares) {
        (, maxShares) = _maxWithdraw(_owner, CollateralType.Collateral);
    }

    function maxRedeemProtected(address _owner) external view virtual returns (uint256 maxShares) {
        (, maxShares) = _maxWithdraw(_owner, CollateralType.Protected);
    }

    function previewRedeemCollateral(uint256 _shares) external view virtual returns (uint256 assets) {
        return _previewRedeem(_shares, CollateralType.Collateral);
    }

    function previewRedeemProtected(uint256 _shares) external view virtual returns (uint256 assets) {
        return _previewRedeem(_shares, CollateralType.Protected);
    }

    function redeemCollateral(
        uint256 _shares,
        address _receiver,
        address _owner
    )
        external
        virtual
        returns (uint256 assets)
    {
        (assets,) = _withdraw({
            _assets: 0,
            _shares: _shares,
            _receiver: _receiver,
            _owner: _owner,
            _spender: msg.sender,
            _collateralType: CollateralType.Collateral
        });
    }

    function redeemProtected(
        uint256 _shares,
        address _receiver,
        address _owner
    )
        external
        virtual
        returns (uint256 assets)
    {
        (assets,) = _withdraw({
            _assets: 0,
            _shares: _shares,
            _receiver: _receiver,
            _owner: _owner,
            _spender: msg.sender,
            _collateralType: CollateralType.Protected
        });
    }

    function transitionCollateralFromCollateral(
        uint256 _shares,
        address _owner
    )
        external
        virtual
        returns (uint256 assets)
    {
        (assets, ) = Actions.transitionCollateral(
            TransitionCollateralArgs({
                shares: _shares,
                owner: _owner,
                transitionFrom: CollateralType.Collateral
            })
        );
    }

    function transitionCollateralFromProtected(
        uint256 _shares,
        address _owner
    )
        external
        virtual
        returns (uint256 assets)
    {
        (assets, ) = Actions.transitionCollateral(
            TransitionCollateralArgs({
                shares: _shares,
                owner: _owner,
                transitionFrom: CollateralType.Protected
            })
        );
    }

    function maxDepositCollateral(address /* _receiver */) external pure virtual returns (uint256 maxAssets) {
        maxAssets = SiloERC4626Lib._VIRTUAL_DEPOSIT_LIMIT;
    }

    function maxDepositProtected(address /* _receiver */) external pure virtual returns (uint256 maxAssets) {
        maxAssets = SiloERC4626Lib._VIRTUAL_DEPOSIT_LIMIT;
    }

    function maxMintCollateral(address /* _receiver */) external view virtual returns (uint256 maxShares) {
        return SiloERC4626Lib._VIRTUAL_DEPOSIT_LIMIT;
    }

    function maxMintProtected(address /* _receiver */) external view virtual returns (uint256 maxShares) {
        return SiloERC4626Lib._VIRTUAL_DEPOSIT_LIMIT;
    }
}