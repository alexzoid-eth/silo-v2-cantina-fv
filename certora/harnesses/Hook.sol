// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { ISiloConfig } from "silo-core/contracts/interfaces/ISiloConfig.sol";
import { ISilo } from "silo-core/contracts/interfaces/ISilo.sol";
import { IPartialLiquidation } from "silo-core/contracts/interfaces/IPartialLiquidation.sol";
import { IERC20 } from "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract Hook {
    ISiloConfig internal immutable _CONFIG;
    ISilo internal immutable _SILO0;
    ISilo internal immutable _SILO1;
    IPartialLiquidation internal immutable _HOOK_RECEIVER;
    address internal immutable _TOKEN0;
    address internal immutable _TOKEN1;

    function liquidationCallValidFlexible(
        address _borrower,
        uint256 _maxDebtToCover,
        bool _receiveSToken,
        bool _bypassInterest,
        bool _ignoreProtectedShares,
        bool _ignoreCollateralShares
    )
        internal
        returns (uint256 withdrawCollateral, uint256 repayDebtAssets)
    {
        // Assume interest is already accrued for both SILOs this block
        if (_bypassInterest) {
            (, uint64 interestRateTimestamp0, , , ) = _SILO0.getSiloStorage();
            (, uint64 interestRateTimestamp1, , , ) = _SILO1.getSiloStorage();
            require(
                interestRateTimestamp0 == block.timestamp &&
                interestRateTimestamp1 == block.timestamp
            );
        }

        // Only one of the two share types can be ignored, not both
        require(
            !_ignoreProtectedShares || !_ignoreCollateralShares
        );

        (ISiloConfig.ConfigData memory collateralConfig, ISiloConfig.ConfigData memory debtConfig) = 
            _CONFIG.getConfigsForSolvency(_borrower);

        if (_ignoreProtectedShares) {
            require(
                IERC20(collateralConfig.protectedShareToken).balanceOf(_borrower) == 0
            );
        } 
        else if (_ignoreCollateralShares) {
            require(
                IERC20(collateralConfig.collateralShareToken).balanceOf(_borrower) == 0
            );
        }
        
        // Actual liquidation call
        (withdrawCollateral, repayDebtAssets) = _HOOK_RECEIVER.liquidationCall(
            _TOKEN0,
            _TOKEN1,
            _borrower,
            _maxDebtToCover,
            _receiveSToken
        );
    }

    // 1) Protected allowed, no bypass, receiveSToken = false
    //    => _ignoreProtectedShares = false, _ignoreCollateralShares = true
    //    => _bypassInterest = false, _receiveSToken = false
    function liquidationCall_noSToken_noBypass_protectedAllowed(
        address _borrower,
        uint256 _maxDebtToCover
    )
        external
        returns (uint256 withdrawCollateral, uint256 repayDebtAssets)
    {
        return liquidationCallValidFlexible(_borrower, _maxDebtToCover, false, false, false, true);
    }

    // 2) Protected allowed, bypass interest, receiveSToken = true
    //    => _ignoreProtectedShares = false, _ignoreCollateralShares = true
    //    => _bypassInterest = true, _receiveSToken = true
    function liquidationCall_receiveSToken_bypassInterest_protectedAllowed(
        address _borrower,
        uint256 _maxDebtToCover
    )
        external
        returns (uint256 withdrawCollateral, uint256 repayDebtAssets)
    {
        return liquidationCallValidFlexible(_borrower, _maxDebtToCover, true, true, false, true);
    }

    // 3) Collateral allowed, bypass interest, receiveSToken = false
    //    => _ignoreProtectedShares = true, _ignoreCollateralShares = false
    //    => _bypassInterest = true, _receiveSToken = false
    function liquidationCall_noSToken_bypassInterest_collateralAllowed(
        address _borrower,
        uint256 _maxDebtToCover
    )
        external
        returns (uint256 withdrawCollateral, uint256 repayDebtAssets)
    {
        return liquidationCallValidFlexible(_borrower, _maxDebtToCover, false, true, true, false);
    }

    // 4) Collateral allowed, bypass interest, receiveSToken = true
    //    => _ignoreProtectedShares = true, _ignoreCollateralShares = false
    //    => _bypassInterest = true, _receiveSToken = true
    function liquidationCall_receiveSToken_bypassInterest_collateralAllowed(
        address _borrower,
        uint256 _maxDebtToCover
    )
        external
        returns (uint256 withdrawCollateral, uint256 repayDebtAssets)
    {
        return liquidationCallValidFlexible(_borrower, _maxDebtToCover, true, true, true, false);
    }
}
