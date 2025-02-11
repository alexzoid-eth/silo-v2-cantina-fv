// These methods simplified in another configurations

import "./silo_math_lib.spec";

methods {

    // Silo

    function _.repay(uint256 _assets, address _borrower) external
        => DISPATCHER(true);

    function _.redeem(uint256 _shares, address _receiver, address _owner, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);

    function _.previewRedeem(uint256 _shares, ISilo.CollateralType _collateralType) external
        => DISPATCHER(true);

    // Share tokens

    function _.forwardTransferFromNoChecks(address _from, address _to, uint256 _amount) external
        => DISPATCHER(true);
}