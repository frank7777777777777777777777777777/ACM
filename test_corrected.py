#!/usr/bin/env python3
"""
测试修正后的算法
"""

from corrected_final_solution import solve_jumping_chess_correct


def test_all_samples():
    """测试所有样例"""
    print("=== 测试所有样例 ===")
    
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


def manual_verify_sample4():
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
    from corrected_final_solution import CorrectJumpingChessSolver
    solver = CorrectJumpingChessSolver(strategy_board, 0)
    _, final_pos = solver.jump_to_end(strategy_board, 0)
    print(f"第1格棋子最终位置: {final_pos + 1}")


if __name__ == "__main__":
    test_all_samples()
    manual_verify_sample4()