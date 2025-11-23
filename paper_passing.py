"""
传纸条问题 - 动态规划解法

问题描述：
在一个m×n的矩阵中，从左上角(1,1)到右下角(m,n)找两条不相交的路径，
使得路径上数值之和最大。

算法思路：
1. 将问题转化为两个人同时从(1,1)出发到(m,n)的问题
2. 使用3维动态规划：dp[step][i1][i2]
   - step: 当前走的步数
   - i1: 第一条路径当前所在的行
   - i2: 第二条路径当前所在的行
   - 由于步数相同，列坐标可以通过 j = step + 2 - i 计算得出

时间复杂度：O((m+n) × m × n)
空间复杂度：O((m+n) × m × m)
"""

def solve_paper_passing():
    # 读取输入
    m, n = map(int, input().split())
    grid = []
    for i in range(m):
        row = list(map(int, input().split()))
        grid.append(row)
    
    # 转换为1-indexed，方便处理
    matrix = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            matrix[i][j] = grid[i-1][j-1]
    
    # 初始化DP数组
    # dp[step][i1][i2] 表示走了step步，第一条路径在第i1行，第二条路径在第i2行时的最大值
    total_steps = m + n - 2  # 从(1,1)到(m,n)需要的总步数
    dp = [[[-1 for _ in range(m + 1)] for _ in range(m + 1)] for _ in range(total_steps + 1)]
    
    # 初始状态：两条路径都从(1,1)开始
    dp[0][1][1] = matrix[1][1]
    
    # 动态规划状态转移
    for step in range(1, total_steps + 1):
        for i1 in range(1, m + 1):
            for i2 in range(1, m + 1):
                # 计算对应的列坐标
                j1 = step + 2 - i1
                j2 = step + 2 - i2
                
                # 检查边界条件
                if j1 < 1 or j1 > n or j2 < 1 or j2 > n:
                    continue
                
                # 计算当前位置的价值
                if i1 == i2 and j1 == j2:
                    # 两条路径在同一位置，只能取一次值
                    current_value = matrix[i1][j1]
                else:
                    # 两条路径在不同位置，可以取两个值
                    current_value = matrix[i1][j1] + matrix[i2][j2]
                
                # 从前一步的四种可能状态转移而来
                max_prev = -1
                
                # 情况1：第一条路径从上方来(i1-1, j1)，第二条路径从上方来(i2-1, j2)
                if i1 - 1 >= 1 and i2 - 1 >= 1 and dp[step - 1][i1 - 1][i2 - 1] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1 - 1][i2 - 1])
                
                # 情况2：第一条路径从上方来(i1-1, j1)，第二条路径从左方来(i2, j2-1)
                if i1 - 1 >= 1 and dp[step - 1][i1 - 1][i2] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1 - 1][i2])
                
                # 情况3：第一条路径从左方来(i1, j1-1)，第二条路径从上方来(i2-1, j2)
                if i2 - 1 >= 1 and dp[step - 1][i1][i2 - 1] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1][i2 - 1])
                
                # 情况4：第一条路径从左方来(i1, j1-1)，第二条路径从左方来(i2, j2-1)
                if dp[step - 1][i1][i2] != -1:
                    max_prev = max(max_prev, dp[step - 1][i1][i2])
                
                # 更新当前状态
                if max_prev != -1:
                    dp[step][i1][i2] = max_prev + current_value
    
    # 返回结果：两条路径都到达(m,n)时的最大值
    return dp[total_steps][m][m]

if __name__ == "__main__":
    result = solve_paper_passing()
    print(result)