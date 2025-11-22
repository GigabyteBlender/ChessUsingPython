"""
GameState class maintaining the complete state of the chess game.
"""
from typing import List, Optional

from model.board import Board
from model.captured_pieces import CapturedPieces
from model.move_history import MoveHistory
from model.move_validator import MoveValidator
from model.piece import Pawn, Queen
from model.position import Position


class GameState:
    """
    Maintains the complete state of the chess game.
    
    This class tracks:
    - The current board state
    - Whose turn it is
    - Move history in algebraic notation
    - Captured pieces for both players
    - Check and checkmate status
    - Game over conditions
    """
    
    def __init__(self):
        """Initialize a new game state."""
        self.board = Board()
        self.board.setup_initial_position()  # Set up pieces in starting position
        self.current_turn = 'white'
        self.move_validator = MoveValidator()
        self.move_history = MoveHistory()
        self.captured_pieces = CapturedPieces()
        self.check_status = {'white': False, 'black': False}
        self.game_over = False
        self.winner: Optional[str] = None
        self.last_move: Optional[tuple] = None  # (start_pos, end_pos, piece)
    
    def is_in_check(self, color: str) -> bool:
        """
        Check if the specified color's king is in check.
        
        Args:
            color: 'white' or 'black'
            
        Returns:
            True if the king is in check, False otherwise
        """
        king_pos = self.board.find_king(color)
        
        # If king not found, something is wrong
        if king_pos is None:
            return False
        
        # Check if the king's position is under attack
        return self.move_validator.is_under_attack(self.board, king_pos, color)
    
    def get_legal_moves(self, position: Position) -> List[Position]:
        """
        Get all legal moves for the piece at the given position.
        
        This filters out moves that would leave the king in check.
        
        Args:
            position: The position of the piece
            
        Returns:
            List of legal destination positions
        """
        piece = self.board.get_piece(position)
        
        # No piece at this position
        if piece is None:
            return []
        
        # Get all possible moves for the piece
        possible_moves = piece.get_possible_moves(self.board)
        
        # Filter out moves that would leave the king in check
        legal_moves = []
        for end_pos in possible_moves:
            if self.move_validator.is_legal_move(
                self.board, position, end_pos, piece.color, self.last_move
            ):
                legal_moves.append(end_pos)
        
        return legal_moves
    
    def is_checkmate(self, color: str) -> bool:
        """
        Check if the specified color is in checkmate.
        
        Checkmate occurs when:
        1. The king is in check
        2. There are no legal moves that remove the check
        
        Args:
            color: 'white' or 'black'
            
        Returns:
            True if the color is in checkmate, False otherwise
        """
        # Must be in check for checkmate
        if not self.is_in_check(color):
            return False
        
        # Check if there are any legal moves
        return not self._has_legal_moves(color)
    
    def is_stalemate(self) -> bool:
        """
        Check if the game is in stalemate.
        
        Stalemate occurs when:
        1. The current player is NOT in check
        2. The current player has no legal moves
        
        Returns:
            True if the game is in stalemate, False otherwise
        """
        # Must NOT be in check for stalemate
        if self.is_in_check(self.current_turn):
            return False
        
        # Check if there are any legal moves
        return not self._has_legal_moves(self.current_turn)
    
    def _has_legal_moves(self, color: str) -> bool:
        """
        Check if the specified color has any legal moves.
        
        Args:
            color: 'white' or 'black'
            
        Returns:
            True if there is at least one legal move, False otherwise
        """
        # Get all pieces of this color
        pieces = self.board.get_all_pieces(color)
        
        # Check each piece for legal moves
        for piece_pos, piece in pieces:
            legal_moves = self.get_legal_moves(piece_pos)
            if len(legal_moves) > 0:
                return True
        
        return False
    
    def make_move(self, start: Position, end: Position) -> bool:
        """
        Execute a move if valid, update state, return success.
        
        This method:
        1. Validates the move is legal
        2. Executes the move on the board
        3. Handles special moves (castling, en passant, pawn promotion)
        4. Updates captured pieces
        5. Updates move history
        6. Updates check status
        7. Switches turns
        8. Detects checkmate and stalemate
        
        Args:
            start: Starting position of the piece
            end: Destination position
            
        Returns:
            True if the move was executed successfully, False otherwise
        """
        # Get the piece at the start position
        piece = self.board.get_piece(start)
        
        # No piece at start position
        if piece is None:
            return False
        
        # Not this player's turn
        if piece.color != self.current_turn:
            return False
        
        # Check if the move is legal
        if not self.move_validator.is_legal_move(self.board, start, end, piece.color, self.last_move):
            return False
        
        # Check if this is a castling move
        from model.piece import King, Rook
        is_castling = False
        if isinstance(piece, King) and abs(end.col - start.col) == 2:
            is_castling = True
            
            # Determine which rook to move
            if end.col > start.col:
                # Kingside castling
                rook_start = Position(start.row, 7)
                rook_end = Position(start.row, start.col + 1)
            else:
                # Queenside castling
                rook_start = Position(start.row, 0)
                rook_end = Position(start.row, start.col - 1)
            
            # Move the rook
            rook = self.board.get_piece(rook_start)
            if rook is not None:
                self.board.move_piece(rook_start, rook_end)
        
        # Check if this is an en passant capture
        is_en_passant = False
        captured_en_passant_piece = None
        if isinstance(piece, Pawn) and start.col != end.col and self.board.get_piece(end) is None:
            # This is a diagonal pawn move to an empty square - must be en passant
            is_en_passant = True
            # Remove the captured pawn from its actual position
            captured_pawn_row = start.row  # Same row as the capturing pawn
            captured_pawn_pos = Position(captured_pawn_row, end.col)
            captured_en_passant_piece = self.board.get_piece(captured_pawn_pos)
            self.board.set_piece(captured_pawn_pos, None)
        
        # Execute the move and capture any piece at the destination
        captured_piece = self.board.move_piece(start, end)
        
        # For en passant, the captured piece is not at the destination
        if is_en_passant and captured_en_passant_piece is not None:
            captured_piece = captured_en_passant_piece
        
        # Update captured pieces if a piece was captured
        if captured_piece is not None:
            self.captured_pieces.add_capture(captured_piece.piece_type, piece.color)
        
        # Check for pawn promotion
        promoted = False
        if isinstance(piece, Pawn):
            # White pawns promote at row 0, black pawns promote at row 7
            promotion_row = 0 if piece.color == 'white' else 7
            
            if end.row == promotion_row:
                # Promote pawn to queen
                queen = Queen(piece.color, end)
                queen.has_moved = True  # The promoted queen has "moved"
                self.board.set_piece(end, queen)
                promoted = True
        
        # Track this move for en passant detection
        self.last_move = (start, end, piece)
        
        # Switch turns
        opponent_color = 'black' if self.current_turn == 'white' else 'white'
        self.current_turn = opponent_color
        
        # Update check status for both players
        self.check_status['white'] = self.is_in_check('white')
        self.check_status['black'] = self.is_in_check('black')
        
        # Determine if this move resulted in check or checkmate
        is_check = self.check_status[opponent_color]
        is_checkmate = False
        
        # Check for checkmate or stalemate
        if self.is_checkmate(opponent_color):
            self.game_over = True
            self.winner = piece.color  # The player who just moved wins
            is_checkmate = True
        elif self.is_stalemate():
            self.game_over = True
            self.winner = None  # Draw
        
        # Add move to history (use the piece that moved, which might have been promoted)
        # If promoted, we want to record the pawn move, not the queen
        moving_piece = piece if not promoted else piece
        self.move_history.add_move(
            piece=moving_piece,
            start=start,
            end=end,
            captured=captured_piece,
            is_check=is_check,
            is_checkmate=is_checkmate,
            is_castling=is_castling,
            is_en_passant=is_en_passant,
            board=self.board
        )
        
        return True
