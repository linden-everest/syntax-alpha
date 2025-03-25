from syntax_alpha.core import OperationRegistry
import numpy as np

registry = OperationRegistry()

@registry.register('CustomOp1')
def custom_op1(arr: np.ndarray) -> np.ndarray:
    """自定义标准化操作"""
    return (arr - np.mean(arr)) / np.std(arr)

@registry.register('SafeDiv')
def safe_div(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """带除零保护的除法"""
    return np.divide(a, b, out=np.zeros_like(a), where=b!=0)