import pygame
import config
from games.board import Board
from gui.banner import Banner
from gui.sounds import play_sound
from AI.ai_engine import AIEngine

class Game:
    def __init__(self, surface, mode, difficulty, player1_name, player2_name):
        self.surface = surface
        self.board = Board(surface)
        self.banner = Banner(surface, player1_name, player2_name)
        self.current_player = 1
        self.selected_piece = None  # pour la phase de déplacement
        self.selected_from = None # pour le shift
        self.phase_message = ""
        self.message_timer = 0
        self.status_message = ""  # For persistent status display
        self.ai_thinking = False

        self.mode = mode
        self.difficulty = difficulty

        self.engine = AIEngine(difficulty=self.difficulty, mode=self.mode)
        
        self.p1 = player1_name
        self.p2 = player2_name
        self.game_over = False
        self.winner = None
        self.last_phase = "placement"
        
        # Initial status
        self.update_status_message()
        self.show_message("Placement Phase - Place your pieces")

        if self.mode == "IAvsIA":
            pygame.time.set_timer(pygame.USEREVENT+1, 500)
    
    def update_status_message(self):
        """Update the status message based on game state"""
        if self.game_over:
            return
        
        current_name = self.p1 if self.current_player == 1 else self.p2
        phase_text = "Placement" if self.board.phase == "placement" else "Movement"
        ai_indicator = ""
        
        if self.is_ai(self.current_player):
            ai_indicator = " (AI)"
        
        self.status_message = f"{current_name}{ai_indicator} - {phase_text} Phase"

    def player_to_prolog(self, player):
        return 'n' if player == 1 else 'b'
    
    def opponent(self, player):
        return 2 if player == 1 else 1
    
    # Game mode management
    def is_ai(self, player):
        if self.mode == "PvsP":
            return False
        
        if self.mode == "PvsIA":
            return player == 2
        
        if self.mode == "IAvsIA":
            return True
        
        return False
    
    def coords_to_index(self, row, col):
        return row * 5 + col

    def handle_click(self, pos):
        if self.game_over:
            return
        
        if self.is_ai(self.current_player):
            self.show_message(f"Waiting for {self.p2}...")
            return
        
        # Get nearest point
        nearest = self.get_nearest_point(pos)
        if not nearest:
            return

        x, y = nearest

        # Convert to index
        index = self.coords_to_index(x, y)

        # Player in prolog format
        prolog_player = self.player_to_prolog(self.current_player)

        # Determine current phase
        self.board.phase = self.engine.get_phase(self.board.to_prolog_state())

        new_state = None 

        if self.board.phase == "placement":
            move = ('placement', index)

            if not self.engine.validate_move(self.board.to_prolog_state(), prolog_player, move):
                self.show_message("Invalid move!", duration=1500)
                return
            
            new_state = self.engine.apply_move(self.board.to_prolog_state(), prolog_player, move)
            if new_state:
                play_sound("pawn_move")

        else:
            # Movement phase
            if self.selected_from is None:
                state = self.board.to_prolog_state()
                # Check that the square belongs to the current player
                if state[index] != prolog_player:
                    self.show_message("Select your piece!", duration=1500)
                    return
                
                self.selected_from = index
                self.show_message("Piece selected - click destination", duration=1500)
                return
            
            else:
                self.selected_piece = index

                # Movement case
                move = ('shift', self.selected_from, self.selected_piece)

                if not self.engine.validate_move(self.board.to_prolog_state(), prolog_player, move):
                    self.show_message("Invalid move!", duration=1500)
                    self.selected_from = None 
                    return
            
                new_state = self.engine.apply_move(self.board.to_prolog_state(), prolog_player, move)
                if new_state:
                    play_sound("pawn_move")
                self.selected_from = None

        # --- Update board only if new state is valid ---
        if new_state:
            self.board.update_from_prolog_state(new_state)
            
            # Display phase change
            if self.board.phase != self.last_phase:
                phase_txt = "Movement Phase" if self.board.phase != "placement" else "Placement Phase"
                self.show_message(phase_txt, duration=2000)
                self.last_phase = self.board.phase
        else:
            self.show_message("Move error!", duration=1500)
            return

        # Check winner
        winner = self.engine.get_winner(self.board.to_prolog_state())
        if winner in ('b', 'n'):
            if winner == 'n':
                self.show_message(f"🎉 {self.p1} wins!", duration=5000)
                self.winner = self.p1
                play_sound("victory")
            else:
                self.show_message(f"🎉 {self.p2} wins!", duration=5000)
                self.winner = self.p2
                play_sound("victory")
            self.game_over = True
            return

        # Change player
        self.current_player = self.opponent(self.current_player)
        self.update_status_message()
        
        # If next player is AI
        if self.is_ai(self.current_player):
            self.ai_thinking = True
            pygame.time.set_timer(pygame.USEREVENT+1, 500)

    def ai_play(self):
        """AI turn"""
        prolog_player = self.player_to_prolog(self.current_player)
        self.ai_thinking = True
        current_name = self.p1 if self.current_player == 1 else self.p2
        self.show_message(f"{current_name} is thinking...", duration=config.AI_THINKING_DELAY)

        ai_move = self.engine.get_best_move(self.board.to_prolog_state(), prolog_player)
        if ai_move:
            new_state = self.engine.apply_move(self.board.to_prolog_state(), prolog_player, ai_move)
            
            if new_state:
                play_sound("pawn_move")
                self.board.update_from_prolog_state(new_state)
                self.board.phase = self.engine.get_phase(self.board.to_prolog_state())
                
                # Display phase change
                if self.board.phase != self.last_phase:
                    phase_txt = "Movement Phase" if self.board.phase != "placement" else "Placement Phase"
                    self.show_message(phase_txt, duration=1500)
                    self.last_phase = self.board.phase
            else:
                self.show_message("AI error!", duration=2000)
        else:
            self.show_message("No valid move found!", duration=2000)

        winner = self.engine.get_winner(self.board.to_prolog_state())
        if winner in ('b', 'n'):
            if winner == 'n':
                self.show_message(f"🎉 {self.p1} wins!", duration=5000)
                self.winner = self.p1
                play_sound("victory")
            else:
                self.show_message(f"🎉 {self.p2} wins!", duration=5000)
                self.winner = self.p2
                play_sound("victory")
            self.game_over = True
            self.ai_thinking = False
            return

        # Change player
        self.current_player = self.opponent(self.current_player)
        self.ai_thinking = False
        self.update_status_message()

        # If next player is also AI
        if self.is_ai(self.current_player):
            pygame.time.set_timer(pygame.USEREVENT+1, config.AI_ENDGAME_DELAY)

    def get_nearest_point(self, pos):
        """Get the nearest board point to a click"""
        return self.board.pixel_to_logical(pos)

    def distance(self, p1, p2):
        """Calculate distance between two points"""
        return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
    
    def show_message(self, message, duration=2000):
        """Show temporary message"""
        self.phase_message = message
        self.message_timer = pygame.time.get_ticks() + duration

    def update(self):
        """Update game state"""
        if self.phase_message and pygame.time.get_ticks() > self.message_timer:
            self.phase_message = ""

    def draw(self):
        """Draw all game elements"""
        self.board.draw()
        self.banner.draw(current_player=self.current_player, status=self.status_message)
        
        # Draw temporary message
        if self.phase_message:
            font = pygame.font.SysFont("Arial", 32, bold=True)
            text_surf = font.render(self.phase_message, True, config.WHITE)
            text_rect = text_surf.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT - 50))
            
            # Draw semi-transparent background
            bg_rect = text_rect.inflate(60, 30)
            pygame.draw.rect(self.surface, (0, 0, 0), bg_rect, border_radius=12)
            pygame.draw.rect(self.surface, (255, 200, 0), bg_rect, 3, border_radius=12)
            
            self.surface.blit(text_surf, text_rect)
        
        # Draw game over screen
        if self.game_over and self.winner:
            font_large = pygame.font.SysFont("Arial", 48, bold=True)
            winner_text = font_large.render(f"{self.winner} WINS!", True, (255, 200, 0))
            winner_rect = winner_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 50))
            
            # Semi-transparent overlay
            overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            overlay.set_alpha(100)
            overlay.fill((0, 0, 0))
            self.surface.blit(overlay, (0, 0))
            
            self.surface.blit(winner_text, winner_rect)
            
            font_small = pygame.font.SysFont("Arial", 24)
            restart_text = font_small.render("Press ESC to exit to menu or R to restart...", True, (200, 200, 200))
            restart_rect = restart_text.get_rect(center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 50))
            self.surface.blit(restart_text, restart_rect)
