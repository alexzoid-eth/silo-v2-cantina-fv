import json
import os

from rule_names import rule_names

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
        ],
        "independent_satisfy": True,
        "link": [
            "Silo1:_SILO_MODE=Silo1",
        ],
        "msg": f"Silo1_{rule_name}_verified",
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
            "Silo1"
        ],
        "rule": [
            rule_name
        ],
        "struct_link": [
            "Silo0:silo=Silo0",
            "Debt0:silo=Silo0",
            "Protected0:silo=Silo0",
            "Silo1:silo=Silo1",
            "Debt1:silo=Silo1",
            "Protected1:silo=Silo1",
        ],
        "verify": "Silo1:certora/specs/eip4626/protected.spec"
    }
    
    os.makedirs("eip4626_protected", exist_ok=True)
    filename = os.path.join("eip4626_protected", f"Silo1_{rule_name}_verified.conf")
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Generated {filename}")

# Generate configuration files
for rule in rule_names:
    generate_config(rule)
