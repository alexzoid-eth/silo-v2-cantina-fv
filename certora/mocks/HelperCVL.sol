// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.20;

import { SiloMathLib } from "silo-core/contracts/lib/SiloMathLib.sol";

interface IUnresolvedCall {
    function unresolvedCall() external;
}

contract HelperCVL {
    
    address public _target;

    function makeUnresolvedCall() external {
        IUnresolvedCall(_target).unresolvedCall();
    }

    function assertOnFalse(bool b) external pure {
        assert(b);
    }

    function getCollateralAmountsWithInterestHarness(
        uint256 _collateralAssets,
        uint256 _debtAssets,
        uint256 _rcomp,
        uint256 _daoFee,
        uint256 _deployerFee
    )
        external
        pure
        returns (
            uint256 collateralAssetsWithInterest,
            uint256 debtAssetsWithInterest,
            uint256 daoAndDeployerRevenue,
            uint256 accruedInterest
        ) {
        (collateralAssetsWithInterest, debtAssetsWithInterest, daoAndDeployerRevenue, accruedInterest) 
            = SiloMathLib.getCollateralAmountsWithInterest(_collateralAssets, _debtAssets, _rcomp, _daoFee, _deployerFee);
    }
}