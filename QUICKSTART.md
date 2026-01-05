# Teeko - Quick Start Guide

## Installation

### 1. Prerequisites
- Python 3.8 or higher
- SWI-Prolog (must be installed separately and in PATH)

### 2. Setup Virtual Environment (Recommended)

**Windows PowerShell:**
```powershell
# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

**macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Verify SWI-Prolog Installation
```bash
# Should show SWI-Prolog version if properly installed
swipl --version
```

## Running the Game

### Start the Game
```bash
python main.py
```

That's it! No command-line configuration needed.

## How to Play

### 1. Game Mode Selection
Click one of three buttons:
- **Player vs Player**: Play against a friend
- **Player vs AI**: Challenge the AI
- **AI vs AI**: Watch two AIs compete

### 2. Difficulty Selection (if playing against AI)
Choose your challenge level:
- **Easy**: Perfect for learning (AI searches 3 moves deep)
- **Medium**: Balanced challenge (AI searches 4 moves deep)
- **Hard**: Maximum difficulty (AI searches 5 moves deep)

### 3. Enter Names
Type player names or leave blank for defaults:
- Player names default to "Player 1", "Player 2", "AI" if empty
- Maximum 15 characters per name
- Click the text field and type (backspace to delete)

### 4. Start the Game
Click "Start Game" to begin!

## During Gameplay

### Controls
- **Left Click**: Place pieces (placement phase) or select/move pieces (movement phase)
- **R**: Restart the current game (keeps same players and difficulty)
- **ESC**: Return to main menu (pressing ESC again from menu exits the application)
- **Exit**: Use the persistent `Exit` button in the top-right to quit at any time

### Game Phases

#### Placement Phase
1. Players alternate clicking to place their 4 pieces on the board
2. Each player places one piece per turn
3. Once all 8 pieces are placed, game moves to movement phase

#### Movement Phase
1. Click a piece to select it (shows selection feedback)
2. Click an adjacent square to move the piece
3. First player to get 4 pieces in a line (horizontal, vertical, or diagonal) wins!

### Status Bar
The banner at the top shows:
- **Player names** with colored indicators (red/blue)
- **Current player** with border highlight
- **Game phase** (Placement or Movement)
- **AI indicator** when AI is playing

### Messages
On-screen messages inform you of:
- Invalid moves
- Piece selection status
- Phase transitions
- Winner announcement

## Menu Navigation

### In Menu
- **Click buttons** to select options
- **Click Back** to go to previous screen
- **Click Start Game** to begin (at least one name required)

### In Game
- **Press ESC** to return to menu
- **Press ESC** again to exit application

## Example Scenarios

### Scenario 1: Player vs Player (Learning)
```
1. Click "Player vs Player"
2. Skip difficulty selection (not needed)
3. Enter names: "Alice" and "Bob"
4. Click "Start Game"
5. Play and take turns placing pieces
6. Once all pieces placed, play movement phase
7. First to get 4 in a row wins!
```

### Scenario 2: Challenge the AI
```
1. Click "Player vs AI"
2. Click "Medium" difficulty
3. Enter your name: "Champion"
4. Click "Start Game"
5. Place your pieces in placement phase
6. AI will place its pieces automatically
7. Battle in movement phase
8. Try to beat the AI!
```

### Scenario 3: Watch AI Battle
```
1. Click "AI vs AI"
2. Click "Hard" difficulty (for fun!)
3. Leave names as default
4. Click "Start Game"
5. Watch two AIs compete
6. The game plays automatically
7. Game ends when one AI gets 4 in a row
```

## Troubleshooting

### "pygame not found"
```bash
pip install pygame
```

### "pyswip not found"
```bash
pip install pyswip
```

### "swipl not found" or "Prolog error"
- Make sure SWI-Prolog is installed: https://www.swi-prolog.org/download/stable
- Verify it's in your PATH by running: `swipl --version`
- On Windows, restart after installing SWI-Prolog to update PATH

### Game doesn't start
- Check console for error messages
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Ensure Python 3.8+ is being used: `python --version`

### AI takes too long to move
- You're on "Hard" difficulty - this is normal! AI thinks carefully
- Try "Medium" or "Easy" for faster games

## Tips for Playing

### Winning Strategies
1. **Control the Center**: Pieces in the middle of the board are more valuable
2. **Think Ahead**: Plan your movement phase strategy during placement
3. **Block Opponent**: Prevent opponent from forming lines
4. **Create Threats**: Set up multiple winning possibilities

### AI Difficulty Tips
- **Easy**: Great for learning the rules
- **Medium**: Good challenge for most players
- **Hard**: Only for advanced players; AI won't make silly mistakes

## File Structure

```
Teeko/
├── main.py              # Start here!
├── requirements.txt     # Dependencies
├── IMPROVEMENTS.md      # Detailed improvements documentation
├── src/
│   ├── controller/
│   │   ├── game.py         # Game logic and flow
│   │   └── board.py        # Board representation
│   ├── gui/
│   │   ├── menu.py         # Menu system (improved!)
│   │   ├── banner.py       # Status display
│   │   └── pieces.py       # Piece rendering
│   └── model/
│       ├── ai/
│       │   ├── ai_engine.py    # Central AI coordinator
│       │   ├── evaluation.py   # Evaluation function
│       │   ├── minmax_alphabeta.py  # Alpha-Beta search
│       │   └── minmax.py       # MinMax algorithm
│       └── prologRules/
│           ├── prolog_manager.py  # Prolog interface
│           ├── ia_helper.py      # AI helpers
│           └── teeko_rules.pl    # Game rules (Prolog)
```

## Customization

### Changing Colors/Appearance
Edit `src/gui/config.py`:
```python
# Change button colors
BUTTON_NORMAL = (80, 80, 120)
BUTTON_HOVER = (100, 100, 150)
BUTTON_ACTIVE = (120, 180, 100)

# Change window size
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Change piece appearance
POINT_RADIUS = 10
```

### Adjusting AI Difficulty
Edit `src/model/ai/ai_engine.py` `get_difficulty_params()` method to add custom levels

## Game Rules Reference

### Placement Phase
- 5x5 board with 25 squares
- Each player places 4 pieces alternately
- Must place on empty squares
- Phase ends when all 8 pieces are placed

### Movement Phase
- Players move their pieces alternately
- Pieces can move to any adjacent square (including diagonals)
- Target square must be empty
- First player to align 4 pieces in a line wins

### Winning
- 4 pieces in a row (horizontal, vertical, or diagonal)
- Can win during placement or movement phase

## Support

For issues or improvements, check the IMPROVEMENTS.md file for technical details.

Enjoy Teeko! 🎮
