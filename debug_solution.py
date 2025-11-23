#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
调试版本 - 找出BFS算法的问题
"""

from collections import deque


def debug_sample4():
    """调试样例4"""
    board = "oxxooxxooxx"
    k = 1
    
    print(f"调试样例: {board}, k={k}")
    print("位置编号:  12345678901")
    print()
    
    # 手动生成所有可能的单次移动
    pieces = [i for i, c in enumerate(board) if c == 'o']
    empties = [i for i, c in enumerate(board) if c == 'x']
    
    print("棋子位置:", [p+1 for p in pieces])
    print("空位位置:", [e+1 for e in empties])
    print()
    
    print("所有可能的移动:")
    move_count = 0
    best_result = 0
    best_strategy = None
    
    for piece_pos in pieces:
        for empty_pos in empties:
            move_count += 1
            new_board = list(board)
            new_board[piece_pos] = 'x'
            new_board[empty_pos] = 'o'
            new_board_str = ''.join(new_board)
            
            # 计算跳跃结果
            pos = 0  # 第1格棋子位置
            current = list(new_board_str)
            
            # 如果第1格棋子被移动了，需要找到它的新位置
            if piece_pos == 0:
                pos = empty_pos
            
            # 执行跳跃
            while True:
                if (pos + 2 < len(current) and 
                    current[pos] == 'o' and 
                    current[pos + 1] == 'o' and 
                    current[pos + 2] == 'x'):
                    
                    current[pos] = 'x'
                    current[pos + 1] = 'x'
                    current[pos + 2] = 'o'
                    pos = pos + 2
                else:
                    break
            
            final_pos = pos + 1  # 转换为1-based
            
            if final_pos > best_result:
                best_result = final_pos
                best_strategy = f"移动位置{piece_pos+1}的棋子到位置{empty_pos+1}"
            
            if move_count <= 10:  # 只显示前10个移动
                print(f"  移动 {piece_pos+1}->{empty_pos+1}: {new_board_str} -> 最终位置{final_pos}")
    
    print(f"\n总共 {move_count} 种可能的移动")
    print(f"最佳结果: {best_result}")
    print(f"最佳策略: {best_strategy}")
    
    # 验证我们之前找到的策略
    print(f"\n验证策略：移动位置5到位置2")
    verify_board = list(board)
    verify_board[4] = 'x'  # 位置5
    verify_board[1] = 'o'  # 位置2
    verify_str = ''.join(verify_board)
    print(f"结果棋盘: {verify_str}")
    
    # 跳跃模拟
    pos = 0
    current = list(verify_str)
    step = 0
    print(f"步骤{step}: {''.join(current)}, 第1格棋子在位置{pos+1}")
    
    while True:
        if (pos + 2 < len(current) and 
            current[pos] == 'o' and 
            current[pos + 1] == 'o' and 
            current[pos + 2] == 'x'):
            
            current[pos] = 'x'
            current[pos + 1] = 'x'
            current[pos + 2] = 'o'
            pos = pos + 2
            step += 1
            print(f"步骤{step}: {''.join(current)}, 第1格棋子在位置{pos+1}")
        else:
            break
    
    print(f"验证结果: {pos+1}")


if __name__ == "__main__":
    debug_sample4()