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
persistent ghost bool ghostReentrancyProtectionDoubleCall {
    init_state axiom ghostReentrancyProtectionDoubleCall == false;
}

function onlySiloOrTokenOrHookReceiverCVL(env e) {
    if (e.msg.sender != _SiloConfig._SILO0 &&
        e.msg.sender != _SiloConfig._SILO1 &&
        e.msg.sender != _SiloConfig._HOOK_RECEIVER &&
        e.msg.sender != _SiloConfig._COLLATERAL_SHARE_TOKEN0 &&
        e.msg.sender != _SiloConfig._COLLATERAL_SHARE_TOKEN1 &&
        e.msg.sender != _SiloConfig._PROTECTED_COLLATERAL_SHARE_TOKEN0 &&
        e.msg.sender != _SiloConfig._PROTECTED_COLLATERAL_SHARE_TOKEN1 &&
        e.msg.sender != _SiloConfig._DEBT_SHARE_TOKEN0 &&
        e.msg.sender != _SiloConfig._DEBT_SHARE_TOKEN1
    ) {
        ASSERT(false);
    }
}

function turnOnReentrancyProtectionCVL(env e) {

    onlySiloOrTokenOrHookReceiverCVL(e);

    ghostReentrancyProtectionDoubleCall = ghostCrossReentrantStatus == _ENTERED();
    ASSERT(ghostCrossReentrantStatus != _ENTERED());
    
    ghostCrossReentrantStatus = _ENTERED();
}

function turnOffReentrancyProtectionCVL(env e) {

    onlySiloOrTokenOrHookReceiverCVL(e);

    ghostReentrancyProtectionDoubleCall = ghostCrossReentrantStatus == _NOT_ENTERED();
    ASSERT(ghostCrossReentrantStatus != _NOT_ENTERED());
    
    ghostCrossReentrantStatus = _NOT_ENTERED();
}

function reentrancyGuardEnteredCVL() returns bool {
    return ghostCrossReentrantStatus == _ENTERED();
}
