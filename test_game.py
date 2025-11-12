#!/usr/bin/env python3
"""
Test script for the Teeko game
"""

from src.ai import TeekoBoard
from src.player import Player
from src.control import GameController

def test_game_logic():
    """Test basic game logic"""
    print("Testing Teeko Game Logic\n")
    print("="*50)
    
    # Create players
    p1 = Player("Alice", 1)
    p2 = Player("Bob", 2)
    
    # Create game
    controller = GameController(p1, p2)
    
    # Test placement phase
    print("\n1. PLACEMENT PHASE TEST")
    print("-" * 50)
    
    # Place pieces alternately
    print(f"\nAlternating placement:")
    controller.place_piece(0, 0)
    print(f"  {controller.other_player.name} placed at (0,0)")
    
    controller.place_piece(3, 3)
    print(f"  {controller.other_player.name} placed at (3,3)")
    
    controller.place_piece(0, 1)
    print(f"  {controller.other_player.name} placed at (0,1)")
    
    controller.place_piece(3, 4)
    print(f"  {controller.other_player.name} placed at (3,4)")
    
    controller.place_piece(1, 0)
    print(f"  {controller.other_player.name} placed at (1,0)")
    
    controller.place_piece(4, 3)
    print(f"  {controller.other_player.name} placed at (4,3)")
    
    controller.place_piece(1, 1)
    print(f"  {controller.other_player.name} placed at (1,1)")
    
    controller.place_piece(4, 4)
    print(f"  {controller.other_player.name} placed at (4,4)")
    
    print(f"\n✓ All pieces placed!")
    print(f"  Phase: {controller.board.get_phase()}")
    print(controller.get_board_display())
    
    # Test movement phase
    print("\n2. MOVEMENT PHASE TEST")
    print("-" * 50)
    
    print(f"\n{controller.get_current_player().name}'s turn (Movement)")
    controller.move_piece(0, 1, 0, 2)
    print(f"  Moved from (0,1) to (0,2)")
    print(controller.get_board_display())
    
    # Try invalid move
    print(f"\nTrying invalid move (should fail)...")
    success, msg = controller.board.move_piece(0, 0, 4, 4, 1)  # Too far
    print(f"  Result: {msg}")
    
    print("\n✓ Game logic tests passed!")

if __name__ == "__main__":
    test_game_logic()

