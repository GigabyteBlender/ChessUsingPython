"""
CapturedPieces dataclass for tracking captured pieces.
"""
from dataclasses import dataclass, field
from typing import Dict, List

from constants import PIECE_VALUES


@dataclass
class CapturedPieces:
    """
    Tracks captured pieces for both players.
    
    Attributes:
        white_captured: List of piece types captured by white (pieces that were black)
        black_captured: List of piece types captured by black (pieces that were white)
    """
    white_captured: List[str] = field(default_factory=list)
    black_captured: List[str] = field(default_factory=list)
    
    def add_capture(self, piece_type: str, captured_by: str) -> None:
        """
        Add a captured piece to the appropriate list.
        
        Args:
            piece_type: The type of piece captured ('P', 'N', 'B', 'R', 'Q', 'K')
            captured_by: The color that captured the piece ('white' or 'black')
            
        Raises:
            ValueError: If captured_by is not 'white' or 'black'
        """
        if captured_by not in ['white', 'black']:
            raise ValueError(f"captured_by must be 'white' or 'black', got {captured_by}")
        
        if piece_type not in ['P', 'N', 'B', 'R', 'Q', 'K']:
            raise ValueError(f"Invalid piece type: {piece_type}")
        
        if captured_by == 'white':
            self.white_captured.append(piece_type)
        else:
            self.black_captured.append(piece_type)
    
    def get_material_advantage(self) -> int:
        """
        Calculate material advantage using standard piece values.
        Positive value means white is ahead, negative means black is ahead.
        
        Returns:
            Integer representing material advantage (white - black)
        """
        white_material = sum(PIECE_VALUES.get(piece, 0) for piece in self.white_captured)
        black_material = sum(PIECE_VALUES.get(piece, 0) for piece in self.black_captured)
        return white_material - black_material
    
    def get_captured_by_type(self, color: str) -> Dict[str, int]:
        """
        Get count of captured pieces grouped by type for a specific color.
        
        Args:
            color: The color that captured the pieces ('white' or 'black')
            
        Returns:
            Dictionary mapping piece type to count
        """
        if color not in ['white', 'black']:
            raise ValueError(f"color must be 'white' or 'black', got {color}")
        
        captured_list = self.white_captured if color == 'white' else self.black_captured
        
        counts: Dict[str, int] = {}
        for piece in captured_list:
            counts[piece] = counts.get(piece, 0) + 1
        
        return counts
    
    def get_total_captured(self, color: str) -> int:
        """
        Get total number of pieces captured by a specific color.
        
        Args:
            color: The color that captured the pieces ('white' or 'black')
            
        Returns:
            Total count of captured pieces
        """
        if color not in ['white', 'black']:
            raise ValueError(f"color must be 'white' or 'black', got {color}")
        
        return len(self.white_captured) if color == 'white' else len(self.black_captured)
    
    def __repr__(self) -> str:
        """String representation of captured pieces."""
        white_counts = self.get_captured_by_type('white')
        black_counts = self.get_captured_by_type('black')
        advantage = self.get_material_advantage()
        
        return (f"CapturedPieces(white: {white_counts}, black: {black_counts}, "
                f"advantage: {'+' if advantage >= 0 else ''}{advantage})")
