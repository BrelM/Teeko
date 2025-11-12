########################################################################
# 
# main.py
#
# Implementation of the Teeko
# This file is the entry point, used to launch the game.
#
# Author : A group of student, FISE-INFO, UTBM
# Date : 09/2025
# Version : 1.0
# Language : Python 3.11
# 
# #######################################################################

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

