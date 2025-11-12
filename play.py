#!/usr/bin/env python3
"""
Interactive Teeko Game Demo
Run this to play the game with another physical player
"""

from src.start import GameUI

if __name__ == "__main__":
    game = GameUI()
    game.start()
