// Common valid state invariants working both for Silo0 and Silo1

function requireSiloCommonValidState() {
    requireInvariant crossReentrancyGuardOpenedOnExit;
    requireInvariant crossReentrancyProtectionNoDoubleCall;
}

function requireSiloCommonValidStateEnv(env e) {
    requireSiloCommonValidState();
    requireErc20ValidState();
}

// CrossReentrancyGuard

invariant crossReentrancyGuardOpenedOnExit()
    ghostCrossReentrantStatus == _NOT_ENTERED();

invariant crossReentrancyProtectionNoDoubleCall()
    ghostReentrancyProtectionDoubleCall == false;