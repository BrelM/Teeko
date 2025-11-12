#!/usr/bin/env python3
"""
GUI Controls and Features Guide for Teeko

This file documents all the features and controls available in the GUI version.
"""

FEATURES = """
================================================================================
                        TEEKO GUI - FEATURES GUIDE
================================================================================

GAME DISPLAY
============
The GUI displays:
  • 5×5 Game board with grid lines
  • Red pieces (●) for Player 1
  • Blue pieces (○) for Player 2
  • Current player information
  • Game phase (Placement or Movement)
  • Piece count during placement
  • Instructions panel
  • Real-time messages

GAMEPLAY MODES
==============

1. PLACEMENT PHASE
   - Players alternate clicking on empty squares
   - Each player places 4 pieces
   - Phase automatically switches to Movement when all pieces are placed
   - Click directly on any empty square to place a piece

2. MOVEMENT PHASE
   - Select a piece by clicking on it (highlights with gold border)
   - Valid moves are shown as green dots
   - Click a green dot to move the piece
   - Pieces can move to any adjacent square (8 directions)
   - First player to get 4 in a row wins!

MOUSE CONTROLS
==============
Left Click        - Place piece (placement phase) or move piece (movement phase)
Left Click        - Select piece (shows valid moves with green dots)
Left Click        - Move to highlighted destination

KEYBOARD CONTROLS
=================
R                 - Restart game / Start new game
ESC               - Quit game
(Click to restart when game is over)

VISUAL FEEDBACK
===============
Gold Border       - Selected piece (movement phase)
Green Dots        - Valid move destinations
Yellow Message    - Game status and feedback
Highlighted Player - Current player's color in info panel

SOUND EFFECTS
=============
Pawn Move Sound   - Plays when a piece is moved
Victory Trumpet   - Plays when a player wins
Optional Defeat Sound - For future use

GAME INFORMATION PANEL
======================
Shows:
  • Current player name and color
  • Game phase (PLACEMENT or MOVEMENT)
  • Number of pieces placed (placement phase only)
  • Gameplay instructions

MESSAGES
========
Game displays temporary messages for:
  ✓ Successful moves
  ✗ Invalid move attempts with reasons
  Game phase transitions
  Victory announcements

WINNING CONDITIONS
==================
Get 4 pieces in a row:
  • Horizontally
  • Vertically
  • Diagonally (both directions)

First player to achieve this wins!

BOARD COORDINATES
=================
Rows:    0 1 2 3 4 (top to bottom)
Columns: 0 1 2 3 4 (left to right)

The board includes coordinate labels for reference.

TIPS FOR BETTER GAMEPLAY
========================
1. During placement, spread pieces to control different areas
2. Try to create multiple winning possibilities
3. Block opponent's potential winning lines
4. In movement phase, plan ahead for piece combinations
5. Watch the opponent's piece positions for threats
6. Use the entire board - don't concentrate pieces in one area

TROUBLESHOOTING
===============
If the game doesn't respond to clicks:
  - Make sure you've placed your pieces in placement phase
  - In movement phase, make sure you select YOUR pieces (your color)
  - Click within the board boundaries
  - Check that target square is empty (not occupied)

If sounds don't play:
  - Make sure pygame audio is initialized
  - Check speaker/audio is not muted
  - Sound files should be in resources/sounds/

If board image doesn't appear:
  - Check that board.jpg exists in resources/images/
  - The game will use a colored background if image is missing

================================================================================
"""

KEYBOARD_SUMMARY = """
╔════════════════════════════════════════╗
║         KEYBOARD SHORTCUTS             ║
╠════════════════════════════════════════╣
║  R  - Restart/New Game                 ║
║  ESC - Quit                            ║
║ MOUSE - Click to place/move pieces     ║
╚════════════════════════════════════════╝
"""

if __name__ == "__main__":
    print(FEATURES)
    print(KEYBOARD_SUMMARY)
    
    # Display HTML version instruction
    with open("GUI_GUIDE.txt", "w", encoding="utf-8") as f:
        f.write(FEATURES)
        f.write("\n\n")
        f.write(KEYBOARD_SUMMARY)
    
    print("\nGuide saved to GUI_GUIDE.txt")
