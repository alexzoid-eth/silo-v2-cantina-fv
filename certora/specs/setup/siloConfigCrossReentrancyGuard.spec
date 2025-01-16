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

function turnOnReentrancyProtectionCVL(env e) {

    ASSERT(onlySiloOrTokenOrHookReceiver(e.msg.sender));

    ASSERT(ghostCrossReentrantStatus != _ENTERED());
    
    ghostCrossReentrantStatus = _ENTERED();
}

function turnOffReentrancyProtectionCVL(env e) {

    ASSERT(onlySiloOrTokenOrHookReceiver(e.msg.sender));

    ASSERT(ghostCrossReentrantStatus != _NOT_ENTERED());
    
    ghostCrossReentrantStatus = _NOT_ENTERED();
}

function reentrancyGuardEnteredCVL() returns bool {
    return ghostCrossReentrantStatus == _ENTERED();
}
