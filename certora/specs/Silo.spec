import "./ERC20Integrity.spec";
import "./setup/storage.spec";

// Sanity

// use builtin rule sanity;

// ERC20 integrity

use rule totalSupplyIntegrity;
use rule balanceOfIntegrity;
use rule allowanceIntegrity;
use rule transferIntegrity;
use rule transferMustRevert;
use rule transferFromIntegrity;
use rule transferFromMustRevert;
use rule approveIntegrity;
use rule approveMustRevert;
