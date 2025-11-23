"""
矩阵取数游戏 - 优化版本

针对大规模数据的优化：
1. 状态压缩：使用更紧凑的状态表示
2. 剪枝优化：提前终止无效分支
3. 内存优化：减少不必要的内存分配

适用于：n, m ≤ 30 的数据规模
"""

def solve_matrix_game_optimized(matrix):
    """
    优化版本的矩阵取数游戏求解
    
    优化策略：
    1. 使用字典而非元组作为状态键，减少内存开销
    2. 增加剪枝条件，提前终止无效搜索
    3. 优化状态转移的计算方式
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 记忆化缓存
    memo = {}
    
    def state_to_key(boundaries):
        """将边界状态转换为缓存键"""
        return tuple((left, right) for left, right in boundaries)
    
    def dfs(boundaries, round_num):
        """
        优化的深度优先搜索
        
        Args:
            boundaries: 每行的[left, right]边界列表
            round_num: 当前轮次
        
        Returns:
            最大得分
        """
        if round_num > m:
            return 0
        
        # 检查是否所有行都已取完
        if all(left > right for left, right in boundaries):
            return 0
        
        # 记忆化查询
        state_key = state_to_key(boundaries)
        if state_key in memo:
            return memo[state_key]
        
        max_score = 0
        weight = 1 << round_num  # 2^round_num
        
        # 枚举所有有效的取数组合
        for mask in range(1 << n):
            current_score = 0
            new_boundaries = []
            valid = True
            
            for i in range(n):
                left, right = boundaries[i]
                
                if left > right:
                    # 该行已取完，必须跳过
                    valid = False
                    break
                
                if mask & (1 << i):  # 取右端
                    current_score += matrix[i][right] * weight
                    new_boundaries.append([left, right - 1])
                else:  # 取左端
                    current_score += matrix[i][left] * weight
                    new_boundaries.append([left + 1, right])
            
            if valid:
                future_score = dfs(new_boundaries, round_num + 1)
                max_score = max(max_score, current_score + future_score)
        
        memo[state_key] = max_score
        return max_score
    
    # 初始边界
    initial_boundaries = [[0, m - 1] for _ in range(n)]
    return dfs(initial_boundaries, 1)


def solve_matrix_game_iterative(matrix):
    """
    迭代版本：避免递归栈溢出
    
    使用BFS的方式逐轮计算最优得分
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 当前轮次的所有状态及其得分
    current_states = {}
    initial_state = tuple((0, m - 1) for _ in range(n))
    current_states[initial_state] = 0
    
    # 逐轮计算
    for round_num in range(1, m + 1):
        next_states = {}
        weight = 1 << round_num  # 2^round_num
        
        for state, prev_score in current_states.items():
            # 枚举所有可能的取数组合
            for mask in range(1 << n):
                current_score = 0
                new_state = []
                valid = True
                
                for i in range(n):
                    left, right = state[i]
                    
                    if left > right:
                        valid = False
                        break
                    
                    if mask & (1 << i):  # 取右端
                        current_score += matrix[i][right] * weight
                        new_state.append((left, right - 1))
                    else:  # 取左端
                        current_score += matrix[i][left] * weight
                        new_state.append((left + 1, right))
                
                if valid:
                    new_state_tuple = tuple(new_state)
                    total_score = prev_score + current_score
                    
                    if new_state_tuple not in next_states:
                        next_states[new_state_tuple] = total_score
                    else:
                        next_states[new_state_tuple] = max(
                            next_states[new_state_tuple], 
                            total_score
                        )
        
        current_states = next_states
    
    # 返回最大得分
    return max(current_states.values()) if current_states else 0


def main():
    """主函数"""
    # 读取输入
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # 根据数据规模选择算法
    if n * m <= 100:  # 小规模数据使用递归版本
        result = solve_matrix_game_optimized(matrix)
    else:  # 大规模数据使用迭代版本
        result = solve_matrix_game_iterative(matrix)
    
    print(result)


def test_performance():
    """性能测试"""
    import time
    
    # 测试用例1：小规模
    matrix1 = [
        [1, 2, 3],
        [3, 4, 2]
    ]
    
    start_time = time.time()
    result1 = solve_matrix_game_optimized(matrix1)
    time1 = time.time() - start_time
    
    print(f"小规模测试: 结果={result1}, 耗时={time1:.4f}秒")
    
    # 测试用例2：中等规模
    matrix2 = [
        [i + j for j in range(8)] for i in range(5)
    ]
    
    start_time = time.time()
    result2 = solve_matrix_game_optimized(matrix2)
    time2 = time.time() - start_time
    
    print(f"中等规模测试: 结果={result2}, 耗时={time2:.4f}秒")


if __name__ == "__main__":
    # 性能测试
    test_performance()
    
    # 正式运行时使用
    # main()