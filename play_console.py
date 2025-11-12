#!/usr/bin/env python3
"""
Console-only Teeko Game
Run this to play the game in console mode
"""

import sys
from src.start import GameUI

if __name__ == "__main__":
    try:
        game = GameUI()
        game.start()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)
