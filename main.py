import pygame
import src.gui.config as config
from src.controller.game import Game
from src.gui.menu import Menu


def main():
    pygame.init()
    flags = pygame.RESIZABLE if getattr(config, 'WINDOW_RESIZABLE', False) else 0
    screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), flags)
    pygame.display.set_caption("Teeko - Strategic Board Game")  
    clock = pygame.time.Clock()

    menu = Menu(screen)
    game = None
    state = "menu"

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Update global size and recreate screen surface
                w, h = event.w, event.h
                config.WINDOW_WIDTH = max(400, w)
                config.WINDOW_HEIGHT = max(300, h)
                flags = pygame.RESIZABLE if getattr(config, 'WINDOW_RESIZABLE', False) else 0
                screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), flags)
                # Recreate menu/game surfaces so they draw to the new screen
                if state == "menu":
                    menu = Menu(screen)
                elif state == "game" and game is not None:
                    game.surface = screen
                    # propagate to subcomponents if present
                    try:
                        game.board.surface = screen
                    except Exception:
                        pass
                    try:
                        game.banner.surface = screen
                    except Exception:
                        pass
            
            # ESC key to exit or return to menu; R to restart
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if state == "game":
                        state = "menu"
                        game = None
                        menu = Menu(screen)
                    else:
                        running = False
                # Restart current game by pressing R
                if event.key == pygame.K_r and state == "game":
                    # Recreate game with same parameters
                    try:
                        game = Game(screen,
                                    mode=game.mode,
                                    difficulty=game.difficulty,
                                    player1_name=game.p1,
                                    player2_name=game.p2)
                        state = "game"
                    except Exception:
                        # If recreation fails, fallback to returning to menu
                        state = "menu"
                        game = None
                        menu = Menu(screen)

            if state == "menu":
                action = menu.handle_event(event)
                if isinstance(action, dict):  # Parameters returned
                    # Menu may return {'exit': True}
                    if action.get("exit"):
                        running = False
                        break
                    # Otherwise expect game parameters
                    if all(k in action for k in ("mode", "difficulty", "player1_name", "player2_name")):
                        game = Game(screen,
                            mode=action["mode"],
                            difficulty=action["difficulty"],
                            player1_name=action["player1_name"],
                            player2_name=action["player2_name"])
                        state = "game"

            elif state == "game":
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game.handle_click(event.pos)
            
                if event.type == pygame.USEREVENT+1:
                    pygame.time.set_timer(pygame.USEREVENT+1, 0)
                    game.ai_play()

        # Update and display
        if state == "menu":
            menu.draw()
        elif state == "game":
            game.update()
            game.draw()

        pygame.display.flip()
        clock.tick(config.FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
