methods {
    function _.turnOnReentrancyProtection() external with (env e)
        => turnOnReentrancyProtectionCVL(e, calledContract)
            expect void;

    function _.turnOffReentrancyProtection() external with (env e)
        => turnOffReentrancyProtectionCVL(e, calledContract)
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

persistent ghost bool ghostReentrancyCalled;

persistent ghost bool ghostReentrancyProtectionDoubleCall {
    init_state axiom ghostReentrancyProtectionDoubleCall == false;
}

function turnOnReentrancyProtectionCVL(env e, address contract) {

    assert(contract != 0);

    onlySiloOrTokenOrHookReceiverCVL(e);

    ghostReentrancyCalled = true;
    ghostReentrancyProtectionDoubleCall = (ghostCrossReentrantStatus == ENTERED());

    ASSERT(ghostCrossReentrantStatus != ENTERED());

    ghostCrossReentrantStatus = ENTERED();
}

function turnOffReentrancyProtectionCVL(env e, address contract) {

    assert(contract != 0);

    onlySiloOrTokenOrHookReceiverCVL(e);

    ghostReentrancyCalled = true;
    ghostReentrancyProtectionDoubleCall = (ghostCrossReentrantStatus == NOT_ENTERED());

    ASSERT(ghostCrossReentrantStatus != NOT_ENTERED());

    ghostCrossReentrantStatus = NOT_ENTERED();
}

function reentrancyGuardEnteredCVL() returns bool {
    return (ghostCrossReentrantStatus == ENTERED());
}