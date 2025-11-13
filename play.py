#!/usr/bin/env python3
"""
Interactive Teeko Game - GUI Version
Run this to play the game with a graphical interface
"""

from src.gui import launch_gui

if __name__ == "__main__":
    # Optional: Get player names
    print("Welcome to Teeko!")
    print("-" * 40)
    player1 = input("Enter Player 1 name (default: Red Player): ").strip() or "Red Player"
    player2 = input("Enter Player 2 name (default: Blue Player): ").strip() or "Blue Player"
    print("Which player(s) should be AI? Enter 0 (none), 1 (Player1), 2 (Player2), 3 (both). [default: 0]: ", end="")
    ai_choice = input().strip() or '0'
    if ai_choice not in ['0','1','2','3']:
        ai_choice = '0'
    ai_p1 = ai_choice in ['1','3']
    ai_p2 = ai_choice in ['2','3']
    
    # If any AI players, ask for depth and timeout
    ai_depth = 3
    ai_timeout = 2.0
    if ai_p1 or ai_p2:
        print("AI search depth (default 3, range 1-6): ", end="")
        depth_str = input().strip() or '3'
        try:
            ai_depth = int(depth_str)
            ai_depth = max(1, min(ai_depth, 6))
        except ValueError:
            ai_depth = 3
        
        print("AI per-move timeout in seconds (default 2.0): ", end="")
        timeout_str = input().strip() or '2.0'
        try:
            ai_timeout = float(timeout_str)
            ai_timeout = max(0.5, min(ai_timeout, 10.0))
        except ValueError:
            ai_timeout = 2.0
    
    launch_gui(player1, player2, ai_player1=ai_p1, ai_player2=ai_p2, ai_depth=ai_depth, ai_timeout=ai_timeout)
