// Environment 

persistent ghost address ghostContract {
    axiom ghostContract == currentContract;
}

persistent ghost address ghostCaller;

function requireValidEnv(env e) {
    // Avoid reverting due non-zero msg.value
    require(e.msg.value == 0);

    // Valid msg.sender
    require(e.msg.sender != 0 && e.msg.sender != currentContract);
    require(ghostCaller == e.msg.sender);
}
