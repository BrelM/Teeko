########################################################################
# 
# gui.py
#
# Implementation of the Teeko GUI using pygame
# This file handles all graphical display and user interaction.
#
# Author : A group of student, FISE-INFO, UTBM
# Date : 09/2025
# Version : 2.0
# Language : Python 3.11
# 
# #######################################################################

import os
import sys
from pathlib import Path

try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("Warning: pygame is not installed. Please install it using:")
    print("  pip install pygame")

from .control import GameController
from .player import Player

class Colors:
    """Color constants"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (200, 200, 200)
    DARK_GRAY = (50, 50, 50)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    YELLOW = (255, 255, 0)
    LIGHT_RED = (255, 100, 100)
    LIGHT_BLUE = (100, 100, 255)
    BOARD_BG = (139, 90, 43)  # Brown
    HIGHLIGHT = (255, 215, 0)  # Gold


class GameGUI:
    """Pygame-based GUI for Teeko game"""
    
    def __init__(self, player1_name="Player 1", player2_name="Player 2"):
        """Initialize the pygame GUI"""
        if not PYGAME_AVAILABLE:
            raise RuntimeError("pygame is required for GUI mode. Install it with: pip install pygame")
        
        # Initialize pygame
        pygame.init()
        
        # Game settings
        self.WINDOW_WIDTH = 1000
        self.WINDOW_HEIGHT = 700
        self.BOARD_SIZE = 5
        self.CELL_SIZE = 80
        self.PIECE_RADIUS = 30
        self.BOARD_OFFSET_X = 150
        self.BOARD_OFFSET_Y = 100
        
        # Create window
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Teeko - Board Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Load resources
        self.load_resources()
        
        # Create game controller
        from .player import Player
        p1 = Player(player1_name, 1, is_ai=False)
        p2 = Player(player2_name, 2, is_ai=False)
        self.controller = GameController(p1, p2)
        
        # Game state
        self.selected_piece = None  # (row, col) for movement phase
        self.valid_moves = []  # List of valid move destinations
        self.message = ""
        self.message_time = 0
        self.game_over = False
        
    def load_resources(self):
        """Load images, fonts, and sounds"""
        resource_path = Path(__file__).parent.parent / "resources"
        
        # Load fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.font_tiny = pygame.font.Font(None, 16)
        
        # Try to load board background
        board_path = resource_path / "images" / "board.jpg"
        if board_path.exists():
            try:
                self.board_image = pygame.image.load(str(board_path))
                self.board_image = pygame.transform.scale(self.board_image, 
                    (self.BOARD_SIZE * self.CELL_SIZE, self.BOARD_SIZE * self.CELL_SIZE))
            except:
                self.board_image = None
        else:
            self.board_image = None
        
        # Load sounds
        self.sounds = {}
        sound_files = {
            'move': 'pawn_move.mp3',
            'victory': 'victory.mp3',
            'defeat': 'defeat.mp3',
            'trumpet': 'victory_trumpet.mp3'
        }
        
        for sound_name, filename in sound_files.items():
            sound_path = resource_path / "sounds" / filename
            if sound_path.exists():
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(str(sound_path))
                    self.sounds[sound_name].set_volume(0.5)
                except:
                    self.sounds[sound_name] = None
            else:
                self.sounds[sound_name] = None
    
    def play_sound(self, sound_name):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except:
                pass
    
    def show_message(self, text, duration=3000):
        """Show a temporary message"""
        self.message = text
        self.message_time = pygame.time.get_ticks() + duration
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:  # R for reset/restart
                    self.reset_game()
    
    def handle_click(self, pos):
        """Handle mouse click"""
        if self.game_over:
            return
        
        x, y = pos
        col = (x - self.BOARD_OFFSET_X) // self.CELL_SIZE
        row = (y - self.BOARD_OFFSET_Y) // self.CELL_SIZE
        
        # Check if click is within board
        if not (0 <= row < self.BOARD_SIZE and 0 <= col < self.BOARD_SIZE):
            return
        
        phase = self.controller.board.get_phase()
        
        if phase == "placement":
            self.handle_placement_click(row, col)
        else:
            self.handle_movement_click(row, col)
    
    def handle_placement_click(self, row, col):
        """Handle click during placement phase"""
        success, message = self.controller.place_piece(row, col)
        
        if success:
            self.play_sound('move')
            self.show_message(f"✓ Piece placed!")
            
            # Check if entering movement phase
            if self.controller.board.get_phase() == "movement":
                self.show_message("All pieces placed! Movement phase begins.")
        else:
            self.show_message(f"✗ {message}", 2000)
    
    def handle_movement_click(self, row, col):
        """Handle click during movement phase"""
        current_player = self.controller.get_current_player()
        board_state = self.controller.board.get_board_state()
        
        # If clicking on own piece, select it
        if board_state[row][col] == current_player.player_id:
            self.selected_piece = (row, col)
            self.calculate_valid_moves(row, col)
            self.show_message(f"Piece selected at ({row}, {col})")
        
        # If clicking on valid destination, move piece
        elif self.selected_piece and (row, col) in self.valid_moves:
            from_row, from_col = self.selected_piece
            success, message = self.controller.move_piece(from_row, from_col, row, col)
            
            if success:
                self.play_sound('move')
                self.show_message(f"✓ Piece moved!")
                
                # Check for winner
                if self.controller.is_game_over():
                    winner = self.controller.get_winner()
                    self.game_over = True
                    self.play_sound('trumpet')
                    self.show_message(f"🎉 {winner.name} wins! Press R to restart.", 5000)
            else:
                self.show_message(f"✗ {message}", 2000)
            
            self.selected_piece = None
            self.valid_moves = []
        
        # Otherwise deselect
        else:
            self.selected_piece = None
            self.valid_moves = []
    
    def calculate_valid_moves(self, row, col):
        """Calculate valid moves for selected piece"""
        self.valid_moves = []
        board_state = self.controller.board.get_board_state()
        
        # Check all adjacent squares
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                
                new_row, new_col = row + dr, col + dc
                
                # Check if within bounds and empty
                if (0 <= new_row < self.BOARD_SIZE and 
                    0 <= new_col < self.BOARD_SIZE and
                    board_state[new_row][new_col] == 0):
                    self.valid_moves.append((new_row, new_col))
    
    def reset_game(self):
        """Reset the game"""
        from .player import Player
        p1 = Player(self.controller.player1.name, 1, is_ai=False)
        p2 = Player(self.controller.player2.name, 2, is_ai=False)
        self.controller = GameController(p1, p2)
        self.selected_piece = None
        self.valid_moves = []
        self.game_over = False
        self.show_message("Game reset!")
    
    def draw(self):
        """Draw the game"""
        # Clear screen
        self.screen.fill(Colors.DARK_GRAY)
        
        # Draw board
        self.draw_board()
        
        # Draw pieces
        self.draw_pieces()
        
        # Draw UI
        self.draw_ui()
        
        # Draw message
        self.draw_message()
        
        # Update display
        pygame.display.flip()
    
    def draw_board(self):
        """Draw the game board"""
        board_x = self.BOARD_OFFSET_X
        board_y = self.BOARD_OFFSET_Y
        board_width = self.BOARD_SIZE * self.CELL_SIZE
        board_height = self.BOARD_SIZE * self.CELL_SIZE
        
        # Draw background
        if self.board_image:
            self.screen.blit(self.board_image, (board_x, board_y))
        else:
            pygame.draw.rect(self.screen, Colors.BOARD_BG, 
                           (board_x, board_y, board_width, board_height))
        
        # Draw grid
        for row in range(self.BOARD_SIZE + 1):
            y = board_y + row * self.CELL_SIZE
            pygame.draw.line(self.screen, Colors.BLACK, 
                           (board_x, y), (board_x + board_width, y), 2)
        
        for col in range(self.BOARD_SIZE + 1):
            x = board_x + col * self.CELL_SIZE
            pygame.draw.line(self.screen, Colors.BLACK,
                           (x, board_y), (x, board_y + board_height), 2)
        
        # Draw coordinates
        for i in range(self.BOARD_SIZE):
            # Row numbers
            text = self.font_tiny.render(str(i), True, Colors.WHITE)
            self.screen.blit(text, (board_x - 30, board_y + i * self.CELL_SIZE + 30))
            
            # Column numbers
            text = self.font_tiny.render(str(i), True, Colors.WHITE)
            self.screen.blit(text, (board_x + i * self.CELL_SIZE + 30, board_y - 25))
    
    def draw_pieces(self):
        """Draw game pieces"""
        board_state = self.controller.board.get_board_state()
        
        for row in range(self.BOARD_SIZE):
            for col in range(self.BOARD_SIZE):
                if board_state[row][col] != 0:
                    x = self.BOARD_OFFSET_X + col * self.CELL_SIZE + self.CELL_SIZE // 2
                    y = self.BOARD_OFFSET_Y + row * self.CELL_SIZE + self.CELL_SIZE // 2
                    
                    # Determine color
                    player_id = board_state[row][col]
                    color = Colors.LIGHT_RED if player_id == 1 else Colors.LIGHT_BLUE
                    
                    # Draw piece
                    pygame.draw.circle(self.screen, color, (x, y), self.PIECE_RADIUS)
                    pygame.draw.circle(self.screen, Colors.BLACK, (x, y), self.PIECE_RADIUS, 3)
                    
                    # Draw highlight if selected
                    if self.selected_piece == (row, col):
                        pygame.draw.circle(self.screen, Colors.HIGHLIGHT, (x, y), 
                                         self.PIECE_RADIUS + 5, 3)
        
        # Draw valid moves
        for row, col in self.valid_moves:
            x = self.BOARD_OFFSET_X + col * self.CELL_SIZE + self.CELL_SIZE // 2
            y = self.BOARD_OFFSET_Y + row * self.CELL_SIZE + self.CELL_SIZE // 2
            pygame.draw.circle(self.screen, Colors.GREEN, (x, y), 10)
            pygame.draw.circle(self.screen, Colors.BLACK, (x, y), 10, 2)
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Draw title
        title = self.font_large.render("TEEKO", True, Colors.YELLOW)
        title_rect = title.get_rect(center=(self.WINDOW_WIDTH // 2, 30))
        self.screen.blit(title, title_rect)
        
        # Draw info panel
        info_x = self.BOARD_OFFSET_X + self.BOARD_SIZE * self.CELL_SIZE + 40
        info_y = self.BOARD_OFFSET_Y
        
        # Current player
        current_player = self.controller.get_current_player()
        player_color = Colors.LIGHT_RED if current_player.player_id == 1 else Colors.LIGHT_BLUE
        
        label = self.font_medium.render("Current Player:", True, Colors.WHITE)
        self.screen.blit(label, (info_x, info_y))
        
        player_text = self.font_medium.render(current_player.name, True, player_color)
        self.screen.blit(player_text, (info_x, info_y + 40))
        
        # Phase
        phase = self.controller.board.get_phase()
        phase_label = self.font_small.render(f"Phase: {phase.upper()}", True, Colors.WHITE)
        self.screen.blit(phase_label, (info_x, info_y + 90))
        
        # Piece counts
        p1_pieces = self.controller.board.get_pieces_placed(1)
        p2_pieces = self.controller.board.get_pieces_placed(2)
        
        if phase == "placement":
            counts = self.font_small.render(f"Pieces: {p1_pieces}/4 - {p2_pieces}/4", True, Colors.WHITE)
            self.screen.blit(counts, (info_x, info_y + 130))
        
        # Instructions
        instructions = [
            "INSTRUCTIONS:",
            "Click to place pieces",
            "in placement phase.",
            "",
            "Click piece to select,",
            "then click square to move.",
            "",
            "Press R to restart",
            "Press ESC to quit"
        ]
        
        instr_y = info_y + 200
        for i, line in enumerate(instructions):
            if line == "":
                instr_y += 10
                continue
            text = self.font_tiny.render(line, True, Colors.WHITE)
            self.screen.blit(text, (info_x, instr_y))
            instr_y += 25
    
    def draw_message(self):
        """Draw temporary message"""
        current_time = pygame.time.get_ticks()
        if current_time < self.message_time and self.message:
            text = self.font_medium.render(self.message, True, Colors.YELLOW)
            text_rect = text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT - 50))
            
            # Draw background for message
            padding = 10
            bg_rect = text_rect.inflate(padding * 2, padding * 2)
            pygame.draw.rect(self.screen, Colors.BLACK, bg_rect)
            pygame.draw.rect(self.screen, Colors.YELLOW, bg_rect, 2)
            
            self.screen.blit(text, text_rect)
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(self.fps)
        
        pygame.quit()
        sys.exit()


def launch_gui(player1_name="Player 1", player2_name="Player 2"):
    """Launch the pygame GUI"""
    if not PYGAME_AVAILABLE:
        print("\nError: pygame is not installed!")
        print("To use the GUI, please install pygame with:")
        print("  pip install pygame")
        print("\nFalling back to console mode...")
        from .start import GameUI
        game = GameUI()
        game.start()
    else:
        gui = GameGUI(player1_name, player2_name)
        gui.run()
