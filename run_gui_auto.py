import threading
import time
import pygame
from src.gui import GameGUI

# Launch GUI with AI-vs-AI and stop when game ends or after timeout
def watcher(gui, timeout=30.0):
    start = time.time()
    while True:
        time.sleep(0.25)
        # stop if game over or draw
        try:
            if gui.controller.is_game_over() or gui.controller.is_draw():
                break
        except Exception:
            pass
        if time.time() - start > timeout:
            break
    try:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    except Exception:
        pass

if __name__ == '__main__':
    # Run AI vs AI, allow up to 30 seconds (adjustable)
    gui = GameGUI(player1_name='AI-1', player2_name='AI-2', ai_player1=True, ai_player2=True, ai_depth=2, ai_timeout=1.0)
    t = threading.Thread(target=watcher, args=(gui, 30.0), daemon=True)
    t.start()
    gui.run()
