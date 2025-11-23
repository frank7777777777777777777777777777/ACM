#!/usr/bin/env python3
"""
性能测试和大规模数据测试
"""

import time
import random
from matrix_game import solve_matrix_game

def generate_test_matrix(n, m, max_val=1000):
    """生成测试矩阵"""
    return [[random.randint(1, max_val) for _ in range(m)] for _ in range(n)]

def test_performance():
    """测试性能"""
    print("=== 性能测试 ===")
    
    test_cases = [
        (5, 5),
        (10, 10),
        (20, 20),
        (30, 30),
        (40, 40),
    ]
    
    for n, m in test_cases:
        print(f"\n测试规模：{n}×{m}")
        matrix = generate_test_matrix(n, m)
        
        start_time = time.time()
        result = solve_matrix_game(n, m, matrix)
        end_time = time.time()
        
        print(f"结果：{result}")
        print(f"耗时：{end_time - start_time:.4f}秒")

def test_large_scale():
    """测试大规模数据"""
    print("\n=== 大规模测试 ===")
    
    # 测试接近题目上限的数据
    n, m = 60, 60  # 稍小于80×80，避免运行时间过长
    print(f"测试规模：{n}×{m}")
    
    matrix = generate_test_matrix(n, m, 100)
    
    start_time = time.time()
    result = solve_matrix_game(n, m, matrix)
    end_time = time.time()
    
    print(f"结果位数：{len(str(result))}")
    print(f"耗时：{end_time - start_time:.4f}秒")

def test_high_precision():
    """测试高精度计算"""
    print("\n=== 高精度测试 ===")
    
    # 创建一个会产生很大数字的测试用例
    n, m = 3, 50  # 50列会产生2^50的权重
    matrix = [[1000] * m for _ in range(n)]
    
    print(f"测试规模：{n}×{m}")
    print(f"最大权重：2^{m} = {2**m}")
    
    start_time = time.time()
    result = solve_matrix_game(n, m, matrix)
    end_time = time.time()
    
    print(f"结果：{result}")
    print(f"结果位数：{len(str(result))}")
    print(f"耗时：{end_time - start_time:.4f}秒")

if __name__ == "__main__":
    random.seed(42)  # 固定随机种子，确保结果可重现
    
    test_performance()
    test_large_scale()
    test_high_precision()