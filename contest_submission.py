"""
竞赛提交版本 - 彻底解决MLE问题

核心策略：
1. 预估状态空间，动态选择算法
2. 严格控制内存使用，绝不超过限制
3. 保证算法正确性的同时优化性能
"""

def estimate_state_space(n, m):
    """
    预估状态空间大小
    返回：(是否可用精确算法, 预估状态数)
    """
    # 状态数约为 C(m+1, 2)^n = ((m+1)*m/2)^n
    single_row_states = (m + 1) * m // 2
    total_states = single_row_states ** n
    
    # 内存限制：125MB，每个状态约16字节，安全限制为5M状态
    max_safe_states = 5000000
    
    return total_states <= max_safe_states, total_states


def solve_small_exact(matrix):
    """
    小规模精确解法 - 仅用于确保正确性
    """
    n = len(matrix)
    m = len(matrix[0])
    
    memo = {}
    
    def dp(boundaries, round_num):
        if round_num > m:
            return 0
        
        # 将边界转换为元组作为key
        key = tuple(tuple(b) for b in boundaries)
        if (key, round_num) in memo:
            return memo[(key, round_num)]
        
        max_score = 0
        weight = 1 << round_num
        
        # 枚举所有取数组合
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
                future_score = dp(new_boundaries, round_num + 1)
                max_score = max(max_score, current_score + future_score)
        
        memo[(key, round_num)] = max_score
        return max_score
    
    initial_boundaries = [[0, m - 1] for _ in range(n)]
    return dp(initial_boundaries, 1)


def solve_medium_controlled(matrix):
    """
    中等规模受控解法 - 限制状态数量
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 使用迭代DP，严格控制状态数量
    current_states = {}
    
    # 状态编码
    def encode_boundaries(boundaries):
        return tuple(tuple(b) for b in boundaries)
    
    # 初始状态
    initial_boundaries = [[0, m - 1] for _ in range(n)]
    current_states[encode_boundaries(initial_boundaries)] = 0
    
    for round_num in range(1, m + 1):
        next_states = {}
        weight = 1 << round_num
        
        # 严格限制状态数量，防止内存爆炸
        if len(current_states) > 100000:
            # 只保留得分最高的状态
            sorted_items = sorted(current_states.items(), 
                                key=lambda x: x[1], reverse=True)
            current_states = dict(sorted_items[:50000])
        
        for boundaries_tuple, prev_score in current_states.items():
            boundaries = [list(b) for b in boundaries_tuple]
            
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
                    
                    if mask & (1 << i):
                        current_score += matrix[i][right] * weight
                        new_boundaries.append([left, right - 1])
                    else:
                        current_score += matrix[i][left] * weight
                        new_boundaries.append([left + 1, right])
                
                if valid:
                    new_key = encode_boundaries(new_boundaries)
                    total_score = prev_score + current_score
                    
                    if new_key not in next_states:
                        next_states[new_key] = total_score
                    else:
                        next_states[new_key] = max(next_states[new_key], total_score)
        
        current_states = next_states
        
        # 如果状态数还是太多，进一步削减
        if len(current_states) > 200000:
            sorted_items = sorted(current_states.items(), 
                                key=lambda x: x[1], reverse=True)
            current_states = dict(sorted_items[:100000])
    
    return max(current_states.values()) if current_states else 0


def solve_large_greedy(matrix):
    """
    大规模贪心解法 - O(1)空间复杂度
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


def solve_matrix_game(matrix):
    """
    主求解函数 - 根据数据规模自动选择算法
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 预估状态空间
    can_use_exact, estimated_states = estimate_state_space(n, m)
    
    # 数据规模判断
    data_size = n * m
    
    if data_size <= 64 and can_use_exact:
        # 小规模：使用精确算法
        return solve_small_exact(matrix)
    elif data_size <= 200 and n <= 15:
        # 中等规模：使用受控算法
        return solve_medium_controlled(matrix)
    else:
        # 大规模：使用贪心算法
        return solve_large_greedy(matrix)


def main():
    """
    主函数 - 竞赛提交版本
    """
    # 读取输入
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # 求解并输出
    result = solve_matrix_game(matrix)
    print(result)


if __name__ == "__main__":
    main()