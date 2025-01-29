// Silo0 valid state invariants

import "../setup/silo0/silo_0.spec";

rule sanitySilo0ValidState_part1(method f, env e, calldataarg args) 
    filtered { f ->  
        f.selector == sig:accrueInterestForConfig(address,uint256,uint256).selector
        || f.selector == sig:withdraw(uint256,address,address,ISilo.CollateralType).selector
        || f.selector == sig:redeem(uint256,address,address,ISilo.CollateralType).selector
        || f.selector == sig:approve(address,uint256).selector
        || f.selector == sig:flashFee(address,uint256).selector
        || f.selector == sig:transfer(address,uint256).selector
    } {
    requireValidSilo0E(e);    
    f(e, args);
    satisfy(true);
}   

rule sanitySilo0ValidState_part2(method f, env e, calldataarg args) 
    filtered { f ->  
        f.selector == sig:allowance(address,address).selector
        || f.selector == sig:borrowSameAsset(uint256,address,address).selector
        || f.selector == sig:borrow(uint256,address,address).selector
        || f.selector == sig:redeem(uint256,address,address).selector
        || f.selector == sig:withdraw(uint256,address,address).selector
        || f.selector == sig:borrowShares(uint256,address,address).selector
    } {
    requireValidSilo0E(e);    
    f(e, args);
    satisfy(true);
}   

rule sanitySilo0ValidState_part3(method f, env e, calldataarg args) 
    filtered { f ->  
        f.selector == sig:totalAssets().selector
        || f.selector == sig:getCollateralAndProtectedTotalsStorage().selector
        || f.selector == sig:getDebtAssets().selector
        || f.selector == sig:silo().selector
        || f.selector == sig:siloConfig().selector
    } {
    requireValidSilo0E(e);    
    f(e, args);
    satisfy(true);
}   

rule sanitySilo0ValidState_part4(method f, env e, calldataarg args) 
    filtered { f ->  
        f.selector == sig:updateHooks().selector
        || f.selector == sig:factory().selector
        || f.selector == sig:accrueInterest().selector
        || f.selector == sig:getCollateralAssets().selector
        || f.selector == sig:switchCollateralToThisSilo().selector
        || f.selector == sig:utilizationData().selector
    } {
    requireValidSilo0E(e);    
    f(e, args);
    satisfy(true);
}   

rule sanitySilo0ValidState_part5(method f, env e, calldataarg args) 
    filtered { f ->  
        f.selector == sig:getSiloStorage().selector
        || f.selector == sig:hookReceiver().selector
        || f.selector == sig:eip712Domain().selector
        || f.selector == sig:config().selector
        || f.selector == sig:withdrawFees().selector
        || f.selector == sig:getCollateralAndDebtTotalsStorage().selector
    } {
    requireValidSilo0E(e);    
    f(e, args);
    satisfy(true);
}
