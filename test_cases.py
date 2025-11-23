"""
传纸条问题测试用例生成和验证
"""

def test_paper_passing():
    """测试传纸条算法的正确性"""
    
    # 测试用例1：题目给出的样例
    test1 = {
        'input': [[0, 3, 9], [2, 8, 5], [5, 7, 0]],
        'expected': 34,
        'description': '题目样例'
    }
    
    # 测试用例2：最小规模
    test2 = {
        'input': [[0, 1], [2, 0]],
        'expected': 3,  # 路径1: 0->1->0, 路径2: 0->2->0, 总和: 1+2 = 3
        'description': '2x2最小规模'
    }
    
    # 测试用例3：单行
    test3 = {
        'input': [[0, 1, 2, 0]],
        'expected': 3,  # 只有一条路径: 0->1->2->0
        'description': '1x4单行'
    }
    
    # 测试用例4：单列
    test4 = {
        'input': [[0], [1], [2], [0]],
        'expected': 3,  # 只有一条路径: 0->1->2->0
        'description': '4x1单列'
    }
    
    # 测试用例5：全零矩阵
    test5 = {
        'input': [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
        'expected': 0,
        'description': '全零矩阵'
    }
    
    test_cases = [test1, test2, test3, test4, test5]
    
    for i, test in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test['description']}")
        print(f"输入矩阵:")
        for row in test['input']:
            print(f"  {row}")
        print(f"期望输出: {test['expected']}")
        
        # 运行算法
        result = solve_for_test(test['input'])
        print(f"实际输出: {result}")
        
        if result == test['expected']:
            print("✓ 通过")
        else:
            print("✗ 失败")
        print("-" * 40)

def solve_for_test(grid):
    """为测试用例运行算法"""
    m, n = len(grid), len(grid[0])
    
    # 转换为1-indexed
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            matrix[i][j] = grid[i-1][j-1]
    
    # 特殊情况：只有一个格子
    if m == 1 and n == 1:
        return matrix[1][1]
    
    # DP算法
    total_steps = m + n - 2
    dp = [[[-1 for _ in range(m + 1)] for _ in range(m + 1)] for _ in range(total_steps + 1)]
    
    dp[0][1][1] = matrix[1][1]
    
    for step in range(1, total_steps + 1):
        for i1 in range(1, m + 1):
            for i2 in range(1, m + 1):
                j1 = step + 2 - i1
                j2 = step + 2 - i2
                
                if j1 < 1 or j1 > n or j2 < 1 or j2 > n:
                    continue
                
                if i1 == i2 and j1 == j2:
                    current_value = matrix[i1][j1]
                else:
                    current_value = matrix[i1][j1] + matrix[i2][j2]
                
                max_prev = -1
                
                if i1 - 1 >= 1 and i2 - 1 >= 1 and dp[step - 1][i1 - 1][i2 - 1] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1 - 1][i2 - 1])
                
                if i1 - 1 >= 1 and dp[step - 1][i1 - 1][i2] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1 - 1][i2])
                
                if i2 - 1 >= 1 and dp[step - 1][i1][i2 - 1] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1][i2 - 1])
                
                if dp[step - 1][i1][i2] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1][i2])
                
                if max_prev != -1:
                    dp[step][i1][i2] = max_prev + current_value
    
    return dp[total_steps][m][m]

if __name__ == "__main__":
    test_paper_passing()