import "./partial_liquidation_lib.spec";

methods {
    // UNSAFE: exclude solvency check from user flow
    function SiloSolvencyLib.isSolvent(
        ISiloConfig.ConfigData memory _collateralConfig,
        ISiloConfig.ConfigData memory _debtConfig,
        address _borrower,
        ISilo.AccrueInterestInMemory _accrueInMemory
    ) internal returns bool
    => ghostUserSolvent[_borrower];
}

persistent ghost mapping(address => bool) ghostUserSolvent {
    init_state axiom forall address user. ghostUserSolvent[user] == false;
}

// @todo summarize redeem/preview