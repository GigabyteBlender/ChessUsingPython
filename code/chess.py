import pygame
import sys
import os

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (222, 184, 135)
DARK_BROWN = (139, 69, 19)
HIGHLIGHT_COLOR = (255, 255, 0)

# Piece images
def load_piece_images():
    pieces = {}
    piece_names = ['bK', 'bQ', 'bR', 'bB', 'bN', 'bP', 'wK', 'wQ', 'wR', 'wB', 'wN', 'wP']
    for name in piece_names:
        try:
            pieces[name] = pygame.transform.scale(pygame.image.load(f'images/{name}.png'), (SQUARE_SIZE, SQUARE_SIZE))
        except pygame.error as e:
            print(f"Error loading image for {name}: {e}")
            sys.exit(1)
    return pieces

PIECES = load_piece_images()

class Menu:
    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

    def main_menu(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = '1'
        mainClock = pygame.time.Clock()
        pygame.init()
        pygame.display.set_caption('Menu')
        screen = pygame.display.set_mode((600, 300), 0, 32)
        font = pygame.font.SysFont(None, 30)

        while True:
            screen.fill((60, 80, 60))
            mx, my = pygame.mouse.get_pos()
            button_1 = pygame.Rect(200, 100, 200, 50)
            button_2 = pygame.Rect(200, 180, 200, 50)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if button_1.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
                pygame.quit()
                game = Chess()
                game.main()

            if button_2.collidepoint((mx, my)) and pygame.mouse.get_pressed()[0]:
                pygame.quit()
                options(screen, self.draw_text, mainClock, font)

            pygame.draw.rect(screen, (200, 0, 0), button_1)
            pygame.draw.rect(screen, (200, 0, 0), button_2)
            self.draw_text('PLAY', font, (255, 255, 255), screen, 270, 115)
            self.draw_text('OPTIONS', font, (255, 255, 255), screen, 250, 195)

            pygame.display.update()
            mainClock.tick(60)

def options(screen, draw_text, mainClock, font):
    pygame.init()
    pygame.display.set_caption('Options')
    running = True

    while running:
        screen.fill((60, 80, 60))
        draw_text('Options Menu', font, (255, 255, 255), screen, 20, 20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        pygame.display.update()
        mainClock.tick(60)

class Chess:
    def create_board(self):
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
        if end is None:
            return
        end_row, end_col = end

        if piece[1] == 'P':
            if board[end_row - direction][end_col + 1] == check_color + 'K' or board[end_row - direction][end_col - 1] == check_color + 'K':
                return True

        if piece[1] in ['R', 'Q']:
            for i in range(1, 8):
                if end_row + i < 8 and board[end_row + i][end_col] == check_color + 'K':
                    return True
                if end_row - i >= 0 and board[end_row - i][end_col] == check_color + 'K':
                    return True
                if end_col + i < 8 and board[end_row][end_col + i] == check_color + 'K':
                    return True
                if end_col - i >= 0 and board[end_row][end_col - i] == check_color + 'K':
                    return True

        if piece[1] in ['B', 'Q']:
            for i in range(1, 8):
                if end_row + i < 8 and end_col + i < 8 and board[end_row + i][end_col + i] == check_color + 'K':
                    return True
                if end_row - i >= 0 and end_col - i >= 0 and board[end_row - i][end_col - i] == check_color + 'K':
                    return True
                if end_row + i < 8 and end_col - i >= 0 and board[end_row + i][end_col - i] == check_color + 'K':
                    return True
                if end_row - i >= 0 and end_col + i < 8 and board[end_row - i][end_col + i] == check_color + 'K':
                    return True

        if piece[1] == 'N':
            knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
            for move in knight_moves:
                n_row, n_col = end_row + move[0], end_col + move[1]
                if 0 <= n_row < 8 and 0 <= n_col < 8 and board[n_row][n_col] == check_color + 'K':
                    return True

        return False

    def ischeck(self, board, end, piece):
        piece_color = piece[0]
        check_color = 'w' if piece_color == 'b' else 'b'
        direction = 1 if piece_color == 'w' else -1
        self.check = self.is_check(piece, board, end, direction, check_color)

        if self.check is not None:
            if self.check:
                print(self.check)
                return

        for piece in PIECES:
            try:
                end = self.get_piece_position(board, piece)
                piece_color = piece[0]
                check_color = 'w' if piece_color == 'b' else 'b'
                direction = 1 if piece_color == 'w' else -1
                self.is_check(piece, board, end, direction, check_color)

                if self.check:
                    print(self.check)
                    return
            except:
                pass

    def is_valid_move(self, piece, start, end, board):
        if start is None:
            print("Error: start position is None.")
            return False

        start_row, start_col = start
        end_row, end_col = end
        piece_color = piece[0]
        direction = 1 if piece_color == 'w' else -1

        self.check = False
        self.ischeck(board, end, piece)

        if piece[1] == 'P':
            if start_col == end_col:
                if (start_row == 1 and piece_color == 'b' and board[2][start_col] == '.' and board[end_row][end_col] == '.') or \
                   (start_row == 6 and piece_color == 'w' and board[5][start_col] == '.' and board[end_row][end_col] == '.'):
                    if abs(start_row - end_row) in [1, 2]:
                        return board[end_row][end_col] == '.'
                if start_row - end_row == direction:
                    return board[end_row][end_col] == '.'
            if abs(start_col - end_col) == 1 and start_row - end_row == direction:
                return board[end_row][end_col] != '.' and board[end_row][end_col][0] != piece_color

        elif piece[1] == 'R':
            if start_row == end_row or start_col == end_col:
                if not any(board[r][start_col] != '.' for r in range(min(start_row, end_row) + 1, max(start_row, end_row))) and \
                   not any(board[start_row][c] != '.' for c in range(min(start_col, end_col) + 1, max(start_col, end_col))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'N':
            if (abs(start_row - end_row), abs(start_col - end_col)) in [(2, 1), (1, 2)]:
                return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'B':
            if abs(start_row - end_row) == abs(start_col - end_col):
                if not any(board[start_row + i * (1 if end_row > start_row else -1)][start_col + i * (1 if end_col > start_col else -1)] != '.' for i in range(1, abs(start_row - end_row))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'Q':
            if start_row == end_row or start_col == end_col:
                if not any(board[r][start_col] != '.' for r in range(min(start_row, end_row) + 1, max(start_row, end_row))) and \
                   not any(board[start_row][c] != '.' for c in range(min(start_col, end_col) + 1, max(start_col, end_col))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color
            elif abs(start_row - end_row) == abs(start_col - end_col):
                if not any(board[start_row + i * (1 if end_row > start_row else -1)][start_col + i * (1 if end_col > start_col else -1)] != '.' for i in range(1, abs(start_row - end_row))):
                    return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        elif piece[1] == 'K':
            if max(abs(start_row - end_row), abs(start_col - end_col)) == 1:
                return board[end_row][end_col] == '.' or board[end_row][end_col][0] != piece_color

        return False

    def highlight_king(self, screen, king_position):
        row, col = king_position
        pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    def get_king_position(self, board):
        for row in range(8):
            for col in range(8):
                if board[row][col] == 'K':
                    return (row, col)

    def get_piece_position(self, board, piece):
        for row in range(8):
            for col in range(8):
                if board[row][col] == piece:
                    return (row, col)

    def draw_board(self, screen, board, selected_pos):
        for row in range(8):
            for col in range(8):
                color = LIGHT_BROWN if (row + col) % 2 == 0 else DARK_BROWN
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                piece = board[row][col]
                if piece != '.':
                    screen.blit(PIECES[piece], (col * SQUARE_SIZE, row * SQUARE_SIZE))
                if selected_pos == (row, col):
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    def handle_mouse_click(self, pos, board, selected_piece, selected_pos, current_turn):
        row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

        if selected_piece:
            if self.is_valid_move(selected_piece, selected_pos, (row, col), board):
                board[row][col] = selected_piece
                board[selected_pos[0]][selected_pos[1]] = '.'
                current_turn = 'b' if current_turn == 'w' else 'w'
            return None, None, current_turn
        else:
            selected_piece = board[row][col]
            if selected_piece[0] == current_turn:
                return selected_piece, (row, col), current_turn
            return None, None, current_turn

    def are_kings_present(self, board):
        white_king_present = any('wK' in row for row in board)
        black_king_present = any('bK' in row for row in board)
        return white_king_present, black_king_present

    def game_over(self, screen, message):
        font = pygame.font.SysFont(None, 55)
        screen.fill((0, 0, 0))
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(2000)
        pygame.quit()

        menu = Menu()
        menu.main_menu()

    def main(self):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "1"
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess")
        clock = pygame.time.Clock()
        full_screen = False
        self.check = False

        board = self.create_board()
        selected_piece = None
        selected_pos = None
        current_turn = 'w'

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    selected_piece, selected_pos, current_turn = self.handle_mouse_click(event.pos, board, selected_piece, selected_pos, current_turn)

                if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
                    if not full_screen:
                        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                        full_screen = True
                    else:
                        screen = pygame.display.set_mode((WIDTH, HEIGHT))
                        full_screen = False

            white_king_present, black_king_present = self.are_kings_present(board)

            if not white_king_present:
                self.game_over(screen, "Black wins")
                return
            if not black_king_present:
                self.game_over(screen, "White wins")
                return

            if self.check:
                king_position = self.get_king_position(board)
                if king_position:
                    self.highlight_king(screen, king_position)

            screen.fill(WHITE)
            self.draw_board(screen, board, selected_pos)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    menu = Menu()
    menu.main_menu()
