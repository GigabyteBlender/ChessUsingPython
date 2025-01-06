import pygame
import sys
import os

# Constants
WIDTH, HEIGHT = 800, 800 # for some reason only 800 x 800 works well???
SQUARE_SIZE = WIDTH // 8
FPS = 60    # most it can handle without lag (still lags)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
HIGHLIGHT_COLOR = (255, 255, 0)  # Yellow for highlighting

# Piece images
PIECES = {          #driectories for some low quality images
    'bK': pygame.transform.scale(pygame.image.load('images/bK.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bQ': pygame.transform.scale(pygame.image.load('images/bQ.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bR': pygame.transform.scale(pygame.image.load('images/bR.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bB': pygame.transform.scale(pygame.image.load('images/bB.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bN': pygame.transform.scale(pygame.image.load('images/bN.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'bP': pygame.transform.scale(pygame.image.load('images/bP.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wK': pygame.transform.scale(pygame.image.load('images/wK.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wQ': pygame.transform.scale(pygame.image.load('images/wQ.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wR': pygame.transform.scale(pygame.image.load('images/wR.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wB': pygame.transform.scale(pygame.image.load('images/wB.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wN': pygame.transform.scale(pygame.image.load('images/wN.png'), (SQUARE_SIZE, SQUARE_SIZE)),
    'wP': pygame.transform.scale(pygame.image.load('images/wP.png'), (SQUARE_SIZE, SQUARE_SIZE)),
}

class Menu():   
    """
    A function that can be used to write text on our screen and buttons
    """
    """
    Represents the main menu of the game with options to play or access settings.
    """
    def draw_text(self, text, font, color, surface, x, y):
        """
        Draw text on the screen at a given position.
        """
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
    
    # A variable to check for the status later
    click = False
    
    # Main container function that holds the buttons and game functions
    def main_menu(self):
        """
        Display the main menu with options to play the game or access settings.
        """
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        mainClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Menu')
        screen = pygame.display.set_mode((600, 300),0,32)
    
        #setting font settings
        font = pygame.font.SysFont(None, 30)
        
        while True:
            screen.fill((60, 80, 60))
            #self.draw_text('Main Menu', font, (0,0,0), screen, 250, 40)
    
            mx, my = pygame.mouse.get_pos()

            #creating buttons
            button_1 = pygame.Rect(200, 100, 200, 50)
            button_2 = pygame.Rect(200, 180, 200, 50)

            #defining functions when a certain button is pressed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit
                    pygame.quit()
            
            # Handle button clicks
            if button_1.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    pygame.display.quit
                    game = Chess()
                    game.main()
            
            if button_2.collidepoint((mx, my)):
                if pygame.mouse.get_pressed()[0]:
                    pygame.display.quit
                    options(screen, self.draw_text, mainClock, font)
                    
            pygame.draw.rect(screen, (200, 0, 0), button_1)
            pygame.draw.rect(screen, (200, 0, 0), button_2)
    
            #writing text on top of button
            self.draw_text('PLAY', font, (255,255,255), screen, 270, 115)
            self.draw_text('OPTIONS', font, (255,255,255), screen, 250, 195)

            pygame.display.update()
            mainClock.tick(60)
    
def options(screen, draw_text, mainClock, font):
    """
    Display the options menu with information or settings. (has nothing yet)
    """
    pygame.init()
    pygame.display.set_caption('options')
    running = True
    
    while running:
        screen.fill((60,80,60))
        draw_text('sam wardle is wrong', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.type == pygame.K_ESCAPE:
                    running = False
       
        pygame.display.update()
        mainClock.tick(60)
        
class Chess():#I wasted so much time for this
    # Initial board setup
    """
    Main chess game logic including board setup, movement, and rules.
    """
    def create_board(self):
        # '.' means empty space
        """
        Initialize the chessboard with the standard piece layout.
        """
        return [
            ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
            ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP'],
            ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'],
        ]
    def is_check(self, piece, board, end, direction, check_color):
        """
        Check if a move puts the opponent's king in check.
        """
        if end != None:
            end_row, end_col = end
        else:
            self.check = False
            return
        
        if piece[1] == 'P':
            if board[end_row-direction][end_col+1] == check_color+'K' or board[end_row-direction][end_col-1] == check_color+'K':
                self.check = True
                return
                
        if piece[1] == 'R' or piece[1] == 'Q':
            for i in range(1, 8):
                if end_row + i < 8 and board[end_row + i][end_col] == check_color + 'K':
                    self.check = True
                    return
                if end_row - i >= 0 and board[end_row - i][end_col] == check_color + 'K':
                    self.check = True
                    return
                if end_col + i < 8 and board[end_row][end_col + i] == check_color + 'K':
                    self.check = True
                    return
                if end_col - i >= 0 and board[end_row][end_col - i] == check_color + 'K':
                    self.check = True
                    return
                    
            # Check for Bishop and Queen (diagonal line)
        if piece[1] == 'B' or piece[1] == 'Q':
            for i in range(1, 8):
                if end_row + i < 8 and end_col + i < 8 and board[end_row + i][end_col + i] == check_color + 'K':
                    self.check = True
                    return
                if end_row - i >= 0 and end_col - i >= 0 and board[end_row - i][end_col - i] == check_color + 'K':
                    self.check = True
                    return
                if end_row + i < 8 and end_col - i >= 0 and board[end_row + i][end_col - i] == check_color + 'K':
                    self.check = True
                    return
                if end_row - i >= 0 and end_col + i < 8 and board[end_row - i][end_col + i] == check_color + 'K':
                    self.check = True
                    return
                    
        # Check for Knight
        if piece[1] == 'N':
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for move in knight_moves:
                n_row, n_col = end_row + move[0], end_col + move[1]
                if 0 <= n_row < 8 and 0 <= n_col < 8:
                    if board[n_row][n_col] == check_color + 'K':
                        self.check = True
                        return
                        
        self.check = False
        return
            

    def ischeck(self, board, end, piece):
        self.check = False
        
        piece_color = piece[0]
        check_color = 'w' if piece_color == 'b' else 'b'
        direction = 1 if piece_color == 'w' else -1
        self.is_check(piece, board, end, direction, check_color)
        
        if self.check == True:
            print(self.check)
            return
        
        for piece in PIECES:
            try:
                end = self.get_piece_position(board, piece)
                piece_color = piece[0]
                check_color = 'w' if piece_color == 'b' else 'b'
                direction = 1 if piece_color == 'w' else -1
                self.is_check(piece, board, end, direction, check_color)
                    
                if self.check == True:
                    print(self.check)
                    return
            except:
                pass
            
    def is_valid_move(self, piece, start, end, board):
        """
        Validate whether a move is legal based on chess rules.
        """
        
        #basic validation for moves that ussualy doesnt even work ... WHHHYHYYYYYYY
        if start is None:
            print("Error: start position is None.")
            return False
        
        # Check if start position is empty
        start_row, start_col = start
        end_row, end_col = end
        piece_color = piece[0]  # 'w' or 'b'
        
        # Determine the direction of movement
        direction = 1 if piece_color == 'w' else -1
        
        self.check = False
        self.ischeck(board, end, piece)

        if piece[1] == 'P':  # Pawn movement
            # Check for capturing move, and this kinda works but not that well
            if start_col == end_col:
                #checking if it is in the starting rows for the pawns
                if (start_row == 1 and piece_color == 'b' and board[2][start_col] == '.' and board[end_row][end_col] == '.') or \
                    (start_row == 6 and piece_color == 'w' and board[5][start_col] == '.' and board[end_row][end_col] == '.'):
                    
                    if abs(start_row - end_row) == 2 or abs(start_row - end_row) == 1:
                        if board[end_row][end_col] != '.':
                            return board[end_row][end_col] == '.'
                        else:
                            return board[end_row][end_col][0] != piece_color
                #moving maximum of 1 in a direction
                if start_row - end_row == direction:
                    
                    if board[end_row][end_col] != '.':
                        return board[end_row][end_col] == '.'
                    else:
                        return board[end_row][end_col][0] != piece_color
                    
            if abs(start_col - end_col) == 1 or abs(end_col - start_col) == 1:
                
                if board[end_row][end_col] != '.':
                    if start_row - end_row == direction:
                        if abs(start_row - end_row) == direction:
                            if board[end_row][end_col] == '.':
                                return board[end_row][end_col] == '.'
                            else:
                                return board[end_row][end_col][0] != piece_color
                        else:
                            return board[end_row][end_col][0] != piece_color
             # pawn movement in a line works but kinda bad

        elif piece[1] == 'R':  # Rook movement
            
            if start_row == end_row or start_col == end_col:  # Straight line
                if not any(board[r][start_col] != '.' for r in range(min(start_row, end_row) + 1, max(start_row, end_row))) and not any(board[start_row][c] != '.' for c in range(min(start_col, end_col) + 1, max(start_col, end_col))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'N':  # Knight movement
            
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
                return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'B':  # Bishop movement
            
            if abs(start_row - end_row) == abs(start_col - end_col):  # Diagonal movement
                if not any(board[start_row + i * (1 if end_row > start_row else -1)][start_col + i * (1 if end_col > start_col else -1)] != '.' for i in range(1, abs(start_row - end_row))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'Q':  # Queen movement
            
            if start_row == end_row or start_col == end_col:  # Rook-like movement
                if not any(board[r][start_col] != '.' for r in range(min(start_row, end_row) + 1, max(start_row, end_row))) and \
                        not any(board[start_row][c] != '.' for c in range(min(start_col, end_col) + 1, max(start_col, end_col))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color
            elif abs(start_row - end_row) == abs(start_col - end_col):  # Bishop-like movement
                if not any(board[start_row + i * (1 if end_row > start_row else -1)][start_col + i * (1 if end_col > start_col else -1)] != '.' for i in range(1, abs(start_row - end_row))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'K':  # King movement
            if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
                return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        #returns false if nothing selected
        return False
    
    def highlight_king(self, screen, king_position, color='red'):
        for row in range(8):
            for col in range(8):
                if king_position == (row, col):
                    pygame.draw.rect (screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
        
    def get_king_position(self, board):
        # Logic to find the king's position
        for row in range(8):
            for col in range(8):
                if board[row][col] == 'K':  # Assuming 'K' represents the king
                    return (row, col)
                
    def get_piece_position(self, board, piece):
        for row in range(8):
            for col in range(8):
                if board[row][col] == piece:
                    return (row, col)

    # Draw the board
    def draw_board(self, screen, board, selected_pos):
        """
        Draw the chessboard with pieces on the screen.
        """
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board[row][col]
                if piece != '.':
                    screen.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                # Highlight the selected piece
                if selected_pos == (row, col):
                    pygame.draw.rect (screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    # Handle mouse click events
    def handle_mouse_click(self, pos, board, selected_piece, selected_pos, current_turn):
        row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE
            
        if selected_piece:  # Move the selected piece
            # Move piece
            if self.is_valid_move(selected_piece, selected_pos, (row, col), board):
                board[row][col] = selected_piece
                board[selected_pos[0]][selected_pos[1]] = '.'
                # Switch turn
                current_turn = 'b' if current_turn == 'w' else 'w'
            return None, None, current_turn  # Deselect piece after move
        else:
            selected_piece = board[row][col]
            # Check if the selected piece matches the current turn
            if selected_piece[0] == current_turn:
                return selected_piece, (row, col), current_turn
            return None, None, current_turn  # Invalid selection
        
    def are_kings_present(self, board):
        white_king_present = any('wK' in row for row in board)
        black_king_present = any('bK' in row for row in board)
        return white_king_present, black_king_present
    
    def game_over(self, screen, message):
        font = pygame.font.SysFont(None, 55)
        screen.fill((0, 0, 0))  # Fill the screen with black
        text = font.render(message, True, (255, 255, 255))  # White text
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.display.quit
        
        menu = Menu()
        menu.main_menu()
        
    # Main function
    def main(self):
        
        x = 100
        y = 0
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
        
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        full_screen = False
        self.check = False
        
        board = self.create_board()
        
        selected_piece = None
        selected_pos = None
        current_turn = 'w'  # Start with white's turn

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_piece, selected_pos, current_turn = self.handle_mouse_click(event.pos, board, selected_piece, selected_pos, current_turn)
                
                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    # Toggle fullscreen mode
                    if not full_screen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        full_screen = True
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
            # Check for game over condition
            white_king_present, black_king_present = self.are_kings_present(board)
            
            if not white_king_present:
                self.game_over(screen, "black wins")
                return  # Exit the main loop
            if not black_king_present:
                self.game_over(screen, "white wins")
                return  # Exit the main loop
            
            if self.check == True:
                king_position = self.get_king_position(board)
                if king_position:
                    self.highlight_king(screen, king_position, color='red')
                    
            screen.fill(WHITE)
            self.draw_board(screen, board, selected_pos)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()
