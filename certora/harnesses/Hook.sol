// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { PartialLiquidation } from "silo-core/contracts/utils/hook-receivers/liquidation/PartialLiquidation.sol";

contract Hook is PartialLiquidation {

    address internal immutable _TOKEN0;
    address internal immutable _TOKEN1;

    function liquidationCall_receiveSTokenTrue(
        address _borrower,
        uint256 _maxDebtToCover
    ) external returns (uint256 withdrawCollateral, uint256 repayDebtAssets) {

        require(_maxDebtToCover < type(uint64).max);

        (withdrawCollateral, repayDebtAssets) = liquidationCall(
            _TOKEN0,
            _TOKEN1,
            _borrower,
            _maxDebtToCover,
            true
        );
    }

    function liquidationCall_receiveSTokenFalse(
        address _borrower,
        uint256 _maxDebtToCover
    ) external returns (uint256 withdrawCollateral, uint256 repayDebtAssets) {

        require(_maxDebtToCover < type(uint64).max);

        (withdrawCollateral, repayDebtAssets) = liquidationCall(
            _TOKEN0,
            _TOKEN1,
            _borrower,
            _maxDebtToCover,
            false
        );
    }
}
