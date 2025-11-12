# Teeko Game Implementation

A two-player strategy board game implementation in Python, with a foundation ready for AI integration.

## Project Structure

```
Teeko/
├── main.py              # Entry point for the game
├── play.py              # Interactive game launcher
├── test_game.py         # Game logic tests
├── LICENSE
├── resources/           # Game assets (fonts, icons, images, sounds)
└── src/
    ├── __init__.py      # Package initialization
    ├── ai.py            # Game logic and board management (TeekoBoard class)
    ├── player.py        # Player management (Player class)
    ├── control.py       # Game controller (GameController class)
    └── start.py         # Game UI and user interface (GameUI class)
```

## How to Play

### Starting the Game

Run the game with:
```bash
python play.py
```

Or directly:
```bash
python main.py
```

### Game Rules

1. **Placement Phase**: 
   - Players alternate placing their 4 pieces on the 5×5 board
   - Input: `row col` (e.g., `0 2` to place at row 0, column 2)
   - Coordinates range from 0-4

2. **Movement Phase** (starts after all 8 pieces are placed):
   - Players alternate moving one piece per turn
   - Each piece can move to any adjacent square (including diagonals)
   - Input: `from_row from_col to_row to_col` (e.g., `0 0 0 1`)

3. **Winning Condition**:
   - First player to get 4 pieces in a row (horizontal, vertical, or diagonal) wins

### Board Display

```
     0   1   2   3   4
   ┌───┬───┬───┬───┬───┐
 0 │ ● │   │ ○ │   │   │
   ├───┼───┼───┼───┼───┤
 1 │   │ ● │   │ ○ │   │
   ├───┼───┼───┼───┼───┤
 2 │   │   │   │   │   │
   ├───┼───┼───┼───┼───┤
 3 │ ● │   │   │   │ ○ │
   ├───┼───┼───┼───┼───┤
 4 │   │   │   │   │   │
   └───┴───┴───┴───┴───┘
```

- `●` = Player 1 (Red)
- `○` = Player 2 (Blue)

## Code Structure

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
- `get_phase()` - Return current game phase (placement or movement)

### `player.py` - Player Class

Manages player information:
- Player name and ID
- AI/Human designation
- Display symbols and colors

### `control.py` - GameController Class

Controls game flow:
- Manages turn switching
- Delegates moves to the board
- Tracks game state and winner
- Provides formatted board display

**Key Methods:**
- `place_piece(row, col)` - Handle a placement move
- `move_piece(from_row, from_col, to_row, to_col)` - Handle a movement move
- `switch_turn()` - Switch to the other player
- `get_board_display()` - Get formatted board
- `get_game_status()` - Get current phase and piece counts

### `start.py` - GameUI Class

Handles user interface:
- Game setup (player names)
- Input handling
- Board display
- Game loop management

### `main.py` - Entry Point

Simple entry point that initializes and starts the game.

## Testing

Run the automated tests:
```bash
python test_game.py
```

This tests:
- Piece placement validation
- Piece movement validation
- Board state management
- Win condition detection (basic setup)

## Future Enhancements

The architecture is designed to support AI integration. The `ai.py` file is separate from the UI layer, making it easy to:

1. **Add AI Logic**: Implement AI player strategies in a new module
2. **Connect to Prolog**: Add a bridge between Python game logic and Prolog AI logic (mentioned in original requirements)
3. **Enhanced UI**: Replace console UI with graphical interface
4. **Game Variations**: Implement different Teeko variants

## Requirements

- Python 3.11+
- No external dependencies for the core game

## Author

A group of students, FISE-INFO, UTBM
September 2025
