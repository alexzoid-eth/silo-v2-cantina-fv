# Additionally split config into methods (hard methods separately and others)

import json
import os
import sys

# If hook_methods.py is one directory up, ensure we can import it:
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'hook'))
sys.path.append(parent_dir)

from rule_names import rule_names
from hook_methods import hook_methods_hard, hook_methods_other

def generate_config(rule_name, method, fn_name):
    """
    Return the JSON config dictionary for a given rule and method.
    """
    config = {
        "build_cache": True,
        "files": [
            "certora/harnesses/Config.sol",
            "certora/mocks/HelperCVL.sol",
            "certora/harnesses/silo0/Silo0.sol",
            "certora/harnesses/silo0/Debt0.sol",
            "certora/harnesses/silo0/Protected0.sol",
            "certora/mocks/Token0.sol",
            "certora/harnesses/silo1/Silo1.sol",
            "certora/harnesses/silo1/Debt1.sol",
            "certora/harnesses/silo1/Protected1.sol",
            "certora/mocks/Token1.sol",
            "certora/harnesses/Hook.sol"
        ],
        "independent_satisfy": True,
        "link": [
            "Config:_SILO0=Silo0",
            "Config:_TOKEN0=Token0",
            "Config:_PROTECTED_COLLATERAL_SHARE_TOKEN0=Protected0",
            "Config:_COLLATERAL_SHARE_TOKEN0=Silo0",
            "Config:_DEBT_SHARE_TOKEN0=Debt0",
            "Config:_SILO_MODE=Hook",
            "Config:_SILO1=Silo1",
            "Config:_TOKEN1=Token1",
            "Config:_PROTECTED_COLLATERAL_SHARE_TOKEN1=Protected1",
            "Config:_COLLATERAL_SHARE_TOKEN1=Silo1",
            "Config:_DEBT_SHARE_TOKEN1=Debt1",
            "Config:_HOOK_RECEIVER=Hook",
            "Hook:siloConfig=Config",
            "Hook:_TOKEN0=Token0",
            "Hook:_TOKEN1=Token1"
        ],
        "msg": f"Hook_{rule_name}_{fn_name}_verified",
        "method": method,
        "multi_assert_check": True, "independent_satisfy": True,
        "mutations": {
            "manual_mutants": [
                {
                    "file_to_mutate": "silo-core/contracts/Silo.sol",
                    "mutants_location": "certora/mutations/Silo"
                },
                {
                    "file_to_mutate": "silo-core/contracts/lib/Actions.sol",
                    "mutants_location": "certora/mutations/Actions"
                }
            ]
        },
        "optimistic_loop": True,
        "packages": [
            "openzeppelin5/=gitmodules/openzeppelin-contracts-5/contracts",
            "openzeppelin5-upgradeable/=gitmodules/openzeppelin-contracts-upgradeable-5/contracts",
            "@openzeppelin/contracts/=gitmodules/openzeppelin-contracts-5/contracts"
        ],
        "parametric_contracts": [
            "Hook"
        ],
        "prover_args": [
            "-maxDecompiledCommandCount 10000000",
            "-maxBlockCount 200000"
        ],
        "rule": [
            rule_name
        ],
        "struct_link": [
            "Silo0:silo=Silo0",
            "Debt0:silo=Silo0",
            "Protected0:silo=Silo0",
            "Silo0:siloConfig=Config",
            "Debt0:siloConfig=Config",
            "Protected0:siloConfig=Config",
            "Silo0:hookReceiver=Hook",
            "Debt0:hookReceiver=Hook",
            "Protected0:hookReceiver=Hook",
            "Silo1:silo=Silo1",
            "Debt1:silo=Silo1",
            "Protected1:silo=Silo1",
            "Silo1:siloConfig=Config",
            "Debt1:siloConfig=Config",
            "Protected1:siloConfig=Config",
            "Silo1:hookReceiver=Hook",
            "Debt1:hookReceiver=Hook",
            "Protected1:hookReceiver=Hook",
        ],
        "verify": "Hook:certora/specs/invariants.spec"
    }
    return config

def base_function_name(method_signature: str) -> str:
    """
    Parse the function signature (e.g., 'redeem(uint256,address,address)')
    and return only the function name before the first '('.
    """
    return method_signature.split('(')[0].strip()

os.makedirs("hook", exist_ok=True)

for rule in rule_names:
    # We will keep track of how many times each base function name appears
    # so we can append "_2", "_3", etc. for overloads
    function_count = {}

    # 1) Create one config per "hard" method
    for method_sig in hook_methods_hard:
        fn_name = base_function_name(method_sig)
        # Increment the function counter
        function_count[fn_name] = function_count.get(fn_name, 0) + 1

        # Build the filename
        # If it's the first time we see fn_name, no suffix
        # Otherwise, suffix with _2, _3, etc.
        count = function_count[fn_name]
        if count == 1:
            filename = f"Hook_{rule}_{fn_name}_verified.conf"
        else:
            filename = f"Hook_{rule}_{fn_name}_{count}_verified.conf"

        full_path = os.path.join("hook", filename)
        config_dict = generate_config(rule, method_sig, fn_name)

        with open(full_path, "w") as f:
            json.dump(config_dict, f, indent=4)

        print(f"Generated {full_path}")