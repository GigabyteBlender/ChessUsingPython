"""
MoveHistory class for tracking and formatting chess moves in algebraic notation.
"""
import time
from typing import List, Optional

from model.move_record import MoveRecord
from model.piece import Piece
from model.position import Position


class MoveHistory:
    """
    Tracks all moves in algebraic notation.
    
    This class maintains a chronological record of all moves made during the game
    and provides methods to format them in standard algebraic notation.
    """
    
    def __init__(self):
        """Initialize an empty move history."""
        self.moves: List[MoveRecord] = []
    
    def add_move(
        self,
        piece: Piece,
        start: Position,
        end: Position,
        captured: Optional[Piece] = None,
        is_check: bool = False,
        is_checkmate: bool = False,
        is_castling: bool = False,
        is_en_passant: bool = False,
        board=None  # Optional board for disambiguation
    ):
        """
        Add a move to the history in algebraic notation.
        
        Args:
            piece: The piece that moved
            start: Starting position
            end: Destination position
            captured: The captured piece, if any
            is_check: Whether this move puts opponent in check
            is_checkmate: Whether this move results in checkmate
            is_castling: Whether this is a castling move
            is_en_passant: Whether this is an en passant capture
            board: Optional board state for disambiguation
        """
        # Calculate move number (increments every 2 moves, starting at 1)
        move_number = (len(self.moves) // 2) + 1
        
        # Generate algebraic notation
        algebraic = self.to_algebraic_notation(
            piece, start, end, captured is not None,
            is_check, is_checkmate, is_castling, is_en_passant, board
        )
        
        # Create move record
        move_record = MoveRecord(
            move_number=move_number,
            player=piece.color,
            piece_type=piece.piece_type,
            start=start,
            end=end,
            captured_piece=captured.piece_type if captured else None,
            is_check=is_check,
            is_checkmate=is_checkmate,
            is_castling=is_castling,
            is_en_passant=is_en_passant,
            algebraic_notation=algebraic,
            timestamp=time.time()
        )
        
        self.moves.append(move_record)
    
    def get_last_move(self) -> Optional[MoveRecord]:
        """
        Get the most recent move.
        
        Returns:
            The last MoveRecord, or None if no moves have been made
        """
        if not self.moves:
            return None
        return self.moves[-1]
    
    def to_algebraic_notation(
        self,
        piece: Piece,
        start: Position,
        end: Position,
        is_capture: bool,
        is_check: bool,
        is_checkmate: bool,
        is_castling: bool = False,
        is_en_passant: bool = False,
        board=None
    ) -> str:
        """
        Convert a move to algebraic notation (e.g., 'Nf3', 'exd5', 'O-O').
        
        Standard algebraic notation rules:
        - Piece moves: Nf3 (piece letter + destination)
        - Pawn moves: e4 (destination only)
        - Captures: Nxf3 or exd5 (x indicates capture)
        - Castling: O-O (kingside) or O-O-O (queenside)
        - Check: + suffix
        - Checkmate: # suffix
        - Disambiguation: Add file, rank, or both if multiple pieces can move to same square
        
        Args:
            piece: The piece that moved
            start: Starting position
            end: Destination position
            is_capture: Whether this move captures a piece
            is_check: Whether this move puts opponent in check
            is_checkmate: Whether this move results in checkmate
            is_castling: Whether this is a castling move
            is_en_passant: Whether this is an en passant capture
            board: Optional board state for disambiguation
            
        Returns:
            String in algebraic notation
        """
        # Handle castling specially
        if is_castling:
            # Kingside castling: king moves from e-file to g-file
            if end.col > start.col:
                notation = "O-O"
            # Queenside castling: king moves from e-file to c-file
            else:
                notation = "O-O-O"
        else:
            notation = ""
            
            # For non-pawn pieces, add piece letter
            if piece.piece_type != 'P':
                notation += piece.piece_type
                
                # Add disambiguation if needed
                if board is not None:
                    disambiguation = self._get_disambiguation(piece, start, end, board)
                    notation += disambiguation
            
            # For pawn captures, add the starting file
            elif is_capture:
                notation += start.to_algebraic()[0]  # Just the file letter
            
            # Add capture indicator
            if is_capture:
                notation += 'x'
            
            # Add destination square
            notation += end.to_algebraic()
            
            # Add en passant indicator (optional, but helpful)
            if is_en_passant:
                notation += " e.p."
        
        # Add check or checkmate indicator
        if is_checkmate:
            notation += '#'
        elif is_check:
            notation += '+'
        
        return notation
    
    def _get_disambiguation(self, piece: Piece, start: Position, end: Position, board) -> str:
        """
        Determine if disambiguation is needed when multiple pieces of the same type
        can move to the same square.
        
        Args:
            piece: The piece that moved
            start: Starting position
            end: Destination position
            board: Current board state
            
        Returns:
            Disambiguation string (empty, file letter, rank number, or both)
        """
        # Get all pieces of the same type and color
        same_type_pieces = []
        for row in range(8):
            for col in range(8):
                pos = Position(row, col)
                other_piece = board.get_piece(pos)
                if (other_piece is not None and
                    other_piece.piece_type == piece.piece_type and
                    other_piece.color == piece.color and
                    pos != start):
                    # Check if this piece can also move to the destination
                    possible_moves = other_piece.get_possible_moves(board)
                    if end in possible_moves:
                        same_type_pieces.append(pos)
        
        # No disambiguation needed if no other pieces can move there
        if not same_type_pieces:
            return ""
        
        # Check if file disambiguation is sufficient
        same_file = any(pos.col == start.col for pos in same_type_pieces)
        same_rank = any(pos.row == start.row for pos in same_type_pieces)
        
        if not same_file:
            # File alone is sufficient
            return start.to_algebraic()[0]
        elif not same_rank:
            # Rank alone is sufficient
            return start.to_algebraic()[1]
        else:
            # Need both file and rank
            return start.to_algebraic()
    
    def get_formatted_history(self) -> List[str]:
        """
        Get formatted move history for display.
        
        Returns:
            List of strings formatted as "1. e4 e5" (move number, white move, black move)
        """
        formatted = []
        
        # Group moves by move number (white and black together)
        i = 0
        while i < len(self.moves):
            white_move = self.moves[i]
            move_str = f"{white_move.move_number}. {white_move.algebraic_notation}"
            
            # Add black's move if it exists
            if i + 1 < len(self.moves):
                black_move = self.moves[i + 1]
                move_str += f" {black_move.algebraic_notation}"
                i += 2
            else:
                i += 1
            
            formatted.append(move_str)
        
        return formatted
    
    def clear(self):
        """Clear all moves from the history."""
        self.moves.clear()
    
    def __len__(self) -> int:
        """Return the number of moves in the history."""
        return len(self.moves)
    
    def __repr__(self) -> str:
        """String representation of the move history."""
        if not self.moves:
            return "MoveHistory(empty)"
        return f"MoveHistory({len(self.moves)} moves)"
