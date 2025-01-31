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
            "certora/mocks/Token1.sol",
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
            "Config:_DEBT_SHARE_TOKEN1=Debt1",
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
            "Protected1:siloConfig=Config",
        ],
        "verify": "Silo1:certora/specs/eip4626.spec"
    }
    
    os.makedirs("eip4626", exist_ok=True)
    filename = os.path.join("silo", f"Silo1_{rule_name}_verified.conf")
    with open(filename, "w") as f:
        json.dump(config, f, indent=4)
    print(f"Generated {filename}")

# List of rule names extracted from the provided ruleset
rule_names = [
    "eip4626_assetIntegrity",
    "eip4626_assetMustNotRevert",
    "eip4626_totalAssetsIntegrity",
    "eip4626_totalAssetsMustNotRevert",
    "eip4626_convertToSharesNotIncludeFeesInDeposit",
    "eip4626_convertToSharesNotIncludeFeesInWithdraw",
    "eip4626_convertToSharesMustNotDependOnCaller",
    "eip4626_convertToSharesMustNotRevert",
    "eip4626_convertToSharesRoundTripDoesNotExceed",
    "eip4626_convertToSharesNoSlippage",
    "eip4626_convertToAssetsNotIncludeFeesRedeem",
    "eip4626_convertToAssetsNotIncludeFeesMint",
    "eip4626_convertToAssetsMustNotDependOnCaller",
    "eip4626_convertToAssetsMustNotRevert",
    "eip4626_convertToAssetsRoundTripDoesNotExceed",
    "eip4626_convertToAssetsNoSlippage",
    "eip4626_maxDepositNoHigherThanActual",
    "eip4626_maxDepositDoesNotDependOnUserBalance",
    "eip4626_maxDepositUnlimitedReturnsMax",
    "eip4626_maxDepositMustNotRevert",
    "eip4626_previewDepositNoMoreThanActualShares",
    "eip4626_previewDepositMustIgnoreLimits",
    "eip4626_previewDepositMustIncludeFees",
    "eip4626_previewDepositMustNotDependOnCaller",
    "eip4626_previewDepositMayRevertOnlyWithDepositRevert",
    "eip4626_depositIntegrity",
    "eip4626_depositToSelfIntegrity",
    "eip4626_depositRespectsApproveTransfer",
    "eip4626_depositMustRevertIfCannotDeposit",
    "eip4626_depositPossibility",
    "eip4626_maxMintNoHigherThanActual",
    "eip4626_maxMintDoesNotDependOnUserBalance",
    "eip4626_maxMintZeroIfDisabled",
    "eip4626_maxMintUnlimitedReturnsMax",
    "eip4626_maxMintMustNotRevert",
    "eip4626_previewMintNoFewerThanActualAssets",
    "eip4626_previewMintMustIgnoreLimits",
    "eip4626_previewMintMustIncludeFees",
    "eip4626_previewMintMustNotDependOnCaller",
    "eip4626_previewMintMayRevertOnlyWithMintRevert",
    "eip4626_mintIntegrity",
    "eip4626_mintToSelfIntegrity",
    "eip4626_mintRespectsApproveTransfer",
    "eip4626_mintMustRevertIfCannotMint",
    "eip4626_mintPossibility",
    "eip4626_maxWithdrawNoHigherThanActual",
    "eip4626_maxWithdrawWithdrawPossibility",
    "eip4626_maxWithdrawDoesNotDependOnUserShares",
    "eip4626_maxWithdrawZeroIfDisabled",
    "eip4626_maxWithdrawMustNotRevert",
    "eip4626_previewWithdrawNoFewerThanActualShares",
    "eip4626_previewWithdrawMustIgnoreLimits",
    "eip4626_previewWithdrawMustNotDependOnCaller",
    "eip4626_previewWithdrawMayRevertOnlyWithWithdrawRevert",
    "eip4626_withdrawIntegrity",
    "eip4626_withdrawFromOtherIntegrity",
    "eip4626_withdrawFromSelfIntegrity",
    "eip4626_withdrawMustRevertIfCannotWithdraw",
    "eip4626_maxRedeemNoHigherThanActual",
    "eip4626_maxRedeemMustNotRevert",
    "eip4626_previewRedeemNoMoreThanActualAssets",
    "eip4626_previewRedeemMustIgnoreLimits",
    "eip4626_previewRedeemMustNotDependOnCaller",
    "eip4626_previewRedeemMayRevertOnlyWithRedeemRevert",
    "eip4626_redeemIntegrity",
    "eip4626_redeemFromOtherIntegrity",
    "eip4626_redeemFromSelfIntegrity",
    "eip4626_redeemMustRevertIfCannotRedeem"
]

# Generate configuration files
for rule in rule_names:
    generate_config(rule)
