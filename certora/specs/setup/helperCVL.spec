// Separate contract with helper functions

using HelperCVL as _HelperCVL;

methods {
    // Link separate HelperCVL contract with helper solidity functions
    function _HelperCVL.assertOnFalse(bool b) external envfree;    
}

function ASSERT(bool expression) {
    _HelperCVL.assertOnFalse(expression);
} 
