#!/usr/bin/env python3
"""
测试用例生成和验证
"""

from matrix_game import solve_matrix_game, solve_single_row

def test_basic_cases():
    """测试基本用例"""
    print("=== 基本测试用例 ===")
    
    # 测试用例1：题目样例
    print("测试用例1：题目样例")
    matrix1 = [[1, 2, 3], [3, 4, 2]]
    result1 = solve_matrix_game(2, 3, matrix1)
    print(f"输入：{matrix1}")
    print(f"输出：{result1}")
    print(f"期望：82")
    print(f"正确：{result1 == 82}\n")
    
    # 测试用例2：单行单列
    print("测试用例2：单行单列")
    matrix2 = [[5]]
    result2 = solve_matrix_game(1, 1, matrix2)
    print(f"输入：{matrix2}")
    print(f"输出：{result2}")
    print(f"期望：{5 * 2}")  # 第1次取数，权重2^1=2
    print(f"正确：{result2 == 10}\n")
    
    # 测试用例3：单行多列
    print("测试用例3：单行多列")
    matrix3 = [[1, 5, 2]]
    result3 = solve_matrix_game(1, 3, matrix3)
    print(f"输入：{matrix3}")
    print(f"输出：{result3}")
    # 最优策略：取1(2^1) + 取2(2^2) + 取5(2^3) = 2 + 8 + 40 = 50
    print(f"期望：50")
    print(f"正确：{result3 == 50}\n")
    
    # 测试用例4：多行单列
    print("测试用例4：多行单列")
    matrix4 = [[3], [7], [2]]
    result4 = solve_matrix_game(3, 1, matrix4)
    print(f"输入：{matrix4}")
    print(f"输出：{result4}")
    print(f"期望：{(3 + 7 + 2) * 2}")  # 每行只有一个元素，权重都是2^1=2
    print(f"正确：{result4 == 24}\n")

def test_edge_cases():
    """测试边界情况"""
    print("=== 边界测试用例 ===")
    
    # 测试用例5：包含0的矩阵
    print("测试用例5：包含0")
    matrix5 = [[0, 1, 0], [2, 0, 3]]
    result5 = solve_matrix_game(2, 3, matrix5)
    print(f"输入：{matrix5}")
    print(f"输出：{result5}")
    
    # 手动计算第一行[0,1,0]最优策略
    row1_score = solve_single_row([0, 1, 0], 3)
    row2_score = solve_single_row([2, 0, 3], 3)
    print(f"第一行得分：{row1_score}")
    print(f"第二行得分：{row2_score}")
    print(f"总分：{row1_score + row2_score}\n")
    
    # 测试用例6：递增序列
    print("测试用例6：递增序列")
    matrix6 = [[1, 2, 3, 4]]
    result6 = solve_matrix_game(1, 4, matrix6)
    print(f"输入：{matrix6}")
    print(f"输出：{result6}")
    
    # 测试用例7：递减序列
    print("测试用例7：递减序列")
    matrix7 = [[4, 3, 2, 1]]
    result7 = solve_matrix_game(1, 4, matrix7)
    print(f"输入：{matrix7}")
    print(f"输出：{result7}")

def test_large_numbers():
    """测试大数情况"""
    print("=== 大数测试用例 ===")
    
    # 测试用例8：较大的数值
    print("测试用例8：大数值")
    matrix8 = [[100, 200], [300, 400]]
    result8 = solve_matrix_game(2, 2, matrix8)
    print(f"输入：{matrix8}")
    print(f"输出：{result8}")
    
    # 手动验证
    # 第一行[100, 200]：取100(2^1) + 取200(2^2) = 200 + 800 = 1000
    #                  或取200(2^1) + 取100(2^2) = 400 + 400 = 800
    # 最优：1000
    # 第二行[300, 400]：取300(2^1) + 取400(2^2) = 600 + 1600 = 2200
    #                  或取400(2^1) + 取300(2^2) = 800 + 1200 = 2000  
    # 最优：2200
    # 总计：1000 + 2200 = 3200
    print(f"期望：3200")
    print(f"正确：{result8 == 3200}\n")

if __name__ == "__main__":
    test_basic_cases()
    test_edge_cases()
    test_large_numbers()