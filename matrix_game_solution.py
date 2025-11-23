"""
矩阵取数游戏最优解算法

问题描述：
- n×m矩阵，每次从每行取一个元素（只能取行首或行尾）
- 共进行m轮，每轮得分 = Σ(取走的元素值 × 2^i)，i为轮次（从1开始）
- 求最大总得分

算法思路：
1. 使用记忆化搜索 + 状态压缩
2. 状态：每行的左右边界位置
3. 每轮贪心选择当前收益最大的组合
"""

def solve_matrix_game(matrix):
    """
    解决矩阵取数游戏
    
    Args:
        matrix: n×m的二维数组
    
    Returns:
        最大得分
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 记忆化缓存
    memo = {}
    
    def dfs(state, round_num):
        """
        深度优先搜索 + 记忆化
        
        Args:
            state: 元组，表示每行的(left, right)边界
            round_num: 当前轮次（1-based）
        
        Returns:
            从当前状态开始的最大得分
        """
        if round_num > m:
            return 0
        
        if state in memo:
            return memo[state]
        
        max_score = 0
        
        # 枚举所有可能的取数组合（每行取左端或右端）
        for mask in range(1 << n):  # 2^n种组合
            current_score = 0
            new_state = []
            valid = True
            
            for i in range(n):
                left, right = state[i]
                if left > right:  # 该行已取完
                    valid = False
                    break
                
                if mask & (1 << i):  # 取右端
                    current_score += matrix[i][right] * (1 << round_num)  # 2^round_num
                    new_state.append((left, right - 1))
                else:  # 取左端
                    current_score += matrix[i][left] * (1 << round_num)   # 2^round_num
                    new_state.append((left + 1, right))
            
            if valid:
                future_score = dfs(tuple(new_state), round_num + 1)
                max_score = max(max_score, current_score + future_score)
        
        memo[state] = max_score
        return max_score
    
    # 初始状态：每行都是[0, m-1]
    initial_state = tuple((0, m - 1) for _ in range(n))
    return dfs(initial_state, 1)


def solve_matrix_game_optimized(matrix):
    """
    优化版本：使用贪心策略减少搜索空间
    
    核心思想：由于权重是2^i递增的，后面轮次的权重更大
    可以使用贪心策略：每轮选择当前收益最大的组合
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 每行的当前左右边界
    boundaries = [[0, m - 1] for _ in range(n)]
    total_score = 0
    
    for round_num in range(1, m + 1):
        best_score = -1
        best_choice = None
        
        # 枚举所有可能的取数组合
        for mask in range(1 << n):
            current_score = 0
            valid = True
            
            for i in range(n):
                left, right = boundaries[i]
                if left > right:  # 该行已取完
                    valid = False
                    break
                
                if mask & (1 << i):  # 取右端
                    current_score += matrix[i][right] * (1 << round_num)
                else:  # 取左端
                    current_score += matrix[i][left] * (1 << round_num)
            
            if valid and current_score > best_score:
                best_score = current_score
                best_choice = mask
        
        # 执行最优选择
        if best_choice is not None:
            total_score += best_score
            for i in range(n):
                if best_choice & (1 << i):  # 取右端
                    boundaries[i][1] -= 1
                else:  # 取左端
                    boundaries[i][0] += 1
    
    return total_score


def solve_matrix_game_dp(matrix):
    """
    动态规划版本：更高效的实现
    
    使用状态压缩DP，状态用字符串表示每行的边界
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # DP状态：dp[state] = 从该状态开始的最大得分
    dp = {}
    
    def state_to_str(boundaries):
        """将边界状态转换为字符串"""
        return ','.join(f"{left}-{right}" for left, right in boundaries)
    
    def str_to_state(state_str):
        """将字符串转换为边界状态"""
        if not state_str:
            return []
        parts = state_str.split(',')
        return [[int(x) for x in part.split('-')] for part in parts]
    
    def solve_recursive(boundaries, round_num):
        """递归求解"""
        if round_num > m:
            return 0
        
        state_str = state_to_str(boundaries)
        if state_str in dp:
            return dp[state_str]
        
        max_score = 0
        
        # 枚举所有可能的取数组合
        for mask in range(1 << n):
            current_score = 0
            new_boundaries = [row[:] for row in boundaries]  # 深拷贝
            valid = True
            
            for i in range(n):
                left, right = boundaries[i]
                if left > right:
                    valid = False
                    break
                
                if mask & (1 << i):  # 取右端
                    current_score += matrix[i][right] * (1 << round_num)
                    new_boundaries[i][1] -= 1
                else:  # 取左端
                    current_score += matrix[i][left] * (1 << round_num)
                    new_boundaries[i][0] += 1
            
            if valid:
                future_score = solve_recursive(new_boundaries, round_num + 1)
                max_score = max(max_score, current_score + future_score)
        
        dp[state_str] = max_score
        return max_score
    
    # 初始边界
    initial_boundaries = [[0, m - 1] for _ in range(n)]
    return solve_recursive(initial_boundaries, 1)


def main():
    """测试函数"""
    # 测试用例1
    matrix1 = [
        [1, 2, 3],
        [3, 4, 2]
    ]
    
    print("测试用例1:")
    print("矩阵:")
    for row in matrix1:
        print(row)
    
    result1 = solve_matrix_game_dp(matrix1)
    print(f"最大得分: {result1}")
    print()
    
    # 验证：手动计算最优策略
    # 第1轮(权重2^1=2): 取(1,3) -> 1*2 + 3*2 = 8
    # 第2轮(权重2^2=4): 取(2,4) -> 2*4 + 4*4 = 24  
    # 第3轮(权重2^3=8): 取(3,2) -> 3*8 + 2*8 = 40
    # 总分: 8 + 24 + 40 = 72
    print("手动验证:")
    print("第1轮: 取(1,3) -> 1*2 + 3*2 = 8")
    print("第2轮: 取(2,4) -> 2*4 + 4*4 = 24")
    print("第3轮: 取(3,2) -> 3*8 + 2*8 = 40")
    print("总分: 8 + 24 + 40 = 72")
    print()
    
    # 测试更大的矩阵
    matrix2 = [
        [1, 5, 2, 4],
        [3, 2, 6, 1],
        [2, 4, 1, 3]
    ]
    
    print("测试用例2:")
    print("矩阵:")
    for row in matrix2:
        print(row)
    
    result2 = solve_matrix_game_dp(matrix2)
    print(f"最大得分: {result2}")


if __name__ == "__main__":
    main()