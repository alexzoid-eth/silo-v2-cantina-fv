// Silo1 violated rule

import "./setup/silo0/silo0.spec";
import "./setup/silo1/silo1.spec";
import "./setup/silo/silo_valid_state.spec";

import "./setup/silo/silo_factory.spec";

// Even if a third party calls the silo, deployer fee receiver can still withdraw
rule silo_deployerFeeReceiverCannotBeBlocked(env e, method f, calldataarg args) {

    setupSilo(e);

    // Must have a valid, nonzero fee receiver
    address deployerFeeReceiver = ghostDeployerFeeReceiver[ghostSiloId];
    require(deployerFeeReceiver != 0);

    // Some other address calls arbitrary function (`SiloFactory.burn()`)
    require(e.msg.sender != deployerFeeReceiver);
    f@withrevert(e, args);

    // Check receiver's balance before/after
    mathint balBefore = ghostERC20Balances[ghostToken1][deployerFeeReceiver];

    _Silo1.withdrawFees(e);

    mathint balAfter = ghostERC20Balances[ghostToken1][deployerFeeReceiver];

    satisfy(balAfter > balBefore);
}
