########################################################################
# 
# player.py
#
# Implementation of the Teeko
# This file contains requirements for managing players.
#
# Author : A group of student, FISE-INFO, UTBM
# Date : 09/2025
# Version : 1.0
# Language : Python 3.11
# 
# #######################################################################

class Player:
    """Represents a player in the Teeko game"""
    
    def __init__(self, name, player_id, is_ai=False):
        """
        Initialize a player
        
        Args:
            name: Player's name
            player_id: Player identifier (1 or 2)
            is_ai: Whether this is an AI player
        """
        self.name = name
        self.player_id = player_id
        self.is_ai = is_ai
        self.symbol = "●" if player_id == 1 else "○"
        self.color = "Red" if player_id == 1 else "Blue"
    
    def get_display_info(self):
        """Return formatted player information"""
        player_type = "AI" if self.is_ai else "Human"
        return f"{self.name} ({self.color}) - {player_type}"
    
    def __str__(self):
        return self.name
