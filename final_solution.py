"""
矩阵取数游戏 - 最终解决方案

题目描述：
师师经常跟同学玩一个矩阵取数游戏：对于一个给定的 n × m 的矩阵，矩阵中的每个元素 aᵢⱼ 均为非负整数。
游戏规则如下：
1. 每次取数时须从每行各取走一个元素，共 n 个。经过 m 次后取完矩阵内所有元素；
2. 每次取走的各个元素只能是该元素所在行的行首或行尾；
3. 每次取数都有一个得分值，为每行取数的得分之和，每行取数的得分 = 被取走的元素值 × 2ⁱ，其中 i 表示第 i 次取数（从 1 开始编号）；
4. 游戏结束总得分为 m 次取数得分之和。

算法思路：
使用动态规划 + 记忆化搜索
- 状态：每行的左右边界位置
- 转移：枚举每行取左端或右端的所有组合
- 优化：使用记忆化避免重复计算
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
    
    # 记忆化缓存：状态 -> 最大得分
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
        # 基础情况：所有轮次结束
        if round_num > m:
            return 0
        
        # 记忆化：如果已经计算过，直接返回
        if state in memo:
            return memo[state]
        
        max_score = 0
        
        # 枚举所有可能的取数组合（每行取左端或右端）
        # 使用位掩码表示：0表示取左端，1表示取右端
        for mask in range(1 << n):  # 2^n种组合
            current_score = 0
            new_state = []
            valid = True
            
            # 对每一行进行取数操作
            for i in range(n):
                left, right = state[i]
                
                # 检查该行是否还有元素可取
                if left > right:
                    valid = False
                    break
                
                if mask & (1 << i):  # 取右端
                    current_score += matrix[i][right] * (1 << round_num)  # 2^round_num
                    new_state.append((left, right - 1))
                else:  # 取左端
                    current_score += matrix[i][left] * (1 << round_num)   # 2^round_num
                    new_state.append((left + 1, right))
            
            # 如果当前组合有效，递归计算后续得分
            if valid:
                future_score = dfs(tuple(new_state), round_num + 1)
                max_score = max(max_score, current_score + future_score)
        
        # 记忆化存储结果
        memo[state] = max_score
        return max_score
    
    # 初始状态：每行都是完整区间[0, m-1]
    initial_state = tuple((0, m - 1) for _ in range(n))
    return dfs(initial_state, 1)


def main():
    """
    主函数：处理输入输出
    """
    # 读取输入
    n, m = map(int, input().split())
    matrix = []
    for _ in range(n):
        row = list(map(int, input().split()))
        matrix.append(row)
    
    # 求解并输出结果
    result = solve_matrix_game(matrix)
    print(result)


def test_with_sample():
    """
    使用题目给出的样例进行测试
    """
    print("测试样例:")
    print("输入:")
    print("2 3")
    print("1 2 3")
    print("3 4 2")
    print()
    
    # 构造测试矩阵
    matrix = [
        [1, 2, 3],
        [3, 4, 2]
    ]
    
    result = solve_matrix_game(matrix)
    print(f"输出: {result}")
    print()
    
    # 验证过程
    print("验证过程:")
    print("最优策略:")
    print("第1轮(权重2): 第1行取左端1, 第2行取右端2 -> 1×2 + 2×2 = 6")
    print("第2轮(权重4): 第1行取左端2, 第2行取左端3 -> 2×4 + 3×4 = 20") 
    print("第3轮(权重8): 第1行取左端3, 第2行取左端4 -> 3×8 + 4×8 = 56")
    print("总得分: 6 + 20 + 56 = 82")


if __name__ == "__main__":
    # 如果需要测试，取消下面的注释
    test_with_sample()
    
    # 正式运行时使用下面的代码
    # main()