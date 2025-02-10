// Silo Factory

using SiloFactoryHarness as _SiloFactory;

methods {
    function _.tokenURI(uint256) external
        => NONDET;
}

hook Sload address val _SiloFactory._owners[KEY uint256 id] {
    // Only active Silo is supported
    require(id == ghostSiloId);
    require(ghostDeployerFeeReceiver[id] == val);
}

hook Sstore _SiloFactory._owners[KEY uint256 id] address val {
    // Only active Silo is supported
    require(id == ghostSiloId);
    ghostDeployerFeeReceiver[id] = val;
}
