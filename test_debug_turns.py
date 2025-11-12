#!/usr/bin/env python3
"""
Debug version to trace the turn-switching issue
"""

from src.player import Player
from src.control import GameController

p1 = Player("Red", 1)
p2 = Player("Blue", 2)
controller = GameController(p1, p2)

print("Placing Red's 4 pieces:")
for i in range(4):
    print(f"\n--- Before placement {i+1} ---")
    print(f"Current player: {controller.get_current_player().name} (ID: {controller.get_current_player().player_id})")
    
    controller.place_piece(0, i)
    
    print(f"After placement - Current player: {controller.get_current_player().name} (ID: {controller.get_current_player().player_id})")
    print(f"Red pieces: {controller.board.get_pieces_placed(1)}, Blue pieces: {controller.board.get_pieces_placed(2)}")
    print(f"Phase: {controller.board.get_phase()}")

print("\n\nPlacing Blue's 4 pieces:")
for i in range(4):
    print(f"\n--- Before placement {i+1} ---")
    print(f"Current player: {controller.get_current_player().name} (ID: {controller.get_current_player().player_id})")
    
    controller.place_piece(2, i)
    
    print(f"After placement - Current player: {controller.get_current_player().name} (ID: {controller.get_current_player().player_id})")
    print(f"Red pieces: {controller.board.get_pieces_placed(1)}, Blue pieces: {controller.board.get_pieces_placed(2)}")
    print(f"Phase: {controller.board.get_phase()}")
