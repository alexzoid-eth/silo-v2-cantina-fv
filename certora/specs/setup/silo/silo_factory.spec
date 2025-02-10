// Silo Factory storage hooks

using SiloFactoryHarness as _SiloFactory;

hook Sload address val _SiloFactory._owners[KEY uint256 id] {
    require(ghostDeployerFeeReceiver[id] == val);
}

hook Sstore _SiloFactory._owners[KEY uint256 id] address val {
    ghostDeployerFeeReceiver[id] = val;
}
