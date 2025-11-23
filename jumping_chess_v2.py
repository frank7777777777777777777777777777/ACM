#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跳跃棋问题求解器 - 正确理解版本
作者: 一个终于理解题意的程序员

经过重新分析，我发现题目的关键在于：
1. 第1格棋子可以按照跳跃规则移动（无限次，只要满足条件）
2. 额外还有k次"任意移动"操作：可以将任意棋子移动到任意空格
3. 目标是让第1格棋子到达最远的位置

这是一个更复杂的优化问题！
"""

from collections import deque
from typing import Dict, Tuple, List, Set
import copy


class AdvancedJumpingChessSolver:
    """
    高级跳跃棋求解器
    
    这个版本考虑了跳跃规则 + 任意移动的组合优化
    """
    
    def __init__(self, board_str: str, extra_moves: int):
        self.initial_board = board_str
        self.n = len(board_str)
        self.k = extra_moves
        
        # 检查第1格是否有棋子
        if board_str[0] != 'o':
            raise ValueError("题目保证第1格一定有棋子")
    
    def find_all_jump_sequences(self, board: str, start_pos: int) -> List[Tuple[str, int]]:
        """
        找到从给定位置开始的所有可能跳跃序列
        
        返回: [(最终棋盘状态, 第1格棋子最终位置), ...]
        """
        results = []
        max_pos = start_pos
        
        # 使用DFS找到最远的跳跃位置
        def dfs_jump(current_board: str, current_pos: int):
            nonlocal max_pos
            max_pos = max(max_pos, current_pos)
            results.append((current_board, current_pos))
            
            # 尝试继续跳跃
            if (current_pos + 2 < self.n and 
                current_board[current_pos] == 'o' and 
                current_board[current_pos + 1] == 'o' and 
                current_board[current_pos + 2] == 'x'):
                
                # 执行跳跃
                new_board = self.execute_jump(current_board, current_pos, current_pos + 2)
                dfs_jump(new_board, current_pos + 2)
        
        dfs_jump(board, start_pos)
        return results
    
    def execute_jump(self, board: str, from_pos: int, to_pos: int) -> str:
        """执行跳跃操作"""
        board_list = list(board)
        board_list[from_pos] = 'x'
        board_list[from_pos + 1] = 'x'
        board_list[to_pos] = 'o'
        return ''.join(board_list)
    
    def get_all_possible_moves(self, board: str) -> List[Tuple[str, str]]:
        """
        获取所有可能的"任意移动"操作
        
        返回: [(新棋盘状态, 操作描述), ...]
        """
        moves = []
        
        # 找到所有有棋子的位置
        piece_positions = [i for i, c in enumerate(board) if c == 'o']
        
        # 找到所有空位置
        empty_positions = [i for i, c in enumerate(board) if c == 'x']
        
        # 尝试所有可能的移动
        for from_pos in piece_positions:
            for to_pos in empty_positions:
                new_board = list(board)
                new_board[from_pos] = 'x'
                new_board[to_pos] = 'o'
                moves.append((''.join(new_board), f"move_{from_pos}_to_{to_pos}"))
        
        return moves
    
    def solve_with_state_space_search(self) -> int:
        """
        使用状态空间搜索求解
        
        状态: (棋盘, 第1格棋子位置, 剩余任意移动次数)
        """
        
        # BFS队列: (棋盘状态, 第1格棋子位置, 剩余k次移动)
        queue = deque([(self.initial_board, 0, self.k)])
        
        # 记录访问过的状态
        visited: Set[Tuple[str, int]] = set()
        visited.add((self.initial_board, self.k))
        
        # 记录最远位置
        max_position = 0
        
        while queue:
            current_board, first_piece_pos, remaining_moves = queue.popleft()
            
            # 首先，尝试所有可能的跳跃序列（不消耗k次移动）
            jump_results = self.find_all_jump_sequences(current_board, first_piece_pos)
            
            for final_board, final_pos in jump_results:
                # 更新最远位置
                max_position = max(max_position, final_pos)
                
                # 如果还有剩余移动次数，继续探索
                if remaining_moves > 0:
                    state_key = (final_board, remaining_moves)
                    if state_key not in visited:
                        visited.add(state_key)
                        
                        # 尝试所有可能的任意移动
                        possible_moves = self.get_all_possible_moves(final_board)
                        
                        for new_board, move_desc in possible_moves:
                            # 找到第1格棋子的新位置
                            new_first_pos = self.find_first_piece_position(new_board, final_pos)
                            
                            queue.append((new_board, new_first_pos, remaining_moves - 1))
        
        return max_position
    
    def find_first_piece_position(self, board: str, last_known_pos: int) -> int:
        """
        找到第1格棋子的当前位置
        
        这里需要一些启发式方法，因为任意移动可能会改变棋子位置
        """
        # 简化处理：假设第1格棋子还在last_known_pos
        # 实际实现中可能需要更复杂的追踪逻辑
        if board[last_known_pos] == 'o':
            return last_known_pos
        
        # 如果原位置没有棋子，尝试找到最可能的位置
        # 这里使用一个简化的策略：找到最右边的棋子
        for i in range(self.n - 1, -1, -1):
            if board[i] == 'o':
                return i
        
        return -1  # 不应该发生
    
    def solve_optimized(self) -> int:
        """
        优化版本：使用更智能的搜索策略
        """
        
        # 首先计算不使用任意移动时能到达的最远位置
        jump_results = self.find_all_jump_sequences(self.initial_board, 0)
        base_max = max(pos for _, pos in jump_results)
        
        # 如果k=0，直接返回基础结果
        if self.k == 0:
            return base_max
        
        # 否则，尝试使用任意移动来优化结果
        # 这里可以使用更复杂的优化策略
        return self.solve_with_state_space_search()


def solve_jumping_chess_with_extra_moves(board: str, k: int) -> int:
    """
    主求解函数
    """
    solver = AdvancedJumpingChessSolver(board, k)
    return solver.solve_optimized()


# 测试函数
def test_with_example():
    """测试示例"""
    board = "ooxoxoxox"
    k = 0
    
    print(f"输入: {board}, k={k}")
    
    # 手动计算期望结果
    print("手动跳跃序列:")
    current = board
    pos = 0
    step = 0
    
    print(f"步骤 {step}: {current}, 位置 {pos+1}")
    
    while True:
        if (pos + 2 < len(current) and 
            current[pos] == 'o' and 
            current[pos+1] == 'o' and 
            current[pos+2] == 'x'):
            
            # 执行跳跃
            board_list = list(current)
            board_list[pos] = 'x'
            board_list[pos+1] = 'x'
            board_list[pos+2] = 'o'
            current = ''.join(board_list)
            pos = pos + 2
            step += 1
            
            print(f"步骤 {step}: {current}, 位置 {pos+1}")
        else:
            break
    
    print(f"最终位置: {pos+1}")
    
    # 使用求解器
    result = solve_jumping_chess_with_extra_moves(board, k)
    print(f"求解器结果: {result}")


if __name__ == "__main__":
    test_with_example()
    
    # 读取输入并求解
    print("\n" + "="*50)
    print("请输入测试数据:")
    try:
        board_input = input().strip()
        k_input = int(input().strip())
        
        result = solve_jumping_chess_with_extra_moves(board_input, k_input)
        print(result)
    except EOFError:
        print("没有输入数据，跳过求解")