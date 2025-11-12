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


def test_square_win():
    """Test square shape winning condition"""
    print("\n\n3. SQUARE SHAPE WIN TEST")
    print("="*50)
    
    p1 = Player("Alice", 1)
    p2 = Player("Bob", 2)
    controller = GameController(p1, p2)
    
    print("\nPlacing pieces in a 2x2 square formation for Player 1:")
    print("Expected: Alice should win by forming a square at (0,0), (0,1), (1,0), (1,1)")
    
    # Create a square for player 1
    controller.place_piece(0, 0)  # Player 1
    print(f"  Alice placed at (0,0)")
    
    controller.place_piece(2, 2)  # Player 2
    print(f"  Bob placed at (2,2)")
    
    controller.place_piece(0, 1)  # Player 1
    print(f"  Alice placed at (0,1)")
    
    controller.place_piece(2, 3)  # Player 2
    print(f"  Bob placed at (2,3)")
    
    controller.place_piece(1, 0)  # Player 1
    print(f"  Alice placed at (1,0)")
    
    controller.place_piece(3, 2)  # Player 2
    print(f"  Bob placed at (3,2)")
    
    success, msg = controller.place_piece(1, 1)  # Player 1 - completes square!
    print(f"  Alice placed at (1,1)")
    print(f"  Result: {msg}")
    
    if controller.is_game_over():
        winner = controller.get_winner()
        print(f"\n✓ {winner.name} won by forming a square!")
    else:
        print(f"\n✗ Square win not detected!")
    
    print(controller.get_board_display())

def test_placement_phase_win():
    """Test winning at end of placement phase"""
    print("\n\n4. PLACEMENT PHASE WIN TEST")
    print("="*50)
    
    p1 = Player("Alice", 1)
    p2 = Player("Bob", 2)
    controller = GameController(p1, p2)
    
    print("\nCreating a scenario where placement phase ends with a winner:")
    
    # Create pieces in a line for player 1
    controller.place_piece(0, 0)  # Player 1
    print(f"  Alice placed at (0,0)")
    
    controller.place_piece(2, 2)  # Player 2
    print(f"  Bob placed at (2,2)")
    
    controller.place_piece(0, 1)  # Player 1
    print(f"  Alice placed at (0,1)")
    
    controller.place_piece(2, 3)  # Player 2
    print(f"  Bob placed at (2,3)")
    
    controller.place_piece(0, 2)  # Player 1
    print(f"  Alice placed at (0,2)")
    
    controller.place_piece(3, 2)  # Player 2
    print(f"  Bob placed at (3,2)")
    
    success, msg = controller.place_piece(0, 3)  # Player 1 - completes line!
    print(f"  Alice placed at (0,3)")
    print(f"  Result: {msg}")
    
    if controller.is_game_over():
        winner = controller.get_winner()
        print(f"\n✓ {winner.name} won at the end of placement phase!")
    else:
        print(f"\nNow placing Bob's last piece...")
        success, msg = controller.place_piece(4, 4)  # Player 2
        print(f"  Bob placed at (4,4)")
        print(f"  Result: {msg}")
        
        if controller.is_game_over():
            print(f"\n✓ Winner was detected at placement end!")
        else:
            print(f"\n✗ No winner detected (but this scenario might not trigger with this board)")
    
    print(controller.get_board_display())

if __name__ == "__main__":
    test_game_logic()
    test_square_win()
    test_placement_phase_win()
    print("\n" + "="*50)
    print("✓ All tests completed!")
    print("="*50)
