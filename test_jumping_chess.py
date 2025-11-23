#!/usr/bin/env python3
"""
跳跃棋问题测试脚本
"""

from jumping_chess import solve_the_jumping_puzzle_intelligently, JumpingChessMaster

def test_example_case():
    """测试题目给出的示例"""
    print("=== 测试示例案例 ===")
    
    # 示例输入
    board = "ooxoxoxox"
    k = 0
    
    print(f"输入棋盘: {board}")
    print(f"最大操作数: {k}")
    
    result = solve_the_jumping_puzzle_intelligently(board, k)
    print(f"输出结果: {result}")
    print(f"期望结果: 9")
    
    if result == 9:
        print("✅ 测试通过！")
    else:
        print("❌ 测试失败！")
    
    print()

def test_manual_trace():
    """手动追踪一个简单的例子"""
    print("=== 手动追踪测试 ===")
    
    # 简单的测试用例
    board = "ooxxx"
    k = 1
    
    print(f"输入棋盘: {board}")
    print(f"最大操作数: {k}")
    
    # 手动分析：
    # 初始状态: ooxxx (第1格棋子在位置0)
    # 位置0有棋子，位置1有棋子，位置2为空 -> 可以跳到位置2
    # 跳跃后: xxoxx (第1格棋子现在在位置2)
    # 期望结果: 2
    
    solver = JumpingChessMaster(board, k)
    
    print("初始状态分析:")
    print(f"  第1格有棋子: {solver.has_first_piece}")
    print(f"  初始位置: {solver.initial_first_piece_pos}")
    
    # 测试跳跃功能
    possible_jumps = solver.can_jump_from_position(board, 0)
    print(f"  从位置0可以跳到: {possible_jumps}")
    
    if possible_jumps:
        new_board = solver.execute_jump_operation(board, 0, possible_jumps[0])
        print(f"  跳跃后棋盘: {new_board}")
    
    result = solve_the_jumping_puzzle_intelligently(board, k)
    print(f"最终结果: {result}")
    print(f"期望结果: 2")
    
    if result == 2:
        print("✅ 测试通过！")
    else:
        print("❌ 测试失败！")
    
    print()

def test_no_moves():
    """测试无法移动的情况"""
    print("=== 测试无法移动的情况 ===")
    
    # 第1格没有棋子
    board1 = "xoxoxoxox"
    k1 = 5
    
    print(f"测试1 - 第1格没有棋子: {board1}")
    result1 = solve_the_jumping_puzzle_intelligently(board1, k1)
    print(f"结果: {result1} (期望: 0)")
    
    # 第1格有棋子但无法跳跃
    board2 = "oxxxxxxxo"
    k2 = 5
    
    print(f"测试2 - 无法跳跃: {board2}")
    result2 = solve_the_jumping_puzzle_intelligently(board2, k2)
    print(f"结果: {result2} (期望: 0)")
    
    print()

def test_multiple_jumps():
    """测试多次跳跃"""
    print("=== 测试多次跳跃 ===")
    
    board = "ooooxxx"
    k = 2
    
    print(f"输入棋盘: {board}")
    print(f"最大操作数: {k}")
    
    # 手动分析：
    # 初始: ooooxxx (位置0)
    # 跳跃1: oxooxxx -> xxooxxx (位置2)
    # 跳跃2: xxooxxx -> xxxxoxx (位置4)
    # 期望结果: 4
    
    result = solve_the_jumping_puzzle_intelligently(board, k)
    print(f"结果: {result}")
    print(f"期望结果: 4")
    
    if result == 4:
        print("✅ 测试通过！")
    else:
        print("❌ 测试失败！")
    
    print()

if __name__ == "__main__":
    test_example_case()
    test_manual_trace()
    test_no_moves()
    test_multiple_jumps()
    
    print("=== 所有测试完成 ===")