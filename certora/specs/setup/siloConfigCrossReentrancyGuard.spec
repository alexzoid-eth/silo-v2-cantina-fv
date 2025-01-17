// Silo config's CrossReentrancyGuard implemented in CVL

methods {
    function _.turnOnReentrancyProtection() external with (env e)
        => turnOnReentrancyProtectionCVL(e) expect void;

    function _.turnOffReentrancyProtection() external with (env e)
        => turnOffReentrancyProtectionCVL(e) expect void;

    function _.reentrancyGuardEntered() external
        => reentrancyGuardEnteredCVL() expect bool;
}

definition _NOT_ENTERED() returns mathint = 0;
definition _ENTERED() returns mathint = 1;

persistent ghost mathint ghostCrossReentrantStatus {
    init_state axiom ghostCrossReentrantStatus == _NOT_ENTERED();
    axiom ghostCrossReentrantStatus == _NOT_ENTERED() || ghostCrossReentrantStatus == _ENTERED();
}

// Set true when on or off was execute twice
ghost bool ghostReentrancyProtectionDoubleCall;

function turnOnReentrancyProtectionCVL(env e) {

    _SiloConfig.onlySiloOrTokenOrHookReceiverHarness(e);

    ghostReentrancyProtectionDoubleCall = ghostCrossReentrantStatus == _ENTERED();
    ASSERT(ghostCrossReentrantStatus != _ENTERED());
    
    ghostCrossReentrantStatus = _ENTERED();
}

function turnOffReentrancyProtectionCVL(env e) {

    _SiloConfig.onlySiloOrTokenOrHookReceiverHarness(e);

    ghostReentrancyProtectionDoubleCall = ghostCrossReentrantStatus == _NOT_ENTERED();
    ASSERT(ghostCrossReentrantStatus != _NOT_ENTERED());
    
    ghostCrossReentrantStatus = _NOT_ENTERED();
}

function reentrancyGuardEnteredCVL() returns bool {
    return ghostCrossReentrantStatus == _ENTERED();
}
