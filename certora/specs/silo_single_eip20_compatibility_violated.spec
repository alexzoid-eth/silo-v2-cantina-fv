// Prove contract is compatible with EIP20 (https://eips.ethereum.org/EIPS/eip-20)

import "./silo_eip20_compatibility.spec";

// Transfers of 0 values MUST be treated as normal transfers
rule transferSupportZeroAmount(env e, address to, uint256 amount) {

    // Perform transfer
    _ERC20.transfer(e, to, amount);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}

// Transfers of 0 values MUST be treated as normal transfers
rule transferFromSupportZeroAmount(env e, address to, address from, uint256 amount) {

    // Perform the transferFrom
    _ERC20.transferFrom(e, from, to, amount);

    // Transfers of 0 values MUST be treated as normal transfers
    satisfy(amount == 0);
}
