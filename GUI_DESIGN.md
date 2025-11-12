# GUI Visual Layout & Design

## Screen Layout (1000×700)

```
╔════════════════════════════════════════════════════════════════════════════════╗
║                                    TEEKO                                       ║
╠════════════════════════════════════════════════════════════════════════════════╣
║                                                                                ║
║    Column Numbers: 0 1 2 3 4                                                  ║
║    Row            ┌───┬───┬───┬───┬───┐                                       ║
║    Numbers   0    │ ● │   │ ○ │   │   │  Info Panel:                         ║
║             1    │   │ ● │   │ ○ │   │  ┌─────────────────────┐             ║
║             2    │   │   │   │   │   │  │ Current Player:     │             ║
║             3    │ ● │   │   │   │ ○ │  │ Alice (Red)         │             ║
║             4    │   │   │   │   │   │  │                     │             ║
║                  └───┴───┴───┴───┴───┘  │ Phase: PLACEMENT    │             ║
║                                          │ Pieces: 3/4 - 2/4   │             ║
║     ● = Player 1 (Red)                   │                     │             ║
║     ○ = Player 2 (Blue)                  │ INSTRUCTIONS:       │             ║
║     ◯ = Valid move (green)               │ Click to place      │             ║
║                                          │ pieces              │             ║
║                                          │                     │             ║
║                                          │ Click piece to      │             ║
║                                          │ select, then move   │             ║
║                                          │                     │             ║
║                                          │ R = Restart         │             ║
║                                          │ ESC = Quit          │             ║
║                                          └─────────────────────┘             ║
║                                                                                ║
║  ✓ Message: Piece placed!                                                    ║
║                                                                                ║
╚════════════════════════════════════════════════════════════════════════════════╝
```

## Game Board Layout (500×500 area)

```
     0     1     2     3     4
   ┌─────┬─────┬─────┬─────┬─────┐
0  │     │     │     │     │     │  Each cell: 100×100 pixels
   ├─────┼─────┼─────┼─────┼─────┤  Piece radius: 30 pixels
1  │     │     │     │     │     │  Piece outline: 3 pixels
   ├─────┼─────┼─────┼─────┼─────┤
2  │     │     │     │     │     │
   ├─────┼─────┼─────┼─────┼─────┤
3  │     │     │     │     │     │
   ├─────┼─────┼─────┼─────┼─────┤
4  │     │     │     │     │     │
   └─────┴─────┴─────┴─────┴─────┘
```

## Color Scheme

```
┌──────────────────────────────────────┐
│         COLOR PALETTE                │
├──────────────────────────────────────┤
│ Background       │ Dark Gray (50,50,50)       │
│ Board Background │ Brown (139,90,43)          │
│ Grid Lines       │ Black (0,0,0)              │
│ Player 1 Piece   │ Light Red (255,100,100)    │
│ Player 2 Piece   │ Light Blue (100,100,255)   │
│ Selected Piece   │ Gold border (255,215,0)    │
│ Valid Move       │ Green dot (0,255,0)        │
│ Text (Title)     │ Yellow (255,255,0)         │
│ Text (Normal)    │ White (255,255,255)        │
│ Highlight        │ Gold (255,215,0)           │
└──────────────────────────────────────┘
```

## UI Elements

### Header
```
  ╔════════════════════════════════════════════════════╗
  ║               TEEKO (large, yellow)               ║
  ╚════════════════════════════════════════════════════╝
  Positioned at: (500, 30) - center top
```

### Game Board
```
  Board Position:    (150, 100)
  Board Size:        500×500 pixels (5×5 cells)
  Cell Size:         100×100 pixels
  Grid Line Width:   2 pixels
  Border:            2 pixel black outline
```

### Info Panel
```
  Position:          Right side of board
  Start X:           (700, 100)
  Width:             250 pixels
  
  Contains:
  - Current Player (medium font, colored)
  - Phase Label (small font)
  - Piece Count (small font, placement phase only)
  - Instructions (tiny font)
```

### Message Area
```
  Position:          Bottom center
  Y:                 650 pixels
  Font:              Medium (36pt)
  Color:             Yellow text, black background
  Auto-Hide:         After 3 seconds
  Format:            ✓ Success / ✗ Error
```

## Piece Representation

### Normal Piece
```
    ╭─────────╮
    │    ●    │  Filled circle (radius 30)
    ╰─────────╯  Black outline (3px)
```

### Selected Piece
```
    ╭───────────╮
    │    ●      │  Filled circle (radius 30)
    │ ◯◯◯◯◯◯◯   │  Gold border around (5px)
    ╰───────────╯  Larger outline
```

### Valid Move Indicator
```
       ◯          Small green circle (radius 10)
                  Black outline (2px)
```

## State Transitions (Visual)

### Placement Phase Visual
```
Empty Board → Players Click → Pieces Appear → Switch Player
(Brown grid)  (at cell)     (+ sound)        (highlight switches)
```

### Movement Phase Visual
```
Full Board → Click Piece → Green Dots → Click Dot → Piece Moves
(all 8)     (gold border)  (show)       (animate)   (+ sound)
```

### Victory State
```
4-in-a-Row Detected → Victory Message → Trumpet Sound → "Press R" Prompt
(visual highlight)    (large yellow)    (plays)         (blink)
```

## Font Sizes & Styling

```
┌─────────────────────────────────┐
│ FONT SIZES                      │
├─────────────────────────────────┤
│ Title (TEEKO)     │ 48pt        │
│ Player Name       │ 36pt        │
│ Labels            │ 24pt        │
│ Instructions      │ 16pt        │
│ Coordinates       │ 16pt        │
│ Messages          │ 36pt        │
└─────────────────────────────────┘

All using pygame.font.Font (system default)
Black outline, White text for contrast
```

## Responsive Behavior

### Window Size: 1000×700

- Board takes: 150→650 (500px width), 100→600 (500px height)
- Info panel: 700→950 (250px width)
- Message area: 250px centered at bottom
- All elements scale proportionally

### Resize Handling
- Window is fixed size (no resizing)
- Hardcoded positions and sizes
- Optimized for 1920×1080 display minimum

## Animation & Effects

### Piece Placement
```
Click → Sound plays → Piece appears → Message shows
(instant)  (pawn_move.mp3)  (immediate)  (3 sec)
```

### Piece Movement
```
Select → Highlights → Click dest → Piece moves → Sound → Message
(gold)  (green dots)  (immediate)   (instant)    (move)  (2 sec)
```

### Victory
```
4-in-a-Row → Screen brightens → Trumpet → Victory Message → Flash
(detected)  (highlight)         (plays)   (5 seconds)     (optional)
```

## Accessibility

- High contrast colors
- Clear text labels
- Large click targets (100×100 cells)
- Visual feedback for all actions
- Sound effects complement (not required)
- Keyboard shortcuts available
- Clear instructions on screen

## Performance

- 60 FPS rendering
- ~50MB memory with all resources
- No visible lag or stuttering
- Smooth piece rendering
- Instant response to clicks

---

This visual design provides:
✅ Clear game state visibility
✅ Intuitive user interface
✅ Professional appearance
✅ Good accessibility
✅ Smooth performance
