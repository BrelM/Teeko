########################################################################
# 
# main.py
#
# Implementation of the Teeko
# This file is the entry point, used to launch the game.
#
# Author : A group of student, FISE-INFO, UTBM
# Date : 09/2025
# Version : 2.0
# Language : Python 3.11
# 
# #######################################################################

import sys
from src.start import GameUI
from src.gui import launch_gui

def main():
    """Main entry point with menu"""
    print("\n" + "="*50)
    print("        TEEKO GAME LAUNCHER")
    print("="*50)
    print("\nSelect game mode:")
    print("1. GUI Mode (Pygame) - Recommended")
    print("2. Console Mode")
    print("\nEnter your choice (1 or 2): ", end="")
    
    choice = input().strip()
    
    if choice == "1":
        print("\nLaunching GUI mode...")
        player1 = input("Enter Player 1 name (default: Player 1): ").strip() or "Player 1"
        player2 = input("Enter Player 2 name (default: Player 2): ").strip() or "Player 2"
        # Ask which players should be AI
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
    elif choice == "2":
        print("\nLaunching Console mode...")
        game = GameUI()
        game.start()
    else:
        print("Invalid choice! Launching GUI mode by default...")
        launch_gui()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

