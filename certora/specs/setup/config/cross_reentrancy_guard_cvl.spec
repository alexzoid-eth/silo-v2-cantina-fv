methods {
    function _.turnOnReentrancyProtection() external with (env e)
        => turnOnReentrancyProtectionCVL(e)
            expect void;

    function _.turnOffReentrancyProtection() external with (env e)
        => turnOffReentrancyProtectionCVL(e)
            expect void;

    function _.reentrancyGuardEntered() external
        => reentrancyGuardEnteredCVL()
            expect (bool);
}

definition ENTERED() returns mathint = 1;
definition NOT_ENTERED() returns mathint = 0;

persistent ghost mathint ghostCrossReentrantStatus {
    init_state axiom ghostCrossReentrantStatus == NOT_ENTERED();
    axiom ghostCrossReentrantStatus == NOT_ENTERED() 
        || ghostCrossReentrantStatus == ENTERED();
}

persistent ghost bool ghostReentrancyProtectionDoubleCall {
    init_state axiom ghostReentrancyProtectionDoubleCall == false;
}

function turnOnReentrancyProtectionCVL(env e) {

    onlySiloOrTokenOrHookReceiverCVL(e);

    ghostReentrancyProtectionDoubleCall = (ghostCrossReentrantStatus == ENTERED());

    ASSERT(ghostCrossReentrantStatus != ENTERED());

    ghostCrossReentrantStatus = ENTERED();
}

function turnOffReentrancyProtectionCVL(env e) {

    onlySiloOrTokenOrHookReceiverCVL(e);

    ghostReentrancyProtectionDoubleCall = (ghostCrossReentrantStatus == NOT_ENTERED());

    ASSERT(ghostCrossReentrantStatus != NOT_ENTERED());

    ghostCrossReentrantStatus = NOT_ENTERED();
}

function reentrancyGuardEnteredCVL() returns bool {
    return (ghostCrossReentrantStatus == ENTERED());
}