import pytest
import numpy as np
from syntax_alpha.core import (
    OperationRegistry,
    parse_expression,
    evaluate_node,
    compute_expressions,
    ASTNode,
    NodeType
)
from syntax_alpha import operations

@pytest.fixture
def variables():
    """测试数据"""
    return {
        'x1': np.array([[1, 2], [3, 4]]),
        'x2': np.array([[5, 6], [7, 8]]),
        'x3': np.array([[9, 10], [11, 12]])
    }

def test_operation_registry():
    """测试操作符注册"""
    registry = OperationRegistry()
    assert registry.get('Add') is not None
    assert registry.get('NonExistent') is None

def test_parse_expression():
    """测试表达式解析"""
    # 测试变量
    node = parse_expression('x1')
    assert isinstance(node, ASTNode)
    assert node.type == NodeType.VARIABLE
    assert node.value == 'x1'
    
    # 测试简单操作
    node = parse_expression('Add(x1, x2)')
    assert isinstance(node, ASTNode)
    assert node.type == NodeType.OPERATION
    assert node.op == 'Add'
    assert len(node.args) == 2
    
    # 测试嵌套操作
    node = parse_expression('Add(x1, Div(x2, x3))')
    assert isinstance(node, ASTNode)
    assert node.type == NodeType.OPERATION
    assert node.op == 'Add'
    assert len(node.args) == 2
    assert node.args[1].op == 'Div'

def test_evaluate_node(variables):
    """测试节点求值"""
    # 测试变量
    node = ASTNode(type=NodeType.VARIABLE, value='x1')
    result = evaluate_node(node, variables)
    np.testing.assert_array_equal(result, variables['x1'])
    
    # 测试简单操作
    node = ASTNode(
        type=NodeType.OPERATION,
        op='Add',
        args=[
            ASTNode(type=NodeType.VARIABLE, value='x1'),
            ASTNode(type=NodeType.VARIABLE, value='x2')
        ]
    )
    result = evaluate_node(node, variables)
    expected = variables['x1'] + variables['x2']
    np.testing.assert_array_equal(result, expected)

def test_compute_expressions(variables):
    """测试表达式计算"""
    expressions = [
        'Add(x1, x2)',
        'Div(x2, x3)'
    ]
    result = compute_expressions(expressions, variables)
    assert result.shape == (2, 2, 2)
    
    # 测试第一个表达式
    np.testing.assert_array_equal(
        result[..., 0],
        variables['x1'] + variables['x2']
    )
    
    # 测试第二个表达式
    np.testing.assert_array_equal(
        result[..., 1],
        variables['x2'] / variables['x3']
    )

def test_error_handling():
    """测试错误处理"""
    # 测试未注册的操作符
    with pytest.raises(ValueError, match="Operation NonExistent not registered"):
        node = ASTNode(
            type=NodeType.OPERATION,
            op='NonExistent',
            args=[]
        )
        evaluate_node(node, {'x1': np.array([1])})
    
    # 测试未定义的变量
    with pytest.raises(ValueError, match="Variable x2 not found"):
        node = ASTNode(type=NodeType.VARIABLE, value='x2')
        evaluate_node(node, {'x1': np.array([1])})
    
    # 测试维度不匹配
    with pytest.raises(ValueError, match="Shape mismatch"):
        compute_expressions(
            ['Add(x1, x2)'],
            {
                'x1': np.array([[1, 2], [3, 4]]),
                'x2': np.array([1, 2])
            }
        ) 