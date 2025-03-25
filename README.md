# Syntax Alpha

一个灵活的因子表达式计算引擎，支持自定义操作符和嵌套表达式计算。

## 特性

- 支持自定义数学和逻辑操作符
- 支持嵌套表达式解析和计算
- 支持numpy数组运算
- 简单直观的表达式语法
- 低耦合设计

## 安装

```bash
pip install -r requirements.txt
```

## 快速开始

1. 定义因子表达式（在factors.txt中）：
```
Add(x1, x2)
Add(x1, Div(x2, x3))
Rank(x1)
```

2. 准备数据：
```python
variables = {
    'x1': np.random.randn(5, 5),
    'x2': np.random.randn(5, 5),
    'x3': np.random.randn(5, 5)
}
```

3. 执行计算：
```python
from syntax_alpha.core import compute_expressions
from syntax_alpha import operations

results = compute_expressions(
    expressions=load_expressions('factors.txt'),
    variables=variables
)
```

## 支持的操作符

- 数学运算：Add, Sub, Mul, Div
- 逻辑运算：If, Or, And, Not, Gt, Lt
- 统计运算：Rank

## 开发

```bash
# 运行测试
pytest

# 代码格式化
black .

# 类型检查
mypy .
```

## 许可证

MIT License 