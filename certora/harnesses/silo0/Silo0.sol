// SPDX-License-Identifier: MIT
pragma solidity 0.8.28;

import { SiloHarness } from "certora/harnesses/SiloHarness.sol";
import { ISiloFactory } from "silo-core/contracts/interfaces/ISiloFactory.sol";

contract Silo0 is SiloHarness {
    constructor(ISiloFactory _siloFactory) SiloHarness(_siloFactory) { }
}
