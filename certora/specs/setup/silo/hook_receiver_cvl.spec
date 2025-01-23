// CVL implementation of `IHookReceiver`

methods {

    function _.beforeAction(address _silo, uint256 _action, bytes _input) external
        => beforeActionCVL(_silo, _action) expect void;

    function _.afterAction(address _silo, uint256 _action, bytes _inputAndOutput) external
        => afterActionCVL(_silo, _action) expect void;

    function _.hookReceiverConfig(address _silo) external
        => hookReceiverConfigCVL(_silo) expect IHookReceiver.HookConfig;
}

function beforeActionCVL(address _silo, uint256 _action) { }

function afterActionCVL(address _silo, uint256 _action) { }

persistent ghost mapping(address => uint24) ghostHooksBefore {
    init_state axiom forall address silo. ghostHooksBefore[silo] == 0;
}
persistent ghost mapping(address => uint24) ghostHooksAfter {
    init_state axiom forall address silo. ghostHooksAfter[silo] == 0;
}
function hookReceiverConfigCVL(address _silo) returns IHookReceiver.HookConfig {
    IHookReceiver.HookConfig config;
    require(config.hooksBefore == ghostHooksBefore[_silo]);
    require(config.hooksAfter == ghostHooksAfter[_silo]);
    return config;
}