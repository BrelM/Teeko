#!/usr/bin/env python3
"""
Board Calibration Tool

This script helps you find the correct piece offset values and board scale
to align pieces with the board image in the GUI.

Run this script and look at where pieces should be positioned on the board.
Adjust offsets and scale as needed.

Usage:
    python calibrate_board.py
    
Then adjust these in src/gui.py GameGUI.__init__():
    self.PIECE_OFFSET_X = ...  # X offset in pixels
    self.PIECE_OFFSET_Y = ...  # Y offset in pixels
    self.BOARD_SCALE = ...     # Scale factor (1.0 = original size, 0.9 = 90%, 1.1 = 110%)
"""

import pygame
from pathlib import Path
from src.player import Player
from src.control import GameController

def main():
    pygame.init()
    
    # Game settings matching gui.py
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    BOARD_SIZE = 5
    CELL_SIZE = 80
    PIECE_RADIUS = 30
    BOARD_OFFSET_X = 150
    BOARD_OFFSET_Y = 100
    
    # Current settings (adjust these to test)
    PIECE_OFFSET_X = 0
    PIECE_OFFSET_Y = 0
    BOARD_SCALE = 1.0  # 1.0 = 100%, 0.9 = 90%, 1.1 = 110%
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Board Calibration Tool - Arrow keys adjust offset, +/- adjust scale")
    clock = pygame.time.Clock()
    
    # Load board image
    resource_path = Path('resources')
    board_path = resource_path / 'images' / 'board.jpg'
    
    board_image = None
    if board_path.exists():
        board_image = pygame.image.load(str(board_path))
    
    # Create a test game
    p1 = Player('Red', 1)
    p2 = Player('Blue', 2)
    controller = GameController(p1, p2)
    
    # Place some pieces for testing
    test_placements = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 2), (2, 3), (3, 2), (3, 3)]
    for i, (r, c) in enumerate(test_placements):
        controller.place_piece(r, c)
    
    font_small = pygame.font.Font(None, 24)
    font_tiny = pygame.font.Font(None, 16)
    font_medium = pygame.font.Font(None, 32)
    
    running = True
    adjustment_size = 1  # Pixels to adjust per keypress
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Offset adjustments
                elif event.key == pygame.K_LEFT:
                    PIECE_OFFSET_X -= adjustment_size
                elif event.key == pygame.K_RIGHT:
                    PIECE_OFFSET_X += adjustment_size
                elif event.key == pygame.K_UP:
                    PIECE_OFFSET_Y -= adjustment_size
                elif event.key == pygame.K_DOWN:
                    PIECE_OFFSET_Y += adjustment_size
                # Scale adjustments
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    BOARD_SCALE += 0.01
                elif event.key == pygame.K_MINUS:
                    BOARD_SCALE -= 0.01
                # Adjustment step size
                elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    adjustment_size = 5 if adjustment_size == 1 else 1
                # Reset
                elif event.key == pygame.K_r:
                    PIECE_OFFSET_X = 0
                    PIECE_OFFSET_Y = 0
                    BOARD_SCALE = 1.0
        
        # Clear screen
        screen.fill((50, 50, 50))
        
        # Draw board background
        board_x = BOARD_OFFSET_X
        board_y = BOARD_OFFSET_Y
        
        # Calculate scaled board size
        scaled_board_width = int(BOARD_SIZE * CELL_SIZE * BOARD_SCALE)
        scaled_board_height = int(BOARD_SIZE * CELL_SIZE * BOARD_SCALE)
        
        if board_image:
            # Scale the board image
            scaled_board = pygame.transform.scale(board_image, 
                                                 (scaled_board_width, scaled_board_height))
            screen.blit(scaled_board, (board_x, board_y))
        else:
            pygame.draw.rect(screen, (139, 90, 43), (board_x, board_y, scaled_board_width, scaled_board_height))
        
        # Draw grid (logical board - NOT scaled)
        # The grid shows the logical board layout and pieces are placed on this grid.
        logical_board_width = BOARD_SIZE * CELL_SIZE
        logical_board_height = BOARD_SIZE * CELL_SIZE

        for row in range(BOARD_SIZE + 1):
            y = board_y + row * CELL_SIZE
            pygame.draw.line(screen, (255, 100, 100), (board_x, y),
                             (board_x + logical_board_width, y), 1)

        for col in range(BOARD_SIZE + 1):
            x = board_x + col * CELL_SIZE
            pygame.draw.line(screen, (255, 100, 100), (x, board_y),
                             (x, board_y + logical_board_height), 1)

        # Draw pieces with current offset (pieces are NOT scaled)
        board_state = controller.board.get_board_state()
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if board_state[row][col] != 0:
                    x = board_x + col * CELL_SIZE + CELL_SIZE // 2 + PIECE_OFFSET_X
                    y = board_y + row * CELL_SIZE + CELL_SIZE // 2 + PIECE_OFFSET_Y

                    player_id = board_state[row][col]
                    color = (255, 100, 100) if player_id == 1 else (100, 100, 255)

                    # Pieces keep original radius (not scaled)
                    pygame.draw.circle(screen, color, (x, y), PIECE_RADIUS)
                    pygame.draw.circle(screen, (0, 0, 0), (x, y), PIECE_RADIUS, 2)
        
        # Draw instructions
        y_offset = 10
        
        # Title
        title = font_medium.render("BOARD CALIBRATION TOOL", True, (255, 255, 0))
        screen.blit(title, (BOARD_OFFSET_X + scaled_board_width + 30, y_offset))
        y_offset += 45
        
        # Current values
        values_text = [
            f"Offset: X={PIECE_OFFSET_X:+3d}, Y={PIECE_OFFSET_Y:+3d}",
            f"Scale:  {BOARD_SCALE:.2f} ({BOARD_SCALE*100:.0f}%)",
            f"Step:   {adjustment_size} pixel(s)"
        ]
        
        for text in values_text:
            surf = font_small.render(text, True, (255, 255, 0))
            screen.blit(surf, (BOARD_OFFSET_X + scaled_board_width + 30, y_offset))
            y_offset += 30
        
        y_offset += 10
        
        # Controls
        controls = [
            "OFFSET CONTROLS:",
            "  LEFT/RIGHT  → Adjust X offset",
            "  UP/DOWN     → Adjust Y offset",
            "  SHIFT       → Toggle 1px/5px steps",
            "",
            "SCALE CONTROLS:",
            "  + / =       → Increase board size",
            "  -           → Decrease board size",
            "",
            "OTHER:",
            "  R           → Reset all to defaults",
            "  ESC         → Exit & show final values",
        ]
        
        for text in controls:
            color = (200, 200, 200) if text == "" else (150, 200, 255) if text.isupper() or "→" in text else (180, 180, 180)
            surf = font_tiny.render(text, True, color)
            screen.blit(surf, (BOARD_OFFSET_X + scaled_board_width + 30, y_offset))
            y_offset += 22
        
        # Legend
        y_offset += 10
        legend_text = [
            "Legend:",
            "Red grid   = Logical board (5×5)",
            "Red circle = Piece (Player 1)",
            "Blue circle= Piece (Player 2)",
        ]
        for text in legend_text:
            surf = font_tiny.render(text, True, (200, 200, 200))
            screen.blit(surf, (BOARD_OFFSET_X + scaled_board_width + 30, y_offset))
            y_offset += 20
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print(f"\n{'='*60}")
    print(f"CALIBRATION COMPLETE")
    print(f"{'='*60}")
    print(f"\nFinal values:")
    print(f"  PIECE_OFFSET_X = {PIECE_OFFSET_X}")
    print(f"  PIECE_OFFSET_Y = {PIECE_OFFSET_Y}")
    print(f"  BOARD_SCALE    = {BOARD_SCALE:.2f}")
    print(f"\nUpdate src/gui.py in the GameGUI.__init__() method:")
    print(f"    self.PIECE_OFFSET_X = {PIECE_OFFSET_X}")
    print(f"    self.PIECE_OFFSET_Y = {PIECE_OFFSET_Y}")
    print(f"    self.BOARD_SCALE = {BOARD_SCALE:.2f}")
    print(f"\nAlso update draw_board() and draw_pieces() to use BOARD_SCALE")
    print(f"if not already done.")
    print(f"{'='*60}\n")

if __name__ == '__main__':
    main()
