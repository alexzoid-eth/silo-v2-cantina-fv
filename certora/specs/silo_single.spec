import "setup/silo0/silo_0.spec";

// Sanity

use builtin rule sanity;

// High Level

// The protected collateral portion must not accrue interest or be counted as borrowed liquidity.
// It should increase/decrease only from user deposits/withdrawals (no borrow/repay events).
// rule protectedCollateralNoInterestAccumulation() 

