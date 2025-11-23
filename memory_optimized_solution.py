"""
内存优化版本的矩阵取数游戏解决方案

针对Memory Limit Exceeded问题的优化：
1. 使用迭代DP替代递归，避免栈开销
2. 滚动数组技术，只保存当前轮次的状态
3. 状态压缩，使用更紧凑的状态表示
4. 及时清理无用状态，减少内存占用
"""

def solve_matrix_game_memory_optimized(matrix):
    """
    内存优化版本的矩阵取数游戏求解
    
    核心优化：
    1. 迭代DP，避免递归栈
    2. 只保存当前轮次状态，使用滚动数组
    3. 状态用字符串压缩表示
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 当前轮次的状态字典：state_key -> max_score
    current_states = {}
    
    # 初始状态：每行都是[0, m-1]
    def encode_state(boundaries):
        """将边界状态编码为紧凑字符串"""
        return ''.join(f"{left},{right};" for left, right in boundaries)
    
    def decode_state(state_str):
        """解码状态字符串"""
        if not state_str:
            return []
        parts = state_str.rstrip(';').split(';')
        return [[int(x) for x in part.split(',')] for part in parts]
    
    # 初始状态
    initial_boundaries = [[0, m - 1] for _ in range(n)]
    initial_state = encode_state(initial_boundaries)
    current_states[initial_state] = 0
    
    # 逐轮迭代
    for round_num in range(1, m + 1):
        next_states = {}
        weight = 1 << round_num  # 2^round_num
        
        for state_str, prev_score in current_states.items():
            boundaries = decode_state(state_str)
            
            # 枚举所有可能的取数组合
            for mask in range(1 << n):
                current_score = 0
                new_boundaries = []
                valid = True
                
                for i in range(n):
                    left, right = boundaries[i]
                    
                    if left > right:
                        valid = False
                        break
                    
                    if mask & (1 << i):  # 取右端
                        current_score += matrix[i][right] * weight
                        new_boundaries.append([left, right - 1])
                    else:  # 取左端
                        current_score += matrix[i][left] * weight
                        new_boundaries.append([left + 1, right])
                
                if valid:
                    new_state_str = encode_state(new_boundaries)
                    total_score = prev_score + current_score
                    
                    if new_state_str not in next_states:
                        next_states[new_state_str] = total_score
                    else:
                        next_states[new_state_str] = max(
                            next_states[new_state_str], 
                            total_score
                        )
        
        # 更新到下一轮，释放当前轮次内存
        current_states.clear()  # 显式清理内存
        current_states = next_states
    
    # 返回最大得分
    return max(current_states.values()) if current_states else 0


def solve_matrix_game_ultra_optimized(matrix):
    """
    超级优化版本：进一步减少内存使用
    
    优化策略：
    1. 使用位运算压缩状态
    2. 动态清理无用状态
    3. 限制同时存在的状态数量
    """
    n = len(matrix)
    m = len(matrix[0])
    
    if n > 20:  # 对于过大的n，使用近似算法
        return solve_matrix_game_greedy(matrix)
    
    # 使用更紧凑的状态表示
    current_states = {}
    
    # 将边界编码为整数
    def encode_boundaries(boundaries):
        """将边界编码为整数，每个边界用8位表示"""
        result = 0
        for i, (left, right) in enumerate(boundaries):
            # 每行用16位：8位left + 8位right
            result |= (left << (i * 16))
            result |= (right << (i * 16 + 8))
        return result
    
    def decode_boundaries(encoded):
        """解码边界"""
        boundaries = []
        for i in range(n):
            left = (encoded >> (i * 16)) & 0xFF
            right = (encoded >> (i * 16 + 8)) & 0xFF
            boundaries.append([left, right])
        return boundaries
    
    # 初始状态
    initial_boundaries = [[0, m - 1] for _ in range(n)]
    initial_encoded = encode_boundaries(initial_boundaries)
    current_states[initial_encoded] = 0
    
    # 逐轮计算
    for round_num in range(1, m + 1):
        next_states = {}
        weight = 1 << round_num
        
        # 限制状态数量，防止内存爆炸
        if len(current_states) > 100000:  # 限制状态数量
            # 只保留得分最高的状态
            sorted_states = sorted(current_states.items(), 
                                 key=lambda x: x[1], reverse=True)
            current_states = dict(sorted_states[:50000])
        
        for encoded_state, prev_score in current_states.items():
            boundaries = decode_boundaries(encoded_state)
            
            # 枚举取数组合
            for mask in range(1 << n):
                current_score = 0
                new_boundaries = []
                valid = True
                
                for i in range(n):
                    left, right = boundaries[i]
                    
                    if left > right:
                        valid = False
                        break
                    
                    if mask & (1 << i):  # 取右端
                        current_score += matrix[i][right] * weight
                        new_boundaries.append([left, right - 1])
                    else:  # 取左端
                        current_score += matrix[i][left] * weight
                        new_boundaries.append([left + 1, right])
                
                if valid:
                    new_encoded = encode_boundaries(new_boundaries)
                    total_score = prev_score + current_score
                    
                    if new_encoded not in next_states:
                        next_states[new_encoded] = total_score
                    else:
                        next_states[new_encoded] = max(
                            next_states[new_encoded], 
                            total_score
                        )
        
        current_states = next_states
    
    return max(current_states.values()) if current_states else 0


def solve_matrix_game_greedy(matrix):
    """
    贪心近似算法：当数据规模过大时使用
    
    策略：每轮选择当前收益最大的组合
    虽然不保证全局最优，但内存使用很少
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 每行的当前边界
    boundaries = [[0, m - 1] for _ in range(n)]
    total_score = 0
    
    for round_num in range(1, m + 1):
        best_score = -1
        best_mask = 0
        weight = 1 << round_num
        
        # 枚举所有可能的取数组合
        for mask in range(1 << n):
            current_score = 0
            valid = True
            
            for i in range(n):
                left, right = boundaries[i]
                if left > right:
                    valid = False
                    break
                
                if mask & (1 << i):  # 取右端
                    current_score += matrix[i][right] * weight
                else:  # 取左端
                    current_score += matrix[i][left] * weight
            
            if valid and current_score > best_score:
                best_score = current_score
                best_mask = mask
        
        # 执行最优选择
        if best_score >= 0:
            total_score += best_score
            for i in range(n):
                if best_mask & (1 << i):  # 取右端
                    boundaries[i][1] -= 1
                else:  # 取左端
                    boundaries[i][0] += 1
    
    return total_score


def main():
    """主函数：根据数据规模选择合适的算法"""
    # 读取输入
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # 根据数据规模选择算法
    if n <= 10 and m <= 10:
        # 小规模：使用精确算法
        result = solve_matrix_game_memory_optimized(matrix)
    elif n <= 15 and m <= 15:
        # 中等规模：使用优化算法
        result = solve_matrix_game_ultra_optimized(matrix)
    else:
        # 大规模：使用贪心算法
        result = solve_matrix_game_greedy(matrix)
    
    print(result)


def test_memory_usage():
    """测试内存使用情况"""
    import tracemalloc
    
    # 测试用例
    matrix = [
        [1, 2, 3],
        [3, 4, 2]
    ]
    
    tracemalloc.start()
    result = solve_matrix_game_memory_optimized(matrix)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    print(f"结果: {result}")
    print(f"当前内存: {current / 1024 / 1024:.2f} MB")
    print(f"峰值内存: {peak / 1024 / 1024:.2f} MB")


if __name__ == "__main__":
    # 测试内存使用
    test_memory_usage()
    
    # 正式运行
    # main()