#!/usr/bin/env python3
"""
矩阵取数游戏 - NOIP 2007
使用区间动态规划解决

算法思路：
1. 每行独立处理，最后求和
2. 对每行使用区间DP：dp[i][j]表示取完区间[i,j]的最大得分
3. 状态转移：dp[i][j] = max(
   dp[i+1][j] + matrix[row][i] * 2^(m-length+1),
   dp[i][j-1] + matrix[row][j] * 2^(m-length+1)
   )
4. 使用Python内置的大整数支持处理高精度计算

时间复杂度：O(n * m^3)
空间复杂度：O(m^2)
"""

def solve_matrix_game(n, m, matrix):
    """
    解决矩阵取数游戏
    
    Args:
        n: 矩阵行数
        m: 矩阵列数  
        matrix: n×m的矩阵
    
    Returns:
        最大得分
    """
    total_score = 0
    
    # 对每一行独立处理
    for row in range(n):
        # 对当前行进行区间DP
        row_score = solve_single_row(matrix[row], m)
        total_score += row_score
    
    return total_score

def solve_single_row(row, m):
    """
    对单行使用区间DP求解最大得分
    
    Args:
        row: 一行的数据
        m: 列数
    
    Returns:
        这一行的最大得分
    """
    # 特殊情况：只有一个元素
    if m == 1:
        return row[0] * 2
    
    # dp[i][j] 表示取完区间[i,j]的最大得分
    dp = [[0] * m for _ in range(m)]
    
    # 预计算2的幂次，避免重复计算
    powers_of_2 = [2 ** i for i in range(1, m + 1)]
    
    # 区间长度从1到m
    for length in range(1, m + 1):
        # 当前轮次（第几次取数）
        round_num = m - length + 1
        power = powers_of_2[round_num - 1]  # 2^round_num
        
        for i in range(m - length + 1):
            j = i + length - 1
            
            if length == 1:
                # 只有一个元素
                dp[i][j] = row[i] * power
            else:
                # 选择取左端点或右端点
                take_left = dp[i + 1][j] + row[i] * power
                take_right = dp[i][j - 1] + row[j] * power
                dp[i][j] = max(take_left, take_right)
    
    return dp[0][m - 1]

def main():
    """主函数"""
    try:
        # 读取输入
        n, m = map(int, input().split())
        
        # 输入验证
        if not (1 <= n <= 80 and 1 <= m <= 80):
            raise ValueError(f"n和m必须在1-80范围内，当前：n={n}, m={m}")
        
        matrix = []
        for i in range(n):
            row = list(map(int, input().split()))
            
            # 验证行长度
            if len(row) != m:
                raise ValueError(f"第{i+1}行应有{m}个元素，实际有{len(row)}个")
            
            # 验证元素范围
            for j, val in enumerate(row):
                if val < 0:
                    raise ValueError(f"矩阵元素必须非负，位置({i+1},{j+1})的值为{val}")
            
            matrix.append(row)
        
        # 求解并输出结果
        result = solve_matrix_game(n, m, matrix)
        print(result)
        
    except ValueError as e:
        print(f"输入错误：{e}")
    except Exception as e:
        print(f"程序错误：{e}")

if __name__ == "__main__":
    main()