// Global valid state

function requireValidState() {
    requireInvariant crossReentrancyGuardOpenedOnExit;
    requireInvariant crossReentrancyProtectionNoDoubleCall;
}

// CrossReentrancyGuard

invariant crossReentrancyGuardOpenedOnExit()
    ghostCrossReentrantStatus == _NOT_ENTERED();

invariant crossReentrancyProtectionNoDoubleCall()
    ghostReentrancyProtectionDoubleCall == false;