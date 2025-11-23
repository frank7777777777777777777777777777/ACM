"""
调试版本：追踪最优策略的具体选择过程
"""

def solve_with_trace(matrix):
    """
    带追踪的求解函数
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # 记忆化缓存
    memo = {}
    # 追踪最优路径
    path_memo = {}
    
    def dfs(state, round_num):
        """
        深度优先搜索 + 记忆化
        """
        if round_num > m:
            return 0, []
        
        if state in memo:
            return memo[state], path_memo[state]
        
        max_score = 0
        best_path = []
        
        # 枚举所有可能的取数组合
        for mask in range(1 << n):
            current_score = 0
            new_state = []
            valid = True
            current_choice = []
            
            for i in range(n):
                left, right = state[i]
                if left > right:
                    valid = False
                    break
                
                if mask & (1 << i):  # 取右端
                    current_score += matrix[i][right] * (1 << round_num)
                    new_state.append((left, right - 1))
                    current_choice.append((i, 'right', matrix[i][right]))
                else:  # 取左端
                    current_score += matrix[i][left] * (1 << round_num)
                    new_state.append((left + 1, right))
                    current_choice.append((i, 'left', matrix[i][left]))
            
            if valid:
                future_score, future_path = dfs(tuple(new_state), round_num + 1)
                total_score = current_score + future_score
                
                if total_score > max_score:
                    max_score = total_score
                    best_path = [(round_num, current_choice, current_score)] + future_path
        
        memo[state] = max_score
        path_memo[state] = best_path
        return max_score, best_path
    
    # 初始状态
    initial_state = tuple((0, m - 1) for _ in range(n))
    max_score, optimal_path = dfs(initial_state, 1)
    
    return max_score, optimal_path


def print_solution_trace(matrix, max_score, optimal_path):
    """
    打印解决方案的详细追踪
    """
    print("矩阵:")
    for i, row in enumerate(matrix):
        print(f"第{i+1}行: {row}")
    print()
    
    print("最优策略:")
    total_check = 0
    
    for round_num, choices, round_score in optimal_path:
        print(f"第{round_num}轮 (权重 2^{round_num} = {1 << round_num}):")
        round_detail = []
        for row_idx, direction, value in choices:
            round_detail.append(f"第{row_idx+1}行取{direction}端: {value}")
        print("  " + ", ".join(round_detail))
        print(f"  本轮得分: {round_score}")
        total_check += round_score
        print()
    
    print(f"总得分: {max_score}")
    print(f"验证总分: {total_check}")
    print(f"验证{'通过' if max_score == total_check else '失败'}")


def main():
    # 测试用例1
    matrix1 = [
        [1, 2, 3],
        [3, 4, 2]
    ]
    
    print("=" * 50)
    print("测试用例1:")
    max_score1, path1 = solve_with_trace(matrix1)
    print_solution_trace(matrix1, max_score1, path1)
    
    print("\n" + "=" * 50)
    print("测试用例2 (题目给出的例子):")
    # 根据题目描述重新构造测试用例
    matrix2 = [
        [1, 2, 3],
        [3, 4, 2]
    ]
    
    max_score2, path2 = solve_with_trace(matrix2)
    print_solution_trace(matrix2, max_score2, path2)


if __name__ == "__main__":
    main()