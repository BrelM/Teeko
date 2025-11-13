########################################################################
# 
# ai.py
#
# Implementation of the Teeko
# This file implements the game logic.
#
# Author : A group of student, FISE-INFO, UTBM
# Date : 09/2025
# Version : 1.0
# Language : Python 3.11
# 
# #######################################################################

class TeekoBoard:
    """Represents the Teeko game board and game logic"""
    
    BOARD_SIZE = 5
    EMPTY = 0
    PLAYER1 = 1
    PLAYER2 = 2
    PIECES_PER_PLAYER = 4
    
    def __init__(self):
        """Initialize the board"""
        self.board = [[self.EMPTY for _ in range(self.BOARD_SIZE)] 
                      for _ in range(self.BOARD_SIZE)]
        self.phase = "placement"  # "placement" or "movement"
        self.pieces_placed = {self.PLAYER1: 0, self.PLAYER2: 0}
        
    def is_valid_position(self, row, col):
        """Check if position is within board bounds"""
        return 0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE
    
    def is_empty(self, row, col):
        """Check if position is empty"""
        if not self.is_valid_position(row, col):
            return False
        return self.board[row][col] == self.EMPTY
    
    def place_piece(self, row, col, player):
        """Place a piece during placement phase"""
        if self.phase != "placement":
            return False, "Not in placement phase"
        
        if not self.is_valid_position(row, col):
            return False, "Position out of bounds"
        
        if not self.is_empty(row, col):
            return False, "Position already occupied"
        
        self.board[row][col] = player
        self.pieces_placed[player] += 1
        
        # Check if all pieces are placed
        if (self.pieces_placed[self.PLAYER1] == self.PIECES_PER_PLAYER and
            self.pieces_placed[self.PLAYER2] == self.PIECES_PER_PLAYER):
            self.phase = "movement"
        
        return True, "Piece placed successfully"
    
    def move_piece(self, from_row, from_col, to_row, to_col, player):
        """Move a piece during movement phase"""
        if self.phase != "movement":
            return False, "Not in movement phase"
        
        if not self.is_valid_position(from_row, from_col):
            return False, "From position out of bounds"
        
        if not self.is_valid_position(to_row, to_col):
            return False, "To position out of bounds"
        
        if self.board[from_row][from_col] != player:
            return False, "No piece of your color at from position"
        
        if not self.is_empty(to_row, to_col):
            return False, "Target position already occupied"
        
        # Check if move is adjacent (including diagonals)
        if not self._is_adjacent(from_row, from_col, to_row, to_col):
            return False, "Can only move to adjacent squares"
        
        # Perform the move
        self.board[from_row][from_col] = self.EMPTY
        self.board[to_row][to_col] = player
        
        return True, "Move successful"
    
    def _is_adjacent(self, row1, col1, row2, col2):
        """Check if two positions are adjacent"""
        return abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1 and (row1, col1) != (row2, col2)
    
    def check_winner(self):
        """Check if there's a winner"""
        # Check for player 1
        if self._has_four_in_a_row(self.PLAYER1):
            return self.PLAYER1
        
        # Check for player 2
        if self._has_four_in_a_row(self.PLAYER2):
            return self.PLAYER2
        
        return None
    
    def _has_four_in_a_row(self, player):
        """Check if player has four pieces in a row or in a square"""
        # Horizontal check
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE - 3):
                if all(self.board[row][col + i] == player for i in range(self.PIECES_PER_PLAYER)):
                    return True
        
        # Vertical check
        for col in range(self.BOARD_SIZE):
            for row in range(self.BOARD_SIZE - 3):
                if all(self.board[row + i][col] == player for i in range(self.PIECES_PER_PLAYER)):
                    return True
        
        # Diagonal check (top-left to bottom-right)
        for row in range(self.BOARD_SIZE - 3):
            for col in range(self.BOARD_SIZE - 3):
                if all(self.board[row + i][col + i] == player for i in range(self.PIECES_PER_PLAYER)):
                    return True
        
        # Diagonal check (top-right to bottom-left)
        for row in range(self.BOARD_SIZE - 3):
            for col in range(3, self.BOARD_SIZE):
                if all(self.board[row + i][col - i] == player for i in range(4)):
                    return True
        
        # Square check (2x2 squares)
        for row in range(self.BOARD_SIZE - 1):
            for col in range(self.BOARD_SIZE - 1):
                if (self.board[row][col] == player and
                    self.board[row][col + 1] == player and
                    self.board[row + 1][col] == player and
                    self.board[row + 1][col + 1] == player):
                    return True
        
        return False
    
    def get_board_state(self):
        """Return current board state"""
        return [row[:] for row in self.board]
    
    def get_phase(self):
        """Return current game phase"""
        return self.phase
    
    def get_pieces_placed(self, player):
        """Return number of pieces placed by player"""
        return self.pieces_placed[player]

    # Helper conversions for AI / Prolog integration
    def get_board_flat(self):
        """Return the board as a flat list of integers (row-major)"""
        return [self.board[r][c] for r in range(self.BOARD_SIZE) for c in range(self.BOARD_SIZE)]

    def rc_to_index(self, row, col):
        """Convert row,col to flat index (0..24)"""
        return row * self.BOARD_SIZE + col

    def index_to_rc(self, index):
        """Convert flat index to (row, col)"""
        row = index // self.BOARD_SIZE
        col = index % self.BOARD_SIZE
        return row, col
