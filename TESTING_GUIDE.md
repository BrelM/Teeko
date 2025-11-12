# Testing Guide for Turn-Switching and Game Logic

## Quick Test Commands

### 1. Run Full Test Suite
```bash
python test_game.py
```
Validates:
- Placement phase mechanics
- Movement phase mechanics  
- Square shape win conditions
- Placement phase victories

### 2. Test Turn Switching
```bash
python test_debug_turns.py
```
Validates:
- Players alternate correctly through all 8 placements
- Phase transitions to "movement" after all pieces placed
- Current player switches properly

### 3. Test Specific Win Scenario
```bash
python -c "
from src.player import Player
from src.control import GameController

p1 = Player('Red', 1)
p2 = Player('Blue', 2)
controller = GameController(p1, p2)

# Square win at (0,0), (0,1), (1,0), (1,1)
coords = [(0,0), (2,2), (0,1), (2,3), (1,0), (3,2), (1,1)]

for r, c in coords:
    success, message = controller.place_piece(r, c)
    print(f'Move {r},{c}: {message}')
    if controller.is_game_over():
        break
"
```

## Manual Testing in GUI

### Scenario 1: Normal Placement
1. Launch GUI: `python play.py`
2. Players alternate clicking to place pieces
3. After 8 total placements (4 per player), game transitions to movement
4. **Expected**: Smooth turn alternation, clear phase transition

### Scenario 2: Victory by Square (Easy to Trigger)
1. Launch GUI
2. Place pieces to form 2×2 square:
   - Player 1: Click (0,0), then (0,1), then (1,0)
   - Player 2: Click any position (e.g., 2,2)
   - Player 1: Click (1,1) → **Victory!**
3. **Expected**: Victory message appears, game becomes unresponsive (correct)

### Scenario 3: Victory by Four-in-a-Row
1. Launch GUI
2. Place pieces in a line (horizontal, vertical, or diagonal)
3. Game detects victory on the 4th piece placement
4. **Expected**: Victory message with player name

## Debugging Turn-Switching Issues

If turn switching appears broken:

### Check 1: Game Logic
```bash
python -c "
from src.control import GameController
from src.player import Player

p1 = Player('A', 1)
p2 = Player('B', 2)
c = GameController(p1, p2)

for i in range(8):
    curr = c.get_current_player().name
    c.place_piece(0, i % 5) if i < 5 else c.place_piece(1, i % 5)
    next = c.get_current_player().name
    print(f'{i+1}. {curr:1} → {next:1}')
"
```

### Check 2: Phase Transition
```bash
python -c "
from src.control import GameController
from src.player import Player

p1 = Player('A', 1)
p2 = Player('B', 2)
c = GameController(p1, p2)

for i in range(8):
    c.place_piece(i % 5, i // 5)
    print(f'{i+1}. Phase: {c.board.get_phase()}, Turn: {c.get_current_player().name}')
"
```

### Check 3: Victory Detection
```bash
python -c "
from src.control import GameController
from src.player import Player

p1 = Player('A', 1)
p2 = Player('B', 2)
c = GameController(p1, p2)

# Try a winning scenario
winning_coords = [(0,0), (2,2), (0,1), (2,3), (1,0), (3,2), (1,1)]
for r, c in winning_coords:
    success, msg = c.place_piece(r, c)
    print(f'({r},{c}): {msg[:30]}...')
    if c.is_game_over():
        print(f'GAME OVER: {c.get_winner().name} wins!')
        break
"
```

## Expected Behavior Summary

### Turn Switching ✓
- Players alternate on each successful placement
- Turn switches even when game ends
- No piece counts get "stuck"

### Victory Detection ✓
- Detected on placement if formation creates win
- Square (2×2) recognized as valid win
- Four-in-a-row (any direction) recognized as valid win

### Game State Management ✓
- `game_over` set to `True` when victory detected
- GUI prevents further clicks when `game_over = True`
- Victory message displayed to users
- Phase transitions correctly to "movement" if no victory

## Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Players keep playing after victory | GUI not checking `is_game_over()` | Update `handle_placement_click()` |
| Turn doesn't switch | Not calling `switch_turn()` after placement | Verify turn switch in controller |
| Victory not detected | Win detection logic broken | Check `_has_four_in_a_row()` method |
| Phase stuck on "placement" | Piece count not updating correctly | Verify `place_piece()` returns success |

## Regression Testing Checklist

Before each release, verify:

- [ ] Turn switching works (test_debug_turns.py passes)
- [ ] Game tests pass (test_game.py passes)
- [ ] Square wins detected (test_game.py - square test)
- [ ] Placement victories detected (test_game.py - placement test)
- [ ] GUI responds to clicks during placement
- [ ] GUI prevents clicks after game end
- [ ] Victory messages display correctly
- [ ] Phase transitions correctly to movement
- [ ] Movement phase works after placement ends without victory

## Performance Considerations

- Turn switching is O(1) - simple pointer swap
- Victory detection is O(n) per placement - optimal for 5×5 board
- No performance issues expected with current implementation
