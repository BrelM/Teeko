#!/usr/bin/env python3
"""
Test for the turn-switching bug fix
Tests that turns switch correctly when the last piece is placed
"""

from src.player import Player
from src.control import GameController

def test_last_piece_turn_switch():
    """Test that turns switch correctly when last piece is placed"""
    print("Testing Last Piece Turn Switch")
    print("="*60)
    
    p1 = Player("Red", 1)
    p2 = Player("Blue", 2)
    controller = GameController(p1, p2)
    
    print("\nPlacing pieces alternately (Red then Blue):")
    print("Expected: Should alternate turns correctly throughout placement\n")
    
    # Red places piece 1
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 1, "Should be Red's turn"
    controller.place_piece(0, 0)
    print(f"  Red placed at (0,0)")
    
    # Blue places piece 1
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 2, "Should be Blue's turn"
    controller.place_piece(2, 2)
    print(f"  Blue placed at (2,2)")
    
    # Red places piece 2
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 1, "Should be Red's turn"
    controller.place_piece(0, 1)
    print(f"  Red placed at (0,1)")
    
    # Blue places piece 2
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 2, "Should be Blue's turn"
    controller.place_piece(2, 3)
    print(f"  Blue placed at (2,3)")
    
    # Red places piece 3
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 1, "Should be Red's turn"
    controller.place_piece(1, 0)
    print(f"  Red placed at (1,0)")
    
    # Blue places piece 3
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 2, "Should be Blue's turn"
    controller.place_piece(3, 2)
    print(f"  Blue placed at (3,2)")
    
    # Red places piece 4 (last piece for Red, but Blue still needs one more)
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 1, "Should be Red's turn"
    controller.place_piece(1, 1)
    print(f"  Red placed at (1,1) - RED'S 4th piece (phase still placement)")
    print(f"  Board phase: {controller.board.get_phase()}")
    print(f"  Red pieces: {controller.board.get_pieces_placed(1)}")
    print(f"  Blue pieces: {controller.board.get_pieces_placed(2)}")
    
    # Blue places piece 4 (last piece for Blue - transitions to movement phase)
    print(f"Current player: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 2, "Should be Blue's turn"
    controller.place_piece(4, 4)
    print(f"  Blue placed at (4,4) - BLUE'S 4th piece (phase changes to movement)")
    print(f"  Board phase: {controller.board.get_phase()}")
    print(f"  Red pieces: {controller.board.get_pieces_placed(1)}")
    print(f"  Blue pieces: {controller.board.get_pieces_placed(2)}")
    
    # Verify turn switched correctly after phase change
    print(f"Current player after phase change: {controller.get_current_player().name}")
    assert controller.get_current_player().player_id == 1, "Should be Red's turn after placement ends"
    
    print("\n" + "="*60)
    print("✅ TEST PASSED!")
    print("   - Turns switched correctly throughout placement")
    print("   - Turn switched correctly after phase change to movement")
    print("   - No infinite turn-taking detected")
    print("="*60)

if __name__ == "__main__":
    test_last_piece_turn_switch()
