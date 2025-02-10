# All other regular rules
rule_names = [
    "share_functionExecutesHooksBasedOnConfig",
    "share_noHookFunctionMustNotExecuteHook",
    "share_hooksShouldBeSynchronized",

    "share_crossReentrancyProtectionNoDoubleCall",
    "share_noStateChangingCallInsideReentrancyEntered",
    "share_protectedFunctionMightChangeState",
    "share_noMovingSharesInsideReentrancyEntered",
    "share_allowedReenterFunctionDoNotCallCrossReentrancyGuard",

    "share_groupShareChangeRequireGroupTimestamp",
    "share_InterestTimestampAlwaysGrow",
]