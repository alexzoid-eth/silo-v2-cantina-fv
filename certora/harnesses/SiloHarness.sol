// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { Silo } from "silo-core/contracts/Silo.sol";
import { ISiloFactory } from "silo-core/contracts/interfaces/ISiloFactory.sol";
import { IERC20R } from "silo-core/contracts/interfaces/IERC20R.sol";
import { IShareToken } from "silo-core/contracts/interfaces/IShareToken.sol";
import { ISilo } from "silo-core/contracts/interfaces/ISilo.sol";
import { SafeERC20 } from "openzeppelin5/token/ERC20/utils/SafeERC20.sol";

import { ERC20Upgradeable } from "openzeppelin5-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import { NoncesUpgradeable } from "openzeppelin5-upgradeable/utils/NoncesUpgradeable.sol";
import { EIP712Upgradeable } from "openzeppelin5-upgradeable/utils/cryptography/EIP712Upgradeable.sol";
import { Initializable } from "@openzeppelin/contracts/proxy/utils/Initializable.sol";

import { Actions } from "silo-core/contracts/lib/Actions.sol";
import { SiloERC4626Lib } from "silo-core/contracts/lib/SiloERC4626Lib.sol";
import { SiloMathLib } from "silo-core/contracts/lib/SiloMathLib.sol";

import { HelperCVL, IUnresolvedCall } from "./HelperCVL.sol";

abstract contract SiloHarness is Silo, HelperCVL {
    constructor(ISiloFactory _siloFactory) Silo(_siloFactory) { }

    // Map storage 

    // 0x01b0b3f9d6e360167e522fa2b18ba597ad7b2b35841fec7e1ca4dbb0adea1200
    uint256[764520080237424869752330524124367139483859928243420876645759593088794890752] private _relativeOffset1;
    IShareToken.ShareTokenStorage private shareTokenStorage; // 4 slots
    
    // 0x52c63247e1f47db19d5ce0460030c497f067ca4cebf71ba98eeadabe20bace00
    uint256[36675316247685935355585565347270393484796677538529859497619462915077111331836] private _relativeOffset2;
    ERC20Upgradeable.ERC20Storage private erc20Storage; // 5 slots
    
    // 0x5a499b742bad5e18c139447ced974d19a977bcf86e03691ee458d10efcd04d00
    uint256[3398372782936750532598662385469945099948450566250362509185534835799841144571] private _relativeOffset3;
    IERC20R.Storage private iERC20RStorage; // 1 slot (not in use)
    
    // 0x5ab42ced628888259c08ac98db1eb0cf702fc1501344311d8b100cd1bfe4bb00
    uint256[188289810017362792616136603551264427055408370604868558661199683125064789503] private _relativeOffset4;
    NoncesUpgradeable.NoncesStorage private noncesStorage; // 1 slot (not in use)

    // 0xa16a46d94261c7517cc8ff89f61c0ce93598e3c849801011dee649a6a557d100
    uint256[31983644469438460855457864970702758242316333351067685845255559058820655420927] private _relativeOffset5;
    EIP712Upgradeable.EIP712Storage private eip712Storage; // 4 slots (not in use)

    // 0xd7513ffe3a01a9f6606089d1b67011bca35bec018ac0faa914e1c529408f8300
    uint256[24380675331288486898706811435138660356087723579803824137572707285927581954556] private _relativeOffset6;
    ISilo.SiloStorage private siloStorage; // 2 slots

    // 0xf0c57e16840df040f15088dc2f81fe391c3923bec73e23a9662efc9c229c6a00
    // Don't worry about `initializableStorage` somewhere in the bottom

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