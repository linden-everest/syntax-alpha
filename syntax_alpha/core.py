import numpy as np
import re
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class NodeType(Enum):
    """AST节点类型"""
    VARIABLE = "variable"
    OPERATION = "operation"

@dataclass
class ASTNode:
    """抽象语法树节点"""
    type: NodeType
    value: Optional[str] = None
    op: Optional[str] = None
    args: Optional[List['ASTNode']] = None

class OperationRegistry:
    """操作符注册中心（单例模式）"""
    _instance = None
    _operations = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._operations = {}
        return cls._instance

    def register(self, name: str, func: callable) -> None:
        """注册操作符
        
        Args:
            name: 操作符名称
            func: 操作符函数
        """
        self._operations[name] = func
        logger.info(f"Registered operation: {name}")

    def get(self, name: str) -> Optional[callable]:
        """获取操作符函数
        
        Args:
            name: 操作符名称
            
        Returns:
            操作符函数或None
        """
        return self._operations.get(name)

def split_args(args_str: str) -> List[str]:
    """智能分割嵌套参数
    
    Args:
        args_str: 参数字符串
        
    Returns:
        分割后的参数列表
    """
    parts = []
    current = []
    level = 0
    
    for c in args_str:
        if c == '(':
            level += 1
        elif c == ')':
            level -= 1
            if level < 0:
                raise ValueError("Unmatched parentheses in expression")
        
        if c == ',' and level == 0:
            parts.append(''.join(current).strip())
            current = []
        else:
            current.append(c)
            
    if current:
        parts.append(''.join(current).strip())
    if level != 0:
        raise ValueError("Unmatched parentheses in expression")
        
    return parts

def parse_expression(expr: str) -> ASTNode:
    """解析表达式为AST
    
    Args:
        expr: 表达式字符串
        
    Returns:
        AST节点
        
    Raises:
        ValueError: 表达式格式错误
    """
    expr = expr.replace(' ', '')
    match = re.match(r'^(\w+)\((.*)\)$', expr)
    
    if not match:
        return ASTNode(type=NodeType.VARIABLE, value=expr)
    
    op_name = match.group(1)
    args_str = match.group(2)
    
    try:
        args = [parse_expression(arg) for arg in split_args(args_str)]
        return ASTNode(type=NodeType.OPERATION, op=op_name, args=args)
    except Exception as e:
        raise ValueError(f"Failed to parse expression: {expr}. Error: {str(e)}")

def evaluate_node(node: ASTNode, variables: Dict[str, np.ndarray]) -> np.ndarray:
    """递归执行AST
    
    Args:
        node: AST节点
        variables: 变量字典
        
    Returns:
        计算结果
        
    Raises:
        ValueError: 变量未找到或操作符未注册
    """
    if node.type == NodeType.VARIABLE:
        if node.value not in variables:
            raise ValueError(f"Variable {node.value} not found")
        return variables[node.value]
    
    op = OperationRegistry().get(node.op)
    if not op:
        raise ValueError(f"Operation {node.op} not registered")
    
    try:
        args = [evaluate_node(arg, variables) for arg in node.args]
        return op(*args)
    except Exception as e:
        raise ValueError(f"Failed to evaluate operation {node.op}. Error: {str(e)}")

def compute_expressions(expressions: List[str], variables: Dict[str, np.ndarray]) -> np.ndarray:
    """执行多个表达式并拼接结果
    
    Args:
        expressions: 表达式列表
        variables: 变量字典
        
    Returns:
        计算结果
        
    Raises:
        ValueError: 表达式执行错误或维度不匹配
    """
    if not variables:
        raise ValueError("No variables provided")
        
    results = []
    base_shape = next(iter(variables.values())).shape
    
    for expr in expressions:
        try:
            ast = parse_expression(expr)
            result = evaluate_node(ast, variables)
            
            if result.shape != base_shape:
                raise ValueError(f"Shape mismatch in expression: {expr}")
                
            results.append(np.expand_dims(result, axis=-1))
            logger.info(f"Successfully evaluated expression: {expr}")
            
        except Exception as e:
            logger.error(f"Failed to evaluate expression: {expr}. Error: {str(e)}")
            raise
    
    return np.concatenate(results, axis=-1)