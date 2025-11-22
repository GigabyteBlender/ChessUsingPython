"""
UIRenderer class for rendering UI elements (move history, captured pieces, status indicators).
"""
from typing import Dict, Optional

import pygame

from constants import BLACK, CHECK_COLOR, LIGHT_BROWN, WHITE
from model.captured_pieces import CapturedPieces
from model.move_history import MoveHistory


class UIRenderer:
    """
    Renders UI elements including move history, captured pieces, and status indicators.
    
    This class is responsible for rendering all non-board UI elements:
    - Move history panel with scrolling
    - Captured pieces display with material advantage
    - Turn indicator showing current player
    - Check indicator for check warnings
    - Game over screen for checkmate and stalemate
    
    Attributes:
        screen: The pygame surface to render on
        fonts: Dictionary of fonts for different text elements
        piece_images: Dictionary of piece images for captured pieces display
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize the UIRenderer with screen and fonts.
        
        Args:
            screen: The pygame surface to render on
        """
        self.screen = screen
        
        # Initialize fonts
        pygame.font.init()
        self.fonts = {
            'large': pygame.font.Font(None, 48),
            'medium': pygame.font.Font(None, 36),
            'small': pygame.font.Font(None, 24),
            'tiny': pygame.font.Font(None, 18)
        }
        
        # Load piece images for captured pieces display
        self.piece_images = self._load_piece_images()
    
    def _load_piece_images(self) -> Dict[str, pygame.Surface]:
        """
        Load piece images for captured pieces display.
        
        Returns:
            Dictionary mapping piece identifiers to pygame surfaces
        """
        piece_images = {}
        colors = ['w', 'b']
        pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
        
        for color in colors:
            for piece in pieces:
                key = f"{color}{piece}"
                try:
                    image = pygame.image.load(f"images/{key}.png")
                    # Scale down for captured pieces display (smaller than board pieces)
                    piece_images[key] = pygame.transform.scale(image, (30, 30))
                except pygame.error as e:
                    print(f"Warning: Could not load image for {key}: {e}")
                    # Create a placeholder surface
                    piece_images[key] = pygame.Surface((30, 30))
                    piece_images[key].fill(WHITE if color == 'w' else BLACK)
        
        return piece_images
    
    def render_move_history(
        self,
        move_history: MoveHistory,
        rect: pygame.Rect,
        scroll_offset: int = 0
    ):
        """
        Render the move history panel with scrolling support.
        
        Args:
            move_history: The MoveHistory object containing all moves
            rect: The rectangle defining the panel area
            scroll_offset: Vertical scroll offset in pixels (for future scrolling)
        """
        # Draw panel background
        pygame.draw.rect(self.screen, LIGHT_BROWN, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)  # Border
        
        # Draw title
        title_text = self.fonts['medium'].render("Move History", True, BLACK)
        title_x = rect.x + (rect.width - title_text.get_width()) // 2
        title_y = rect.y + 10
        self.screen.blit(title_text, (title_x, title_y))
        
        # Draw separator line
        separator_y = title_y + title_text.get_height() + 10
        pygame.draw.line(
            self.screen, BLACK,
            (rect.x + 10, separator_y),
            (rect.x + rect.width - 10, separator_y),
            2
        )
        
        # Get formatted move history
        formatted_moves = move_history.get_formatted_history()
        
        # Render moves
        line_height = 25
        start_y = separator_y + 15
        max_visible_lines = (rect.height - (start_y - rect.y) - 10) // line_height
        
        # Calculate which moves to display (with scrolling)
        start_index = scroll_offset // line_height
        end_index = min(start_index + max_visible_lines, len(formatted_moves))
        
        for i in range(start_index, end_index):
            move_text = formatted_moves[i]
            text_surface = self.fonts['small'].render(move_text, True, BLACK)
            
            y_pos = start_y + (i - start_index) * line_height
            x_pos = rect.x + 15
            
            self.screen.blit(text_surface, (x_pos, y_pos))
        
        # If no moves yet, show placeholder
        if len(formatted_moves) == 0:
            no_moves_text = self.fonts['small'].render("No moves yet", True, (128, 128, 128))
            text_x = rect.x + (rect.width - no_moves_text.get_width()) // 2
            text_y = start_y + 20
            self.screen.blit(no_moves_text, (text_x, text_y))
    
    def render_captured_pieces(
        self,
        captured_pieces: CapturedPieces,
        top_rect: pygame.Rect,
        bottom_rect: pygame.Rect
    ):
        """
        Render captured pieces display showing grouped pieces by type.
        
        Args:
            captured_pieces: The CapturedPieces object tracking all captures
            top_rect: Rectangle for top captured pieces panel (black's captures)
            bottom_rect: Rectangle for bottom captured pieces panel (white's captures)
        """
        # Render white's captured pieces (pieces captured by white, shown at bottom)
        self._render_captured_panel(
            captured_pieces,
            'white',
            bottom_rect,
            "White Captured"
        )
        
        # Render black's captured pieces (pieces captured by black, shown at top)
        self._render_captured_panel(
            captured_pieces,
            'black',
            top_rect,
            "Black Captured"
        )
        
        # Render material advantage
        self._render_material_advantage(captured_pieces, bottom_rect)
    
    def _render_captured_panel(
        self,
        captured_pieces: CapturedPieces,
        captured_by: str,
        rect: pygame.Rect,
        title: str
    ):
        """
        Render a single captured pieces panel.
        
        Args:
            captured_pieces: The CapturedPieces object
            captured_by: 'white' or 'black' - who captured these pieces
            rect: Rectangle for this panel
            title: Title text for the panel
        """
        # Draw panel background
        pygame.draw.rect(self.screen, LIGHT_BROWN, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 2)  # Border
        
        # Get captured pieces grouped by type
        captured_by_type = captured_pieces.get_captured_by_type(captured_by)
        
        # Render pieces
        x_offset = rect.x + 10
        y_offset = rect.y + (rect.height - 30) // 2  # Center vertically
        
        # Determine which color pieces were captured (opposite of who captured them)
        piece_color = 'b' if captured_by == 'white' else 'w'
        
        # Render each piece type with count
        piece_order = ['Q', 'R', 'B', 'N', 'P']  # Order to display pieces
        
        for piece_type in piece_order:
            count = captured_by_type.get(piece_type, 0)
            if count > 0:
                # Render piece image
                piece_key = f"{piece_color}{piece_type}"
                if piece_key in self.piece_images:
                    self.screen.blit(self.piece_images[piece_key], (x_offset, y_offset))
                
                # Render count if more than 1
                if count > 1:
                    count_text = self.fonts['tiny'].render(f"x{count}", True, BLACK)
                    self.screen.blit(count_text, (x_offset + 32, y_offset + 8))
                    x_offset += 65  # More space for count
                else:
                    x_offset += 35  # Just piece width + margin
    
    def _render_material_advantage(
        self,
        captured_pieces: CapturedPieces,
        bottom_rect: pygame.Rect
    ):
        """
        Render material advantage indicator.
        
        Args:
            captured_pieces: The CapturedPieces object
            bottom_rect: Rectangle for positioning (will render to the right)
        """
        advantage = captured_pieces.get_material_advantage()
        
        if advantage == 0:
            return  # No advantage to display
        
        # Determine text and color
        if advantage > 0:
            text = f"+{advantage}"
            color = WHITE  # White is ahead
            bg_color = (50, 50, 50)
        else:
            text = f"{advantage}"  # Already has minus sign
            color = BLACK  # Black is ahead
            bg_color = (200, 200, 200)
        
        # Render advantage text
        advantage_text = self.fonts['medium'].render(text, True, color)
        
        # Position to the right of the bottom panel
        text_x = bottom_rect.x + bottom_rect.width - advantage_text.get_width() - 15
        text_y = bottom_rect.y + (bottom_rect.height - advantage_text.get_height()) // 2
        
        # Draw background box
        padding = 5
        bg_rect = pygame.Rect(
            text_x - padding,
            text_y - padding,
            advantage_text.get_width() + 2 * padding,
            advantage_text.get_height() + 2 * padding
        )
        pygame.draw.rect(self.screen, bg_color, bg_rect)
        pygame.draw.rect(self.screen, BLACK, bg_rect, 2)
        
        # Draw text
        self.screen.blit(advantage_text, (text_x, text_y))
    

    
    def render_turn_indicator(self, current_turn: str, rect: pygame.Rect):
        """
        Render turn indicator showing current player.
        
        Args:
            current_turn: 'white' or 'black'
            rect: Rectangle for the status area
        """
        # Create turn text
        turn_text = f"{current_turn.capitalize()}'s Turn"
        text_surface = self.fonts['large'].render(turn_text, True, BLACK)
        
        # Position in the center of the status rect
        text_x = rect.x + (rect.width - text_surface.get_width()) // 2
        text_y = rect.y + (rect.height - text_surface.get_height()) // 2
        
        self.screen.blit(text_surface, (text_x, text_y))
    
    def render_check_indicator(self, in_check: bool, checked_color: str, rect: pygame.Rect):
        """
        Render check indicator for check warnings.
        
        Args:
            in_check: Whether a player is in check
            checked_color: 'white' or 'black' - which player is in check
            rect: Rectangle for the status area
        """
        if not in_check:
            return
        
        # Create check warning text
        check_text = f"{checked_color.capitalize()} is in CHECK!"
        text_surface = self.fonts['large'].render(check_text, True, CHECK_COLOR)
        
        # Position below the turn indicator
        text_x = rect.x + (rect.width - text_surface.get_width()) // 2
        text_y = rect.y + rect.height - text_surface.get_height() - 10
        
        # Draw background for visibility
        padding = 10
        bg_rect = pygame.Rect(
            text_x - padding,
            text_y - padding,
            text_surface.get_width() + 2 * padding,
            text_surface.get_height() + 2 * padding
        )
        pygame.draw.rect(self.screen, WHITE, bg_rect)
        pygame.draw.rect(self.screen, CHECK_COLOR, bg_rect, 3)
        
        self.screen.blit(text_surface, (text_x, text_y))
    
    def render_game_over(
        self,
        winner: Optional[str],
        is_stalemate: bool,
        screen_center: tuple
    ):
        """
        Render game over screen for checkmate and stalemate.
        
        Args:
            winner: 'white', 'black', or None (for stalemate)
            is_stalemate: Whether the game ended in stalemate
            screen_center: Tuple of (x, y) for screen center
        """
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Determine game over message
        if is_stalemate:
            title_text = "Stalemate!"
            subtitle_text = "Game is a draw"
            title_color = (255, 255, 0)  # Yellow
        else:
            title_text = "Checkmate!"
            subtitle_text = f"{winner.capitalize()} wins!"
            title_color = (0, 255, 0)  # Green
        
        # Render title
        title_surface = self.fonts['large'].render(title_text, True, title_color)
        title_x = screen_center[0] - title_surface.get_width() // 2
        title_y = screen_center[1] - 60
        self.screen.blit(title_surface, (title_x, title_y))
        
        # Render subtitle
        subtitle_surface = self.fonts['medium'].render(subtitle_text, True, WHITE)
        subtitle_x = screen_center[0] - subtitle_surface.get_width() // 2
        subtitle_y = title_y + title_surface.get_height() + 20
        self.screen.blit(subtitle_surface, (subtitle_x, subtitle_y))
        
        # Render instructions
        instruction_text = "Press ESC for menu or R to restart"
        instruction_surface = self.fonts['small'].render(instruction_text, True, (200, 200, 200))
        instruction_x = screen_center[0] - instruction_surface.get_width() // 2
        instruction_y = subtitle_y + subtitle_surface.get_height() + 40
        self.screen.blit(instruction_surface, (instruction_x, instruction_y))
