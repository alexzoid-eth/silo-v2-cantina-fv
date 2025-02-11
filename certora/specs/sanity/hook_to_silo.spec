// PartialLiquidation sanity for full silo configuration 

import "../setup/silo/silo_valid_state.spec";
import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";

import "../setup/partial_liquidation/partial_liquidation_to_silo.spec";

rule sanity_liquidationCall_noSToken_noBypass_protectedAllowed(
    env e,         
    address _borrower,
    uint256 _maxDebtToCover
) {
    setupSilo(e);
    liquidationCall_noSToken_noBypass_protectedAllowed(e, _borrower, _maxDebtToCover);
    satisfy(true);
}

rule sanity_liquidationCall_receiveSToken_bypassInterest_protectedAllowed(
    env e,         
    address _borrower,
    uint256 _maxDebtToCover
) {
    setupSilo(e);
    liquidationCall_receiveSToken_bypassInterest_protectedAllowed(e, _borrower, _maxDebtToCover);
    satisfy(true);
}

rule sanity_liquidationCall_noSToken_bypassInterest_collateralAllowed(
    env e,         
    address _borrower,
    uint256 _maxDebtToCover
) {
    setupSilo(e);
    liquidationCall_noSToken_bypassInterest_collateralAllowed(e, _borrower, _maxDebtToCover);
    satisfy(true);
}

rule sanity_liquidationCall_receiveSToken_bypassInterest_collateralAllowed(
    env e,         
    address _borrower,
    uint256 _maxDebtToCover
) {
    setupSilo(e);
    liquidationCall_receiveSToken_bypassInterest_collateralAllowed(e, _borrower, _maxDebtToCover);
    satisfy(true);
}