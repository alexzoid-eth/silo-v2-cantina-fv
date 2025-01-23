// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { ShareDebtToken } from "silo-core/contracts/utils/ShareDebtToken.sol";
import { IShareToken } from "silo-core/contracts/interfaces/IShareToken.sol";
import { ERC20Upgradeable } from "openzeppelin5-upgradeable/token/ERC20/ERC20Upgradeable.sol";
import { IERC20R } from "silo-core/contracts/interfaces/IERC20R.sol";

abstract contract ShareDebtTokenHarness is ShareDebtToken {    

    // 0x01b0b3f9d6e360167e522fa2b18ba597ad7b2b35841fec7e1ca4dbb0adea1200
    uint256[764520080237424869752330524124367139483859928243420876645759593088794890752] private _relativeOffset1;
    IShareToken.ShareTokenStorage private shareTokenStorage; // 4 slots total
    
    // 0x52c63247e1f47db19d5ce0460030c497f067ca4cebf71ba98eeadabe20bace00
    uint256[36675316247685935355585565347270393484796677538529859497619462915077111331836] private _relativeOffset2;
    ERC20Upgradeable.ERC20Storage private erc20Storage; // 5 slots

    // 0x5a499b742bad5e18c139447ced974d19a977bcf86e03691ee458d10efcd04d00
    uint256[3398372782936750532598662385469945099948450566250362509185534835799841144571] private _relativeOffset3;
    IERC20R.Storage private iERC20RStorage; // 1 slot
}
