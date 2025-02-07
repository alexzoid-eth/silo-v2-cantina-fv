// CVL implementation of SiloConfig

import "./cross_reentrancy_guard_cvl.spec";

methods {
    
    function _.borrowerCollateralSilo(address _borrower) external
        => ghostConfigBorrowerCollateralSilo[_borrower]
            expect address;

    function _.setThisSiloAsCollateralSilo(address _borrower) external with (env e)
        => setThisSiloAsCollateralSiloCVL(e, _borrower) 
            expect void;
    
    function _.setOtherSiloAsCollateralSilo(address _borrower) external with (env e)
        => setOtherSiloAsCollateralSiloCVL(e, _borrower) 
            expect void;

    function _.onDebtTransfer(address _sender, address _recipient) external with (env e)
        => onDebtTransferCVL(e, _sender, _recipient) 
            expect void;

    function _.accrueInterestForSilo(address _silo) external with (env e)
        => accrueInterestForSiloCVL(e, _silo) 
            expect void;

    function _.accrueInterestForBothSilos() external with (env e)
        => accrueInterestForBothSilosCVL(e) 
            expect void;

    function _.getConfigsForSolvency(address _borrower) external
        => getConfigsForSolvencyCVL(_borrower) 
            expect (ISiloConfig.ConfigData, ISiloConfig.ConfigData);

    function _.getConfigsForWithdraw(address _silo, address _depositOwner) external
        => getConfigsForWithdrawCVL(_silo, _depositOwner) 
            expect (ISiloConfig.DepositConfig, ISiloConfig.ConfigData, ISiloConfig.ConfigData);

    function _.getConfigsForBorrow(address _debtSilo) external 
        => getConfigsForBorrowCVL(_debtSilo) 
            expect (ISiloConfig.ConfigData, ISiloConfig.ConfigData);

    function _.getSilos() external 
        => getSilosCVL()
            expect (address, address);

    function _.getShareTokens(address _silo) external
        => getShareTokensCVL(_silo)
            expect (address, address, address);

    function _.getAssetForSilo(address _silo) external
        => getAssetForSiloCVL(_silo)
            expect (address);

    function _.getFeesWithAsset(address _silo) external
        => getFeesWithAssetCVL(_silo)
            expect (uint256, uint256, uint256, address);

    function _.getCollateralShareTokenAndAsset(address _silo, ISilo.CollateralType _collateralType) external
        => getCollateralShareTokenAndAssetCVL(_silo, _collateralType)
            expect (address, address);

    function _.getDebtShareTokenAndAsset(address _silo) external 
        => getDebtShareTokenAndAssetCVL(_silo)
            expect (address, address);
    
    function _.getConfig(address _silo) external
        => getConfigCVL(_silo)
            expect (ISiloConfig.ConfigData);
    
    function _.hasDebtInOtherSilo(address _thisSilo, address _borrower)  external 
        => hasDebtInOtherSiloCVL(_thisSilo, _borrower)
            expect (bool);

    function _.getDebtSilo(address _borrower) external 
        => getDebtSiloCVL(_borrower)
            expect (address);

    function _.SILO_ID() external
        => NONDET DELETE;
}

function setThisSiloAsCollateralSiloCVL(env e, address _borrower) {
    ASSERT(e.msg.sender == _Silo0 || e.msg.sender == _Silo1);
    ghostConfigBorrowerCollateralSilo[_borrower] = e.msg.sender;
}

function setOtherSiloAsCollateralSiloCVL(env e, address _borrower) {
    ASSERT(e.msg.sender == _Silo0 || e.msg.sender == _Silo1);
    if(e.msg.sender == _Silo0) {
        ghostConfigBorrowerCollateralSilo[_borrower] = _Silo1;
    } else {
        ghostConfigBorrowerCollateralSilo[_borrower] = _Silo0;
    }
}

function onDebtTransferCVL(env e, address _sender, address _recipient) {
    ASSERT(e.msg.sender == _Debt0 || e.msg.sender == _Debt1);

    address thisSilo;
    if(e.msg.sender == _Debt0) {
        thisSilo = _Silo0;
    } else {
        thisSilo = _Silo1;
    }

    ASSERT(!hasDebtInOtherSiloCVL(thisSilo, _recipient));

    if (ghostConfigBorrowerCollateralSilo[_recipient] == 0) {
        ghostConfigBorrowerCollateralSilo[_recipient] = ghostConfigBorrowerCollateralSilo[_sender];
    }
}

function accrueInterestForSiloCVL(env e, address _silo) {
    ASSERT(_silo == _Silo0 || _silo == _Silo1);

    address irm;
    if(_silo == _Silo0) {
        irm = ghostConfigInterestRateModel0;
    } else {
        irm = ghostConfigInterestRateModel1;
    }
    
    _silo.accrueInterestForConfig(
        e,
        irm,
        require_uint256(ghostConfigDaoFee),
        require_uint256(ghostConfigDeployerFee)
    );
}

function accrueInterestForBothSilosCVL(env e) {
    _Silo0.accrueInterestForConfig(
        e,
        ghostConfigInterestRateModel0,
        require_uint256(ghostConfigDaoFee),
        require_uint256(ghostConfigDeployerFee)
    );
    _Silo1.accrueInterestForConfig(
        e,
        ghostConfigInterestRateModel1,
        require_uint256(ghostConfigDaoFee),
        require_uint256(ghostConfigDeployerFee)
    );
}

function getConfigsForSolvencyCVL(address _borrower) returns (ISiloConfig.ConfigData, ISiloConfig.ConfigData) {
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

function getConfigsForBorrowCVL(
    address _debtSilo
    ) returns (ISiloConfig.ConfigData, ISiloConfig.ConfigData) {
    
    ASSERT(_debtSilo == _Silo0 || _debtSilo == _Silo1);

    ISiloConfig.ConfigData ccfg;
    ISiloConfig.ConfigData dcfg = getConfigCVL(_debtSilo);

    if(_debtSilo == _Silo0) {
        ccfg = getConfigCVL(_Silo1);
    } else {
        ccfg = getConfigCVL(_Silo0);
    }

    return (ccfg, dcfg);
}

function getSilosCVL() returns (address, address) {
    return (_Silo0, _Silo1);
}

function getShareTokensCVL(address _silo) returns (address, address, address) {
    ASSERT(_silo == _Silo0 || _silo == _Silo1);
    if(_silo == _Silo0) {
        return (_Protected0, _Collateral0, _Debt0);
    } else {
        return (_Protected1, _Collateral1, _Debt1);
    }
}

function getAssetForSiloCVL(address _silo) returns address {
    ASSERT(_silo == _Silo0 || _silo == _Silo1);
    if(_silo == _Silo0) {
        return ghostToken0;
    } else {
        return ghostToken1;
    }
}

function getFeesWithAssetCVL(address _silo) returns (uint256, uint256, uint256, address) {
    ASSERT(_silo == _Silo0 || _silo == _Silo1);

    if(_silo == _Silo0) {
        return (
            require_uint256(ghostConfigDaoFee), 
            require_uint256(ghostConfigDeployerFee), 
            require_uint256(ghostConfigFlashloanFee0), 
            ghostToken0
            );
    } else {
        return (
            require_uint256(ghostConfigDaoFee), 
            require_uint256(ghostConfigDeployerFee), 
            require_uint256(ghostConfigFlashloanFee1), 
            ghostToken1
            );
    }
}

function getCollateralShareTokenAndAssetCVL(
    address _silo, ISilo.CollateralType _collateralType
    ) returns (address, address) {

    ASSERT(_silo == _Silo0 || _silo == _Silo1);

    if(_silo == _Silo0) {
        if(_collateralType == ISilo.CollateralType.Collateral) {
            return (_Collateral0, ghostToken0);
        } else {
            return (_Protected0, ghostToken0);
        }
    } else {
        if(_collateralType == ISilo.CollateralType.Collateral) {
            return (_Collateral1, ghostToken1);
        } else {
            return (_Protected1, ghostToken1);
        }
    }
}

function getDebtShareTokenAndAssetCVL(address _silo) returns (address, address) {
    ASSERT(_silo == _Silo0 || _silo == _Silo1);

    if(_silo == _Silo0) {
        return (_Debt0, ghostToken0);
    } else {
        return (_Debt1, ghostToken1);
    }
}

function getConfigCVL(address _silo) returns ISiloConfig.ConfigData {
    ASSERT(_silo == _Silo0 || _silo == _Silo1);

    if(_silo == _Silo0) {
        return _silo0ConfigDataCVL();
    } else {
        return _silo1ConfigDataCVL();
    }
}

function hasDebtInOtherSiloCVL(address _thisSilo, address _borrower) returns bool {
    ASSERT(_thisSilo == _Silo0 || _thisSilo == _Silo1);

    if(_thisSilo == _Silo0) {
        return (ghostERC20Balances[_Debt1][_borrower] != 0);
    } else {
        return (ghostERC20Balances[_Debt0][_borrower] != 0);
    }
}

function getDebtSiloCVL(address _borrower) returns address {
    mathint db0 = ghostERC20Balances[_Debt0][_borrower];
    mathint db1 = ghostERC20Balances[_Debt1][_borrower];

    ASSERT(db0 == 0 || db1 == 0);

    if(db0 == 0 && db1 == 0) {
        return 0;
    } else if (db0 != 0) {
        return _Silo0;
    } else {
        return _Silo1;
    }
}

function _getDepositConfigCVL(address _silo) returns ISiloConfig.DepositConfig {
    ASSERT(_silo == _Silo0 || _silo == _Silo1);

    if(_silo == _Silo0) {
        return _silo0DepositConfigCVL();
    } else {
        return _silo1DepositConfigCVL();
    }
}

function _silo0ConfigDataCVL() returns ISiloConfig.ConfigData {
    ISiloConfig.ConfigData config;
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.silo == _Silo0);
    require(config.token == ghostToken0);
    require(config.protectedShareToken == _Protected0);
    require(config.collateralShareToken == _Collateral0);
    require(config.debtShareToken == _Debt0);
    require(config.solvencyOracle == ghostConfigSolvencyOracle0);
    require(config.maxLtvOracle == ghostConfigMaxLtvOracle0);
    require(config.interestRateModel == ghostConfigInterestRateModel0);
    require(config.maxLtv == require_uint256(ghostConfigMaxLtv0));
    require(config.lt == require_uint256(ghostConfigLt0));
    require(config.liquidationTargetLtv == require_uint256(ghostConfigLiquidationTargetLtv0));
    require(config.liquidationFee == require_uint256(ghostConfigLiquidationFee0));
    require(config.flashloanFee == require_uint256(ghostConfigFlashloanFee0));
    require(config.hookReceiver == ghostHookReceiver);
    require(config.callBeforeQuote == ghostConfigCallBeforeQuote0);
    return config;
}

function _silo1ConfigDataCVL() returns ISiloConfig.ConfigData {
    ISiloConfig.ConfigData config;
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.silo == _Silo1);
    require(config.token == ghostToken1);
    require(config.protectedShareToken == _Protected1);
    require(config.collateralShareToken == _Collateral1);
    require(config.debtShareToken == _Debt1);
    require(config.solvencyOracle == ghostConfigSolvencyOracle1);
    require(config.maxLtvOracle == ghostConfigMaxLtvOracle1);
    require(config.interestRateModel == ghostConfigInterestRateModel1);
    require(config.maxLtv == require_uint256(ghostConfigMaxLtv1));
    require(config.lt == require_uint256(ghostConfigLt1));
    require(config.liquidationTargetLtv == require_uint256(ghostConfigLiquidationTargetLtv1));
    require(config.liquidationFee == require_uint256(ghostConfigLiquidationFee1));
    require(config.flashloanFee == require_uint256(ghostConfigFlashloanFee1));
    require(config.hookReceiver == ghostHookReceiver);
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
    require(config.silo == _Silo0);
    require(config.token == ghostToken0);
    require(config.collateralShareToken == _Collateral0);
    require(config.protectedShareToken == _Protected0);
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.interestRateModel == ghostConfigInterestRateModel0);
    return config;
}

function _silo1DepositConfigCVL() returns ISiloConfig.DepositConfig {
    ISiloConfig.DepositConfig config;
    require(config.silo == _Silo1);
    require(config.token == ghostToken1);
    require(config.collateralShareToken == _Collateral1);
    require(config.protectedShareToken == _Protected1);
    require(config.daoFee == require_uint256(ghostConfigDaoFee));
    require(config.deployerFee == require_uint256(ghostConfigDeployerFee));
    require(config.interestRateModel == ghostConfigInterestRateModel1);
    return config;
}

function onlySiloOrTokenOrHookReceiverCVL(env e) {
    ASSERT(
        e.msg.sender == _Silo0 ||
        e.msg.sender == _Silo1 ||
        e.msg.sender == ghostHookReceiver ||
        e.msg.sender == _Collateral0 ||
        e.msg.sender == _Collateral1 ||
        e.msg.sender == _Protected0 ||
        e.msg.sender == _Protected1 ||
        e.msg.sender == _Debt0 ||
        e.msg.sender == _Debt1
        );
}