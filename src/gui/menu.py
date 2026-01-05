import pygame
import src.gui.config as config

class MenuButton:
    """Reusable button class for menu items"""
    def __init__(self, x, y, width, height, text, font, callback=None, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.callback = callback
        self.hovered = False
        self.active = False
        self.text_color = config.BUTTON_TEXT_COLOR
        self.color = color if color else config.BUTTON_NORMAL
        self.hover_color = config.BUTTON_HOVER
        self.active_color = config.BUTTON_ACTIVE
    
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        # Draw button with color based on state
        if self.active:
            color = self.active_color
            self.text_color = config.BUTTON_NORMAL
        elif self.hovered:
            color = self.hover_color
        else:
            self.text_color = config.BUTTON_TEXT_COLOR
            color = self.color
        
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, config.BUTTON_BORDER, self.rect, 2, border_radius=10)
        
        # Draw text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.font_title = pygame.font.Font(None, 72)
        self.font_section = pygame.font.Font(None, 44)
        self.font_text = pygame.font.Font(None, 38)
        self.font_small = pygame.font.Font(None, 32)
        self.font_tiny = pygame.font.Font(None, 26)

        # Image de fond
        board_path = config.RESOURCE_PATH / "images" / "board.jpg"
        if board_path.exists():
            self.background = pygame.image.load(str(board_path)).convert()
        else:
            self.background = None

        # Current menu state
        self.current_screen = "mode"  # "mode", "difficulty", "names", "confirm"
        
        # Données du menu
        self.modes = ["PvsP", "PvsIA", "IAvsIA"]
        self.mode_index = 0
        self.mode = self.modes[self.mode_index]

        self.difficulties = ["Easy", "Medium", "Hard"]
        self.difficulty_map = {
            "Easy": "Débutant",
            "Medium": "Intermédiaire", 
            "Hard": "Expert"
        }
        self.diff_index = 1  # Default to Medium
        self.difficulty = self.difficulty_map[self.difficulties[self.diff_index]]

        self.player1_name = ""
        self.player2_name = ""
        self.active_input = None
        self.cursor_visible = True
        self.cursor_timer = pygame.time.get_ticks()

        # Create buttons for mode selection
        self.mode_buttons = [
            MenuButton(config.WINDOW_WIDTH//2 - config.BUTTON_WIDTH_LARGE - config.BUTTON_SPACING - config.BUTTON_WIDTH_SMALL//2, 300, config.BUTTON_WIDTH_LARGE, config.BUTTON_HEIGHT, "Player vs Player", self.font_text),
            MenuButton(config.WINDOW_WIDTH//2 - config.BUTTON_WIDTH_SMALL//2, 300, config.BUTTON_WIDTH_SMALL, config.BUTTON_HEIGHT, "Player vs AI", self.font_text),
            MenuButton(config.WINDOW_WIDTH//2 + config.BUTTON_WIDTH_SMALL//2 + config.BUTTON_SPACING, 300, config.BUTTON_WIDTH_SMALL, config.BUTTON_HEIGHT, "AI vs AI", self.font_text)
        ]
        
        # Create buttons for difficulty selection
        self.difficulty_buttons = [
            MenuButton(config.WINDOW_WIDTH//2 - config.BUTTON_WIDTH_SMALL - config.BUTTON_SPACING - config.BUTTON_WIDTH_SMALL//2, 300, config.BUTTON_WIDTH_SMALL, config.BUTTON_HEIGHT, "EASY", self.font_section),
            MenuButton(config.WINDOW_WIDTH//2 - config.BUTTON_WIDTH_SMALL//2, 300, config.BUTTON_WIDTH_SMALL, config.BUTTON_HEIGHT, "MEDIUM", self.font_section),
            MenuButton(config.WINDOW_WIDTH//2 + config.BUTTON_WIDTH_SMALL//2 + config.BUTTON_SPACING, 300, config.BUTTON_WIDTH_SMALL, config.BUTTON_HEIGHT, "HARD", self.font_section)
        ]
        
        # Interactive rectangles for text input
        self.input_player1 = pygame.Rect(config.WINDOW_WIDTH//2 - 150, 300, 300, 50)
        self.input_player2 = pygame.Rect(config.WINDOW_WIDTH//2 - 150, 380, 300, 50)
        
        # Start button
        self.start_button = pygame.Rect(config.WINDOW_WIDTH//2 - config.BUTTON_WIDTH_LARGE//2, 600, config.BUTTON_WIDTH_LARGE, config.BUTTON_HEIGHT)
        self.back_button = pygame.Rect(50, 600, config.BUTTON_WIDTH_SMALLV2, config.BUTTON_HEIGHT)
        # Exit button (top-right)
        self.exit_button = pygame.Rect(config.WINDOW_WIDTH - config.BUTTON_WIDTH_SMALLV2 - config.BUTTON_SPACING_SMALL, 20, config.BUTTON_WIDTH_SMALLV2, config.BUTTON_HEIGHT)

    def handle_event(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        # Update button hover states
        if self.current_screen == "mode":
            for i, btn in enumerate(self.mode_buttons):
                btn.update(mouse_pos)
                btn.active = (i == self.mode_index)
        elif self.current_screen == "difficulty":
            for i, btn in enumerate(self.difficulty_buttons):
                btn.update(mouse_pos)
                btn.active = (i == self.diff_index)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Exit button
            if self.exit_button.collidepoint(event.pos):
                return {"exit": True}
            # Back button
            if self.back_button.collidepoint(event.pos):
                if self.current_screen != "difficulty":
                    if self.mode_index != 0:
                        self.current_screen = "difficulty"
                        self.player1_name = ""
                        self.player2_name = ""
                    else:
                        self.current_screen = "mode"
                else:
                    self.current_screen = "mode"
                    
                return None
            
            # Mode selection screen
            if self.current_screen == "mode":
                for i, btn in enumerate(self.mode_buttons):
                    if btn.rect.collidepoint(event.pos):
                        self.mode_index = i
                        self.mode = self.modes[i]
                        self.current_screen = "difficulty" if i != 0 else "names"
                        self.diff_index = 1  # Reset to medium
                        return None
            
            # Difficulty selection screen
            elif self.current_screen == "difficulty":
                for i, btn in enumerate(self.difficulty_buttons):
                    if btn.rect.collidepoint(event.pos):
                        self.diff_index = i
                        self.difficulty = self.difficulty_map[self.difficulties[i]]
                        self.current_screen = "names"
                        self.player1_name = ""
                        self.player2_name = ""
                        return None
            
            # Names/Confirmation screen
            elif self.current_screen == "names":
                if self.start_button.collidepoint(event.pos):
                    # Return game parameters
                    p1_name = self.player1_name or "Player 1"
                    p2_name = self.player2_name or "Player 2"
                    
                    # Adjust names based on mode
                    if self.mode == "PvsIA":
                        p2_name = "AI"
                    elif self.mode == "IAvsIA":
                        p1_name = "AI 1"
                        p2_name = "AI 2"
                    
                    return {
                        "mode": self.mode,
                        "difficulty": self.difficulty,
                        "player1_name": p1_name,
                        "player2_name": p2_name
                    }
                
                # Text input fields (only for human players)
                if self.mode == "PvsP":
                    if self.input_player1.collidepoint(event.pos):
                        self.active_input = "p1"
                    elif self.input_player2.collidepoint(event.pos):
                        self.active_input = "p2"
                    else:
                        self.active_input = None
                elif self.mode == "PvsIA":
                    if self.input_player1.collidepoint(event.pos):
                        self.active_input = "p1"
                    else:
                        self.active_input = None
                else:
                    # IAvsIA: no inputs required
                    self.active_input = None
        
        elif event.type == pygame.KEYDOWN:
            if self.active_input and self.current_screen == "names":
                if event.key == pygame.K_BACKSPACE:
                    if self.active_input == "p1":
                        self.player1_name = self.player1_name[:-1]
                    elif self.active_input == "p2":
                        self.player2_name = self.player2_name[:-1]
                else:
                    char = event.unicode
                    if char.isprintable():
                        if self.active_input == "p1" and len(self.player1_name) < 15:
                            self.player1_name += char
                        elif self.active_input == "p2" and len(self.player2_name) < 15:
                            self.player2_name += char
        
        return None

    def update_cursor(self):
        now = pygame.time.get_ticks()
        if now - self.cursor_timer > 500:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = now
    
    def draw_background(self):
        """Draw background"""
        if self.background:
            bg_scaled = pygame.transform.scale(self.background, (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
            self.surface.blit(bg_scaled, (0, 0))
            # Draw semi-opaque overlay to improve contrast
            overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((*config.MENU_OVERLAY_COLOR, config.MENU_OVERLAY_ALPHA))
            self.surface.blit(overlay, (0, 0))
        else:
            # Gradient-like background
            for y in range(config.WINDOW_HEIGHT):
                progress = y / config.WINDOW_HEIGHT
                r = int(25 + (60 - 25) * progress)
                g = int(25 + (40 - 25) * progress)
                b = int(45 + (80 - 45) * progress)
                pygame.draw.line(self.surface, (r, g, b), (0, y), (config.WINDOW_WIDTH, y))
            # Add light overlay for readability
            overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((*config.MENU_OVERLAY_COLOR, config.MENU_OVERLAY_ALPHA))
            self.surface.blit(overlay, (0, 0))
    
    def draw(self):
        """Main draw method that dispatches to screen-specific draws"""
        self.draw_background()
        # Draw exit button top-right
        pygame.draw.rect(self.surface, config.BUTTON_EXIT, self.exit_button, border_radius=8)
        pygame.draw.rect(self.surface, config.WHITE, self.exit_button, 2, border_radius=8)
        exit_txt = self.font_small.render("Exit", True, config.TEXT_PRIMARY)
        exit_rect = exit_txt.get_rect(center=self.exit_button.center)
        self.surface.blit(exit_txt, exit_rect)
        
        if self.current_screen == "mode":
            self.draw_mode_screen()
        elif self.current_screen == "difficulty":
            self.draw_difficulty_screen()
        elif self.current_screen == "names":
            self.draw_names_screen()
    
    def draw_mode_screen(self):
        """Draw game mode selection screen"""
        # Title
        title_surface = self.font_title.render("TEEKO", True, config.TEXT_TITLE)
        title_rect = title_surface.get_rect(center=(config.WINDOW_WIDTH//2, 80))
        self.surface.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle = self.font_text.render("Select game mode", True, config.TEXT_TITLE_SECONDARY)
        subtitle_rect = subtitle.get_rect(center=(config.WINDOW_WIDTH//2, 170))
        self.surface.blit(subtitle, subtitle_rect)
        
        # Draw mode buttons
        for btn in self.mode_buttons:
            btn.draw(self.surface)
    
    def draw_difficulty_screen(self):
        """Draw difficulty selection screen"""
        # Title
        title_surface = self.font_title.render("TEEKO", True, config.TEXT_TITLE)
        title_rect = title_surface.get_rect(center=(config.WINDOW_WIDTH//2, 60))
        self.surface.blit(title_surface, title_rect)
        
        # Mode display
        mode_text = self.get_mode_display_text()
        mode_surface = self.font_text.render(mode_text, True, config.TEXT_TITLE_SECONDARY)
        mode_rect = mode_surface.get_rect(center=(config.WINDOW_WIDTH//2, 140))
        self.surface.blit(mode_surface, mode_rect)
        
        # Subtitle
        subtitle = self.font_text.render("Select difficulty level", True, config.TEXT_PRIMARY)
        subtitle_rect = subtitle.get_rect(center=(config.WINDOW_WIDTH//2, 220))
        self.surface.blit(subtitle, subtitle_rect)
        
        # Draw difficulty buttons
        for btn in self.difficulty_buttons:
            btn.draw(self.surface)
        
        # Draw back button
        pygame.draw.rect(self.surface, config.BUTTON_NORMAL, self.back_button, border_radius=10)
        pygame.draw.rect(self.surface, config.BUTTON_BORDER, self.back_button, 2, border_radius=10)
        back_text = self.font_small.render("Back", True, config.BUTTON_TEXT_COLOR)
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.surface.blit(back_text, back_rect)
    
    def draw_names_screen(self):
        """Draw player names input screen"""
        # Title
        title_surface = self.font_title.render("TEEKO", True, config.TEXT_TITLE)
        title_rect = title_surface.get_rect(center=(config.WINDOW_WIDTH//2, 40))
        self.surface.blit(title_surface, title_rect)
        
        # Mode and Difficulty display
        mode_text = self.get_mode_display_text()
        mode_surface = self.font_small.render(f"{mode_text} - {self.difficulty}", True, config.TEXT_TITLE_SECONDARY)
        mode_rect = mode_surface.get_rect(center=(config.WINDOW_WIDTH//2, 110))
        self.surface.blit(mode_surface, mode_rect)
        
        # Instructions
        instructions = self.font_text.render("Enter player names", True, config.TEXT_PRIMARY)
        instructions_rect = instructions.get_rect(center=(config.WINDOW_WIDTH//2, 170))
        self.surface.blit(instructions, instructions_rect)
        
        # Draw input fields
        if self.mode == "PvsP":
            label1 = self.font_small.render("Player 1:", True, config.TEXT_PRIMARY)
            self.surface.blit(label1, (self.input_player1.x - 150, self.input_player1.y + 10))
            self.draw_input_field(self.input_player1, self.player1_name, "p1", "Enter name...")
            
            label2 = self.font_small.render("Player 2:", True, config.TEXT_PRIMARY)
            self.surface.blit(label2, (self.input_player2.x - 150, self.input_player2.y + 10))
            self.draw_input_field(self.input_player2, self.player2_name, "p2", "Enter name...")
        elif self.mode == "PvsIA":
            label1 = self.font_small.render("Your Name:", True, config.TEXT_PRIMARY)
            self.surface.blit(label1, (self.input_player1.x - 150, self.input_player1.y + 10))
            self.draw_input_field(self.input_player1, self.player1_name, "p1", "Enter name...")
        else:
            # AI vs AI: no name input
            info = self.font_small.render("AI vs AI - no player names required", True, config.TEXT_PRIMARY)
            info_rect = info.get_rect(center=(config.WINDOW_WIDTH//2, 300))
            self.surface.blit(info, info_rect)
        
        # Draw start button
        pygame.draw.rect(self.surface, config.BUTTON_ACTIVE if (self.mode != "IAvsIA" and self.player1_name) or self.mode=="IAvsIA" else config.BUTTON_NORMAL, 
                self.start_button, border_radius=10)
        pygame.draw.rect(self.surface, config.GREEN, self.start_button, 2, border_radius=10)
        start_text = self.font_text.render("Start Game", True, config.GREEN)
        start_rect = start_text.get_rect(center=self.start_button.center)
        self.surface.blit(start_text, start_rect)
        
        # Draw back button
        pygame.draw.rect(self.surface, config.BUTTON_NORMAL, self.back_button, border_radius=10)
        pygame.draw.rect(self.surface, config.BUTTON_BORDER, self.back_button, 2, border_radius=10)
        back_text = self.font_small.render("Back", True, config.BUTTON_TEXT_COLOR)
        back_rect = back_text.get_rect(center=self.back_button.center)
        self.surface.blit(back_text, back_rect)
    
    def draw_input_field(self, rect, text, field_id, placeholder):
        """Draw an input field with cursor"""
        pygame.draw.rect(self.surface, config.BUTTON_NORMAL, rect, border_radius=6)
        pygame.draw.rect(self.surface, config.BUTTON_BORDER, rect, 2, border_radius=6)
        
        display_text = text if text else placeholder
        color = config.TEXT_PRIMARY
        txt_surface = self.font_small.render(display_text, True, color)
        self.surface.blit(txt_surface, (rect.x + 15, rect.y + 12))
        
        # Draw cursor
        self.update_cursor()
        if self.cursor_visible and self.active_input == field_id:
            cursor_x = rect.x + 15 + self.font_small.size(text)[0]
            pygame.draw.line(self.surface, config.TEXT_PRIMARY, (cursor_x, rect.y + 8), (cursor_x, rect.y + 42), 2)
    
    def get_mode_display_text(self):
        """Get human-readable mode text"""
        if self.mode == "PvsP":
            return "Player vs Player"
        elif self.mode == "PvsIA":
            return "Player vs AI"
        else:
            return "AI vs AI"
