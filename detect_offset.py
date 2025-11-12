#!/usr/bin/env python3
"""
Automatic Board Offset Detection

This script analyzes the board image to detect where the game squares are
and automatically calculates the correct piece offsets.
"""

import pygame
import numpy as np
from pathlib import Path

def detect_board_offset():
    """
    Analyze the board image to find the correct offset
    """
    pygame.init()
    
    resource_path = Path('resources')
    board_path = resource_path / 'images' / 'board.jpg'
    
    if not board_path.exists():
        print("Board image not found!")
        return None, None
    
    # Load the original image
    original_image = pygame.image.load(str(board_path))
    original_size = original_image.get_size()
    print(f"Original board image size: {original_size}")
    
    # Scale to match GUI size (5 cells × 80 pixels)
    CELL_SIZE = 80
    BOARD_SIZE = 5
    scaled_size = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
    scaled_image = pygame.transform.scale(original_image, scaled_size)
    print(f"Scaled board size: {scaled_size}")
    
    # Convert to numpy array for analysis
    pygame.surfarray.use_arraytype('numpy')
    image_array = pygame.surfarray.pixels3d(scaled_image)
    
    # Get dimensions
    width, height = scaled_image.get_size()
    print(f"\nAnalyzing {width}x{height} scaled image...")
    
    # The board image likely has brown/tan squares. Let's detect the grid
    # by looking for lines or edges in the image
    
    # Sample the image to find where lines/edges are
    # Convert to grayscale for analysis
    gray_array = np.mean(image_array, axis=2)
    
    # Look for significant variations (edges/lines)
    edges_x = np.abs(np.diff(gray_array.mean(axis=0)))
    edges_y = np.abs(np.diff(gray_array.mean(axis=1)))
    
    # Find peaks that represent grid lines
    threshold = np.percentile(edges_x, 90)
    grid_x = np.where(edges_x > threshold)[0]
    grid_y = np.where(edges_y > threshold)[0]
    
    print(f"\nDetected potential grid line positions:")
    print(f"X positions: {grid_x}")
    print(f"Y positions: {grid_y}")
    
    # Calculate spacing
    if len(grid_x) > 1:
        x_spacing = np.mean(np.diff(grid_x))
        print(f"X spacing: {x_spacing:.1f} pixels (expected ~80)")
    
    if len(grid_y) > 1:
        y_spacing = np.mean(np.diff(grid_y))
        print(f"Y spacing: {y_spacing:.1f} pixels (expected ~80)")
    
    # If board has padding, calculate offset
    if len(grid_x) > 0:
        first_x = grid_x[0]
        expected_first = 0  # Should start at 0
        offset_x = first_x - expected_first
        print(f"\nDetected X offset: {offset_x}")
    else:
        offset_x = 0
    
    if len(grid_y) > 0:
        first_y = grid_y[0]
        expected_first = 0  # Should start at 0
        offset_y = first_y - expected_first
        print(f"Detected Y offset: {offset_y}")
    else:
        offset_y = 0
    
    print(f"\n" + "="*50)
    print(f"Recommended offset values:")
    print(f"  PIECE_OFFSET_X = {int(offset_x)}")
    print(f"  PIECE_OFFSET_Y = {int(offset_y)}")
    print(f"="*50)
    
    return int(offset_x), int(offset_y)

if __name__ == '__main__':
    try:
        offset_x, offset_y = detect_board_offset()
        if offset_x is not None:
            print(f"\nUpdate src/gui.py with:")
            print(f"    self.PIECE_OFFSET_X = {offset_x}")
            print(f"    self.PIECE_OFFSET_Y = {offset_y}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
