#!/usr/bin/env python3
"""
Detailed Board Analysis - Visual inspection

This creates a test image showing the actual grid vs the image content
"""

import pygame
from pathlib import Path
import numpy as np

def analyze_board_visually():
    """
    Create a detailed analysis by comparing expected grid with image
    """
    pygame.init()
    
    resource_path = Path('resources')
    board_path = resource_path / 'images' / 'board.jpg'
    
    if not board_path.exists():
        print("Board image not found!")
        return
    
    # Load the image
    original_image = pygame.image.load(str(board_path))
    print(f"Original image size: {original_image.get_size()}")
    
    # Calculate scale factor
    original_w, original_h = original_image.get_size()
    cell_size = 80
    board_size = 5
    expected_w = board_size * cell_size
    expected_h = board_size * cell_size
    
    scale_x = original_w / expected_w
    scale_y = original_h / expected_h
    
    print(f"\nScale factors: {scale_x:.2f}x (width), {scale_y:.2f}x (height)")
    print(f"Expected board size: {expected_w}x{expected_h}")
    
    # The key insight: if the original image is 557x554 and needs to become 400x400,
    # the scaling will distort proportionally
    
    # Convert to numpy for analysis
    pygame.surfarray.use_arraytype('numpy')
    
    # Create a surface from the image and analyze it
    scaled = pygame.transform.scale(original_image, (expected_w, expected_h))
    
    # Sample at key positions - the center of where game squares should be
    centers = []
    for row in range(board_size):
        for col in range(board_size):
            x = col * cell_size + cell_size // 2
            y = row * cell_size + cell_size // 2
            centers.append((x, y, row, col))
    
    # For a more detailed analysis, let's look at the pixel colors
    pixel_array = pygame.surfarray.array3d(scaled)
    
    # Check if pieces placed on squares would align
    print("\n" + "="*60)
    print("Sample squares - checking color uniformity:")
    print("="*60)
    
    for row in range(min(2, board_size)):  # Check first 2 rows
        for col in range(min(2, board_size)):  # Check first 2 cols
            x_center = col * cell_size + cell_size // 2
            y_center = row * cell_size + cell_size // 2
            
            # Sample colors at this position and nearby
            samples = []
            for dx in [-10, -5, 0, 5, 10]:
                for dy in [-10, -5, 0, 5, 10]:
                    px = min(max(x_center + dx, 0), expected_w - 1)
                    py = min(max(y_center + dy, 0), expected_h - 1)
                    color = pixel_array[px, py]
                    samples.append(np.mean(color))
            
            avg_brightness = np.mean(samples)
            brightness_variance = np.std(samples)
            
            print(f"Square [{row},{col}] at ({x_center},{y_center}): "
                  f"brightness={avg_brightness:.0f}, variance={brightness_variance:.0f}")
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("\nThe board image appears to be:")
    print(f"  - {original_w} pixels wide (scales to {expected_w})")
    print(f"  - {original_h} pixels tall (scales to {expected_h})")
    print("\nIf pieces don't align with squares:")
    print("1. Run 'python calibrate_board.py' for manual adjustment")
    print("2. Or check if the board image needs re-centering")

if __name__ == '__main__':
    try:
        analyze_board_visually()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
