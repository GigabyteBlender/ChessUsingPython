"""
Piece classes representing chess pieces with their movement rules.
"""
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, List

from model.position import Position

if TYPE_CHECKING:
    from model.board import Board


class Piece(ABC):
    """
    Abstract base class for all chess pieces.
    
    Attributes:
        color: 'white' or 'black'
        position: Current position on the board
        has_moved: Whether the piece has moved (important for castling and pawn double-move)
        piece_type: Single character representing piece type (P, R, N, B, Q, K)
    """
    
    def __init__(self, color: str, position: Position):
        """
        Initialize a chess piece.
        
        Args:
            color: 'white' or 'black'
            position: Initial position on the board
        """
        if color not in ('white', 'black'):
            raise ValueError(f"Invalid color: {color}. Must be 'white' or 'black'")
        
        self.color = color
        self.position = position
        self.has_moved = False
        self.piece_type = self._get_piece_type()
    
    @abstractmethod
    def _get_piece_type(self) -> str:
        """Return the piece type character (P, R, N, B, Q, K)."""
        pass
    
    @abstractmethod
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        """
        Get all possible moves for this piece (not considering check).
        
        Args:
            board: The current board state
            
        Returns:
            List of Position objects representing possible destination squares
        """
        pass
    
    def get_sprite_name(self) -> str:
        """
        Return the sprite name for rendering (e.g., 'wK', 'bP').
        
        Returns:
            String in format: color_initial + piece_type (e.g., 'wK' for white king)
        """
        color_char = 'w' if self.color == 'white' else 'b'
        return f"{color_char}{self.piece_type}"
    
    def copy(self) -> 'Piece':
        """
        Create a copy of this piece.
        
        Returns:
            A new Piece instance with the same attributes
        """
        piece_class = self.__class__
        new_piece = piece_class(self.color, self.position)
        new_piece.has_moved = self.has_moved
        return new_piece
    
    def __repr__(self) -> str:
        """String representation of the piece."""
        return f"{self.__class__.__name__}({self.color}, {self.position})"


class Pawn(Piece):
    """Pawn piece with forward movement and diagonal capture."""
    
    def _get_piece_type(self) -> str:
        return 'P'
    
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        """
        Get possible pawn moves including forward movement and diagonal captures.
        Does not include en passant (handled separately by MoveValidator).
        """
        moves = []
        direction = -1 if self.color == 'white' else 1  # White moves up (decreasing row)
        
        # Forward movement (one square)
        forward_row = self.position.row + direction
        if 0 <= forward_row < 8:
            forward_one = Position(forward_row, self.position.col)
            if board.get_piece(forward_one) is None:
                moves.append(forward_one)
                
                # Forward movement (two squares from starting position)
                if not self.has_moved:
                    forward_two_row = self.position.row + 2 * direction
                    if 0 <= forward_two_row < 8:
                        forward_two = Position(forward_two_row, self.position.col)
                        if board.get_piece(forward_two) is None:
                            moves.append(forward_two)
        
        # Diagonal captures
        for col_offset in [-1, 1]:
            capture_row = self.position.row + direction
            capture_col = self.position.col + col_offset
            if 0 <= capture_row < 8 and 0 <= capture_col < 8:
                capture_pos = Position(capture_row, capture_col)
                target_piece = board.get_piece(capture_pos)
                if target_piece is not None and target_piece.color != self.color:
                    moves.append(capture_pos)
        
        return moves


class Rook(Piece):
    """Rook piece with horizontal and vertical movement."""
    
    def _get_piece_type(self) -> str:
        return 'R'
    
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        """Get possible rook moves (horizontal and vertical lines)."""
        moves = []
        
        # Four directions: up, down, left, right
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for dr, dc in directions:
            row, col = self.position.row + dr, self.position.col + dc
            
            while 0 <= row < 8 and 0 <= col < 8:
                pos = Position(row, col)
                target_piece = board.get_piece(pos)
                
                if target_piece is None:
                    moves.append(pos)
                else:
                    # Can capture opponent's piece
                    if target_piece.color != self.color:
                        moves.append(pos)
                    break  # Can't move past any piece
                
                row += dr
                col += dc
        
        return moves


class Knight(Piece):
    """Knight piece with L-shaped movement."""
    
    def _get_piece_type(self) -> str:
        return 'N'
    
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        """Get possible knight moves (L-shaped: 2+1 or 1+2)."""
        moves = []
        
        # All possible L-shaped moves
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dr, dc in knight_moves:
            row, col = self.position.row + dr, self.position.col + dc
            
            if 0 <= row < 8 and 0 <= col < 8:
                pos = Position(row, col)
                target_piece = board.get_piece(pos)
                
                # Can move to empty square or capture opponent's piece
                if target_piece is None or target_piece.color != self.color:
                    moves.append(pos)
        
        return moves


class Bishop(Piece):
    """Bishop piece with diagonal movement."""
    
    def _get_piece_type(self) -> str:
        return 'B'
    
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        """Get possible bishop moves (diagonal lines)."""
        moves = []
        
        # Four diagonal directions
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dr, dc in directions:
            row, col = self.position.row + dr, self.position.col + dc
            
            while 0 <= row < 8 and 0 <= col < 8:
                pos = Position(row, col)
                target_piece = board.get_piece(pos)
                
                if target_piece is None:
                    moves.append(pos)
                else:
                    # Can capture opponent's piece
                    if target_piece.color != self.color:
                        moves.append(pos)
                    break  # Can't move past any piece
                
                row += dr
                col += dc
        
        return moves


class Queen(Piece):
    """Queen piece combining rook and bishop movement."""
    
    def _get_piece_type(self) -> str:
        return 'Q'
    
    def get_possible_moves(self, board: 'Board') -> List[Position]:
        """Get possible queen moves (horizontal, vertical, and diagonal lines)."""
        moves = []
        
        # Eight directions: four straight + four diagonal
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Straight (rook-like)
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal (bishop-like)
        ]
        
        for dr, dc in directions:
            row, col = self.position.row + dr, self.position.col + dc
            
            while 0 <= row < 8 and 0 <= col < 8:
                pos = Position(row, col)
                target_piece = board.get_piece(pos)
                
                if target_piece is None:
                    moves.append(pos)
                else:
                    # Can capture opponent's piece
                    if target_piece.color != self.color:
                        moves.append(pos)
                    break  # Can't move past any piece
                
                row += dr
                col += dc
        
        return moves


class King(Piece):
    """King piece with one-square movement in any direction."""
    
    def _get_piece_type(self) -> str:
        return 'K'
    
    def get_possible_moves(self, board: 'Board', include_castling: bool = True) -> List[Position]:
        """
        Get possible king moves (one square in any direction).
        Includes castling moves if conditions are met and include_castling is True.
        
        Args:
            board: The current board state
            include_castling: Whether to include castling moves (default True).
                             Set to False when checking for attacks to avoid infinite recursion.
        """
        moves = []
        
        # Eight directions: one square in any direction
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),  # Straight
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # Diagonal
        ]
        
        for dr, dc in directions:
            row, col = self.position.row + dr, self.position.col + dc
            
            if 0 <= row < 8 and 0 <= col < 8:
                pos = Position(row, col)
                target_piece = board.get_piece(pos)
                
                # Can move to empty square or capture opponent's piece
                if target_piece is None or target_piece.color != self.color:
                    moves.append(pos)
        
        # Add castling moves if the king hasn't moved and we should include them
        if include_castling and not self.has_moved:
            # Import here to avoid circular dependency
            from model.move_validator import MoveValidator
            validator = MoveValidator()
            
            # Check for kingside castling (rook on column 7)
            kingside_rook_pos = Position(self.position.row, 7)
            if validator.can_castle(board, self.position, kingside_rook_pos):
                # King moves 2 squares to the right
                castling_pos = Position(self.position.row, self.position.col + 2)
                moves.append(castling_pos)
            
            # Check for queenside castling (rook on column 0)
            queenside_rook_pos = Position(self.position.row, 0)
            if validator.can_castle(board, self.position, queenside_rook_pos):
                # King moves 2 squares to the left
                castling_pos = Position(self.position.row, self.position.col - 2)
                moves.append(castling_pos)
        
        return moves
