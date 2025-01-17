// Common ShareTokenStorage ghosts for all contracts

// Ghost copy of `ShareTokenStorage.silo` in `siloX.spec`

// Ghost copy of `ShareTokenStorage.siloConfig`

persistent ghost address ghostShareTokenSiloConfig {
    // Link global config
    axiom ghostShareTokenSiloConfig == _SiloConfig;
}

// Ghost copy of `ShareTokenStorage.hookSetup.hookReceiver`

persistent ghost mapping (address => address) ghostShareTokenHookReceiver {
    init_state axiom forall address contract. ghostShareTokenHookReceiver[contract] == 0;
}

// Ghost copy of `ShareTokenStorage.hookSetup.hooksBefore`

persistent ghost mapping (address => mathint) ghostShareTokenHooksBefore {
    init_state axiom forall address contract. ghostShareTokenHooksBefore[contract] == 0;
    axiom forall address contract. 
        ghostShareTokenHooksBefore[contract] >= 0 && ghostShareTokenHooksBefore[contract] <= max_uint24;
}

// Ghost copy of `ShareTokenStorage.hookSetup.hooksAfter`

persistent ghost mapping (address => mathint) ghostShareTokenHooksAfter {
    init_state axiom forall address contract. ghostShareTokenHooksAfter[contract] == 0;
    axiom forall address contract. 
        ghostShareTokenHooksAfter[contract] >= 0 && ghostShareTokenHooksAfter[contract] <= max_uint24;
}

// Ghost copy of `ShareTokenStorage.hookSetup.tokenType`

persistent ghost mapping (address => mathint) ghostShareTokenTokenType {
    axiom forall address contract. 
        ghostShareTokenTokenType[contract] >= 0 && ghostShareTokenTokenType[contract] <= max_uint24;
}

// Ghost copy of `ShareTokenStorage.transferWithChecks`

persistent ghost mapping (address => bool) ghostShareTokenTransferWithChecks {
    init_state axiom forall address contract. ghostShareTokenTransferWithChecks[contract] == false;
}