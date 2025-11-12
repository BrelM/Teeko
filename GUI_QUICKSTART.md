# Teeko GUI - Getting Started

## Quick Start

### Launch the GUI
```bash
python play.py
```

Then enter player names when prompted. The GUI will load with the 5×5 game board.

## What's New: GUI Features

✨ **Complete Graphical Interface**
- Point-and-click gameplay
- Visual board with piece rendering
- Real-time game status display
- Sound effects
- Smooth piece selection and movement visualization

🎮 **How to Play**

### Placement Phase (Place 4 pieces each)
1. Click on any empty square to place a piece
2. Players alternate placing pieces
3. Game automatically moves to Movement phase when all 8 pieces are placed

### Movement Phase (Move your pieces)
1. **Click a piece** of your color to select it
   - Selection is highlighted with a gold border
   - Green dots appear showing where you can move
2. **Click a green dot** to move the piece there
3. **Goal**: Get 4 of your pieces in a row (horizontal, vertical, or diagonal)

### Controls
| Key | Action |
|-----|--------|
| **Left Click** | Place piece or move piece |
| **R** | Restart game |
| **ESC** | Quit game |

## File Organization

### Main Launchers
- **`play.py`** - GUI launcher (recommended) ⭐
- **`main.py`** - Interactive mode selector (GUI or Console)
- **`play_console.py`** - Console mode only
- **`verify_gui.py`** - Check GUI setup

### Game Code
- **`src/gui.py`** - **NEW** Pygame GUI implementation
- **`src/ai.py`** - Game logic (board, moves, win detection)
- **`src/player.py`** - Player management
- **`src/control.py`** - Game controller
- **`src/start.py`** - Console UI (still available)

### Testing & Docs
- **`test_game.py`** - Game logic tests
- **`GUI_GUIDE.py`** - GUI features and controls
- **`README.md`** - Full documentation
- **`resources/`** - Images, sounds, fonts

## Installation Requirements

### For GUI Mode
```bash
pip install pygame
```

### Verify Installation
```bash
python verify_gui.py
```

You should see: ✓ All checks passed!

## Architecture

The implementation maintains clean separation:

```
GUI Layer (gui.py)
    ↓
Game Logic (ai.py, control.py, player.py)
    ↓
Independent of UI
```

This means:
- Console mode (`start.py`) still works unchanged
- Game logic is completely separate from UI
- Easy to add AI integration later
- Multiple interfaces can use same game engine

## Resources Used

The GUI automatically uses:
- **Board Image**: `resources/images/board.jpg`
- **Sounds**: 
  - Move: `resources/sounds/pawn_move.mp3`
  - Victory: `resources/sounds/victory_trumpet.mp3`
  - Other effects in sounds/ folder

*Resources are optional - game works with or without them*

## Troubleshooting

### "pygame is not installed"
```bash
pip install pygame
```

### Click not registering?
- Make sure you're clicking within the board area
- In movement phase, click YOUR pieces (your color)
- Target square must be empty

### No sound?
- Check speaker is not muted
- Verify `resources/sounds/` folder exists
- Game works fine without sound

### Board image not showing?
- Game uses a brown color as fallback
- Board functionality is not affected
- Check `resources/images/board.jpg` exists

## What's Different from Console Version

### Console Version (play_console.py)
- Text-based input/output
- Enter moves as text: `row col` or `from_row from_col to_row to_col`
- Works in any terminal

### GUI Version (play.py) ⭐ **New**
- Click-based gameplay
- Visual piece selection
- Real-time feedback
- Sound effects
- Professional appearance
- More intuitive to learn

## Game Strategy Tips

1. **Placement Phase**: Spread pieces to control the board
2. **Create Threats**: Try to make multiple winning possibilities
3. **Block Opponent**: Watch for opponent's potential lines
4. **Plan Movement**: Think ahead about piece combinations
5. **Use Full Board**: Don't cluster pieces in one area

## Performance

- **Smooth**: 60 FPS rendering
- **Responsive**: Immediate click feedback
- **Lightweight**: Minimal resource usage
- **No Lag**: Even with board images and sounds

## Next Steps

The GUI is complete and ready for:
- ✅ Two-player gameplay
- 🔮 Future AI integration (Prolog backend)
- 🎨 Theme customization
- 🌐 Network multiplayer
- 📊 Statistics tracking

## Support

For issues or questions:
1. Check `verify_gui.py` output
2. Review `GUI_GUIDE.py` for detailed features
3. Check `README.md` for comprehensive documentation
4. Ensure pygame is installed: `pip install pygame`

---

**Enjoy playing Teeko!** 🎮

For console mode, run: `python play_console.py`
