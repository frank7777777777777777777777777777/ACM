#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跳跃棋问题解决方案
作者: 一个追求算法艺术的程序员

核心思路：
1. 第1格棋子只能通过跳跃规则移动
2. k次任意移动只能移动其他棋子
3. 通过BFS探索所有可能的移动组合
4. 为每种组合计算最优跳跃序列
"""

from collections import deque
from typing import List, Set, Tuple
import sys


class ChessJumpingSolver:
    """跳跃棋求解器"""
    
    def __init__(self, board_pattern: str, magic_moves: int):
        self.board = board_pattern
        self.n = len(board_pattern)
        self.k = magic_moves
        
        if board_pattern[0] != 'o':
            raise ValueError("第1格必须有棋子")
    
    def can_jump(self, board: str, pos: int) -> bool:
        """检查是否可以跳跃"""
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
        """执行完整跳跃序列"""
        current_board = board
        current_pos = start_pos
        
        while self.can_jump(current_board, current_pos):
            current_board, current_pos = self.execute_jump(current_board, current_pos)
        
        return current_board, current_pos
    
    def generate_moves(self, board: str) -> List[str]:
        """生成所有可能的移动（不包括第1格棋子）"""
        moves = []
        
        # 可移动的棋子（排除第1格）
        movable_pieces = [i for i in range(1, self.n) if board[i] == 'o']
        # 空位
        empty_spots = [i for i, c in enumerate(board) if c == 'x']
        
        for piece_pos in movable_pieces:
            for empty_pos in empty_spots:
                new_board = list(board)
                new_board[piece_pos] = 'x'
                new_board[empty_pos] = 'o'
                moves.append(''.join(new_board))
        
        return moves
    
    def solve_with_bfs(self) -> int:
        """使用BFS求解"""
        # 基础情况
        _, base_result = self.jump_to_end(self.board, 0)
        
        if self.k == 0:
            return base_result + 1
        
        # BFS搜索
        queue = deque([(self.board, self.k)])
        visited = set([(self.board, self.k)])
        
        max_position = base_result
        
        while queue:
            current_board, remaining_moves = queue.popleft()
            
            # 计算当前状态的跳跃结果
            _, jump_result = self.jump_to_end(current_board, 0)
            max_position = max(max_position, jump_result)
            
            # 继续探索
            if remaining_moves > 0:
                possible_moves = self.generate_moves(current_board)
                
                for new_board in possible_moves:
                    state_key = (new_board, remaining_moves - 1)
                    if state_key not in visited:
                        visited.add(state_key)
                        queue.append(state_key)
        
        return max_position + 1
    
    def solve_heuristic(self) -> int:
        """启发式求解"""
        _, base_result = self.jump_to_end(self.board, 0)
        best_result = base_result
        
        if self.k > 0:
            # 尝试一些有希望的移动
            for target_pos in range(1, min(self.n, 15)):
                if self.board[target_pos] == 'x':
                    for piece_pos in range(1, self.n):
                        if self.board[piece_pos] == 'o':
                            new_board = list(self.board)
                            new_board[piece_pos] = 'x'
                            new_board[target_pos] = 'o'
                            new_board_str = ''.join(new_board)
                            
                            _, result = self.jump_to_end(new_board_str, 0)
                            best_result = max(best_result, result)
        
        return best_result + 1
    
    def solve(self) -> int:
        """智能求解"""
        if self.k == 0:
            _, result = self.jump_to_end(self.board, 0)
            return result + 1
        
        # 估算状态空间
        movable_pieces = sum(1 for i in range(1, self.n) if self.board[i] == 'o')
        empty_spots = self.board.count('x')
        estimated_states = (movable_pieces * empty_spots) ** min(self.k, 3)
        
        if estimated_states <= 100000:
            return self.solve_with_bfs()
        else:
            return self.solve_heuristic()


def solve_jumping_chess(board: str, k: int) -> int:
    """主求解函数"""
    solver = ChessJumpingSolver(board, k)
    return solver.solve()


# 主程序
if __name__ == "__main__":
    try:
        board_input = input().strip()
        k_input = int(input().strip())
        
        result = solve_jumping_chess(board_input, k_input)
        print(result)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)