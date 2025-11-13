"""
Simple test: Human vs AI with configurable delay.
Manually place some pieces to watch the AI response delay.
"""
from src.gui import GameGUI

# Human (Player 1) vs AI (Player 2)
# Try placing pieces manually and observe the 1.5-second delay before AI responds
gui = GameGUI(
    player1_name='You',
    player2_name='AI Opponent',
    ai_player1=False,
    ai_player2=True,
    ai_depth=2,
    ai_timeout=1.0
)
gui.run()
