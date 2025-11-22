"""
BoardRenderer for rendering the chess board and pieces with proper orientation.
"""
from typing import Dict, List, Optional, Tuple

import pygame

from constants import (
    CAPTURE_MOVE_COLOR,
    DARK_BROWN,
    HIGHLIGHT_COLOR,
    LAST_MOVE_COLOR,
    LEGAL_MOVE_COLOR,
    LIGHT_BROWN,
    SQUARE_SIZE,
)
from model.board import Board
from model.position import Position


class BoardRenderer:
    """
    Renders the chess board and pieces with proper orientation.
    
    This class handles all visual rendering of the chess board including:
    - Drawing the checkerboard pattern
    - Rendering pieces with rotation support
    - Highlighting selected pieces and legal moves
    - Distinguishing capture moves from regular moves
    - Handling coordinate transformations for board rotation
    
    Attributes:
        screen: Pygame surface to render on
        piece_images: Dictionary mapping piece sprite names to loaded images
        board_orientation: Current rotation angle in degrees (0 or 180)
        square_size: Size of each square in pixels
        board_rect: Rectangle defining the board area on screen
    """
    
    def __init__(self, screen: pygame.Surface, piece_images: Dict[str, pygame.Surface], 
                 board_rect: pygame.Rect, square_size: int = SQUARE_SIZE):
        """
        Initialize the BoardRenderer.
        
        Args:
            screen: Pygame surface to render on
            piece_images: Dictionary mapping piece names (e.g., 'wK', 'bP') to images
            board_rect: Rectangle defining the board area on screen
            square_size: Size of each square in pixels
        """
        self.screen = screen
        self.piece_images = piece_images
        self.board_rect = board_rect
        self.board_orientation = 0.0  # Rotation angle in degrees
        self.square_size = square_size
    
    def set_orientation(self, angle: float):
        """
        Set the board orientation angle.
        
        Args:
            angle: Rotation angle in degrees (typically 0 or 180)
        """
        self.board_orientation = angle
    
    def render(self, board: Board, selected_pos: Optional[Position] = None,
               legal_moves: Optional[List[Position]] = None,
               last_move: Optional[Tuple[Position, Position]] = None,
               hover_pos: Optional[Position] = None):
        """
        Render the complete board with highlights.
        
        Args:
            board: The current board state
            selected_pos: Position of the selected piece (if any)
            legal_moves: List of legal move positions for the selected piece
            last_move: Tuple of (start, end) positions for the last move
            hover_pos: Position being hovered over (if any)
        """
        # Draw the checkerboard pattern
        self.draw_squares()
        
        # Highlight last move if provided
        if last_move is not None:
            start_pos, end_pos = last_move
            self.highlight_square(start_pos, LAST_MOVE_COLOR)
            self.highlight_square(end_pos, LAST_MOVE_COLOR)
        
        # Highlight selected piece
        if selected_pos is not None:
            self.highlight_square(selected_pos, HIGHLIGHT_COLOR)
        
        # Highlight legal moves
        if legal_moves is not None and len(legal_moves) > 0:
            self.highlight_legal_moves(legal_moves, board, hover_pos)
        
        # Draw all pieces
        self.draw_pieces(board)
    
    def draw_squares(self):
        """
        Draw the checkerboard pattern.
        
        Draws an 8x8 checkerboard with alternating light and dark squares.
        The pattern starts with a light square in the top-left (a8).
        """
        for row in range(8):
            for col in range(8):
                # Determine square color (light squares on even sum of row+col)
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                
                # Get visual row/col based on orientation
                if self.board_orientation == 180:
                    visual_row = 7 - row
                    visual_col = 7 - col
                else:
                    visual_row = row
                    visual_col = col
                
                # Calculate screen position
                x = self.board_rect.x + visual_col * self.square_size
                y = self.board_rect.y + visual_row * self.square_size
                
                # Draw the square
                rect = pygame.Rect(x, y, self.square_size, self.square_size)
                pygame.draw.rect(self.screen, color, rect)
    
    def draw_pieces(self, board: Board):
        """
        Draw all pieces considering current orientation.
        
        Args:
            board: The current board state
        """
        for row in range(8):
            for col in range(8):
                position = Position(row, col)
                piece = board.get_piece(position)
                
                if piece is not None:
                    # Get the piece image
                    sprite_name = piece.get_sprite_name()
                    if sprite_name in self.piece_images:
                        piece_image = self.piece_images[sprite_name]
                        
                        # Get screen position for this piece
                        screen_pos = self.get_screen_position(position)
                        
                        # Center the piece in the square
                        piece_rect = piece_image.get_rect()
                        piece_rect.center = (
                            screen_pos[0] + self.square_size // 2,
                            screen_pos[1] + self.square_size // 2
                        )
                        
                        # Always draw pieces upright (no rotation)
                        self.screen.blit(piece_image, piece_rect)
    
    def highlight_square(self, position: Position, color: Tuple[int, int, int], 
                        alpha: int = 128):
        """
        Highlight a specific square with the given color.
        
        Args:
            position: Board position to highlight
            color: RGB color tuple for the highlight
            alpha: Transparency level (0-255, default 128 for 50% transparency)
        """
        if not position.is_valid():
            return
        
        # Get screen position
        screen_pos = self.get_screen_position(position)
        
        # Create a semi-transparent surface for the highlight
        highlight_surface = pygame.Surface((self.square_size, self.square_size))
        highlight_surface.set_alpha(alpha)
        highlight_surface.fill(color)
        
        # Blit the highlight
        self.screen.blit(highlight_surface, screen_pos)
    
    def highlight_legal_moves(self, positions: List[Position], board: Board, 
                             hover_pos: Optional[Position] = None):
        """
        Highlight legal move destinations with different colors for captures.
        
        Args:
            positions: List of legal move positions
            board: Current board state (to check for captures)
            hover_pos: Position being hovered over (for enhanced feedback)
        """
        for position in positions:
            if not position.is_valid():
                continue
            
            # Check if this move would be a capture
            target_piece = board.get_piece(position)
            is_capture = target_piece is not None
            
            # Check if this is the hovered position
            is_hovered = hover_pos is not None and position == hover_pos
            
            # Use different color for capture moves
            color = CAPTURE_MOVE_COLOR if is_capture else LEGAL_MOVE_COLOR
            
            # Get screen position
            screen_pos = self.get_screen_position(position)
            
            # Add hover effect - brighter highlight
            if is_hovered:
                hover_color = (255, 255, 255)  # White highlight for hover
                self.highlight_square(position, hover_color, alpha=100)
            
            # Draw a circle in the center of the square for non-captures
            # Draw a border for captures
            if is_capture:
                # Draw a thick border around the square
                rect = pygame.Rect(
                    screen_pos[0], screen_pos[1],
                    self.square_size, self.square_size
                )
                border_width = 6 if is_hovered else 4  # Thicker border on hover
                pygame.draw.rect(self.screen, color, rect, border_width)
            else:
                # Draw a circle in the center
                center_x = screen_pos[0] + self.square_size // 2
                center_y = screen_pos[1] + self.square_size // 2
                radius = (self.square_size // 5) if is_hovered else (self.square_size // 6)
                pygame.draw.circle(self.screen, color, (center_x, center_y), radius)
    
    def get_board_position(self, screen_pos: Tuple[int, int]) -> Optional[Position]:
        """
        Convert screen coordinates to board position considering orientation.
        
        Args:
            screen_pos: Screen coordinates (x, y)
            
        Returns:
            Position object if within board bounds, None otherwise
        """
        x, y = screen_pos
        
        # Check if position is within board bounds
        if not self.board_rect.collidepoint(x, y):
            return None
        
        # Calculate relative position within board
        rel_x = x - self.board_rect.x
        rel_y = y - self.board_rect.y
        
        # Convert to visual square indices
        visual_col = int(rel_x // self.square_size)
        visual_row = int(rel_y // self.square_size)
        
        # Ensure within bounds
        if not (0 <= visual_row < 8 and 0 <= visual_col < 8):
            return None
        
        # Convert visual position to board position based on orientation
        if self.board_orientation == 180:
            row = 7 - visual_row
            col = 7 - visual_col
        else:
            row = visual_row
            col = visual_col
        
        return Position(row, col)
    
    def get_screen_position(self, board_pos: Position) -> Tuple[int, int]:
        """
        Convert board position to screen coordinates (top-left of square).
        
        Args:
            board_pos: Board position
            
        Returns:
            Tuple of (x, y) screen coordinates for the top-left of the square
        """
        if not board_pos.is_valid():
            return (0, 0)
        
        # Get visual position based on orientation
        if self.board_orientation == 180:
            visual_row = 7 - board_pos.row
            visual_col = 7 - board_pos.col
        else:
            visual_row = board_pos.row
            visual_col = board_pos.col
        
        # Calculate screen position
        x = self.board_rect.x + visual_col * self.square_size
        y = self.board_rect.y + visual_row * self.square_size
        
        return (int(x), int(y))
