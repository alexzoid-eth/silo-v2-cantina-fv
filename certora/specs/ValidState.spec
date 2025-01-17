// CrossReentrancyGuard

invariant crossReentrancyGuardOpenedOnExit()
    ghostCrossReentrantStatus == _NOT_ENTERED();

invariant crossReentrancyProtectionNoDoubleCall()
    ghostReentrancyProtectionDoubleCall == false;