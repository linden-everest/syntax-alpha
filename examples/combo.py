import numpy as np
import logging
from typing import List
from pathlib import Path
from syntax_alpha.core import compute_expressions
from syntax_alpha import operations  # 加载默认运算符

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_expressions(file_path: str) -> List[str]:
    """从文件加载表达式
    
    Args:
        file_path: 表达式文件路径
        
    Returns:
        表达式列表
        
    Raises:
        FileNotFoundError: 文件不存在
        ValueError: 文件为空
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Expression file not found: {file_path}")
        
    with open(path, 'r', encoding='utf-8') as f:
        expressions = [line.strip() for line in f if line.strip()]
        
    if not expressions:
        raise ValueError(f"No valid expressions found in file: {file_path}")
        
    logger.info(f"Loaded {len(expressions)} expressions from {file_path}")
    return expressions

def main():
    """主函数"""
    try:
        # 准备数据
        variables = {
            'x1': np.random.randn(5, 5),
            'x2': np.random.randn(5, 5),
            'x3': np.random.randn(5, 5)
        }

        # 从文件加载表达式
        expressions = load_expressions('./examples/factors.txt')

        # 执行计算
        results = compute_expressions(
            expressions=expressions,
            variables=variables
        )
        
        logger.info(f"Results shape: {results.shape}")
        logger.info("Sample result:\n%s", results[..., 0])
        
    except Exception as e:
        logger.error("Failed to execute expressions: %s", str(e))
        raise

if __name__ == "__main__":
    main()