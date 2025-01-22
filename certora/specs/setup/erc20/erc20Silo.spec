// Entry to all ERC20 calls splitting to CVL based and ShareToken Solidity implementations

import "./erc20CVL.spec";
import "./erc20.spec";

methods {

    function _.decimals() external
        => decimalsSiloCVL(calledContract) expect uint8;
    
    function ShareTokenLib.decimals() external returns (uint8)
        => decimalsSiloCVL(calledContract);
    
    function _.totalSupply() external with (env e)
        => totalSupplySiloCVL(e, calledContract) expect uint256;

    function _.balanceOf(address owner) external with (env e)
        => balanceOfSiloCVL(e, calledContract, owner) expect uint256;

    function _.allowance(address owner, address spender) external with (env e)
        => allowanceSiloCVL(e, calledContract, owner, spender) expect uint256;

    function _.approve(address spender, uint256 value) external with (env e)
        => approveSiloCVL(e, calledContract, e.msg.sender, spender, value) expect bool;

    function _.transfer(address to, uint256 value) external with (env e)
        => transferFromSiloCVL(e, calledContract, e.msg.sender, to, value, false) expect bool;

    function _.transferFrom(address from, address to, uint256 value) external with (env e)
        => transferFromSiloCVL(e, calledContract, from, to, value, true) expect bool;

    function _.safeTransfer(address token, address to, uint256 value) internal with (env e)
        => safeTransferFromSiloCVL(e, token, calledContract, to, value, false) expect void;

    function _.safeTransferFrom(address token, address from, address to, uint256 value) internal with (env e)
        => safeTransferFromSiloCVL(e, token, from, to, value, true) expect void;
}

persistent ghost uint8 ghostDecimals0 {
    axiom ghostDecimals0 == 0 || (ghostDecimals0 >= 6 && ghostDecimals0 <= 18);
}
persistent ghost uint8 ghostDecimals1 {
    axiom ghostDecimals0 == 0 || (ghostDecimals1 >= 6 && ghostDecimals1 <= 18);
}
function decimalsSiloCVL(address token) returns uint8 {
    // Different decimals for Token0 and Token1
    bool isSilo0 = (token == _CollateralShareToken0 
        || token == _ShareDebtToken0 
        || token == _ShareProtectedCollateralToken0
        || token == ghostToken0
        ); 
    return (isSilo0 ? ghostDecimals0 : ghostDecimals1);
}

function totalSupplySiloCVL(env e, address token) returns uint256 {
    return VALID_ERC20CVL_ADDRESS(token) 
        ? totalSupplyCVL(token)
        : token.totalSupply(e);
}

function balanceOfSiloCVL(env e, address token, address owner) returns uint256 {
    return VALID_ERC20CVL_ADDRESS(token) 
        ? balanceOfCVL(token, owner)
        : token.balanceOf(e, owner);
}

function allowanceSiloCVL(env e, address token, address owner, address spender) returns uint256 {
    return VALID_ERC20CVL_ADDRESS(token) 
        ? allowanceCVL(token, owner, spender)
        : token.allowance(e, owner, spender);
}

function approveSiloCVL(env e, address token, address owner, address spender, uint256 value) returns bool {
    return VALID_ERC20CVL_ADDRESS(token) 
        ? approveCVL(e, token, owner, spender, value)
        : token.approve(e, spender, value);
}

function transferFromSiloCVL(
    env e, address token, address from, address to, uint256 amount, bool transferFrom
    ) returns bool {
    return VALID_ERC20CVL_ADDRESS(token) 
    ? transferFromCVL(e, token, from, to, amount, transferFrom)
    : (transferFrom
        ? token.transferFrom(e, from, to, amount)
        : token.transfer(e, to, amount)
    );
}

function safeTransferFromSiloCVL(
    env e, address token, address from, address to, uint256 amount, bool transferFrom
    ) {
    if(VALID_ERC20CVL_ADDRESS(token)) {
        ASSERT(transferFromCVL(e, token, from, to, amount, transferFrom));
    } else {
        ASSERT(transferFrom 
            ? token.transferFrom(e, from, to, amount)
            : token.transfer(e, to, amount)
            );
    }
}
