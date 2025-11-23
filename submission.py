#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
跳跃棋问题 - 重新实现版本
更加谨慎地处理所有边界情况
"""

from collections import deque
import sys


def can_jump(board, pos):
    """检查位置pos的棋子是否可以跳跃"""
    n = len(board)
    return (pos + 2 < n and 
            board[pos] == 'o' and 
            board[pos + 1] == 'o' and 
            board[pos + 2] == 'x')


def do_jump(board, pos):
    """执行跳跃，返回新棋盘和新位置"""
    new_board = list(board)
    new_board[pos] = 'x'      # 原位置变空
    new_board[pos + 1] = 'x'  # 被跳过的位置变空
    new_board[pos + 2] = 'o'  # 目标位置有棋子
    return ''.join(new_board), pos + 2


def jump_sequence(board, start_pos):
    """执行完整的跳跃序列"""
    current_board = board
    current_pos = start_pos
    
    while can_jump(current_board, current_pos):
        current_board, current_pos = do_jump(current_board, current_pos)
    
    return current_board, current_pos


def generate_all_moves(board):
    """生成所有可能的移动（不包括位置0的棋子）"""
    n = len(board)
    moves = []
    
    # 找到所有可移动的棋子（除了位置0）
    pieces = [i for i in range(1, n) if board[i] == 'o']
    # 找到所有空位
    empties = [i for i in range(n) if board[i] == 'x']
    
    for piece_pos in pieces:
        for empty_pos in empties:
            new_board = list(board)
            new_board[piece_pos] = 'x'
            new_board[empty_pos] = 'o'
            moves.append(''.join(new_board))
    
    return moves


def solve_bfs(board, k):
    """使用BFS求解"""
    # 计算初始状态的结果
    _, initial_result = jump_sequence(board, 0)
    
    if k == 0:
        return initial_result + 1
    
    # BFS搜索所有可能的状态
    queue = deque([(board, k)])
    visited = set([(board, k)])
    
    max_position = initial_result
    
    while queue:
        current_board, remaining_k = queue.popleft()
        
        # 计算当前状态的跳跃结果
        _, pos = jump_sequence(current_board, 0)
        max_position = max(max_position, pos)
        
        # 如果还有移动次数，继续探索
        if remaining_k > 0:
            possible_moves = generate_all_moves(current_board)
            
            for new_board in possible_moves:
                state = (new_board, remaining_k - 1)
                if state not in visited:
                    visited.add(state)
                    queue.append(state)
    
    return max_position + 1


def solve_limited_bfs(board, k, max_depth=2):
    """有限深度BFS"""
    _, initial_result = jump_sequence(board, 0)
    
    if k == 0:
        return initial_result + 1
    
    queue = deque([(board, min(k, max_depth))])
    visited = set([(board, min(k, max_depth))])
    
    max_position = initial_result
    
    while queue:
        current_board, remaining_k = queue.popleft()
        
        _, pos = jump_sequence(current_board, 0)
        max_position = max(max_position, pos)
        
        if remaining_k > 0:
            possible_moves = generate_all_moves(current_board)
            
            for new_board in possible_moves:
                state = (new_board, remaining_k - 1)
                if state not in visited:
                    visited.add(state)
                    queue.append(state)
    
    return max_position + 1


def solve(board, k):
    """主求解函数"""
    n = len(board)
    
    if board[0] != 'o':
        raise ValueError("第1格必须有棋子")
    
    # 对于小规模问题，使用完整BFS
    if k <= 2 or n <= 10:
        return solve_bfs(board, k)
    
    # 估算状态空间大小
    pieces = sum(1 for i in range(1, n) if board[i] == 'o')
    empties = board.count('x')
    estimated_states = (pieces * empties) ** min(k, 2)
    
    if estimated_states <= 50000:
        return solve_bfs(board, k)
    else:
        return solve_limited_bfs(board, k, max_depth=2)


def main():
    """主函数"""
    try:
        board = input().strip()
        k = int(input().strip())
        
        result = solve(board, k)
        print(result)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()