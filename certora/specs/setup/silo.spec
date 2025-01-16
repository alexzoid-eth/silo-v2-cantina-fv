// Silo core

import "./siloStorage.spec";
import "./siloConfig.spec";
import "./helperCVL.spec";
import "./erc20CVL.spec";
import "./siloERC20.spec";

using SiloHarness as _Silo;

methods {
    function _Silo.initialize(address _config) external => NONDET DELETE;
}

persistent ghost address ghostCaller;

function requireValidEnv(env e) {
    // Avoid reverting due non-zero msg.value
    require(e.msg.value == 0);

    // Valid msg.sender
    require(e.msg.sender != 0 && e.msg.sender != currentContract);
    require(ghostCaller == e.msg.sender);
}
