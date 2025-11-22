"""
MoveRecord dataclass for tracking individual moves in the game.
"""
from dataclasses import dataclass
from typing import Optional

from model.position import Position


@dataclass
class MoveRecord:
    """
    Represents a single move in the chess game.
    
    Attributes:
        move_number: The move number in the game (1, 2, 3, ...)
        player: The player who made the move ('white' or 'black')
        piece_type: The type of piece moved ('P', 'N', 'B', 'R', 'Q', 'K')
        start: Starting position of the move
        end: Ending position of the move
        captured_piece: Type of piece captured, if any
        is_check: Whether this move puts opponent in check
        is_checkmate: Whether this move results in checkmate
        is_castling: Whether this move is a castling move
        is_en_passant: Whether this move is an en passant capture
        algebraic_notation: The move in standard algebraic notation
        timestamp: Unix timestamp when the move was made
    """
    move_number: int
    player: str
    piece_type: str
    start: Position
    end: Position
    captured_piece: Optional[str] = None
    is_check: bool = False
    is_checkmate: bool = False
    is_castling: bool = False
    is_en_passant: bool = False
    algebraic_notation: str = ""
    timestamp: float = 0.0
    
    def __post_init__(self):
        """Validate move record data."""
        if self.player not in ['white', 'black']:
            raise ValueError(f"Player must be 'white' or 'black', got {self.player}")
        if self.piece_type not in ['P', 'N', 'B', 'R', 'Q', 'K']:
            raise ValueError(f"Invalid piece type: {self.piece_type}")
        if self.move_number < 1:
            raise ValueError(f"Move number must be positive, got {self.move_number}")
    
    def __repr__(self) -> str:
        """String representation of the move."""
        return f"Move {self.move_number}: {self.player} {self.algebraic_notation}"
