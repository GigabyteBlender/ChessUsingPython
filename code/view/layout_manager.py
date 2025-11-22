"""
LayoutManager for organizing screen layout and coordinate transformations.
"""
import math
from typing import Tuple

import pygame

from constants import HEIGHT, SQUARE_SIZE, WIDTH


class LayoutManager:
    """
    Manages screen layout and coordinate transformations for the chess game.
    
    This class calculates the positions and sizes of all UI elements including
    the chess board, move history panel, captured pieces display, and status
    indicators. It also handles coordinate transformations for board rotation.
    
    Attributes:
        screen_width: Width of the game window
        screen_height: Height of the game window
        board_rect: Rectangle defining the chess board area
        move_history_rect: Rectangle for the move history panel
        captured_pieces_rect: Rectangle for captured pieces display
        status_rect: Rectangle for turn and check indicators
    """
    
    def __init__(self, screen_width: int = WIDTH, screen_height: int = HEIGHT):
        """
        Initialize the LayoutManager with screen dimensions.
        
        Args:
            screen_width: Width of the game window (default: WIDTH constant)
            screen_height: Height of the game window (default: HEIGHT constant)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Calculate optimal square size for this screen
        self.square_size = self._calculate_square_size()
        
        # Calculate layout for all UI elements
        self.board_rect: pygame.Rect = None
        self.move_history_rect: pygame.Rect = None
        self.captured_pieces_rect: pygame.Rect = None
        self.status_rect: pygame.Rect = None
        
        self.calculate_layout()
    
    def _calculate_square_size(self) -> int:
        """
        Calculate optimal square size to maximize board size while fitting on screen.
        
        Returns:
            Optimal square size in pixels
        """
        # Reserve space for UI elements
        # Move history panel: ~25% of width
        # Captured pieces: ~120px total height (60px top + 60px bottom)
        # Margins: ~40px total
        
        ui_width_ratio = 0.25  # 25% for move history
        captured_height = 120
        margin = 40
        
        # Calculate available space for board
        available_width = self.screen_width * (1 - ui_width_ratio) - margin
        available_height = self.screen_height - captured_height - margin
        
        # Board is 8x8 squares, so calculate max square size
        max_square_from_width = available_width / 8
        max_square_from_height = available_height / 8
        
        # Use the smaller of the two to ensure board fits
        optimal_square_size = min(max_square_from_width, max_square_from_height)
        
        # Ensure minimum size and round to integer
        return max(40, int(optimal_square_size))
    
    def calculate_layout(self):
        """
        Calculate positions and sizes for all UI elements.
        
        The layout is organized as follows:
        - Board: Centered vertically to match move history height
        - Move history: Right panel showing game moves
        - Captured pieces: Side panels (top and bottom of board area)
        """
        # Move history panel on the right side (calculate first to match its height)
        board_area_width = int(self.screen_width * 0.65)  # 65% for board area
        history_width = self.screen_width - board_area_width - 20  # 20px margin
        history_height = self.screen_height - 40  # 20px margin top and bottom
        history_x = board_area_width + 10
        history_y = 20
        
        self.move_history_rect = pygame.Rect(
            history_x, history_y, history_width, history_height
        )
        
        # Board dimensions (8x8 squares)
        board_size = self.square_size * 8
        
        # Captured pieces dimensions
        captured_height = 60
        
        # Calculate total height needed for board + captured pieces
        total_board_height = board_size + (captured_height * 2) + 20  # 20px spacing
        
        # Center the board+captured pieces vertically to match move history
        board_area_y = history_y + (history_height - total_board_height) // 2
        
        # Calculate board position (centered horizontally in left portion)
        board_x = (board_area_width - board_size) // 2
        board_y = board_area_y + captured_height + 10  # Below top captured pieces
        
        self.board_rect = pygame.Rect(board_x, board_y, board_size, board_size)
        
        # Captured pieces display (above and below the board)
        captured_width = board_size
        captured_x = board_x
        
        # Top captured pieces (for pieces captured by black)
        captured_top_y = board_y - captured_height - 10
        
        # Bottom captured pieces (for pieces captured by white)
        captured_bottom_y = board_y + board_size + 10
        
        # Store both as a dict for easy access
        self.captured_pieces_rect = {
            'top': pygame.Rect(captured_x, captured_top_y, captured_width, captured_height),
            'bottom': pygame.Rect(captured_x, captured_bottom_y, captured_width, captured_height)
        }
        
        # Status rect is no longer used but keep for compatibility
        self.status_rect = pygame.Rect(0, 0, 0, 0)
    
    def transform_coordinates(self, pos: Tuple[int, int], rotation: float) -> Tuple[int, int]:
        """
        Transform screen coordinates based on board rotation.
        
        This method handles coordinate transformation when the board is rotated
        (e.g., during board flip animation). It rotates coordinates around the
        center of the board.
        
        Args:
            pos: Screen coordinates (x, y) to transform
            rotation: Rotation angle in degrees (0 or 180 for normal play)
            
        Returns:
            Transformed coordinates (x, y)
        """
        if rotation == 0.0:
            # No rotation, return original coordinates
            return pos
        
        x, y = pos
        
        # Calculate board center
        center_x = self.board_rect.centerx
        center_y = self.board_rect.centery
        
        # Translate to origin (board center)
        translated_x = x - center_x
        translated_y = y - center_y
        
        # Convert rotation to radians
        angle_rad = math.radians(rotation)
        
        # Apply rotation transformation
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        
        rotated_x = translated_x * cos_angle - translated_y * sin_angle
        rotated_y = translated_x * sin_angle + translated_y * cos_angle
        
        # Translate back to board position
        final_x = rotated_x + center_x
        final_y = rotated_y + center_y
        
        return (int(final_x), int(final_y))
    
    def get_board_center(self) -> Tuple[int, int]:
        """
        Get the center coordinates of the board.
        
        Returns:
            Tuple of (x, y) coordinates for the board center
        """
        return (self.board_rect.centerx, self.board_rect.centery)
    
    def is_within_board(self, pos: Tuple[int, int]) -> bool:
        """
        Check if screen coordinates are within the board area.
        
        Args:
            pos: Screen coordinates (x, y) to check
            
        Returns:
            True if coordinates are within board bounds, False otherwise
        """
        return self.board_rect.collidepoint(pos)
    
    def get_square_at_position(self, pos: Tuple[int, int], rotation: float = 0.0) -> Tuple[int, int]:
        """
        Convert screen coordinates to board square indices.
        
        Args:
            pos: Screen coordinates (x, y)
            rotation: Current board rotation in degrees
            
        Returns:
            Tuple of (row, col) for the board square, or None if outside board
        """
        # First check if position is within board
        if not self.is_within_board(pos):
            return None
        
        # Transform coordinates if board is rotated
        if rotation != 0.0:
            pos = self.transform_coordinates(pos, -rotation)  # Inverse rotation
        
        x, y = pos
        
        # Calculate relative position within board
        rel_x = x - self.board_rect.x
        rel_y = y - self.board_rect.y
        
        # Convert to square indices
        col = rel_x // SQUARE_SIZE
        row = rel_y // SQUARE_SIZE
        
        # Ensure within bounds
        if 0 <= row < 8 and 0 <= col < 8:
            return (int(row), int(col))
        
        return None
    
    def get_square_screen_position(self, row: int, col: int, rotation: float = 0.0) -> Tuple[int, int]:
        """
        Convert board square indices to screen coordinates (top-left of square).
        
        Args:
            row: Board row index (0-7)
            col: Board column index (0-7)
            rotation: Current board rotation in degrees
            
        Returns:
            Tuple of (x, y) screen coordinates for the top-left of the square
        """
        # Calculate base position (no rotation)
        x = self.board_rect.x + col * SQUARE_SIZE
        y = self.board_rect.y + row * SQUARE_SIZE
        
        # Apply rotation if needed
        if rotation != 0.0:
            x, y = self.transform_coordinates((x, y), rotation)
        
        return (x, y)
    
    def get_square_center_position(self, row: int, col: int, rotation: float = 0.0) -> Tuple[int, int]:
        """
        Convert board square indices to screen coordinates (center of square).
        
        Args:
            row: Board row index (0-7)
            col: Board column index (0-7)
            rotation: Current board rotation in degrees
            
        Returns:
            Tuple of (x, y) screen coordinates for the center of the square
        """
        # Calculate base position (no rotation)
        x = self.board_rect.x + col * SQUARE_SIZE + SQUARE_SIZE // 2
        y = self.board_rect.y + row * SQUARE_SIZE + SQUARE_SIZE // 2
        
        # Apply rotation if needed
        if rotation != 0.0:
            x, y = self.transform_coordinates((x, y), rotation)
        
        return (x, y)
