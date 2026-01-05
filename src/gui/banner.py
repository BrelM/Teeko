import pygame
import src.gui.config as config

class Banner:
    def __init__(self, surface, p1, p2):
        self.surface = surface
        self.font_title = pygame.font.SysFont("Arial", 28, bold=True)
        self.font_status = pygame.font.SysFont("Arial", 20)
        self.player1_name = p1
        self.player2_name = p2

    def draw(self, current_player=1, status=""):
        # Main banner background
        banner_rect = pygame.Rect(0, 0, config.BANNER_WIDTH, config.BANNER_HEIGHT)
        pygame.draw.rect(self.surface, config.BANNER_BG, banner_rect)
        pygame.draw.line(self.surface, (100, 100, 150), (0, 90), (config.WINDOW_WIDTH, 90), 2)

        # Player 1
        player1_text_color = (255, 200, 150) if current_player == 1 else (150, 150, 150)
        text1 = self.font_title.render(self.player1_name, True, player1_text_color)
        self.surface.blit(text1, (20, 10))
        pygame.draw.circle(self.surface, config.PLAYER1, (35, 60), 12)
        pygame.draw.circle(self.surface, config.PLAYER1, (35, 60), 16, 2)

        # Player 2
        player2_text_color = (150, 200, 255) if current_player == 2 else (150, 150, 150)
        text2 = self.font_title.render(self.player2_name, True, player2_text_color)
        text2_rect = text2.get_rect(right=config.WINDOW_WIDTH - 20, top=10)
        self.surface.blit(text2, text2_rect)
        pygame.draw.circle(self.surface, config.PLAYER2, (config.WINDOW_WIDTH - 35, 60), 12)
        pygame.draw.circle(self.surface, config.PLAYER2, (config.WINDOW_WIDTH - 35, 60), 16, 2)

        # Active player indicator (border)
        if current_player == 1:
            pygame.draw.rect(self.surface, config.PLAYER1, (8, 5, 180, 80), 3, border_radius=8)
        else:
            pygame.draw.rect(self.surface, config.PLAYER2, (config.WINDOW_WIDTH - 188, 5, 180, 80), 3, border_radius=8)

        # Status/Phase information
        if status:
            status_text = self.font_status.render(status, True, (200, 220, 255))
            status_rect = status_text.get_rect(center=(config.WINDOW_WIDTH // 2, 50))
            self.surface.blit(status_text, status_rect)