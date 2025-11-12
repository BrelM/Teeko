# Teeko Game Implementation

A two-player strategy board game implementation in Python with both console and **graphical user interface (GUI)** using pygame.

## Features

- **Console Mode**: Text-based interface for terminal play
- **GUI Mode**: Interactive graphical interface using pygame with:
  - Visual board with piece rendering
  - Point-and-click gameplay
  - Real-time game status display
  - Sound effects (pawn move, victory, defeat)
  - Board image background
  - Player information panel
  - Automatic winner detection
  - Game restart functionality

## Project Structure

```
Teeko/
├── main.py                # Entry point with mode selection
├── play.py                # Quick launcher for GUI mode
├── play_console.py        # Console mode launcher
├── verify_gui.py          # GUI verification script
├── test_game.py           # Game logic tests
├── LICENSE
├── resources/             # Game assets
│   ├── fonts/             # Font files
│   ├── icons/             # Icon templates
│   ├── images/            # Board images
│   └── sounds/            # Sound effects
└── src/
    ├── __init__.py        # Package initialization
    ├── ai.py              # Game logic (TeekoBoard class)
    ├── player.py          # Player management (Player class)
    ├── control.py         # Game controller (GameController class)
    ├── start.py           # Console UI (GameUI class)
    └── gui.py             # Pygame GUI (GameGUI class)
```

## How to Play

### Starting the Game

**Quick GUI Launch:**
```bash
python play.py
```

**Interactive Mode Selector:**
```bash
python main.py
```
Then choose between GUI (1) or Console (2) mode.

**Console Mode Only:**
```bash
python play_console.py
```

### GUI Mode Instructions

1. **Placement Phase**: 
   - Click on board squares to place your 4 pieces
   - Players alternate placing pieces
   - Game automatically switches to movement phase when all 8 pieces are placed

2. **Movement Phase**:
   - Click a piece to select it (highlighted with gold border)
   - Green dots show valid moves
   - Click a green dot to move your piece there
   - Pieces can only move to adjacent squares (including diagonals)

3. **Controls**:
   - **Left Click**: Place piece or move piece
   - **R Key**: Restart game
   - **ESC Key**: Quit game

4. **Winning**:
   - First player to get 4 pieces in a row wins
   - Victory trumpet sound plays on win
   - Press R to restart a new game

### Console Mode Instructions

Run `python play_console.py` and follow the prompts:

1. **Placement Phase**: Enter `row col` (e.g., `0 2`)
2. **Movement Phase**: Enter `from_row from_col to_row to_col` (e.g., `0 0 0 1`)

Board coordinates range from 0-4.

## Code Structure

### `gui.py` - GameGUI Class (NEW)

Handles all pygame-based graphical display and interaction:
- Board rendering with grid
- Piece rendering with highlighting
- Mouse click handling for placement and movement
- Game state display (current player, phase, piece counts)
- Message system for feedback
- Sound effect playback
- Resource loading (images, sounds)

**Key Methods:**
- `handle_click(pos)` - Process mouse clicks
- `handle_placement_click(row, col)` - Handle placement phase clicks
- `handle_movement_click(row, col)` - Handle movement phase clicks
- `draw()` - Render the complete game state
- `run()` - Main game loop

### `ai.py` - TeekoBoard Class

Handles all game logic:
- Board state management
- Move validation (placement and movement phases)
- Win condition detection
- Board state queries

**Key Methods:**
- `place_piece(row, col, player)` - Place a piece during placement phase
- `move_piece(from_row, from_col, to_row, to_col, player)` - Move a piece during movement phase
- `check_winner()` - Check if there's a winner
- `get_board_state()` - Return current board state
- `get_phase()` - Return current game phase

### `player.py` - Player Class

Manages player information:
- Player name and ID (1 or 2)
- AI/Human designation
- Display symbols and colors

### `control.py` - GameController Class

Controls game flow:
- Manages turn switching
- Delegates moves to the board
- Tracks game state and winner
- Provides formatted displays

**Key Methods:**
- `place_piece(row, col)` - Handle a placement move
- `move_piece(from_row, from_col, to_row, to_col)` - Handle a movement move
- `switch_turn()` - Switch to the other player
- `get_board_display()` - Get formatted board (console)

### `start.py` - GameUI Class (Console)

Handles console-based user interface:
- Game setup (player names)
- Console input handling
- Text-based board display
- Game loop management

### `main.py` - Entry Point

Provides mode selection menu:
- Choose between GUI (pygame) and Console modes
- Accepts player names
- Launches appropriate interface

## Requirements

### Core
- Python 3.11+
- No dependencies for console mode

### GUI Mode
- pygame (install with: `pip install pygame`)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/BrelM/Teeko.git
cd Teeko
```

### 2. Install dependencies (for GUI mode)
```bash
pip install pygame
```

### 3. Verify GUI setup
```bash
python verify_gui.py
```

## Testing

Run the automated game logic tests:
```bash
python test_game.py
```

This tests:
- Piece placement validation
- Piece movement validation
- Board state management
- Win condition detection

## Game Rules

- **Board**: 5×5 grid
- **Pieces per player**: 4
- **Phases**: 
  1. Placement (place 4 pieces alternately)
  2. Movement (move pieces to adjacent squares)
- **Winning**: First to get 4 pieces in a row (horizontal, vertical, or diagonal)

## Assets Used

- **Images**: `resources/images/board.jpg` - Board background
- **Icons**: `resources/icons/icon_template.png` - Icon template
- **Sounds**: 
  - `resources/sounds/pawn_move.mp3` - Move sound
  - `resources/sounds/victory.mp3` - Victory sound
  - `resources/sounds/defeat.mp3` - Defeat sound
  - `resources/sounds/victory_trumpet.mp3` - Trumpet fanfare

## Future Enhancements

The architecture supports:
1. **AI Integration**: Add AI players using Prolog backend
2. **Extended GUI**: Add animations, particle effects
3. **Network Play**: Multi-player over network
4. **Statistics**: Track wins, losses, game history
5. **Themes**: Customizable board themes and piece colors

## Author

A group of students, FISE-INFO, UTBM
September 2025 - Updated November 2025

## License

See LICENSE file for details.
 
## Recent updates (Nov 13, 2025)

- Background image can be scaled via `BOARD_SCALE` in `src/gui.py` (visual only). The logical grid remains unscaled and is centered on the scaled background.
- Click mapping and piece rendering use the computed `grid_origin_x`/`grid_origin_y` so visuals align with the scaled board.
- Piece spacing and alignment: use `PIECE_OFFSET_X`, `PIECE_OFFSET_Y`, and `PIECE_PADDING` in `src/gui.py`. `PIECE_RADIUS` is now derived from `CELL_SIZE` so spacing between pieces is easier to tune.
- Calibration tools: run `calibrate_board.py` (interactive) or `detect_offset.py` (automatic) to determine recommended offsets and scale; copy the printed values into `src/gui.py` (in `GameGUI.__init__`).

Quick commands:

```powershell
python calibrate_board.py   # interactively tune offsets/scale
python main.py              # launch GUI
```

Proposed deletions (please confirm before removal): `BUG_FIX_SUMMARY.md`, `IMPLEMENTATION_SUMMARY.md`.

