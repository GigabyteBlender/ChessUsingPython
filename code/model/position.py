"""
Position dataclass representing a position on the chess board.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Position:
    """
    Represents a position on the chess board.
    
    Attributes:
        row: Row index (0-7, where 0 is the top row for black)
        col: Column index (0-7, where 0 is the 'a' file)
    """
    row: int
    col: int
    
    def __post_init__(self):
        """Validate that position is within board bounds."""
        if not (0 <= self.row < 8):
            raise ValueError(f"Row must be between 0 and 7, got {self.row}")
        if not (0 <= self.col < 8):
            raise ValueError(f"Column must be between 0 and 7, got {self.col}")
    
    def to_algebraic(self) -> str:
        """
        Convert position to algebraic notation (e.g., 'e4').
        
        Returns:
            String in algebraic notation (file + rank)
        """
        file = chr(ord('a') + self.col)
        rank = str(8 - self.row)
        return f"{file}{rank}"
    
    @staticmethod
    def from_algebraic(notation: str) -> 'Position':
        """
        Create Position from algebraic notation (e.g., 'e4').
        
        Args:
            notation: String in algebraic notation (e.g., 'e4', 'a1')
            
        Returns:
            Position object
            
        Raises:
            ValueError: If notation is invalid
        """
        if len(notation) != 2:
            raise ValueError(f"Invalid algebraic notation: {notation}")
        
        file_char = notation[0].lower()
        rank_char = notation[1]
        
        if not ('a' <= file_char <= 'h'):
            raise ValueError(f"Invalid file in notation: {notation}")
        if not ('1' <= rank_char <= '8'):
            raise ValueError(f"Invalid rank in notation: {notation}")
        
        col = ord(file_char) - ord('a')
        row = 8 - int(rank_char)
        
        return Position(row, col)
    
    def is_valid(self) -> bool:
        """
        Check if position is within board bounds.
        
        Returns:
            True if position is valid, False otherwise
        """
        return 0 <= self.row < 8 and 0 <= self.col < 8
    
    def __eq__(self, other) -> bool:
        """Check equality with another Position."""
        if not isinstance(other, Position):
            return False
        return self.row == other.row and self.col == other.col
    
    def __hash__(self) -> int:
        """Make Position hashable for use in sets and dicts."""
        return hash((self.row, self.col))
    
    def __repr__(self) -> str:
        """String representation showing both coordinates and algebraic notation."""
        return f"Position({self.row}, {self.col}) [{self.to_algebraic()}]"
