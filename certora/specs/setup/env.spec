// Common environment for all tested contracts

import "./helper_cvl.spec";
import "./math_cvl.spec";

persistent ghost address ghostCaller;

function requireValidEnv(env e) {
    // Avoid reverting due non-zero msg.value
    require(e.msg.value == 0);

    // Valid msg.sender
    require(e.msg.sender != 0 && e.msg.sender != currentContract);
    require(ghostCaller == e.msg.sender);
}
