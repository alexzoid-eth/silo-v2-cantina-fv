// CVL implementation of SiloConfig

methods {
    
    function _SiloConfig.setThisSiloAsCollateralSilo(address _borrower) external with (env e)
        => setThisSiloAsCollateralSiloCVL(e, _borrower);

    function _SiloConfig.setOtherSiloAsCollateralSilo(address _borrower) external with (env e)
        => setOtherSiloAsCollateralSiloCVL(e, _borrower);

    function _SiloConfig.onDebtTransfer(address _sender, address _recipient) external with (env e)
        => onDebtTransferCVL(e, _sender, _recipient);

    function _SiloConfig.accrueInterestForSilo(address _silo) external with (env e)
        => accrueInterestForSiloCVL(e, _silo);

    function _SiloConfig.accrueInterestForBothSilos() external with (env e)
        => accrueInterestForBothSilosCVL(e);

    function _SiloConfig.getConfigsForSolvency(address _borrower)
        external
        returns (ISiloConfig.ConfigData, ISiloConfig.ConfigData)
    => getConfigsForSolvencyCVL(_borrower);

    function _SiloConfig.getConfigsForWithdraw(address _silo, address _depositOwner)
        external
        returns (ISiloConfig.DepositConfig, ISiloConfig.ConfigData, ISiloConfig.ConfigData)
    => getConfigsForWithdrawCVL(_silo, _depositOwner);

    function _SiloConfig.getConfigsForBorrow(address _debtSilo)
        external
        returns (ISiloConfig.ConfigData, ISiloConfig.ConfigData)
    => getConfigsForBorrowCVL(_debtSilo);

    function _SiloConfig.getSilos() external returns (address, address)
        => getSilosCVL();

    function _SiloConfig.getShareTokens(address _silo)
        external
        returns (address, address, address)
    => getShareTokensCVL(_silo);

    function _SiloConfig.getAssetForSilo(address _silo) external returns address
    => getAssetForSiloCVL(_silo);

    function _SiloConfig.getFeesWithAsset(address _silo)
        external
        returns (uint256, uint256, uint256, address)
    => getFeesWithAssetCVL(_silo);

    function _SiloConfig.getCollateralShareTokenAndAsset(address _silo, ISilo.CollateralType _collateralType)
        external
        returns (address, address)
    => getCollateralShareTokenAndAssetCVL(_silo, _collateralType);

    function _SiloConfig.getDebtShareTokenAndAsset(address _silo)
        external
        returns (address, address)
    => getDebtShareTokenAndAssetCVL(_silo);
    
    function _SiloConfig.getConfig(address _silo)
        external
        returns (ISiloConfig.ConfigData)
    => getConfigCVL(_silo);
    
    function _SiloConfig.hasDebtInOtherSilo(address _thisSilo, address _borrower) 
        external 
        returns (bool)
        => hasDebtInOtherSiloCVL(_thisSilo, _borrower);

    function _SiloConfig.getDebtSilo(address _borrower) external returns address
        => getDebtSiloCVL(_borrower);

    function _SiloConfig.SILO_ID() external returns (uint256)
        => getSiloIdCVL();
}

function setThisSiloAsCollateralSiloCVL(env e, address _borrower) {
    ASSERT(e.msg.sender == ghostSilo0 || e.msg.sender == ghostSilo1);
    ghostConfigBorrowerCollateralSilo[_borrower] = e.msg.sender;
}

function setOtherSiloAsCollateralSiloCVL(env e, address _borrower) {
    ASSERT(e.msg.sender == ghostSilo0 || e.msg.sender == ghostSilo1);
    ghostConfigBorrowerCollateralSilo[_borrower] = (e.msg.sender == ghostSilo0) ? ghostSilo1 : ghostSilo0;
}

function onDebtTransferCVL(env e, address _sender, address _recipient) {
    ASSERT(e.msg.sender == ghostDebtToken0 || e.msg.sender == ghostDebtToken1);
    address thisSilo = (e.msg.sender == ghostDebtToken0) ? ghostSilo0 : ghostSilo1;
    bool recipientHasDebtElsewhere = hasDebtInOtherSiloCVL(thisSilo, _recipient);
    ASSERT(!recipientHasDebtElsewhere);
    if (ghostConfigBorrowerCollateralSilo[_recipient] == 0) {
        ghostConfigBorrowerCollateralSilo[_recipient] = ghostConfigBorrowerCollateralSilo[_sender];
    }
}

function accrueInterestForSiloCVL(env e, address _silo) {
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    address irm = (_silo == ghostSilo0) ? ghostConfigInterestRateModel0 : ghostConfigInterestRateModel1;
    _silo.accrueInterestForConfig(
        e,
        irm,
        require_uint256(ghostConfigDaoFee),
        require_uint256(ghostConfigDeployerFee)
    );
}

function accrueInterestForBothSilosCVL(env e) {
    ghostSilo0.accrueInterestForConfig(
        e,
        ghostConfigInterestRateModel0,
        require_uint256(ghostConfigDaoFee),
        require_uint256(ghostConfigDeployerFee)
    );
    ghostSilo1.accrueInterestForConfig(
        e,
        ghostConfigInterestRateModel1,
        require_uint256(ghostConfigDaoFee),
        require_uint256(ghostConfigDeployerFee)
    );
}

function getConfigsForSolvencyCVL(address _borrower) 
    returns (ISiloConfig.ConfigData, ISiloConfig.ConfigData)
{
    address ds = getDebtSiloCVL(_borrower);
    if (ds == 0) {
        return (_emptyConfigDataCVL(), _emptyConfigDataCVL());
    }
    address cs = ghostConfigBorrowerCollateralSilo[_borrower];
    ISiloConfig.ConfigData ccfg = getConfigCVL(cs);
    ISiloConfig.ConfigData dcfg = getConfigCVL(ds);
    return (ccfg, dcfg);
}

function getConfigsForWithdrawCVL(address _silo, address _depositOwner)
    returns (ISiloConfig.DepositConfig, ISiloConfig.ConfigData, ISiloConfig.ConfigData)
{
    ISiloConfig.DepositConfig depositCfg = _getDepositConfigCVL(_silo);
    ISiloConfig.ConfigData ccfg; ISiloConfig.ConfigData dcfg;
    (ccfg, dcfg) = getConfigsForSolvencyCVL(_depositOwner);
    return (depositCfg, ccfg, dcfg);
}

function getConfigsForBorrowCVL(address _debtSilo)
    returns (ISiloConfig.ConfigData, ISiloConfig.ConfigData)
{
    ASSERT(_debtSilo == ghostSilo0 || _debtSilo == ghostSilo1);
    address collateralSilo = (_debtSilo == ghostSilo0) ? ghostSilo1 : ghostSilo0;
    ISiloConfig.ConfigData ccfg = getConfigCVL(collateralSilo);
    ISiloConfig.ConfigData dcfg = getConfigCVL(_debtSilo);
    return (ccfg, dcfg);
}

function getSilosCVL() returns (address, address) {
    return (ghostSilo0, ghostSilo1);
}

function getShareTokensCVL(address _silo) returns (address, address, address) {
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    if(_silo == ghostSilo0) {
        return (ghostProtectedToken0, ghostCollateralToken0, ghostDebtToken0);
    } else {
        return (ghostProtectedToken1, ghostCollateralToken1, ghostDebtToken1);
    }
}

function getAssetForSiloCVL(address _silo) returns address {
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    return (_silo == ghostSilo0) ? ghostToken0 : ghostToken1;
}

function getFeesWithAssetCVL(address _silo) returns (uint256, uint256, uint256, address) {
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    uint256 daoFee = require_uint256(ghostConfigDaoFee);
    uint256 deployerFee = require_uint256(ghostConfigDeployerFee);
    bool isSilo0 = (_silo == ghostSilo0);
    uint256 flashloanFee = isSilo0
        ? require_uint256(ghostConfigFlashloanFee0)
        : require_uint256(ghostConfigFlashloanFee1);
    address asset = isSilo0 ? ghostToken0 : ghostToken1;
    return (daoFee, deployerFee, flashloanFee, asset);
}

function getCollateralShareTokenAndAssetCVL(address _silo, ISilo.CollateralType _collateralType)
    returns (address, address)
{
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    bool isSilo0 = (_silo == ghostSilo0);
    bool isRegular = (_collateralType == ISilo.CollateralType.Collateral);
    address share = isSilo0
        ? (isRegular ? ghostCollateralToken0 : ghostProtectedToken0)
        : (isRegular ? ghostCollateralToken1 : ghostProtectedToken1);
    address asset = isSilo0 ? ghostToken0 : ghostToken1;
    return (share, asset);
}

function getDebtShareTokenAndAssetCVL(address _silo) returns (address, address) {
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    bool isSilo0 = (_silo == ghostSilo0);
    return (isSilo0 ? ghostDebtToken0 : ghostDebtToken1, isSilo0 ? ghostToken0 : ghostToken1);
}

function getConfigCVL(address _silo) returns ISiloConfig.ConfigData {
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    return (_silo == ghostSilo0) ? _silo0ConfigDataCVL() : _silo1ConfigDataCVL();
}

function hasDebtInOtherSiloCVL(address _thisSilo, address _borrower) returns bool {
    ASSERT(_thisSilo == ghostSilo0 || _thisSilo == ghostSilo1);
    bool isSilo0 = (_thisSilo == ghostSilo0);
    mathint balance = isSilo0
        ? ghostERC20Balances[ghostDebtToken1][_borrower]
        : ghostERC20Balances[ghostDebtToken0][_borrower];
    return balance != 0;
}

function getDebtSiloCVL(address _borrower) returns address {
    mathint db0 = ghostERC20Balances[ghostDebtToken0][_borrower];
    mathint db1 = ghostERC20Balances[ghostDebtToken1][_borrower];
    ASSERT(db0 == 0 || db1 == 0);
    address retVal = ((db0 == 0 && db1 == 0) ? 0 : (db0 != 0 ? ghostSilo0 : ghostSilo1));
    return retVal;
}

function getSiloIdCVL() returns uint256 {
    return require_uint256(ghostSiloId);
}

function _getDepositConfigCVL(address _silo) returns ISiloConfig.DepositConfig {
    ASSERT(_silo == ghostSilo0 || _silo == ghostSilo1);
    return (_silo == ghostSilo0) ? _silo0DepositConfigCVL() : _silo1DepositConfigCVL();
}

function _silo0ConfigDataCVL() returns ISiloConfig.ConfigData {
    ISiloConfig.ConfigData config;
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.silo == ghostSilo0);
    require(config.token == ghostToken0);
    require(config.protectedShareToken == ghostProtectedToken0);
    require(config.collateralShareToken == ghostCollateralToken0);
    require(config.debtShareToken == ghostDebtToken0);
    require(config.solvencyOracle == ghostConfigSolvencyOracle0);
    require(config.maxLtvOracle == ghostConfigMaxLtvOracle0);
    require(config.interestRateModel == ghostConfigInterestRateModel0);
    require(config.maxLtv == require_uint256(ghostConfigMaxLtv0));
    require(config.lt == require_uint256(ghostConfigLt0));
    require(config.liquidationTargetLtv == require_uint256(ghostConfigLiquidationTargetLtv0));
    require(config.liquidationFee == require_uint256(ghostConfigLiquidationFee0));
    require(config.flashloanFee == require_uint256(ghostConfigFlashloanFee0));
    require(config.hookReceiver == ghostConfigHookReceiver);
    require(config.callBeforeQuote == ghostConfigCallBeforeQuote0);
    return config;
}

function _silo1ConfigDataCVL() returns ISiloConfig.ConfigData {
    ISiloConfig.ConfigData config;
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.silo == ghostSilo1);
    require(config.token == ghostToken1);
    require(config.protectedShareToken == ghostProtectedToken1);
    require(config.collateralShareToken == ghostCollateralToken1);
    require(config.debtShareToken == ghostDebtToken1);
    require(config.solvencyOracle == ghostConfigSolvencyOracle1);
    require(config.maxLtvOracle == ghostConfigMaxLtvOracle1);
    require(config.interestRateModel == ghostConfigInterestRateModel1);
    require(config.maxLtv == require_uint256(ghostConfigMaxLtv1));
    require(config.lt == require_uint256(ghostConfigLt1));
    require(config.liquidationTargetLtv == require_uint256(ghostConfigLiquidationTargetLtv1));
    require(config.liquidationFee == require_uint256(ghostConfigLiquidationFee1));
    require(config.flashloanFee == require_uint256(ghostConfigFlashloanFee1));
    require(config.hookReceiver == ghostConfigHookReceiver);
    require(config.callBeforeQuote == ghostConfigCallBeforeQuote1);
    return config;
}

function _emptyConfigDataCVL() returns ISiloConfig.ConfigData {
    ISiloConfig.ConfigData config;
    require(config.daoFee == 0);
    require(config.deployerFee == 0);
    require(config.silo == 0);
    require(config.token == 0);
    require(config.protectedShareToken == 0);
    require(config.collateralShareToken == 0);
    require(config.debtShareToken == 0);
    require(config.solvencyOracle == 0);
    require(config.maxLtvOracle == 0);
    require(config.interestRateModel == 0);
    require(config.maxLtv == 0);
    require(config.lt == 0);
    require(config.liquidationTargetLtv == 0);
    require(config.liquidationFee == 0);
    require(config.flashloanFee == 0);
    require(config.hookReceiver == 0);
    require(config.callBeforeQuote == false);
    return config;
}

function _silo0DepositConfigCVL() returns ISiloConfig.DepositConfig {
    ISiloConfig.DepositConfig config;
    require(config.silo == ghostSilo0);
    require(config.token == ghostToken0);
    require(config.collateralShareToken == ghostCollateralToken0);
    require(config.protectedShareToken == ghostProtectedToken0);
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.interestRateModel == ghostConfigInterestRateModel0);
    return config;
}

function _silo1DepositConfigCVL() returns ISiloConfig.DepositConfig {
    ISiloConfig.DepositConfig config;
    require(config.silo == ghostSilo1);
    require(config.token == ghostToken1);
    require(config.collateralShareToken == ghostCollateralToken1);
    require(config.protectedShareToken == ghostProtectedToken1);
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.interestRateModel == ghostConfigInterestRateModel1);
    return config;
}
