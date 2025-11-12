########################################################################
# 
# start.py
#
# Implementation of the Teeko
# This file contains requirements for starting a new game.
#
# Author : A group of student, FISE-INFO, UTBM
# Date : 09/2025
# Version : 1.0
# Language : Python 3.11
# 
# #######################################################################

from .player import Player
from .control import GameController

class GameUI:
    """Handles the user interface for the Teeko game"""
    
    def __init__(self):
        self.controller = None
    
    def print_header(self):
        """Print game header"""
        print("\n" + "="*50)
        print("        WELCOME TO TEEKO")
        print("="*50)
        print("\nTeeko is a strategy board game for 2 players.")
        print("- Place your 4 pieces on the 5x5 board")
        print("- Move your pieces to form a line of 4")
        print("- First to get 4 in a row wins!")
        print("="*50 + "\n")
    
    def setup_game(self):
        """Setup game with player configuration"""
        print("\n--- GAME SETUP ---")
        
        # Get player names
        player1_name = input("Enter Player 1 (Red) name: ").strip() or "Player 1"
        player2_name = input("Enter Player 2 (Blue) name: ").strip() or "Player 2"
        
        # Create players (both human for now)
        player1 = Player(player1_name, 1, is_ai=False)
        player2 = Player(player2_name, 2, is_ai=False)
        
        print(f"\nPlayers created:")
        print(f"  Player 1: {player1.get_display_info()}")
        print(f"  Player 2: {player2.get_display_info()}")
        
        # Create game controller
        self.controller = GameController(player1, player2)
        print("\nGame initialized!")
    
    def run_game(self):
        """Run the main game loop"""
        self.setup_game()
        
        while not self.controller.is_game_over():
            # Display board and status
            print(self.controller.get_board_display())
            print(self.controller.get_game_status())
            
            current_player = self.controller.get_current_player()
            print(f"\n{current_player.name}'s turn ({current_player.color})")
            
            phase = self.controller.board.get_phase()
            
            if phase == "placement":
                self._handle_placement()
            else:
                self._handle_movement()
        
        # Game over
        self._display_end_game()
    
    def _handle_placement(self):
        """Handle piece placement phase"""
        while True:
            try:
                position = input("Enter position to place piece (row col): ").strip()
                if position.lower() == 'quit':
                    exit()
                
                parts = position.split()
                if len(parts) != 2:
                    print("Invalid input! Enter: row col (e.g., '0 2')")
                    continue
                
                row, col = int(parts[0]), int(parts[1])
                success, message = self.controller.place_piece(row, col)
                
                if success:
                    print(f"✓ {message}")
                    break
                else:
                    print(f"✗ {message}")
            
            except ValueError:
                print("Invalid input! Enter: row col (e.g., '0 2')")
            except KeyboardInterrupt:
                exit()
    
    def _handle_movement(self):
        """Handle piece movement phase"""
        while True:
            try:
                move = input("Enter move (from_row from_col to_row to_col): ").strip()
                if move.lower() == 'quit':
                    exit()
                
                parts = move.split()
                if len(parts) != 4:
                    print("Invalid input! Enter: from_row from_col to_row to_col (e.g., '0 0 0 1')")
                    continue
                
                from_row, from_col, to_row, to_col = map(int, parts)
                success, message = self.controller.move_piece(from_row, from_col, to_row, to_col)
                
                if success:
                    print(f"✓ {message}")
                    break
                else:
                    print(f"✗ {message}")
            
            except ValueError:
                print("Invalid input! Enter: from_row from_col to_row to_col (e.g., '0 0 0 1')")
            except KeyboardInterrupt:
                exit()
    
    def _display_end_game(self):
        """Display end game screen"""
        print("\n" + "="*50)
        print("                GAME OVER!")
        print("="*50)
        
        winner = self.controller.get_winner()
        if winner:
            print(f"\n🎉 Congratulations! {winner.name} ({winner.color}) wins! 🎉")
        
        print(self.controller.get_board_display())
        print("="*50 + "\n")
    
    def start(self):
        """Start the game"""
        self.print_header()
        self.run_game()
