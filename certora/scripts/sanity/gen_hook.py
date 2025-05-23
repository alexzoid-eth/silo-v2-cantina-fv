import json
import os

def generate_config(rule_name):
    config = {
        "build_cache": True,
        "files": [
            "certora/harnesses/silo0/Silo0.sol",
            "certora/harnesses/silo0/Debt0.sol",
            "certora/harnesses/silo0/Protected0.sol",
            "certora/harnesses/silo1/Silo1.sol",
            "certora/harnesses/silo1/Debt1.sol",
            "certora/harnesses/silo1/Protected1.sol",
            "certora/harnesses/Hook.sol",
            "silo-core/contracts/utils/hook-receivers/liquidation/PartialLiquidation.sol",
        ],
        "link": [
            "Silo1:_SILO_MODE=Hook",
            "Hook:_HOOK_RECEIVER=PartialLiquidation",
            "Hook:_SILO0=Silo0",
            "Hook:_SILO1=Silo1",
        ],
        "msg": f"Hook_{rule_name}_verified",
        "mutations": {
            "manual_mutants": [
                {
                    "file_to_mutate": "silo-core/contracts/utils/hook-receivers/liquidation/PartialLiquidation.sol",
                    "mutants_location": "certora/mutations/PartialLiquidation",
                }
            ]
        },
        "optimistic_loop": True,
        "packages": [
            "openzeppelin5/=gitmodules/openzeppelin-contracts-5/contracts/",
            "openzeppelin5-upgradeable/=gitmodules/openzeppelin-contracts-upgradeable-5/contracts/",
            "@openzeppelin/contracts/=gitmodules/openzeppelin-contracts-5/contracts/"
        ],
        "parametric_contracts": [
            "Hook"
        ],
        "prover_args": [
            "-maxDecompiledCommandCount 10000000",
            "-maxBlockCount 300000",
        ],
        "rule": [
            rule_name
        ],
        "struct_link": [
            "Silo0:silo=Silo0",
            "Debt0:silo=Silo0",
            "Protected0:silo=Silo0",
            "Silo0:hookReceiver=PartialLiquidation",
            "Debt0:hookReceiver=PartialLiquidation",
            "Protected0:hookReceiver=PartialLiquidation",
            "Silo1:silo=Silo1",
            "Debt1:silo=Silo1",
            "Protected1:silo=Silo1",
            "Silo1:hookReceiver=PartialLiquidation",
            "Debt1:hookReceiver=PartialLiquidation",
            "Protected1:hookReceiver=PartialLiquidation",
        ],
        "verify": "Hook:certora/specs/sanity/hook.spec"
    }
    
    os.makedirs("hook", exist_ok=True)
    filename = os.path.join("hook", f"Hook_{rule_name}_verified.conf")
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Generated {filename}")

# List of rule names extracted from the provided ruleset
rule_names = [
    "sanity_liquidationCall_noSToken_noBypass_protectedAllowed",
    "sanity_liquidationCall_receiveSToken_bypassInterest_protectedAllowed",
    "sanity_liquidationCall_noSToken_bypassInterest_collateralAllowed",
    "sanity_liquidationCall_receiveSToken_bypassInterest_collateralAllowed"
]

# Generate configuration files
for rule in rule_names:
    generate_config(rule)
