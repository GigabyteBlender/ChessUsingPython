"""
GameController class handling the game loop and user interaction.

This module implements the controller layer of the MVC architecture,
coordinating between the model (game state) and view (rendering) components.
"""

import sys
from typing import Dict, List, Optional, Tuple

import pygame

from constants import FPS, HEIGHT, SQUARE_SIZE, WHITE, WIDTH
from model.game_state import GameState
from model.position import Position
from view.animation_manager import AnimationManager
from view.board_renderer import BoardRenderer
from view.layout_manager import LayoutManager
from view.ui_renderer import UIRenderer


class GameController:
    """
    Main game controller handling the game loop and user interaction.
    
    This class coordinates all game components:
    - Manages the game state (model)
    - Handles user input and events
    - Coordinates rendering (view)
    - Manages animations
    - Controls game flow
    
    Attributes:
        game_state: The GameState object managing game logic
        board_renderer: Renderer for the chess board and pieces
        ui_renderer: Renderer for UI elements
        animation_manager: Manager for animations
        layout_manager: Manager for screen layout
        selected_position: Currently selected piece position
        legal_moves_cache: Cached legal moves for selected piece
        screen: Pygame display surface
        clock: Pygame clock for FPS control
        running: Flag indicating if game is running
    """
    
    def __init__(self):
        """Initialize the GameController and all components."""
        # Initialize pygame
        pygame.init()
        
        # Create display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
        
        # Create clock for FPS control
        self.clock = pygame.time.Clock()
        
        # Initialize game state (model)
        self.game_state = GameState()
        
        # Initialize layout manager
        self.layout_manager = LayoutManager(WIDTH, HEIGHT)
        
        # Load piece images
        self.piece_images = self._load_piece_images(self.layout_manager.square_size)
        
        # Initialize renderers (view)
        self.board_renderer = BoardRenderer(
            self.screen,
            self.piece_images,
            self.layout_manager.board_rect,
            self.layout_manager.square_size
        )
        self.ui_renderer = UIRenderer(self.screen)
        
        # Initialize animation manager
        self.animation_manager = AnimationManager()
        
        # Game state tracking
        self.selected_position: Optional[Position] = None
        self.legal_moves_cache: List[Position] = []
        self.running = True
        self.fullscreen = False
        
        # Track last move for highlighting
        self.last_move_positions: Optional[Tuple[Position, Position]] = None
        self.last_move_timer: float = 0.0  # Timer for last move highlight (2 seconds)
        
        # Track hover position for visual feedback
        self.hover_position: Optional[Position] = None
    
    def _load_piece_images(self, square_size: int = SQUARE_SIZE) -> Dict[str, pygame.Surface]:
        """
        Load all chess piece images.
        
        Args:
            square_size: Size to scale pieces to
        
        Returns:
            Dictionary mapping piece sprite names to pygame surfaces
        """
        piece_images = {}
        colors = ['w', 'b']
        pieces = ['K', 'Q', 'R', 'B', 'N', 'P']
        
        for color in colors:
            for piece in pieces:
                key = f"{color}{piece}"
                try:
                    image = pygame.image.load(f"images/{key}.png")
                    # Scale to square size
                    piece_images[key] = pygame.transform.scale(
                        image, (square_size, square_size)
                    )
                except pygame.error as e:
                    print(f"Error loading image for {key}: {e}")
                    # Create placeholder
                    piece_images[key] = pygame.Surface((square_size, square_size))
                    piece_images[key].fill(WHITE if color == 'w' else (0, 0, 0))
        
        return piece_images
    
    def run(self):
        """
        Main game loop.
        
        This method runs the main game loop, handling events, updating
        animations, and rendering the game state.
        """
        while self.running:
            # Calculate delta time for animations
            delta_time = self.clock.get_time() / 1000.0  # Convert to seconds
            
            # Handle events
            events = pygame.event.get()
            self.handle_events(events)
            
            # Update animations
            self.update(delta_time)
            
            # Render everything
            self.render()
            
            # Update display
            pygame.display.flip()
            
            # Cap framerate
            self.clock.tick(FPS)
        
        # Clean up
        pygame.quit()
        sys.exit()
    
    def handle_events(self, events: List[pygame.event.Event]):
        """
        Process all pygame events.
        
        Args:
            events: List of pygame events to process
        """
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keypress(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse_click(event.pos)
            
            elif event.type == pygame.MOUSEMOTION:
                # Update hover position for visual feedback
                self._handle_mouse_motion(event.pos)
    
    def _handle_keypress(self, key: int):
        """
        Handle keyboard input.
        
        Args:
            key: Pygame key constant
        """
        if key == pygame.K_ESCAPE:
            # Return to menu (for now, just quit)
            self.running = False
        
        elif key == pygame.K_f:
            # Toggle fullscreen
            self._toggle_fullscreen()
        
        elif key == pygame.K_r:
            # Restart game (works anytime, not just game over)
            self._restart_game()
    
    def _handle_mouse_motion(self, screen_pos: Tuple[int, int]):
        """
        Handle mouse motion for hover effects.
        
        Args:
            screen_pos: Screen coordinates (x, y) of the mouse
        """
        # Convert screen position to board position
        board_pos = self.board_renderer.get_board_position(screen_pos)
        
        # Only set hover if it's a legal move
        if board_pos is not None and self.selected_position is not None:
            if board_pos in self.legal_moves_cache:
                self.hover_position = board_pos
            else:
                self.hover_position = None
        else:
            self.hover_position = None
    
    def _toggle_fullscreen(self):
        """Toggle between fullscreen and windowed mode."""
        if not self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.fullscreen = True
        else:
            self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            self.fullscreen = False
        
        # Get actual screen dimensions
        screen_width, screen_height = self.screen.get_size()
        
        # Recalculate layout for new screen size
        self.layout_manager = LayoutManager(screen_width, screen_height)
        
        # Reload piece images with new square size
        self.piece_images = self._load_piece_images(self.layout_manager.square_size)
        
        # Update renderers with new screen and layout
        self.board_renderer.screen = self.screen
        self.board_renderer.board_rect = self.layout_manager.board_rect
        self.board_renderer.square_size = self.layout_manager.square_size
        self.board_renderer.piece_images = self.piece_images
        self.ui_renderer.screen = self.screen
    
    def _restart_game(self):
        """Restart the game with a fresh state."""
        self.game_state = GameState()
        self.selected_position = None
        self.legal_moves_cache = []
        self.last_move_positions = None
        self.last_move_timer = 0.0
        self.hover_position = None
        self.animation_manager = AnimationManager()
        self.board_renderer.set_orientation(0.0)
    
    def handle_mouse_click(self, screen_pos: Tuple[int, int]):
        """
        Handle mouse click for piece selection and movement.
        
        Args:
            screen_pos: Screen coordinates (x, y) of the click
        """
        # Don't handle clicks during game over
        if self.game_state.game_over:
            return
        
        # Convert screen position to board position
        board_pos = self.board_renderer.get_board_position(screen_pos)
        
        # If click is outside the board, deselect
        if board_pos is None:
            self.selected_position = None
            self.legal_moves_cache = []
            return
        
        # If a piece is already selected
        if self.selected_position is not None:
            # Check if clicked position is a legal move
            if board_pos in self.legal_moves_cache:
                # Attempt to make the move
                self.attempt_move(board_pos)
            else:
                # Check if clicking on another piece of the same color
                piece = self.game_state.board.get_piece(board_pos)
                if piece is not None and piece.color == self.game_state.current_turn:
                    # Select the new piece
                    self.select_piece(board_pos)
                else:
                    # Deselect
                    self.selected_position = None
                    self.legal_moves_cache = []
        else:
            # No piece selected, try to select one
            self.select_piece(board_pos)
    
    def select_piece(self, position: Position):
        """
        Select a piece and calculate legal moves.
        
        Args:
            position: Board position of the piece to select
        """
        piece = self.game_state.board.get_piece(position)
        
        # Check if there's a piece at this position
        if piece is None:
            self.selected_position = None
            self.legal_moves_cache = []
            return
        
        # Check if it's the current player's piece
        if piece.color != self.game_state.current_turn:
            self.selected_position = None
            self.legal_moves_cache = []
            return
        
        # Select the piece and cache legal moves
        self.selected_position = position
        self.legal_moves_cache = self.game_state.get_legal_moves(position)
    
    def attempt_move(self, end_position: Position):
        """
        Attempt to move the selected piece to the destination.
        
        Args:
            end_position: Destination position for the move
        """
        if self.selected_position is None:
            return
        
        # Try to make the move
        success = self.execute_move(self.selected_position, end_position)
        
        # Clear selection regardless of success
        self.selected_position = None
        self.legal_moves_cache = []
    
    def execute_move(self, start: Position, end: Position) -> bool:
        """
        Execute a validated move and update game state.
        
        This method:
        1. Executes the move in the game state
        2. Updates last move tracking
        3. Flips the board 180° for the next player
        
        Args:
            start: Starting position
            end: Destination position
            
        Returns:
            True if move was successful, False otherwise
        """
        # Attempt to make the move
        success = self.game_state.make_move(start, end)
        
        if success:
            # Update last move for highlighting (with 2-second timer)
            self.last_move_positions = (start, end)
            self.last_move_timer = 2.0  # Highlight for 2 seconds
            
            # Flip board instantly for next player
            current_rotation = self.board_renderer.board_orientation
            new_rotation = (current_rotation + 180) % 360
            self.board_renderer.set_orientation(new_rotation)
        
        return success
    
    def update(self, delta_time: float):
        """
        Update game state and animations.
        
        Args:
            delta_time: Time elapsed since last update in seconds
        """
        # Update last move highlight timer
        if self.last_move_timer > 0:
            self.last_move_timer -= delta_time
            if self.last_move_timer <= 0:
                self.last_move_positions = None
                self.last_move_timer = 0.0
    
    def render(self):
        """Render the complete game state."""
        # Clear screen
        self.screen.fill(WHITE)
        
        # Render the board with highlights
        self.board_renderer.render(
            self.game_state.board,
            self.selected_position,
            self.legal_moves_cache if self.selected_position else None,
            self.last_move_positions,
            self.hover_position
        )
        
        # Render UI elements
        self._render_ui()
        
        # Render game over screen if applicable
        if self.game_state.game_over:
            screen_center = (WIDTH // 2, HEIGHT // 2)
            is_stalemate = self.game_state.winner is None
            self.ui_renderer.render_game_over(
                self.game_state.winner,
                is_stalemate,
                screen_center
            )
    
    def _render_ui(self):
        """Render all UI elements."""
        # Render move history
        self.ui_renderer.render_move_history(
            self.game_state.move_history,
            self.layout_manager.move_history_rect,
            scroll_offset=0
        )
        
        # Render captured pieces
        self.ui_renderer.render_captured_pieces(
            self.game_state.captured_pieces,
            self.layout_manager.captured_pieces_rect['top'],
            self.layout_manager.captured_pieces_rect['bottom']
        )
