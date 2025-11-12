########################################################################
# 
# control.py
#
# Implementation of the Teeko
# This file contains the controlling interface (between the game logic and the UI).
#
# Author : A group of student, FISE-INFO, UTBM
# Date : 09/2025
# Version : 1.0
# Language : Python 3.11
# 
# #######################################################################

from .ai import TeekoBoard

class GameController:
    """Controls the game flow and manages turns"""
    
    def __init__(self, player1, player2):
        """
        Initialize the game controller
        
        Args:
            player1: First player object
            player2: Second player object
        """
        self.player1 = player1
        self.player2 = player2
        self.board = TeekoBoard()
        self.current_player = player1
        self.other_player = player2
        self.game_over = False
        self.winner = None
    
    def get_current_player(self):
        """Return the current player"""
        return self.current_player
    
    def switch_turn(self):
        """Switch to the other player's turn"""
        self.current_player, self.other_player = self.other_player, self.current_player
    
    def place_piece(self, row, col):
        """
        Place a piece at the given position
        
        Returns:
            (success, message)
        """
        success, message = self.board.place_piece(row, col, self.current_player.player_id)
        
        if success:
            # Check if all pieces are placed
            if self.board.get_phase() == "movement":
                print(f"\n✓ All pieces placed! Entering movement phase.")
            
            # Check for winner
            winner = self.board.check_winner()
            if winner:
                self.game_over = True
                self.winner = self.player1 if winner == self.player1.player_id else self.player2
                return True, f"Winner: {self.winner.name}!"
            
            self.switch_turn()
        
        return success, message
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        """
        Move a piece from one position to another
        
        Returns:
            (success, message)
        """
        success, message = self.board.move_piece(
            from_row, from_col, to_row, to_col, self.current_player.player_id
        )
        
        if success:
            # Check for winner after each move
            winner = self.board.check_winner()
            if winner:
                self.game_over = True
                self.winner = self.player1 if winner == self.player1.player_id else self.player2
                return True, f"Winner: {self.winner.name}!"
            
            self.switch_turn()
        
        return success, message
    
    def get_board_display(self):
        """Return a formatted display of the board"""
        board_state = self.board.get_board_state()
        display = "\n     0   1   2   3   4\n"
        display += "   ┌───┬───┬───┬───┬───┐\n"
        
        for row in range(5):
            display += f" {row} │"
            for col in range(5):
                cell = board_state[row][col]
                if cell == 0:
                    display += "   │"
                elif cell == 1:
                    display += " ● │"
                else:
                    display += " ○ │"
            display += "\n"
            if row < 4:
                display += "   ├───┼───┼───┼───┼───┤\n"
            else:
                display += "   └───┴───┴───┴───┴───┘\n"
        
        return display
    
    def get_game_status(self):
        """Return current game status"""
        phase = self.board.get_phase()
        if phase == "placement":
            p1_placed = self.board.get_pieces_placed(self.player1.player_id)
            p2_placed = self.board.get_pieces_placed(self.player2.player_id)
            status = f"PLACEMENT PHASE - {self.player1.name}: {p1_placed}/4, {self.player2.name}: {p2_placed}/4"
        else:
            status = "MOVEMENT PHASE"
        
        return status
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.game_over
    
    def get_winner(self):
        """Return the winner if game is over"""
        return self.winner
