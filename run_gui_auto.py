import threading
import time
import pygame
from src.gui import GameGUI

# Launch GUI with player2 as AI
def stopper(delay=3.0):
    time.sleep(delay)
    try:
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    except Exception:
        pass

if __name__ == '__main__':
    gui = GameGUI(player1_name='Human', player2_name='AI', ai_player1=False, ai_player2=True, ai_depth=2, ai_timeout=1.0)
    t = threading.Thread(target=stopper, args=(3.0,), daemon=True)
    t.start()
    gui.run()
