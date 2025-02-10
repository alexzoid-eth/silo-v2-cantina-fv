import json
import os

rule_names_violated = [
    "silo_deployerFeeReceiverCannotBeBlocked",
]

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
            "certora/harnesses/SiloFactoryHarness.sol"
        ],
        "independent_satisfy": True,
        "link": [
            "Silo1:_SILO_MODE=SiloFactoryHarness",
        ],
        "msg": f"Silo1_{rule_name}_violated",
        "method": "burn(uint256)",
        "multi_assert_check": True, "independent_satisfy": True,
        "optimistic_loop": True,
        "packages": [
            "openzeppelin5/=gitmodules/openzeppelin-contracts-5/contracts/",
            "openzeppelin5-upgradeable/=gitmodules/openzeppelin-contracts-upgradeable-5/contracts/",
            "@openzeppelin/contracts/=gitmodules/openzeppelin-contracts-5/contracts/",

        ],
        "parametric_contracts": [
            "Silo1", "SiloFactoryHarness"
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
        "verify": "Silo1:certora/specs/silo_violated.spec"
    }
    
    os.makedirs("silo", exist_ok=True)
    filename = os.path.join("silo", f"Silo1_{rule_name}_violated.conf")
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Generated {filename}")

# Generate configuration files
for rule in rule_names_violated:
    generate_config(rule)
