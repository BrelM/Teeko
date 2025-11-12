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
    
    launch_gui(player1, player2)
