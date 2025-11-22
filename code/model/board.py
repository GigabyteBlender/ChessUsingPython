"""
Board class representing the chess board and piece positions.
"""
from typing import List, Optional, Tuple

from model.piece import Bishop, King, Knight, Pawn, Piece, Queen, Rook
from model.position import Position


class Board:
    """
    Represents the chess board and piece positions.
    
    The board is an 8x8 grid where:
    - Row 0 is the top (black's back rank)
    - Row 7 is the bottom (white's back rank)
    - Column 0 is the 'a' file
    - Column 7 is the 'h' file
    """
    
    def __init__(self):
        """Initialize an empty 8x8 board."""
        self.grid: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
    
    def get_piece(self, position: Position) -> Optional[Piece]:
        """
        Get the piece at the specified position.
        
        Args:
            position: The position to check
            
        Returns:
            The Piece at that position, or None if empty
        """
        if not position.is_valid():
            return None
        return self.grid[position.row][position.col]
    
    def set_piece(self, position: Position, piece: Optional[Piece]):
        """
        Place or remove a piece at the specified position.
        
        Args:
            position: The position to modify
            piece: The piece to place, or None to clear the square
        """
        if not position.is_valid():
            raise ValueError(f"Invalid position: {position}")
        
        self.grid[position.row][position.col] = piece
        
        # Update the piece's position if placing a piece
        if piece is not None:
            piece.position = position
    
    def move_piece(self, start: Position, end: Position) -> Optional[Piece]:
        """
        Move a piece from start to end position.
        
        Args:
            start: Starting position
            end: Destination position
            
        Returns:
            The captured piece if any, or None
            
        Raises:
            ValueError: If there's no piece at the start position
        """
        piece = self.get_piece(start)
        if piece is None:
            raise ValueError(f"No piece at position {start}")
        
        # Get any piece being captured
        captured_piece = self.get_piece(end)
        
        # Move the piece
        self.set_piece(end, piece)
        self.set_piece(start, None)
        
        # Mark that the piece has moved
        piece.has_moved = True
        
        return captured_piece
    
    def find_king(self, color: str) -> Optional[Position]:
        """
        Find the position of the king for the specified color.
        
        Args:
            color: 'white' or 'black'
            
        Returns:
            Position of the king, or None if not found
        """
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and isinstance(piece, King) and piece.color == color:
                    return Position(row, col)
        return None
    
    def get_all_pieces(self, color: str) -> List[Tuple[Position, Piece]]:
        """
        Get all pieces of the specified color.
        
        Args:
            color: 'white' or 'black'
            
        Returns:
            List of tuples (Position, Piece) for all pieces of that color
        """
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None and piece.color == color:
                    pieces.append((Position(row, col), piece))
        return pieces
    
    def copy(self) -> 'Board':
        """
        Create a deep copy of the board for move simulation.
        
        Returns:
            A new Board instance with copied pieces
        """
        new_board = Board()
        
        for row in range(8):
            for col in range(8):
                piece = self.grid[row][col]
                if piece is not None:
                    # Create a copy of the piece
                    new_piece = piece.copy()
                    new_board.grid[row][col] = new_piece
        
        return new_board
    
    def setup_initial_position(self):
        """
        Set up the standard chess starting position.
        """
        # Black pieces (row 0 and 1)
        self.set_piece(Position(0, 0), Rook('black', Position(0, 0)))
        self.set_piece(Position(0, 1), Knight('black', Position(0, 1)))
        self.set_piece(Position(0, 2), Bishop('black', Position(0, 2)))
        self.set_piece(Position(0, 3), Queen('black', Position(0, 3)))
        self.set_piece(Position(0, 4), King('black', Position(0, 4)))
        self.set_piece(Position(0, 5), Bishop('black', Position(0, 5)))
        self.set_piece(Position(0, 6), Knight('black', Position(0, 6)))
        self.set_piece(Position(0, 7), Rook('black', Position(0, 7)))
        
        for col in range(8):
            self.set_piece(Position(1, col), Pawn('black', Position(1, col)))
        
        # White pieces (row 6 and 7)
        for col in range(8):
            self.set_piece(Position(6, col), Pawn('white', Position(6, col)))
        
        self.set_piece(Position(7, 0), Rook('white', Position(7, 0)))
        self.set_piece(Position(7, 1), Knight('white', Position(7, 1)))
        self.set_piece(Position(7, 2), Bishop('white', Position(7, 2)))
        self.set_piece(Position(7, 3), Queen('white', Position(7, 3)))
        self.set_piece(Position(7, 4), King('white', Position(7, 4)))
        self.set_piece(Position(7, 5), Bishop('white', Position(7, 5)))
        self.set_piece(Position(7, 6), Knight('white', Position(7, 6)))
        self.set_piece(Position(7, 7), Rook('white', Position(7, 7)))
    
    def __repr__(self) -> str:
        """String representation of the board for debugging."""
        lines = []
        for row in range(8):
            line = []
            for col in range(8):
                piece = self.grid[row][col]
                if piece is None:
                    line.append('.')
                else:
                    line.append(piece.get_sprite_name())
            lines.append(' '.join(line))
        return '\n'.join(lines)
