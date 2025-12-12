# config.py
# Paramètres globaux du jeu / UI (light modern theme)

# Fenêtre
WINDOW_WIDTH = 960
WINDOW_HEIGHT = 680
FPS = 60
# Window can be resized by user
WINDOW_RESIZABLE = True

# Banner / main surface background: darker surface for modern contrast
BANNER_BG = (30, 34, 36)  # dark slate background
# Banner rectangles size
BANNER_WIDTH = WINDOW_WIDTH
BANNER_HEIGHT = 90 

# Plateau
BOARD_ROWS = 5
CELL_SIZE = 110
MARGIN_X = WINDOW_WIDTH - BOARD_ROWS*CELL_SIZE - CELL_SIZE - 30    						# marge autour du plateau (px)
MARGIN_Y = WINDOW_HEIGHT - BOARD_ROWS*CELL_SIZE - CELL_SIZE + BANNER_HEIGHT +  30     # marge autour du plateau (px)

# Couleurs (R, G, B) - Muted light / modern palette (less bright)
BLACK = (28, 28, 30)
WHITE = (250, 250, 250)
GREEN = (60, 242, 80)
# Softer primary: muted teal/green
PRIMARY = (32, 100, 86)   # primary accent (muted green-teal)
# Muted accent (warmer, not neon)
ACCENT = (200, 150, 35)   # softer gold
# Slightly desaturated player colors
PLAYER1 = (170, 70, 70)   # muted red
PLAYER2 = (50, 100, 170)  # muted blue
GREY = (120, 120, 120)
LIGHT_GREY = (237, 240, 242)



# Backwards-compatible aliases for older code
# Many modules still expect `RED`/`BLUE` names — keep aliases to avoid crashes.
RED = PLAYER1
BLUE = PLAYER2

# Apparence
BOARD_BORDER_RADIUS = 8
GRID_LINE_WIDTH = 2
CELL_PADDING = 8    # espacement interne pour les surlignages
POINT_RADIUS = 20
POINT_RADIUS_EMPTY = 10

# Background
BACKGROUND_WIDTH = 400
BACKGROUND_HEIGHT = 600

# Menu overlay (to improve text readability over background image)
# Value from 0 (transparent) to 255 (opaque white)
MENU_OVERLAY_ALPHA = 230
# Use a dark overlay to gently dim the background (RGB)
MENU_OVERLAY_COLOR = (225, 225, 225)

# Button Colors (light theme)
# Muted button colors
# Darker button surfaces with lighter text
BUTTON_NORMAL = (225, 225, 225)
BUTTON_HOVER = (172, 243, 255)
BUTTON_ACTIVE = (20, 90, 120)
BUTTON_BORDER = (40, 90, 140)
BUTTON_EXIT = (180, 15, 15)
BUTTON_TEXT_COLOR = (40, 90, 140)#(220, 220, 215)

# Button size
BUTTON_WIDTH_LARGE = 250
BUTTON_WIDTH_SMALL = 180
BUTTON_WIDTH_SMALLV2 = 100
BUTTON_HEIGHT = 70
BUTTON_SPACING = 100
BUTTON_SPACING_SMALL = 50

# Text colors
TEXT_TITLE = (68, 178, 17)
TEXT_TITLE_SECONDARY = (196, 0, 0)
TEXT_PRIMARY = (10, 21, 61)
TEXT_SECONDARY = (190, 195, 190)

# Board grid colors and layout (light theme)
# Board background: subtle light green (muted)
BOARD_BG_COLOR = (5, 80, 23)  # dark muted green surface
# Grid color: subtle lighter lines to show cells
GRID_COLOR = (70, 80, 72)      # thin pale lines
GRID_LINE_WIDTH = 1               # thinner
# Default cell dimension (can be changed)
DEFAULT_CELL_SIZE = 100
CELL_RADIUS = 10

# ========== AUDIO ==========
# Enable/disable sound effects
ENABLE_SOUND = True


# Assets paths
from pathlib import Path
RESOURCE_PATH = Path(__file__).parent / "assets"

# Sound file paths (relative to project root)
SOUND_PATHS = {
    "pawn_move": "sounds/pawn_move.mp3",
    "victory": "sounds/victory.mp3",
    "defeat": "sounds/defeat.mp3",
    "victory_trumpet": "sounds/victory_trumpet.mp3"
}


# ========== AI SETTINGS ==========
# Default AI difficulty level
AI_DEFAULT_DIFFICULTY = "medium"  # options: 'easy', 'medium', 'hard'
# Mapping difficulty levels to search depths
AI_SEARCH_DEPTHS = {
	"easy": 1,
	"medium": 2,
	"hard": 3
}
# Time delay (ms) for AI "thinking" simulation
AI_THINKING_DELAY = 800  # milliseconds
# Time delay (ms) before showing victory/defeat message
AI_ENDGAME_DELAY = 1000  # milliseconds
# Maximum time (seconds) allowed for AI to make a move
AI_MAX_TIME_PER_MOVE = 5
# Minimum time (seconds) AI should take to make a move (for realism)
AI_MIN_TIME_PER_MOVE = 1.5
# Use opening book for AI moves in placement phase
AI_USE_OPENING_BOOK = True
# Path to AI opening book file
AI_OPENING_BOOK_PATH = RESOURCE_PATH / "ai" / "opening_book.json"