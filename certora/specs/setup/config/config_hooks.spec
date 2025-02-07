using Config as _SiloConfig;

// SiloConfig

hook Sload address collateralSilo _SiloConfig.borrowerCollateralSilo[KEY address borrower] {
    require(ghostConfigBorrowerCollateralSilo[borrower] == collateralSilo);
}

hook Sstore _SiloConfig.borrowerCollateralSilo[KEY address borrower] address collateralSilo {
    ghostConfigBorrowerCollateralSilo[borrower] = collateralSilo;
}

// CrossReentrancyGuard

hook ALL_TLOAD(uint256 addr) uint256 val {
    if(executingContract == _SiloConfig) {
        require(require_uint256(ghostCrossReentrantStatus) == val);
    }
}

hook ALL_TSTORE(uint256 addr, uint256 val)  {
    if(executingContract == _SiloConfig) {
        ghostReentrancyProtectionDoubleCall = (val == ghostCrossReentrantStatus);
        ghostCrossReentrantStatus = val;
    }
}
