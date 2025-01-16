// Silo config implemented in CVL

import "./siloConfigCrossReentrancyGuard.spec";

methods {
    function _.getAssetForSilo(address _silo) external
        => ghostConfigToken0 expect address;
}

persistent ghost address ghostConfigToken0 {
    axiom ghostConfigToken0 == ghostERC20CVLToken[0];
}

persistent ghost mapping(address => address) ghostBorrowerCollateralSilo;

definition onlySiloOrTokenOrHookReceiver(address caller) returns bool =
    caller == _Silo
    || caller == ghostConfigToken0
    // @todo
    ;
