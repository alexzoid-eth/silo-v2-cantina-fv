// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import {IPartialLiquidation} from "silo-core/contracts/interfaces/IPartialLiquidation.sol";
import { ISilo } from "silo-core/contracts/interfaces/ISilo.sol";

contract Hook {

    IPartialLiquidation internal immutable _HOOK_RECEIVER;
    address internal immutable _TOKEN0;
    address internal immutable _TOKEN1;

    function liquidationCall_receiveSTokenTrue(
        address _borrower,
        uint256 _maxDebtToCover
    ) external returns (uint256 withdrawCollateral, uint256 repayDebtAssets) {

        require(_maxDebtToCover < type(uint64).max);

        (withdrawCollateral, repayDebtAssets) = _HOOK_RECEIVER.liquidationCall(
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

        (withdrawCollateral, repayDebtAssets) = _HOOK_RECEIVER.liquidationCall(
            _TOKEN1,
            _TOKEN0,
            _borrower,
            _maxDebtToCover,
            false
        );
    }
}
