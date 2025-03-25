import numpy as np
from typing import Any, Callable
from .core import OperationRegistry

registry = OperationRegistry()

def register_operation(name: str) -> Callable:
    """注册操作符的装饰器
    
    Args:
        name: 操作符名称
        
    Returns:
        装饰器函数
    """
    def decorator(func: Callable) -> Callable:
        registry.register(name, func)
        return func
    return decorator

# 数学运算
@register_operation('Add')
def add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """加法运算"""
    return a + b

@register_operation('Sub')
def sub(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """减法运算"""
    return a - b

@register_operation('Mul')
def mul(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """乘法运算"""
    return a * b

@register_operation('Div')
def div(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """除法运算"""
    return a / b

# 逻辑运算
@register_operation('If')
def if_else(cond: np.ndarray, t: np.ndarray, f: np.ndarray) -> np.ndarray:
    """条件运算"""
    return np.where(cond, t, f)

@register_operation('Or')
def or_op(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """逻辑或运算"""
    return np.logical_or(a, b)

@register_operation('And')
def and_op(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """逻辑与运算"""
    return np.logical_and(a, b)

@register_operation('Not')
def not_op(a: np.ndarray) -> np.ndarray:
    """逻辑非运算"""
    return np.logical_not(a)

@register_operation('Gt')
def gt(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """大于运算"""
    return a > b

@register_operation('Lt')
def lt(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """小于运算"""
    return a < b

# 统计运算
@register_operation('Rank')
def rank(a: np.ndarray) -> np.ndarray:
    """排序运算"""
    return np.argsort(np.argsort(a, axis=-1), axis=-1)
