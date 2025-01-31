import json
import os

def generate_config(rule_name):
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
            "certora/mocks/Token1.sol"
        ],
        "link": [
            "Config:_SILO0=Silo0",
            "Config:_TOKEN0=Token0",
            "Config:_PROTECTED_COLLATERAL_SHARE_TOKEN0=Protected0",
            "Config:_COLLATERAL_SHARE_TOKEN0=Silo0",
            "Config:_DEBT_SHARE_TOKEN0=Debt0",
            "Config:_LAST_SILO_ADDRESS=Silo1",
            "Config:_SILO1=Silo1",
            "Config:_TOKEN1=Token1",
            "Config:_PROTECTED_COLLATERAL_SHARE_TOKEN1=Protected1",
            "Config:_COLLATERAL_SHARE_TOKEN1=Silo1",
            "Config:_DEBT_SHARE_TOKEN1=Debt1"
        ],
        "msg": f"Silo1_{rule_name}_verified",
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
            "Silo0:siloConfig=Config",
            "Debt0:siloConfig=Config",
            "Protected0:siloConfig=Config",
            "Silo1:silo=Silo1",
            "Debt1:silo=Silo1",
            "Protected1:silo=Silo1",
            "Silo1:siloConfig=Config",
            "Debt1:siloConfig=Config",
            "Protected1:siloConfig=Config"
        ],
        "verify": "Silo1:certora/specs/sanity/silo.spec"
    }
    
    filename = f"Silo1_{rule_name}_verified.conf"
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Generated {filename}")

# List of rule names extracted from the provided ruleset
rule_names = [
    "sanity_accrueInterestForConfig", "sanity_withdraw", "sanity_redeem", "sanity_approve",
    "sanity_flashFee", "sanity_transfer", "sanity_allowance", "sanity_borrowSameAsset",
    "sanity_borrow", "sanity_redeem_2", "sanity_withdraw_2", "sanity_borrowShares",
    "sanity_totalAssets", "sanity_getCollateralAndProtectedTotalsStorage", "sanity_getDebtAssets",
    "sanity_silo", "sanity_siloConfig", "sanity_updateHooks", "sanity_factory", "sanity_accrueInterest",
    "sanity_getCollateralAssets", "sanity_switchCollateralToThisSilo", "sanity_utilizationData",
    "sanity_getSiloStorage", "sanity_hookReceiver", "sanity_eip712Domain", "sanity_config",
    "sanity_withdrawFees", "sanity_getCollateralAndDebtTotalsStorage"
]

# Generate configuration files
for rule in rule_names:
    generate_config(rule)
