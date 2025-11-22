"""
Shared constants for the chess game.
"""

# Window and board dimensions
WIDTH = 1200
HEIGHT = 900
SQUARE_SIZE = 80  # Fixed square size for consistent board
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 217, 181)  # Light square color - slightly warmer
DARK_BROWN = (181, 136, 99)    # Dark square color - better contrast
HIGHLIGHT_COLOR = (255, 255, 102)  # Selected piece highlight - brighter yellow
CHECK_COLOR = (220, 20, 60)  # Check indicator color - crimson red
LEGAL_MOVE_COLOR = (100, 150, 100)  # Legal move highlight - darker green for better visibility
CAPTURE_MOVE_COLOR = (220, 50, 50)  # Capture move highlight - darker red for better contrast
LAST_MOVE_COLOR = (170, 162, 58)  # Last move highlight - more saturated for visibility

# Player colors
COLOR_WHITE = 'white'
COLOR_BLACK = 'black'

# Piece values for material calculation (standard chess values)
PIECE_VALUES = {
    'P': 1,  # Pawn
    'N': 3,  # Knight
    'B': 3,  # Bishop
    'R': 5,  # Rook
    'Q': 9,  # Queen
    'K': 0   # King (not counted in material)
}

# Piece types
PIECE_PAWN = 'P'
PIECE_KNIGHT = 'N'
PIECE_BISHOP = 'B'
PIECE_ROOK = 'R'
PIECE_QUEEN = 'Q'
PIECE_KING = 'K'

# Animation settings
BOARD_FLIP_DURATION_MS = 500  # Duration for board flip animation
