"""
MoveValidator class for validating chess moves according to all rules.
"""
from typing import Optional

from model.board import Board
from model.piece import King, Rook
from model.position import Position


class MoveValidator:
    """
    Validates chess moves according to all standard chess rules.
    
    This class handles:
    - Piece-specific movement validation
    - Preventing capture of own pieces
    - Out-of-bounds move validation
    - King safety (preventing moves that leave king in check)
    """
    
    def is_legal_move(self, board: Board, start: Position, end: Position, 
                     current_turn: str, last_move: Optional[tuple] = None) -> bool:
        """
        Check if a move is legal considering all chess rules including check.
        
        Args:
            board: The current board state
            start: Starting position
            end: Destination position
            current_turn: The color of the player whose turn it is ('white' or 'black')
            last_move: The last move made (start_pos, end_pos, piece) for en passant
            
        Returns:
            True if the move is legal, False otherwise
        """
        # Validate positions are within bounds
        if not start.is_valid() or not end.is_valid():
            return False
        
        # Get the piece at the starting position
        piece = board.get_piece(start)
        
        # Must have a piece at the start position
        if piece is None:
            return False
        
        # Piece must belong to the current player
        if piece.color != current_turn:
            return False
        
        # Can't move to the same square
        if start == end:
            return False
        
        # Get the piece at the destination (if any)
        target_piece = board.get_piece(end)
        
        # Can't capture your own piece
        if target_piece is not None and target_piece.color == piece.color:
            return False
        
        # Check if the move follows piece-specific movement rules
        possible_moves = piece.get_possible_moves(board)
        
        # Check for en passant as a special case for pawns
        from model.piece import Pawn
        if isinstance(piece, Pawn) and end not in possible_moves:
            # Check if this could be an en passant move
            if self.is_en_passant_legal(board, start, end, last_move):
                # En passant is legal, but still need to check if it leaves king in check
                if not self.would_leave_in_check_en_passant(board, start, end, current_turn):
                    return True
            return False
        
        if end not in possible_moves:
            return False
        
        # Check if the move would leave the king in check
        if self.would_leave_in_check(board, start, end, current_turn):
            return False
        
        return True
    
    def would_leave_in_check(self, board: Board, start: Position, 
                            end: Position, color: str) -> bool:
        """
        Check if a move would leave the player's king in check.
        
        This method simulates the move on a copy of the board and checks
        if the king would be under attack after the move.
        
        Args:
            board: The current board state
            start: Starting position of the move
            end: Destination position of the move
            color: The color of the player making the move
            
        Returns:
            True if the move would leave the king in check, False otherwise
        """
        # Create a copy of the board to simulate the move
        board_copy = board.copy()
        
        # Simulate the move on the copy
        board_copy.move_piece(start, end)
        
        # Find the king's position after the move
        king_pos = board_copy.find_king(color)
        
        # If king not found, something is wrong (should not happen in valid game)
        if king_pos is None:
            return True  # Treat as unsafe
        
        # Check if the king is under attack
        return self.is_under_attack(board_copy, king_pos, color)
    
    def is_under_attack(self, board: Board, position: Position, 
                       defending_color: str) -> bool:
        """
        Check if a position is under attack by the opponent.
        
        Args:
            board: The current board state
            position: The position to check
            defending_color: The color of the player defending the position
            
        Returns:
            True if the position is under attack, False otherwise
        """
        opponent_color = 'black' if defending_color == 'white' else 'white'
        
        # Get all opponent pieces
        opponent_pieces = board.get_all_pieces(opponent_color)
        
        # Check if any opponent piece can move to this position
        for piece_pos, piece in opponent_pieces:
            # For kings, don't include castling moves to avoid infinite recursion
            if isinstance(piece, King):
                possible_moves = piece.get_possible_moves(board, include_castling=False)
            else:
                possible_moves = piece.get_possible_moves(board)
            if position in possible_moves:
                return True
        
        return False
    
    def is_en_passant_legal(self, board: Board, start: Position, end: Position, 
                           last_move: Optional[tuple]) -> bool:
        """
        Check if an en passant capture is legal.
        
        En passant requirements:
        1. The moving piece must be a pawn
        2. The pawn must be on the correct rank (row 3 for white, row 4 for black)
        3. The destination must be diagonally adjacent
        4. An opponent pawn must have just moved 2 squares to land adjacent to our pawn
        5. The capture must be made immediately (on the very next turn)
        
        Args:
            board: The current board state
            start: Starting position of the pawn
            end: Destination position (diagonal move to empty square)
            last_move: The last move made (start_pos, end_pos, piece)
            
        Returns:
            True if en passant is legal, False otherwise
        """
        # Must have a last move to check
        if last_move is None:
            return False
        
        last_start, last_end, last_piece = last_move
        
        # Get the moving piece
        piece = board.get_piece(start)
        from model.piece import Pawn
        
        # Must be a pawn
        if not isinstance(piece, Pawn):
            return False
        
        # The last move must have been by a pawn
        if not isinstance(last_piece, Pawn):
            return False
        
        # The last pawn must be of opposite color
        if last_piece.color == piece.color:
            return False
        
        # Check if our pawn is on the correct rank
        # White pawns can en passant from row 3, black pawns from row 4
        correct_rank = 3 if piece.color == 'white' else 4
        if start.row != correct_rank:
            return False
        
        # Check if the last move was a 2-square pawn advance
        if abs(last_end.row - last_start.row) != 2:
            return False
        
        # Check if the opponent pawn landed adjacent to our pawn
        if last_end.row != start.row:
            return False
        
        if abs(last_end.col - start.col) != 1:
            return False
        
        # Check if the destination is the correct square
        # Should be diagonally forward from our pawn, behind the opponent pawn
        direction = -1 if piece.color == 'white' else 1
        expected_end_row = start.row + direction
        expected_end_col = last_end.col
        
        if end.row != expected_end_row or end.col != expected_end_col:
            return False
        
        return True
    
    def would_leave_in_check_en_passant(self, board: Board, start: Position, 
                                        end: Position, color: str) -> bool:
        """
        Check if an en passant move would leave the player's king in check.
        
        This is similar to would_leave_in_check but handles the special case
        where the captured pawn is not at the destination square.
        
        Args:
            board: The current board state
            start: Starting position of the capturing pawn
            end: Destination position of the capturing pawn
            color: The color of the player making the move
            
        Returns:
            True if the move would leave the king in check, False otherwise
        """
        # Create a copy of the board to simulate the move
        board_copy = board.copy()
        
        # Remove the captured pawn (which is on the same row as start, same col as end)
        captured_pawn_pos = Position(start.row, end.col)
        board_copy.set_piece(captured_pawn_pos, None)
        
        # Move the capturing pawn
        board_copy.move_piece(start, end)
        
        # Find the king's position after the move
        king_pos = board_copy.find_king(color)
        
        # If king not found, something is wrong (should not happen in valid game)
        if king_pos is None:
            return True  # Treat as unsafe
        
        # Check if the king is under attack
        return self.is_under_attack(board_copy, king_pos, color)
    
    def can_castle(self, board: Board, king_pos: Position, rook_pos: Position) -> bool:
        """
        Check if castling is legal between the king and rook at the given positions.
        
        Castling requirements:
        1. Neither the king nor the rook has moved
        2. There are no pieces between the king and rook
        3. The king is not currently in check
        4. The king does not move through a square that is under attack
        5. The king does not end up in check
        
        Args:
            board: The current board state
            king_pos: Position of the king
            rook_pos: Position of the rook
            
        Returns:
            True if castling is legal, False otherwise
        """
        # Get the king and rook pieces
        king = board.get_piece(king_pos)
        rook = board.get_piece(rook_pos)
        
        # Must have a king and rook at the specified positions
        if not isinstance(king, King) or not isinstance(rook, Rook):
            return False
        
        # King and rook must be the same color
        if king.color != rook.color:
            return False
        
        # Neither piece can have moved
        if king.has_moved or rook.has_moved:
            return False
        
        # King cannot be in check
        if self.is_under_attack(board, king_pos, king.color):
            return False
        
        # Determine direction (kingside or queenside)
        # Kingside: rook is to the right (higher column)
        # Queenside: rook is to the left (lower column)
        if rook_pos.col > king_pos.col:
            # Kingside castling
            direction = 1
            squares_between = range(king_pos.col + 1, rook_pos.col)
        else:
            # Queenside castling
            direction = -1
            squares_between = range(rook_pos.col + 1, king_pos.col)
        
        # Check that all squares between king and rook are empty
        for col in squares_between:
            if board.get_piece(Position(king_pos.row, col)) is not None:
                return False
        
        # Check that the king doesn't move through or into check
        # King moves 2 squares toward the rook
        king_path = [
            Position(king_pos.row, king_pos.col + direction),
            Position(king_pos.row, king_pos.col + 2 * direction)
        ]
        
        for pos in king_path:
            if self.is_under_attack(board, pos, king.color):
                return False
        
        return True
