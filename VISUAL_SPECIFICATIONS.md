# Teeko - Visual Design Specifications

## Application Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    START APPLICATION                        │
│                     python main.py                          │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              MAIN MENU LOOP                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  EVENT HANDLING                                      │   │
│  │  - Mouse clicks on buttons                          │   │
│  │  - Keyboard input for text fields                   │   │
│  │  - ESC key for exit                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  STATE MANAGEMENT                                   │   │
│  │  - current_screen: "mode", "difficulty", "names"   │   │
│  │  - Update based on user interactions                │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    [Screen 1]        [Screen 2]        [Screen 3]
   MODE SELECT      DIFFICULTY         NAMES INPUT
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                  [START GAME BUTTON]
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│              GAME LOOP                                      │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  INPUT HANDLING                                     │   │
│  │  - Mouse clicks on board                           │   │
│  │  - ESC key to return to menu                       │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  GAME LOGIC                                         │   │
│  │  - Piece placement/movement                        │   │
│  │  - AI turn execution                               │   │
│  │  - Winner detection                                │   │
│  └─────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  RENDERING                                          │   │
│  │  - Board display                                    │   │
│  │  - Status bar (banner)                             │   │
│  │  - Messages and overlays                           │   │
│  └─────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
                   [GAME OVER?]
                      /    \
                    NO      YES
                    │        │
                    │        ▼
                    │   [Victory Screen]
                    │        │
                    │        ▼
                    │   [ESC pressed?]
                    │    /     \
                    │  YES      NO
                    │   │       │
                    └───┼─────┬─┘
                        │     │
                        ▼     ▼
                   [MENU]  [Wait]
```

## Menu Screen Progression

### SCREEN 1: Mode Selection
```
┌────────────────────────────────────────────────┐
│                                                │
│                    TEEKO                       │
│                                                │
│              Select Game Mode                  │
│                                                │
│  ┌──────────────┐ ┌──────────────┐ ┌────────┐ │
│  │Player vs     │ │Player vs IA  │ │IA vs  │ │
│  │ Player       │ │              │ │  IA    │ │
│  └──────────────┘ └──────────────┘ └────────┘ │
│                                                │
│  (Click any button to select and proceed)     │
│                                                │
└────────────────────────────────────────────────┘
```

### SCREEN 2: Difficulty Selection
```
┌────────────────────────────────────────────────┐
│                    TEEKO                       │
│                                                │
│               Player vs AI                     │
│                                                │
│            Select Difficulty                   │
│                                                │
│  ┌──────────────┐ ┌──────────────┐ ┌────────┐ │
│  │  EASY        │ │  MEDIUM      │ │ HARD   │ │
│  │ (Débutant)   │ │(Intermédiaire)│(Expert) │ │
│  └──────────────┘ └──────────────┘ └────────┘ │
│                                                │
│                             [Back]             │
│                                                │
└────────────────────────────────────────────────┘
```

### SCREEN 3: Names Input
```
┌────────────────────────────────────────────────┐
│                    TEEKO                       │
│                                                │
│      Player vs AI - Intermédiaire              │
│                                                │
│           Enter Player Names                   │
│                                                │
│  Your Name: [                            |     │
│             (Enter your name here)             │
│                                                │
│  ┌─────────────────────────────────────────┐  │
│  │            Start Game               │Back│  │
│  └─────────────────────────────────────────┘  │
│                                                │
└────────────────────────────────────────────────┘
```

## Game Board Display

```
┌──────────────────────────────────────────────┐
│ Player 1 ●    |  Turn: Player 1  |  ● Player2 │  ← Status Bar
│ [Active border highlight]                   │     (90px height)
├──────────────────────────────────────────────┤
│                                              │
│            ●  ●  ●  ●  ●                   │
│            ●  ●  ●  ●  ●                   │
│            ●  ●  ●  ●  ●                   │
│            ●  ●  ●  ●  ●                   │
│            ●  ●  ●  ●  ●                   │
│                                              │
│  (Red piece = Player 1)                     │
│  (Blue piece = Player 2)                    │
│  (Black dots = empty positions)             │
│                                              │
└──────────────────────────────────────────────┘
     ▲
     └── Game area (600x800 window, less banner)
```

## Status Bar (Banner) Design

```
┌────────────────────────────────────────────────────────────┐
│ Player1 ●     │     Placement Phase - Player 1's Turn      │     ● Player2 │
│ ■■■■■■■                                                   ■■■■■■■        │
│ (Red border = Active player)     (Centered text)    (Blue border)         │
│  16px circle (piece)                                        16px circle   │
│   name text (28px bold)                          name text (28px bold)    │
└────────────────────────────────────────────────────────────┘
  └─ Height: 90px ─────────────────────────────────────────────┘
```

## Color Palette (current dark theme)

### Primary Colors
```
┌──────────────────────────────────────┐
│ Surfaces:    ■ dark slate (e.g. 28,34,36)
│ Text:        ■ light ivory (e.g. 245,245,240)
│ Player 1:    ■ muted red
│ Player 2:    ■ muted blue
│ Accents:     ■ soft gold (e.g. 200,150,35)
└──────────────────────────────────────┘

### Button Colors (darker surfaces)
┌──────────────────────────────────────┐
│ Normal:      ■ (50, 56, 52)
│ Hover:       ■ (70, 76, 72)
│ Active:      ■ (90,100,92)
│ Border:      ■ (28, 32, 30)
└──────────────────────────────────────┘

### Text Colors
┌──────────────────────────────────────┐
│ Primary:     ■ (245, 245, 240) LIGHT
│ Secondary:   ■ (190, 195, 190) SOFT
│ Placeholder: ■ (150, 150, 150) MUTED
│ Disabled:    ■ (100, 100, 100) DARK
└──────────────────────────────────────┘
```

## Typography Hierarchy

```
TITLE (72px bold)
    ▲
    │
SECTION HEADER (44px bold)
    ▲
    │
BODY TEXT (38px)
    ▲
    │
SMALL TEXT (32px)
    ▲
    │
TINY TEXT (26px)
```

### Font Usage
- **72px**: "TEEKO" title
- **44px**: Section headers ("Select Game Mode", etc.)
- **38px**: Button text, main labels
- **32px**: Labels, player names, smaller content
- **26px**: Small text, additional info

## Button Design

### Standard Button
```
┌────────────────────────────┐
│  Button Text (centered)    │  ← 38px font
│  (80, 80, 120)             │  ← Normal color
│  2px white border          │  ← Border color
└────────────────────────────┘
  └─ 10px border radius ─┘
```

### Hover State
```
┌────────────────────────────┐
│  Button Text (centered)    │  ← Lighter/highlighted
│  (100, 100, 150)           │  ← Hover color
│  2px white border          │
└────────────────────────────┘
  Slightly lightened appearance
```

### Active/Selected State
```
┌────────────────────────────┐
│  Button Text (centered)    │  ← Green tint
│  (120, 180, 100)           │  ← Active color
│  2px white border          │
└────────────────────────────┘
  Green indicates selection
```

## Text Input Field Design

```
┌────────────────────────────────────────┐
│ [Enter your name here]|                │  ← 32px font
│ (50, 50, 70) background                │  ← Dark background
│ 2px white border                       │  ← Border
│ Blinking cursor when active            │
└────────────────────────────────────────┘
  └─ 6px border radius ─┘
```

## Message Box Design

```
            ┌─────────────────────────────┐
            │ 3px gold border             │
            │ (255, 200, 0)               │
            │                             │
            │    Message Text (36px)      │
            │    (255, 255, 255)          │
            │                             │
            │ Black background (50% alpha)│
            │                             │
            └─────────────────────────────┘
              └─ 12px border radius ─┘
```

## Victory Overlay Design

```
┌─────────────────────────────────────────────┐
│                                             │
│  [Semi-transparent black overlay]           │
│   (100% alpha coverage)                     │
│                                             │
│          "PLAYER NAME WINS!"                │
│          (48px bold, gold)                  │
│          (255, 200, 0)                      │
│                                             │
│  "Press ESC to exit or wait..."             │
│  (24px normal, gray)                        │
│  (200, 200, 200)                            │
│                                             │
└─────────────────────────────────────────────┘
```

## Window Layout (1280x720)

```
┌────────────────────────────────────────────────────┐
│                 1280px wide                        │
│ ┌──────────────────────────────────────────────┐  │
│ │ STATUS BAR (90px)                            │  │
│ │ - Player names, colors, current turn        │  │
│ │ - Phase indicator                           │  │
│ ├──────────────────────────────────────────────┤  │
│ │                                              │  │
│ │         GAME BOARD AREA (centered)           │  │
│ │                                              │  │
│ │         5x5 Grid with pieces                │  │
│ │         Messages overlay on center          │  │
│ │                                              │  │
│ │                                              │  │
│ └──────────────────────────────────────────────┘  │
│ 720px tall                                         │
└────────────────────────────────────────────────────┘

**Notes:** The window is resizable; UI elements reposition dynamically. An `Exit` button is present at the top-right at all times. Pressing `R` restarts the current game while keeping the same players and difficulty.
```

## Interaction Flow Chart

```
                    GAME START
                        │
                        ▼
            ┌─────────────────────┐
            │  PLACEMENT PHASE    │
            │  (Both players)     │
            └────────┬────────────┘
                     │
           4 pieces placed per player
                     │
                     ▼
            ┌─────────────────────┐
            │  MOVEMENT PHASE     │
            │  (Alternating turns)│
            └────────┬────────────┘
                     │
          Four in a row achieved
                     │
                     ▼
            ┌─────────────────────┐
            │  GAME OVER          │
            │  Victory screen     │
            └─────────┬───────────┘
                      │
                    ESC Key
                      │
                      ▼
                  MAIN MENU
```

---

This visual specification provides a complete reference for the UI/UX design of the enhanced Teeko game.
