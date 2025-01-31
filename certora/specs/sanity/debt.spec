// ShareDebtToken sanity for full silo configuration 

import "../setup/silo0/silo0.spec";
import "../setup/silo1/silo1.spec";

rule sanity_approve(env e, calldataarg args) {
    setupSilo(e);
    approve(e, args);
    satisfy(true);
}

rule sanity_transfer(env e, calldataarg args) {
    setupSilo(e);
    transfer(e, args);
    satisfy(true);
}

rule sanity_decreaseReceiveAllowance(env e, calldataarg args) {
    setupSilo(e);
    decreaseReceiveAllowance(e, args);
    satisfy(true);
}

rule sanity_increaseReceiveAllowance(env e, calldataarg args) {
    setupSilo(e);
    increaseReceiveAllowance(e, args);
    satisfy(true);
}

rule sanity_setReceiveApproval(env e, calldataarg args) {
    setupSilo(e);
    setReceiveApproval(e, args);
    satisfy(true);
}

rule sanity_receiveAllowance(env e, calldataarg args) {
    setupSilo(e);
    receiveAllowance(e, args);
    satisfy(true);
}

rule sanity_allowance(env e, calldataarg args) {
    setupSilo(e);
    allowance(e, args);
    satisfy(true);
}

rule sanity_silo(env e, calldataarg args) {
    setupSilo(e);
    silo(e, args);
    satisfy(true);
}

rule sanity_siloConfig(env e, calldataarg args) {
    setupSilo(e);
    siloConfig(e, args);
    satisfy(true);
}

rule sanity_hookReceiver(env e, calldataarg args) {
    setupSilo(e);
    hookReceiver(e, args);
    satisfy(true);
}

rule sanity_eip712Domain(env e, calldataarg args) {
    setupSilo(e);
    eip712Domain(e, args);
    satisfy(true);
}

rule sanity_DOMAIN_SEPARATOR(env e, calldataarg args) {
    setupSilo(e);
    DOMAIN_SEPARATOR(e, args);
    satisfy(true);
}

rule sanity_decimals(env e, calldataarg args) {
    setupSilo(e);
    decimals(e, args);
    satisfy(true);
}

rule sanity_totalSupply(env e, calldataarg args) {
    setupSilo(e);
    totalSupply(e, args);
    satisfy(true);
}

rule sanity_hookSetup(env e, calldataarg args) {
    setupSilo(e);
    hookSetup(e, args);
    satisfy(true);
}

rule sanity_synchronizeHooks(env e, calldataarg args) {
    setupSilo(e);
    synchronizeHooks(e, args);
    satisfy(true);
}

rule sanity_balanceOf(env e, calldataarg args) {
    setupSilo(e);
    balanceOf(e, args);
    satisfy(true);
}

rule sanity_balanceOfAndTotalSupply(env e, calldataarg args) {
    setupSilo(e);
    balanceOfAndTotalSupply(e, args);
    satisfy(true);
}

rule sanity_callOnBehalfOfShareToken(env e, calldataarg args) {
    setupSilo(e);
    callOnBehalfOfShareToken(e, args);
    satisfy(true);
}

rule sanity_initialize(env e, calldataarg args) {
    setupSilo(e);
    initialize(e, args);
    satisfy(true);
}

rule sanity_transferFrom(env e, calldataarg args) {
    setupSilo(e);
    transferFrom(e, args);
    satisfy(true);
}

rule sanity_burn(env e, calldataarg args) {
    setupSilo(e);
    burn(e, args);
    satisfy(true);
}

rule sanity_forwardTransferFromNoChecks(env e, calldataarg args) {
    setupSilo(e);
    forwardTransferFromNoChecks(e, args);
    satisfy(true);
}

rule sanity_mint(env e, calldataarg args) {
    setupSilo(e);
    mint(e, args);
    satisfy(true);
}
