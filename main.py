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
        launch_gui(player1, player2)
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

