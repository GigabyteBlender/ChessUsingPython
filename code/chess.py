import pygame
import sys
import os

# Constants for game window dimensions and gameplay
WIDTH, HEIGHT = 800, 800  # Game window size
SQUARE_SIZE = WIDTH // 8  # Size of each chess square
FPS = 60  # Frames per second for smooth animation

# Color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (231, 230, 223)  # Light square color
DARK_BROWN = (105, 146, 62)    # Dark square color
HIGHLIGHT_COLOR = (253, 253, 150)  # Color for highlighting selected pieces
CHECK_COLOR = (255, 0, 0)  # Color for highlighting king in check

# Function to load chess piece images
def load_piece_images():
    """
    Loads all chess piece images and scales them to fit the board squares.
    Naming convention: 'bK' = black King, 'wP' = white Pawn, etc.
    Returns a dictionary mapping piece names to their respective images.
    """
    pieces = {}
    piece_names = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'wK', 'wQ', 'wR', 'wB', 'wN', 'wP']
    for name in piece_names:
        try:
            pieces[name] = pygame.transform.scale(pygame.image.load(f'images/{name}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        except pygame.error as e:
            print(f"Error loading image for {name}: {e}")
            sys.exit(1)
    return pieces

# Load piece images
PIECES = load_piece_images()

class Menu:
    """
    Handles the game menu system including main menu and options.
    """
    def draw_text(self, text, font, color, surface, x, y):
        """
        Utility method to render text on a surface.
        
        Args:
            text: The text to display
            font: The font to use
            color: RGB color tuple
            surface: The surface to draw on
            x, y: Top-left position coordinates
        """
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        """
        Displays the main menu with play and options buttons.
        Handles user interaction with the menu.
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'  # Position window at top-left
        mainClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Chess Game')
        screen = pygame.display.set_mode((600, 300), 0, 32)
        font = pygame.font.SysFont(None, 30)

        while True:
            screen.fill((60, 80, 60))  # Background color
            mx, my = pygame.mouse.get_pos()  # Get mouse position
            
            # Define button rectangles
            button_1 = pygame.Rect(200, 100, 200, 50)  # Play button
            button_2 = pygame.Rect(200, 180, 200, 50)  # Options button

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Check if play button is clicked
            if button_1.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
                pygame.quit()
                game = Chess()
                game.main()  # Start the game

            # Check if options button is clicked
            if button_2.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
                pygame.quit()
                options(screen, self.draw_text, mainClock, font)  # Open options menu

            # Draw buttons and their text
            pygame.draw.rect(screen, (200, 0, 0), button_1)
            pygame.draw.rect(screen, (200, 0, 0), button_2)
            self.draw_text('PLAY', font, (255, 255, 255), screen, 270, 115)
            self.draw_text('OPTIONS', font, (255, 255, 255), screen, 250, 195)

            pygame.display.update()
            mainClock.tick(60)  # Cap at 60 FPS

def options(screen, draw_text, mainClock, font):
    """
    Displays the options menu.
    
    Args:
        screen: The pygame display surface
        draw_text: Function to render text
        mainClock: The game clock
        font: The font to use for text
    """
    pygame.init()
    pygame.display.set_caption('Options')
    running = True

    while running:
        screen.fill((60, 80, 60))  # Background color
        draw_text('Options Menu', font, (255, 255, 255), screen, 20, 20)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False  # Return to main menu

        pygame.display.update()
        mainClock.tick(60)  # Cap at 60 FPS

class Chess:
    """
    Main class handling the chess game logic and rendering.
    """
    def __init__(self):
        """Initialize game state variables."""
        self.check = False  # Flag for check status
        self.checkmate = False  # Flag for checkmate status
        self.in_check_color = None  # Color of the king in check (if any)

    def create_board(self):
        """
        Creates and returns the initial chess board.
        '.' represents empty squares.
        First character of piece codes represents color ('w' or 'b').
        Second character represents piece type (K=King, Q=Queen, R=Rook, B=Bishop, N=Knight, P=Pawn).
        
        Returns:
            2D list representing the chess board
        """
        return [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],  # Black back row
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],  # Black pawns
            ['.', '.', '.', '.', '.', '.', '.', '.'],  # Empty rows
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],  # White pawns
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],  # White back row
        ]

    def get_king_position(self, board, color):
        """
        Finds and returns the position of the king of the specified color.
        
        Args:
            board: The current chess board
            color: 'w' for white king, 'b' for black king
            
        Returns:
            Tuple (row, col) representing king position, or None if not found
        """
        for row in range(8):
            for col in range(8):
                if board[row][col] == color + 'K':
                    return (row, col)
        return None

    def get_all_pieces_positions(self, board, color):
        """
        Gets the positions of all pieces of the specified color.
        
        Args:
            board: The current chess board
            color: 'w' for white pieces, 'b' for black pieces
            
        Returns:
            List of tuples (row, col, piece) for all pieces of the specified color
        """
        positions = []
        for row in range(8):
            for col in range(8):
                if board[row][col] != '.' and board[row][col][0] == color:
                    positions.append((row, col, board[row][col]))
        return positions

    def is_under_attack(self, board, pos, attacking_color):
        """
        Checks if the position is under attack by any piece of the specified color.
        
        Args:
            board: The current chess board
            pos: Tuple (row, col) to check
            attacking_color: 'w' for white attackers, 'b' for black attackers
            
        Returns:
            Boolean indicating whether the position is under attack
        """
        row, col = pos
        
        # Check for pawn attacks (moves diagonally to capture)
        direction = 1 if attacking_color == 'b' else -1
        if 0 <= row - direction < 8:
            if 0 <= col - 1 < 8 and board[row - direction][col - 1] == attacking_color + 'P':
                return True
            if 0 <= col + 1 < 8 and board[row - direction][col + 1] == attacking_color + 'P':
                return True
                
        # Check for knight attacks (L-shaped movements)
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        for move in knight_moves:
            n_row, n_col = row + move[0], col + move[1]
            if 0 <= n_row < 8 and 0 <= n_col < 8 and board[n_row][n_col] == attacking_color + 'N':
                return True
                
        # Check for king attacks (adjacent squares)
        king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for move in king_moves:
            k_row, k_col = row + move[0], col + move[1]
            if 0 <= k_row < 8 and 0 <= k_col < 8 and board[k_row][k_col] == attacking_color + 'K':
                return True
                
        # Check for rook and queen attacks (horizontal and vertical lines)
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] != '.':  # Found a piece
                    if board[r][c] in [attacking_color + 'R', attacking_color + 'Q']:
                        return True  # Rook or Queen can attack this position
                    break  # Other piece blocks the attack
                r += dr
                c += dc
                
        # Check for bishop and queen attacks (diagonal lines)
        for dr, dc in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8:
                if board[r][c] != '.':  # Found a piece
                    if board[r][c] in [attacking_color + 'B', attacking_color + 'Q']:
                        return True  # Bishop or Queen can attack this position
                    break  # Other piece blocks the attack
                r += dr
                c += dc
                
        return False  # Position is not under attack

    def is_in_check(self, board, color):
        """
        Determines if the king of the specified color is in check.
        
        Args:
            board: The current chess board
            color: 'w' for white king, 'b' for black king
            
        Returns:
            Boolean indicating whether the king is in check
        """
        king_pos = self.get_king_position(board, color)
        if not king_pos:
            return False
            
        opposing_color = 'b' if color == 'w' else 'w'
        return self.is_under_attack(board, king_pos, opposing_color)

    def simulate_move(self, board, start, end):
        """
        Creates a copy of the board with the specified move applied.
        Used to check if a move would result in check without modifying the actual board.
        
        Args:
            board: The current chess board
            start: Tuple (row, col) of the starting position
            end: Tuple (row, col) of the destination position
            
        Returns:
            A new board with the move applied
        """
        temp_board = [row[:] for row in board]  # Create a deep copy of the board
        temp_board[end[0]][end[1]] = temp_board[start[0]][start[1]]  # Move piece
        temp_board[start[0]][start[1]] = '.'  # Clear original position
        return temp_board

    def get_valid_moves_for_piece(self, board, start_row, start_col, piece, check_for_check=True):
        """
        Get all valid moves for a specific piece.
        
        Args:
            board: The current chess board
            start_row, start_col: Starting position of the piece
            piece: The piece code (e.g., 'wK', 'bP')
            check_for_check: Whether to verify the move doesn't put own king in check
            
        Returns:
            List of tuples (row, col) representing valid destination positions
        """
        valid_moves = []
        piece_color = piece[0]

        # Check all possible destination squares
        for end_row in range(8):
            for end_col in range(8):
                # First check if the move is valid according to piece movement rules
                if self.is_valid_move(piece, (start_row, start_col), (end_row, end_col), board, False):
                    if check_for_check:
                        # If required, verify the move doesn't put/leave own king in check
                        temp_board = self.simulate_move(board, (start_row, start_col), (end_row, end_col))
                        if not self.is_in_check(temp_board, piece_color):
                            valid_moves.append((end_row, end_col))
                    else:
                        valid_moves.append((end_row, end_col))
                        
        return valid_moves

    def is_checkmate(self, board, color):
        """
        Determines if the king of the specified color is in checkmate.
        A king is in checkmate if it's in check and has no valid moves.
        
        Args:
            board: The current chess board
            color: 'w' for white king, 'b' for black king
            
        Returns:
            Boolean indicating whether the king is in checkmate
        """
        # If not in check, it can't be checkmate
        if not self.is_in_check(board, color):
            return False
            
        # Check if any piece can make a move to get out of check
        pieces = self.get_all_pieces_positions(board, color)
        for piece_pos in pieces:
            row, col, piece = piece_pos
            valid_moves = self.get_valid_moves_for_piece(board, row, col, piece)
            if valid_moves:  # If any valid move exists, it's not checkmate
                return False
                
        return True  # No valid moves found, it's checkmate

    def is_valid_move(self, piece, start, end, board, check_for_check=True):
        """
        Determines if a move is valid according to chess rules.
        
        Args:
            piece: The piece being moved (e.g., 'wK', 'bP')
            start: Tuple (row, col) of starting position
            end: Tuple (row, col) of destination position
            board: The current chess board
            check_for_check: Whether to verify the move doesn't put own king in check
            
        Returns:
            Boolean indicating if the move is valid
        """
        if start is None:
            return False

        start_row, start_col = start
        end_row, end_col = end
        
        # Check if the destination is the same as the start (no movement)
        if start_row == end_row and start_col == end_col:
            return False
            
        piece_color = piece[0]  # 'w' or 'b'
        direction = 1 if piece_color == 'w' else -1  # Movement direction for pawns

        # If destination has a piece of the same color, it's invalid (can't capture own pieces)
        if board[end_row][end_col] != '.' and board[end_row][end_col][0] == piece_color:
            return False

        # Check specific piece movement rules
        if piece[1] == 'P':  # Pawn
            # Pawn movement
            if start_col == end_col:  # Forward movement (no capture)
                # Single step forward
                if start_row - end_row == direction:
                    return board[end_row][end_col] == '.'  # Destination must be empty
                # Double step from starting position
                elif ((piece_color == 'w' and start_row == 6 and end_row == 4) or 
                      (piece_color == 'b' and start_row == 1 and end_row == 3)):
                    middle_row = start_row - direction
                    # Both destination and intermediate square must be empty
                    return board[end_row][end_col] == '.' and board[middle_row][end_col] == '.'
            # Diagonal capture
            elif abs(start_col - end_col) == 1 and start_row - end_row == direction:
                # Destination must have an opponent's piece
                return board[end_row][end_col] != '.' and board[end_row][end_col][0] != piece_color

        elif piece[1] == 'R':  # Rook
            # Rook movement (horizontal or vertical)
            if start_row == end_row:  # Horizontal movement
                step = 1 if end_col > start_col else -1
                # Check that path is clear
                for col in range(start_col + step, end_col, step):
                    if board[start_row][col] != '.':
                        return False
                return True
            elif start_col == end_col:  # Vertical movement
                step = 1 if end_row > start_row else -1
                # Check that path is clear
                for row in range(start_row + step, end_row, step):
                    if board[row][start_col] != '.':
                        return False
                return True

        elif piece[1] == 'N':  # Knight
            # Knight movement (L-shaped: 2 squares in one direction, 1 square perpendicular)
            return (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]

        elif piece[1] == 'B':  # Bishop
            # Bishop movement (diagonal)
            if abs(start_row - end_row) != abs(start_col - end_col):
                return False  # Must move diagonally
                
            row_step = 1 if end_row > start_row else -1
            col_step = 1 if end_col > start_col else -1
            
            # Check that path is clear
            row, col = start_row + row_step, start_col + col_step
            while row != end_row and col != end_col:
                if board[row][col] != '.':
                    return False
                row += row_step
                col += col_step
                
            return True

        elif piece[1] == 'Q':  # Queen
            # Queen movement (combines rook and bishop movements)
            if start_row == end_row or start_col == end_col:  # Horizontal/Vertical like Rook
                if start_row == end_row:  # Horizontal
                    step = 1 if end_col > start_col else -1
                    # Check that path is clear
                    for col in range(start_col + step, end_col, step):
                        if board[start_row][col] != '.':
                            return False
                    return True
                else:  # Vertical
                    step = 1 if end_row > start_row else -1
                    # Check that path is clear
                    for row in range(start_row + step, end_row, step):
                        if board[row][start_col] != '.':
                            return False
                    return True
            elif abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal like Bishop
                row_step = 1 if end_row > start_row else -1
                col_step = 1 if end_col > start_col else -1
                
                # Check that path is clear
                row, col = start_row + row_step, start_col + col_step
                while row != end_row and col != end_col:
                    if board[row][col] != '.':
                        return False
                    row += row_step
                    col += col_step
                    
                return True

        elif piece[1] == 'K':  # King
            # King movement (one square in any direction)
            return max(abs(start_row - end_row), abs(start_col - end_col)) == 1

        return False  # If we get here, the move is invalid

    def highlight_king(self, screen, king_position, color=HIGHLIGHT_COLOR):
        """
        Highlight the king's square (used for showing check).
        
        Args:
            screen: The pygame display surface
            king_position: Tuple (row, col) of the king's position
            color: RGB color tuple for the highlight
        """
        if king_position:
            row, col = king_position
            pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    def draw_board(self, screen, board, selected_pos):
        """
        Draw the chess board and pieces.
        
        Args:
            screen: The pygame display surface
            board: The current chess board
            selected_pos: Tuple (row, col) of the currently selected piece (if any)
        """
        # Draw board squares
        for row in range(8):
            for col in range(8):
                # Alternate colors for checkerboard pattern
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                
                # Draw piece if present
                piece = board[row][col]
                if piece != '.':
                    screen.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                    
        # Highlight selected piece
        if selected_pos:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, (selected_pos[1] * SQUARE_SIZE, selected_pos[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    def handle_mouse_click(self, pos, board, selected_piece, selected_pos, current_turn):
        """
        Handle mouse clicks for selecting pieces and making moves.
        
        Args:
            pos: Tuple (x, y) of mouse click position
            board: The current chess board
            selected_piece: The currently selected piece (if any)
            selected_pos: Tuple (row, col) of the selected piece's position
            current_turn: Current player's turn ('w' or 'b')
            
        Returns:
            Tuple of (new_selected_piece, new_selected_pos, new_current_turn)
        """
        # Convert pixel coordinates to board coordinates
        col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE

        if selected_piece:  # If a piece is already selected
            if self.is_valid_move(selected_piece, selected_pos, (row, col), board):
                # Simulate the move to check if it would put or leave own king in check
                temp_board = self.simulate_move(board, selected_pos, (row, col))
                if not self.is_in_check(temp_board, selected_piece[0]):
                    # Make the move
                    board[row][col] = selected_piece
                    board[selected_pos[0]][selected_pos[1]] = '.'
                    
                    # Check if the move puts the opponent in check or checkmate
                    next_turn = 'b' if current_turn == 'w' else 'w'
                    self.check = self.is_in_check(board, next_turn)
                    self.in_check_color = next_turn if self.check else None
                    
                    if self.check:
                        self.checkmate = self.is_checkmate(board, next_turn)
                    
                    # Switch turns
                    current_turn = next_turn
                    
            return None, None, current_turn  # Deselect piece after attempting move
        else:  # No piece selected yet
            piece = board[row][col]
            if piece != '.' and piece[0] == current_turn:  # Select a piece of current player
                return piece, (row, col), current_turn
            return None, None, current_turn  # No valid piece selected

    def game_over(self, screen, message):
        """
        Display game over message and return to menu.
        
        Args:
            screen: The pygame display surface
            message: Text to display (e.g., checkmate announcement)
        """
        font = pygame.font.SysFont(None, 55)
        screen.fill((0, 0, 0))  # Black background
        text = font.render(message, True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)  # Wait 2 seconds before returning to menu
        pygame.quit()

        # Return to main menu
        menu = Menu()
        menu.main_menu()

    def main(self):
        """
        Main game loop.
        Initializes the game, handles events, and updates the display.
        """
        os.environ['SDL_VIDEO_WINDOW_POS'] = "1"  # Position window at top-left
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        full_screen = False
        
        # Initialize game state
        board = self.create_board()
        selected_piece = None
        selected_pos = None
        current_turn = 'w'  # White goes first

        while True:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Handle piece selection and moves
                    selected_piece, selected_pos, current_turn = self.handle_mouse_click(
                        event.pos, board, selected_piece, selected_pos, current_turn
                    )

                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    # Toggle fullscreen mode
                    if not full_screen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        full_screen = True
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        full_screen = False
                
            # Check for checkmate
            if self.checkmate:
                winner = "White" if self.in_check_color == 'b' else "Black"
                self.game_over(screen, f"{winner} wins by checkmate!")
                return

            # Draw game board and pieces
            screen.fill(WHITE)
            self.draw_board(screen, board, selected_pos)
            
            # Highlight king in check with red color
            if self.check:
                king_pos = self.get_king_position(board, self.in_check_color)
                self.highlight_king(screen, king_pos, CHECK_COLOR)
            
            pygame.display.flip()  # Update display
            clock.tick(FPS)  # Cap at defined FPS

# Start the game when the script is run directly
if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()