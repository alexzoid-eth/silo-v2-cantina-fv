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

    // Valid time
    require(e.block.timestamp != 0);
    require(e.block.number != 0);
}

function requireSameEnv(env e1, env e2) {
    require(e1.block.number == e2.block.number);
    require(e1.block.timestamp == e2.block.timestamp);
    require(e1.msg.sender == e2.msg.sender);
    require(e1.msg.value == e2.msg.value);
}