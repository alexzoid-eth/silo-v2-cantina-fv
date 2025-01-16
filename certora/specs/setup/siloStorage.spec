// Silo CVL storage ghosts and hooks

//
// ShareTokenStorage
//

// Ghost copy of `ShareTokenStorage.silo`

persistent ghost address ghostShareTokenSilo {
    axiom ghostShareTokenSilo == _Silo;
}

hook Sload address val _Silo.shareTokenStorage.silo {
    require(ghostShareTokenSilo == val);
}

hook Sstore _Silo.shareTokenStorage.silo address val {
    ghostShareTokenSilo = val;
}

// Ghost copy of `ShareTokenStorage.siloConfig`

persistent ghost address ghostShareTokenSiloConfig;

hook Sload address val _Silo.shareTokenStorage.siloConfig {
    require(ghostShareTokenSiloConfig == val);
}

hook Sstore _Silo.shareTokenStorage.siloConfig address val {
    ghostShareTokenSiloConfig = val;
}

// Ghost copy of `ShareTokenStorage.hookSetup.hookReceiver`

persistent ghost address ghostShareTokenHookReceiver {
    init_state axiom ghostShareTokenHookReceiver == 0;
}

hook Sload address val _Silo.shareTokenStorage.hookSetup.hookReceiver {
    require(ghostShareTokenHookReceiver == val);
}

hook Sstore _Silo.shareTokenStorage.hookSetup.hookReceiver address val {
    ghostShareTokenHookReceiver = val;
}

// Ghost copy of `ShareTokenStorage.hookSetup.hooksBefore`

persistent ghost mathint ghostShareTokenHooksBefore {
    init_state axiom ghostShareTokenHooksBefore == 0;
    axiom ghostShareTokenHooksBefore >= 0 && ghostShareTokenHooksBefore <= max_uint24;
}

hook Sload uint24 val _Silo.shareTokenStorage.hookSetup.hooksBefore {
    require(require_uint24(ghostShareTokenHooksBefore) == val);
}

hook Sstore _Silo.shareTokenStorage.hookSetup.hooksBefore uint24 val {
    ghostShareTokenHooksBefore = val;
}

// Ghost copy of `ShareTokenStorage.hookSetup.hooksAfter`

persistent ghost mathint ghostShareTokenHooksAfter {
    init_state axiom ghostShareTokenHooksAfter == 0;
    axiom ghostShareTokenHooksAfter >= 0 && ghostShareTokenHooksAfter <= max_uint24;
}

hook Sload uint24 val _Silo.shareTokenStorage.hookSetup.hooksAfter {
    require(require_uint24(ghostShareTokenHooksAfter) == val);
}

hook Sstore _Silo.shareTokenStorage.hookSetup.hooksAfter uint24 val {
    ghostShareTokenHooksAfter = val;
}

// Ghost copy of `ShareTokenStorage.hookSetup.tokenType`

persistent ghost mathint ghostShareTokenTokenType {
    init_state axiom ghostShareTokenTokenType == 0;
    axiom ghostShareTokenTokenType >= 0 && ghostShareTokenTokenType <= max_uint24;
}

hook Sload uint24 val _Silo.shareTokenStorage.hookSetup.tokenType {
    require(require_uint24(ghostShareTokenTokenType) == val);
}

hook Sstore _Silo.shareTokenStorage.hookSetup.tokenType uint24 val {
    ghostShareTokenTokenType = val;
}

// Ghost copy of `ShareTokenStorage.transferWithChecks`

persistent ghost bool ghostShareTokenTransferWithChecks {
    init_state axiom ghostShareTokenTransferWithChecks == false;
}

hook Sload bool val _Silo.shareTokenStorage.transferWithChecks {
    require(ghostShareTokenTransferWithChecks == val);
}

hook Sstore _Silo.shareTokenStorage.transferWithChecks bool val {
    ghostShareTokenTransferWithChecks = val;
}

//
// IERC20R
//

// Ghost copy of `IERC20RStorage._receiveAllowances`

persistent ghost mapping(address => mapping(address => mathint)) ghostReceiveAllowances {
    init_state axiom forall address owner. forall address recipient. ghostReceiveAllowances[owner][recipient] == 0;
    axiom forall address owner. forall address recipient. 
        ghostReceiveAllowances[owner][recipient] >= 0 && ghostReceiveAllowances[owner][recipient] <= max_uint256;
}

hook Sload uint256 val _Silo.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] {
    require(require_uint256(ghostReceiveAllowances[owner][recipient]) == val);
}

hook Sstore _Silo.iERC20RStorage._receiveAllowances[KEY address owner][KEY address recipient] uint256 val {
    ghostReceiveAllowances[owner][recipient] = val;
}

//
// SiloStorage
//

// Ghost copy of `SiloStorage.daoAndDeployerRevenue`

persistent ghost mathint ghostDaoAndDeployerRevenue {
    init_state axiom ghostDaoAndDeployerRevenue == 0;
    axiom ghostDaoAndDeployerRevenue >= 0 && ghostDaoAndDeployerRevenue <= max_uint192;
}

hook Sload uint192 val _Silo.siloStorage.daoAndDeployerRevenue {
    require(require_uint192(ghostDaoAndDeployerRevenue) == val);
}

hook Sstore _Silo.siloStorage.daoAndDeployerRevenue uint192 val {
    ghostDaoAndDeployerRevenue = val;
}

// Ghost copy of `SiloStorage.interestRateTimestamp`

persistent ghost mathint ghostInterestRateTimestamp {
    init_state axiom ghostInterestRateTimestamp == 0;
    axiom ghostInterestRateTimestamp >= 0 && ghostInterestRateTimestamp <= max_uint64;
}

hook Sload uint64 val _Silo.siloStorage.interestRateTimestamp {
    require(require_uint64(ghostInterestRateTimestamp) == val);
}

hook Sstore _Silo.siloStorage.interestRateTimestamp uint64 val {
    ghostInterestRateTimestamp = val;
}

// Ghost copy of `SiloStorage.totalAssets`

persistent ghost mapping(mathint => mathint) ghostTotalAssets {
    init_state axiom forall mathint assetType. ghostTotalAssets[assetType] == 0;
    axiom forall mathint assetType. ghostTotalAssets[assetType] >= 0 && ghostTotalAssets[assetType] <= max_uint256;
    axiom forall mathint assetType. assetType > 2 => ghostTotalAssets[assetType] == 0; // Support only 3 types of accounting 
}

hook Sload uint256 val _Silo.siloStorage.totalAssets[KEY ISilo.AssetType assetType] {
    require(require_uint256(ghostTotalAssets[to_mathint(assetType)]) == val);
}

hook Sstore _Silo.siloStorage.totalAssets[KEY ISilo.AssetType assetType] uint256 val {
    ghostTotalAssets[to_mathint(assetType)] = val;
}
