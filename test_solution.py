#!/usr/bin/env python3
"""
测试跳跃棋解决方案
"""

from solution import solve_jumping_chess_problem, JumpingChessOptimizer

def test_basic_cases():
    """测试基础案例"""
    print("=== 基础测试案例 ===")
    
    test_cases = [
        ("ooxoxoxox", 0, 9),  # 示例案例
        ("oox", 0, 3),        # 一次跳跃：o跳过o到x
        ("ooox", 0, 1),       # 无法跳跃：位置2不是空的
        ("oooox", 0, 1),      # 无法跳跃：位置2不是空的
        ("ooxox", 0, 5),      # 两次跳跃：o跳过o到x，再跳过o到x
        ("ooxoox", 0, 3),     # 一次跳跃后停止：o跳过o到x，然后无法继续
        ("oxoxox", 0, 1),     # 无法跳跃
        ("oxxxxxxx", 0, 1),   # 无法跳跃
    ]
    
    for board, k, expected in test_cases:
        result = solve_jumping_chess_problem(board, k)
        status = "✅" if result == expected else "❌"
        print(f"{status} {board}, k={k} -> {result} (期望: {expected})")

def test_with_extra_moves():
    """测试有额外移动的案例"""
    print("\n=== 额外移动测试案例 ===")
    
    # 这些案例需要手动分析期望结果
    test_cases = [
        ("oxoxoxoxo", 1),  # 可以移动一个棋子来帮助跳跃
        ("oxxxxxxx", 2),   # 需要移动棋子来创建跳跃路径
        ("ooxxx", 1),      # 简单的额外移动
    ]
    
    for board, k in test_cases:
        result = solve_jumping_chess_problem(board, k)
        print(f"📊 {board}, k={k} -> {result}")

def manual_trace_example():
    """手动追踪示例"""
    print("\n=== 手动追踪示例 ===")
    
    board = "ooxoxoxox"
    print(f"初始棋盘: {board}")
    
    optimizer = JumpingChessOptimizer(board, 0)
    
    # 手动模拟跳跃过程
    current_board = list(board)
    position = 0
    step = 0
    
    print(f"步骤 {step}: {''.join(current_board)}, 第1格棋子在位置 {position + 1}")
    
    while True:
        next_pos = position + 2
        if (next_pos < len(current_board) and 
            current_board[position] == 'o' and 
            current_board[position + 1] == 'o' and 
            current_board[next_pos] == 'x'):
            
            # 执行跳跃
            current_board[position] = 'x'
            current_board[position + 1] = 'x'
            current_board[next_pos] = 'o'
            position = next_pos
            step += 1
            
            print(f"步骤 {step}: {''.join(current_board)}, 第1格棋子在位置 {position + 1}")
        else:
            break
    
    print(f"最终位置: {position + 1}")

def test_edge_cases():
    """测试边界情况"""
    print("\n=== 边界情况测试 ===")
    
    edge_cases = [
        ("o", 0, 1),          # 最小棋盘
        ("ox", 0, 1),         # 无法跳跃
        ("oox", 0, 3),        # 一次跳跃
        ("o" + "x" * 16, 0, 1),  # 长棋盘但无法跳跃
    ]
    
    for board, k, expected in edge_cases:
        result = solve_jumping_chess_problem(board, k)
        status = "✅" if result == expected else "❌"
        print(f"{status} {board[:10]}{'...' if len(board) > 10 else ''}, k={k} -> {result} (期望: {expected})")

if __name__ == "__main__":
    test_basic_cases()
    test_with_extra_moves()
    manual_trace_example()
    test_edge_cases()
    
    print("\n=== 测试完成 ===")