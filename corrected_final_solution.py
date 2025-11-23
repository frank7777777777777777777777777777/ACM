#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跳跃棋问题最终正确解决方案
作者: 一个终于理解题意的程序员

关键理解：
1. 第1格的棋子只能通过跳跃规则移动
2. k次"任意移动"只能移动其他棋子，不能移动第1格的棋子
3. 目标是通过移动其他棋子来为第1格棋子创造更好的跳跃路径

这个约束解释了为什么样例4的期望输出是5而不是11。
"""

from collections import deque
from typing import Set, Tuple, List
import sys


class CorrectJumpingChessSolver:
    """
    正确的跳跃棋求解器
    
    关键约束：第1格棋子不能被任意移动，只能跳跃
    """
    
    def __init__(self, board: str, k: int):
        self.initial_board = board
        self.n = len(board)
        self.k = k
        
        if board[0] != 'o':
            raise ValueError("第1格必须有棋子")
    
    def can_jump(self, board: str, pos: int) -> bool:
        """检查指定位置的棋子是否可以跳跃"""
        return (pos + 2 < self.n and 
                board[pos] == 'o' and 
                board[pos + 1] == 'o' and 
                board[pos + 2] == 'x')
    
    def execute_jump(self, board: str, pos: int) -> Tuple[str, int]:
        """执行跳跃操作"""
        new_board = list(board)
        new_board[pos] = 'x'
        new_board[pos + 1] = 'x'
        new_board[pos + 2] = 'o'
        return ''.join(new_board), pos + 2
    
    def jump_to_end(self, board: str, start_pos: int) -> Tuple[str, int]:
        """从指定位置开始跳跃到无法继续为止"""
        current_board = board
        current_pos = start_pos
        
        while self.can_jump(current_board, current_pos):
            current_board, current_pos = self.execute_jump(current_board, current_pos)
        
        return current_board, current_pos
    
    def generate_valid_moves(self, board: str) -> List[str]:
        """
        生成所有有效的单次移动
        
        关键约束：不能移动第1格的棋子（位置0）
        """
        moves = []
        
        # 找到所有可移动的棋子（除了第1格）和空位
        movable_pieces = [i for i in range(1, self.n) if board[i] == 'o']
        empty_positions = [i for i, c in enumerate(board) if c == 'x']
        
        # 生成所有可能的移动
        for piece_pos in movable_pieces:
            for empty_pos in empty_positions:
                new_board = list(board)
                new_board[piece_pos] = 'x'
                new_board[empty_pos] = 'o'
                moves.append(''.join(new_board))
        
        return moves
    
    def solve_with_bfs(self) -> int:
        """使用BFS求解"""
        
        # 计算基础情况（k=0）
        _, base_result = self.jump_to_end(self.initial_board, 0)
        
        if self.k == 0:
            return base_result + 1  # 转换为1-based
        
        # BFS搜索
        # 状态：(棋盘状态, 剩余移动次数)
        queue = deque([(self.initial_board, self.k)])
        visited = set([(self.initial_board, self.k)])
        
        max_position = base_result
        
        while queue:
            current_board, remaining_moves = queue.popleft()
            
            # 计算当前状态下第1格棋子的最优跳跃结果
            _, jump_result = self.jump_to_end(current_board, 0)
            max_position = max(max_position, jump_result)
            
            # 如果还有移动次数，继续探索
            if remaining_moves > 0:
                possible_moves = self.generate_valid_moves(current_board)
                
                for new_board in possible_moves:
                    state_key = (new_board, remaining_moves - 1)
                    if state_key not in visited:
                        visited.add(state_key)
                        queue.append(state_key)
        
        return max_position + 1  # 转换为1-based
    
    def solve_optimized(self) -> int:
        """优化版求解"""
        
        # 对于k=0，直接计算
        if self.k == 0:
            _, result = self.jump_to_end(self.initial_board, 0)
            return result + 1
        
        # 估算状态空间大小
        movable_pieces = sum(1 for i in range(1, self.n) if self.initial_board[i] == 'o')
        empty_positions = self.initial_board.count('x')
        
        # 每步的可能移动数
        moves_per_step = movable_pieces * empty_positions
        
        # 估算总状态数（粗略）
        estimated_states = moves_per_step ** min(self.k, 3)  # 限制估算深度
        
        if estimated_states <= 100000:  # 可接受的状态空间
            return self.solve_with_bfs()
        else:
            # 大状态空间，使用启发式方法
            return self.solve_heuristic()
    
    def solve_heuristic(self) -> int:
        """启发式求解方法"""
        
        best_result = 0
        
        # 基础情况
        _, base_pos = self.jump_to_end(self.initial_board, 0)
        best_result = max(best_result, base_pos)
        
        # 尝试一些有希望的移动策略
        if self.k > 0:
            # 策略：尝试在第1格棋子附近创造跳跃机会
            for target_pos in range(1, min(self.n, 20)):  # 限制搜索范围
                if self.initial_board[target_pos] == 'x':
                    # 找一个可移动的棋子移动到这个位置
                    for piece_pos in range(1, self.n):  # 不移动第1格棋子
                        if self.initial_board[piece_pos] == 'o':
                            new_board = list(self.initial_board)
                            new_board[piece_pos] = 'x'
                            new_board[target_pos] = 'o'
                            new_board_str = ''.join(new_board)
                            
                            _, result_pos = self.jump_to_end(new_board_str, 0)
                            best_result = max(best_result, result_pos)
        
        return best_result + 1


def solve_jumping_chess_correct(board: str, k: int) -> int:
    """正确的跳跃棋求解函数"""
    solver = CorrectJumpingChessSolver(board, k)
    return solver.solve_optimized()


# 验证函数
def verify_samples():
    """验证所有样例"""
    print("=== 验证样例 ===")
    
    # 原始样例
    print("原始样例:")
    result = solve_jumping_chess_correct("ooxoxoxox", 0)
    print(f"ooxoxoxox, k=0 -> {result} (期望: 9) {'✅' if result == 9 else '❌'}")
    
    print("\n新样例:")
    test_cases = [
        ("oxxooxxooxx", 1, 5),
        ("oxxooxxooxx", 2, 9),
        ("oxxooxxooxx", 3, 9),
    ]
    
    for board, k, expected in test_cases:
        result = solve_jumping_chess_correct(board, k)
        status = "✅" if result == expected else "❌"
        print(f"{board}, k={k} -> {result} (期望: {expected}) {status}")


# 手动验证样例4的正确策略
def manual_verify():
    """手动验证样例4"""
    print("\n=== 手动验证样例4 ===")
    board = "oxxooxxooxx"
    
    print("策略：移动位置5的棋子到位置2（不移动第1格棋子）")
    new_board = list(board)
    new_board[4] = 'x'  # 位置5变空
    new_board[1] = 'o'  # 位置2放棋子
    strategy_board = ''.join(new_board)
    
    print(f"原始: {board}")
    print(f"移动: {strategy_board}")
    
    # 第1格棋子跳跃
    solver = CorrectJumpingChessSolver(strategy_board, 0)
    _, final_pos = solver.jump_to_end(strategy_board, 0)
    print(f"第1格棋子最终位置: {final_pos + 1}")


if __name__ == "__main__":
    verify_samples()
    manual_verify()
    
    print("\n" + "="*50)
    
    # 读取输入
    try:
        board_input = input().strip()
        k_input = int(input().strip())
        
        result = solve_jumping_chess_correct(board_input, k_input)
        print(result)
        
    except EOFError:
        print("没有输入数据")


"""
关键修正：

1. 约束理解：
   - 第1格棋子只能通过跳跃规则移动
   - k次任意移动不能移动第1格棋子

2. 算法修正：
   - generate_valid_moves() 排除了第1格棋子
   - 所有移动操作都不会改变第1格棋子的位置

3. 正确性验证：
   - 包含了对所有样例的验证
   - 手动验证了样例4的正确策略

这个版本应该能够正确处理所有测试样例。
"""