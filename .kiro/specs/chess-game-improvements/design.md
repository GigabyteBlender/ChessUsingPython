# Design Document: Chess Game Improvements

## Overview

This design document outlines the architecture and implementation approach for improving the existing pygame-based chess game. The improvements focus on three main areas:

1. **Architectural Refactoring**: Implementing a clean Model-View-Controller (MVC) pattern to separate concerns
2. **Enhanced Playability**: Adding modern chess game features like move highlighting, history tracking, and captured pieces display
3. **Board Flipping**: Implementing smooth board rotation between turns so each player views the board from their perspective

The design maintains backward compatibility with the existing piece images and pygame infrastructure while restructuring the codebase for better maintainability and extensibility.

## Architecture

### Model-View-Controller Pattern

The application will be restructured using the MVC pattern:

```
┌─────────────────────────────────────────────────────────┐
│                      Controller                          │
│  - GameController: Handles user input and game flow     │
│  - Coordinates between Model and View                    │
└──────────────┬──────────────────────────┬────────────────┘
               │                          │
               ▼                          ▼
┌──────────────────────────┐  ┌──────────────────────────┐
│         Model            │  │          View            │
│  - GameState             │  │  - BoardRenderer         │
│  - Board                 │  │  - UIRenderer            │
│  - Piece (abstract)      │  │  - AnimationManager      │
│  - MoveValidator         │  │  - LayoutManager         │
│  - MoveHistory           │  │                          │
└──────────────────────────┘  └──────────────────────────┘
```

**Benefits of this architecture:**
- Game logic is independent of rendering (can be tested without pygame)
- View can be swapped or modified without changing game rules
- Controller manages the interaction flow cleanly
- Each component has a single, well-defined responsibility

### Component Responsibilities

**Model Layer:**
- `GameState`: Maintains the current state of the game (board, turn, check status, captured pieces)
- `Board`: Represents the 8x8 chess board and piece positions
- `Piece` classes: Encapsulate piece-specific movement rules
- `MoveValidator`: Validates moves according to chess rules
- `MoveHistory`: Tracks all moves in algebraic notation

**View Layer:**
- `BoardRenderer`: Renders the chess board and pieces with proper orientation
- `UIRenderer`: Renders UI elements (move history, captured pieces, turn indicator)
- `AnimationManager`: Handles smooth animations (board flipping, move animations)
- `LayoutManager`: Manages screen layout and coordinate transformations

**Controller Layer:**
- `GameController`: Main game loop and event handling
- Translates user input to model operations
- Triggers view updates based on model changes

## Components and Interfaces

### Model Components

#### GameState Class

```python
class GameState:
    """
    Maintains the complete state of the chess game.
    """
    def __init__(self):
        self.board: Board
        self.current_turn: str  # 'white' or 'black'
        self.move_history: MoveHistory
        self.captured_pieces: dict  # {'white': [], 'black': []}
        self.check_status: dict  # {'white': False, 'black': False}
        self.game_over: bool
        self.winner: Optional[str]
        
    def make_move(self, start: Position, end: Position) -> bool:
        """Execute a move if valid, update state, return success."""
        
    def is_in_check(self, color: str) -> bool:
        """Check if the specified color's king is in check."""
        
    def is_checkmate(self, color: str) -> bool:
        """Check if the specified color is in checkmate."""
        
    def is_stalemate(self) -> bool:
        """Check if the game is in stalemate."""
        
    def get_legal_moves(self, position: Position) -> List[Position]:
        """Get all legal moves for the piece at the given position."""
```

#### Board Class

```python
class Board:
    """
    Represents the chess board and piece positions.
    """
    def __init__(self):
        self.grid: List[List[Optional[Piece]]]  # 8x8 grid
        
    def get_piece(self, position: Position) -> Optional[Piece]:
        """Get the piece at the specified position."""
        
    def set_piece(self, position: Position, piece: Optional[Piece]):
        """Place or remove a piece at the specified position."""
        
    def move_piece(self, start: Position, end: Position) -> Optional[Piece]:
        """Move a piece and return any captured piece."""
        
    def find_king(self, color: str) -> Position:
        """Find the position of the king for the specified color."""
        
    def get_all_pieces(self, color: str) -> List[Tuple[Position, Piece]]:
        """Get all pieces of the specified color."""
        
    def copy(self) -> 'Board':
        """Create a deep copy of the board for move simulation."""
```

#### Piece Classes

```python
class Piece(ABC):
    """
    Abstract base class for all chess pieces.
    """
    def __init__(self, color: str, position: Position):
        self.color: str  # 'white' or 'black'
        self.position: Position
        self.has_moved: bool = False
        self.piece_type: str  # 'pawn', 'rook', 'knight', etc.
        
    @abstractmethod
    def get_possible_moves(self, board: Board) -> List[Position]:
        """Get all possible moves (not considering check)."""
        
    def get_sprite_name(self) -> str:
        """Return the sprite name for rendering (e.g., 'wK', 'bP')."""

class Pawn(Piece):
    def get_possible_moves(self, board: Board) -> List[Position]:
        # Implement pawn movement including en passant
        
class Rook(Piece):
    def get_possible_moves(self, board: Board) -> List[Position]:
        # Implement rook movement
        
# Similar classes for Knight, Bishop, Queen, King
```

#### MoveValidator Class

```python
class MoveValidator:
    """
    Validates chess moves according to all rules.
    """
    def is_legal_move(self, board: Board, start: Position, end: Position, 
                     current_turn: str) -> bool:
        """Check if a move is legal considering all rules including check."""
        
    def would_leave_in_check(self, board: Board, start: Position, 
                            end: Position, color: str) -> bool:
        """Check if a move would leave the player's king in check."""
        
    def can_castle(self, board: Board, king_pos: Position, 
                   rook_pos: Position) -> bool:
        """Check if castling is legal."""
        
    def is_en_passant_legal(self, board: Board, start: Position, 
                           end: Position, move_history: MoveHistory) -> bool:
        """Check if en passant capture is legal."""
```

#### MoveHistory Class

```python
class MoveHistory:
    """
    Tracks all moves in algebraic notation.
    """
    def __init__(self):
        self.moves: List[MoveRecord]
        
    def add_move(self, piece: Piece, start: Position, end: Position, 
                 captured: Optional[Piece], is_check: bool, 
                 is_checkmate: bool):
        """Add a move to the history in algebraic notation."""
        
    def get_last_move(self) -> Optional[MoveRecord]:
        """Get the most recent move."""
        
    def to_algebraic_notation(self, piece: Piece, start: Position, 
                             end: Position, captured: bool, 
                             is_check: bool, is_checkmate: bool) -> str:
        """Convert a move to algebraic notation (e.g., 'Nf3', 'exd5')."""
        
    def get_formatted_history(self) -> List[str]:
        """Get formatted move history for display."""
```

### View Components

#### BoardRenderer Class

```python
class BoardRenderer:
    """
    Renders the chess board and pieces with proper orientation.
    """
    def __init__(self, screen: pygame.Surface, piece_images: dict):
        self.screen: pygame.Surface
        self.piece_images: dict
        self.board_orientation: float = 0.0  # Rotation angle in degrees
        self.square_size: int
        
    def render(self, board: Board, selected_pos: Optional[Position], 
               legal_moves: List[Position], last_move: Optional[Tuple[Position, Position]]):
        """Render the complete board with highlights."""
        
    def draw_squares(self):
        """Draw the checkerboard pattern."""
        
    def draw_pieces(self, board: Board):
        """Draw all pieces considering current orientation."""
        
    def highlight_square(self, position: Position, color: tuple):
        """Highlight a specific square."""
        
    def highlight_legal_moves(self, positions: List[Position], board: Board):
        """Highlight legal move destinations (different for captures)."""
        
    def get_board_position(self, screen_pos: tuple) -> Position:
        """Convert screen coordinates to board position considering orientation."""
        
    def get_screen_position(self, board_pos: Position) -> tuple:
        """Convert board position to screen coordinates considering orientation."""
```

#### UIRenderer Class

```python
class UIRenderer:
    """
    Renders UI elements (move history, captured pieces, status indicators).
    """
    def __init__(self, screen: pygame.Surface):
        self.screen: pygame.Surface
        self.fonts: dict
        
    def render_move_history(self, move_history: MoveHistory, scroll_offset: int):
        """Render the move history panel."""
        
    def render_captured_pieces(self, captured_pieces: dict):
        """Render captured pieces with material advantage."""
        
    def render_turn_indicator(self, current_turn: str):
        """Render whose turn it is."""
        
    def render_check_indicator(self, in_check: bool):
        """Render check warning if applicable."""
        
    def render_game_over(self, winner: Optional[str], is_stalemate: bool):
        """Render game over screen."""
        
    def calculate_material_advantage(self, captured_pieces: dict) -> dict:
        """Calculate material advantage in points."""
```

#### AnimationManager Class

```python
class AnimationManager:
    """
    Manages smooth animations for board flipping and piece movement.
    """
    def __init__(self):
        self.active_animations: List[Animation]
        
    def start_board_flip(self, from_angle: float, to_angle: float, 
                        duration_ms: int):
        """Start a board flip animation."""
        
    def update(self, delta_time: float) -> bool:
        """Update all active animations, return True if any are active."""
        
    def get_current_rotation(self) -> float:
        """Get the current board rotation angle."""
        
    def is_animating(self) -> bool:
        """Check if any animations are active."""
```

#### LayoutManager Class

```python
class LayoutManager:
    """
    Manages screen layout and coordinate transformations.
    """
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width: int
        self.screen_height: int
        self.board_rect: pygame.Rect
        self.move_history_rect: pygame.Rect
        self.captured_pieces_rect: pygame.Rect
        self.status_rect: pygame.Rect
        
    def calculate_layout(self):
        """Calculate positions for all UI elements."""
        
    def transform_coordinates(self, pos: tuple, rotation: float) -> tuple:
        """Transform coordinates based on board rotation."""
```

### Controller Components

#### GameController Class

```python
class GameController:
    """
    Main game controller handling the game loop and user interaction.
    """
    def __init__(self):
        self.game_state: GameState
        self.board_renderer: BoardRenderer
        self.ui_renderer: UIRenderer
        self.animation_manager: AnimationManager
        self.layout_manager: LayoutManager
        self.selected_position: Optional[Position] = None
        self.legal_moves_cache: List[Position] = []
        
    def run(self):
        """Main game loop."""
        
    def handle_events(self, events: List[pygame.event.Event]):
        """Process all pygame events."""
        
    def handle_mouse_click(self, screen_pos: tuple):
        """Handle mouse click for piece selection and movement."""
        
    def select_piece(self, position: Position):
        """Select a piece and calculate legal moves."""
        
    def attempt_move(self, end_position: Position):
        """Attempt to move the selected piece."""
        
    def execute_move(self, start: Position, end: Position):
        """Execute a validated move and update game state."""
        
    def flip_board(self):
        """Initiate board flip animation."""
        
    def update(self, delta_time: float):
        """Update game state and animations."""
        
    def render(self):
        """Render the complete game state."""
```

## Data Models

### Position

```python
@dataclass
class Position:
    """Represents a position on the chess board."""
    row: int  # 0-7
    col: int  # 0-7
    
    def to_algebraic(self) -> str:
        """Convert to algebraic notation (e.g., 'e4')."""
        return f"{chr(ord('a') + self.col)}{8 - self.row}"
    
    @staticmethod
    def from_algebraic(notation: str) -> 'Position':
        """Create Position from algebraic notation."""
        col = ord(notation[0]) - ord('a')
        row = 8 - int(notation[1])
        return Position(row, col)
```

### MoveRecord

```python
@dataclass
class MoveRecord:
    """Represents a single move in the game."""
    move_number: int
    player: str  # 'white' or 'black'
    piece_type: str
    start: Position
    end: Position
    captured_piece: Optional[str]
    is_check: bool
    is_checkmate: bool
    is_castling: bool
    is_en_passant: bool
    algebraic_notation: str
    timestamp: float
```

### CapturedPieces

```python
@dataclass
class CapturedPieces:
    """Tracks captured pieces for both players."""
    white_captured: List[str]  # Pieces captured by white
    black_captured: List[str]  # Pieces captured by black
    
    def add_capture(self, piece_type: str, captured_by: str):
        """Add a captured piece."""
        
    def get_material_advantage(self) -> int:
        """Calculate material advantage (positive = white ahead)."""
```

## Co
rrectness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Board flip rotation invariant

*For any* valid move executed on the board, the board rotation angle should change by exactly 180 degrees (modulo 360).
**Validates: Requirements 1.1**

### Property 2: Board orientation preserves game logic

*For any* board state and rotation angle, the set of legal moves for any piece should remain identical regardless of the visual orientation.
**Validates: Requirements 1.2**

### Property 3: Coordinate transformation consistency

*For any* screen position and board rotation angle, transforming screen coordinates to board coordinates and then back to screen coordinates should yield the original position (within pixel tolerance).
**Validates: Requirements 1.5**

### Property 4: Legal moves highlight completeness

*For any* selected piece on any board state, the set of highlighted squares should exactly match the set of legal moves calculated by the move validator.
**Validates: Requirements 2.1**

### Property 5: Capture move visual distinction

*For any* set of legal moves for a piece, moves that result in captures should have different visual indicators than moves that don't result in captures.
**Validates: Requirements 2.2**

### Property 6: Selected piece highlighting

*For any* piece selection, the piece's square should be highlighted with a distinct color different from legal move highlights.
**Validates: Requirements 2.3**

### Property 7: Algebraic notation correctness

*For any* valid move, the generated algebraic notation should correctly represent the piece type, destination square, and any special conditions (capture, check, checkmate).
**Validates: Requirements 3.1**

### Property 8: Move history chronological ordering

*For any* sequence of moves, the move history should maintain chronological order where move N+1 comes after move N.
**Validates: Requirements 3.2**

### Property 9: Move attribution correctness

*For any* move in the history, the player attribution should alternate between white and black, starting with white.
**Validates: Requirements 3.4**

### Property 10: Capture tracking accuracy

*For any* move that captures a piece, the captured piece should appear in the capturing player's captured pieces list.
**Validates: Requirements 4.1**

### Property 11: Captured pieces grouping

*For any* list of captured pieces, pieces of the same type should be grouped together with accurate counts.
**Validates: Requirements 4.2**

### Property 12: Material advantage calculation

*For any* set of captured pieces, the material advantage should equal the sum of captured pieces using standard values (Pawn=1, Knight=3, Bishop=3, Rook=5, Queen=9) for the capturing player minus the opponent's captures.
**Validates: Requirements 4.4, 4.5**

### Property 13: Move validation completeness

*For any* attempted move, the move validator should reject moves that violate piece-specific movement rules, capture own pieces, or move out of bounds.
**Validates: Requirements 6.1**

### Property 14: King safety enforcement

*For any* move that would leave or place the moving player's king in check, the move should be rejected and the board state should remain unchanged.
**Validates: Requirements 6.2**

### Property 15: Check escape requirement

*For any* board state where a player is in check, all legal moves for that player should result in a board state where the player is no longer in check.
**Validates: Requirements 6.3**

### Property 16: Pawn promotion execution

*For any* pawn that reaches the opposite end of the board (row 0 for white, row 7 for black), the pawn should be replaced with a queen.
**Validates: Requirements 6.5**

### Property 17: Turn indicator accuracy

*For any* turn change, the turn indicator should display the color of the player whose turn it is.
**Validates: Requirements 7.2**

### Property 18: Check indicator display

*For any* board state where a player's king is in check, the check indicator should be displayed.
**Validates: Requirements 7.3**

### Property 19: Stalemate detection

*For any* board state where a player has no legal moves and is not in check, the game should be declared a stalemate.
**Validates: Requirements 7.5**

### Property 20: Castling legality

*For any* board state, castling should be legal only when: the king and rook haven't moved, no pieces are between them, the king is not in check, and the king doesn't move through or into check.
**Validates: Requirements 8.1, 8.5**

### Property 21: Castling execution correctness

*For any* castling move (kingside or queenside), both the king and rook should move to their correct final positions (king moves 2 squares toward rook, rook moves to square king crossed).
**Validates: Requirements 8.2**

### Property 22: En passant legality

*For any* board state, en passant should be legal only when: a pawn is on the 5th rank (white) or 4th rank (black), an opponent pawn just moved two squares to an adjacent file, and the capture is made immediately on the next turn.
**Validates: Requirements 8.3**

### Property 23: En passant execution correctness

*For any* en passant capture, the captured pawn should be removed from its current square (not the destination square), and the capturing pawn should move diagonally to the destination square.
**Validates: Requirements 8.4**

## Error Handling

### Model Layer Error Handling

**Invalid Move Attempts:**
- When an invalid move is attempted, the `MoveValidator` returns `False` without modifying the board
- The `GameState` maintains its previous state
- No exceptions are thrown for invalid moves (they are expected user input)

**Missing Pieces:**
- When a piece is expected but not found (e.g., king), the system should log an error and enter a safe state
- This indicates a critical bug and should be caught during testing

**Board State Corruption:**
- All board modifications go through controlled methods
- Deep copies are used for move simulation to prevent accidental state corruption
- Validation checks ensure board integrity after each move

### View Layer Error Handling

**Missing Assets:**
- If piece images fail to load, the application should display an error message and exit gracefully
- Asset loading happens at initialization, not during gameplay

**Rendering Failures:**
- If pygame rendering fails, log the error and attempt to continue
- Critical rendering failures should display an error dialog

**Coordinate Transformation Errors:**
- Out-of-bounds coordinates should be clamped or rejected
- Invalid transformations should log warnings but not crash

### Controller Layer Error Handling

**Event Processing:**
- Unexpected events should be logged but not crash the application
- Invalid user input should be silently ignored (e.g., clicking outside the board)

**Animation Failures:**
- If animations fail to complete, snap to the final state
- Don't block gameplay waiting for animations

## Testing Strategy

### Unit Testing Approach

The chess game will use unit tests to verify specific examples and edge cases:

**Model Layer Unit Tests:**
- Test initial board setup matches standard chess starting position
- Test each piece type's basic movement rules with specific examples
- Test edge cases like pawn promotion at row boundaries
- Test castling with specific board configurations
- Test en passant with specific move sequences
- Test checkmate detection with known checkmate patterns (e.g., back rank mate, fool's mate)
- Test stalemate detection with known stalemate positions

**View Layer Unit Tests:**
- Test coordinate transformation with specific screen positions and rotation angles
- Test algebraic notation generation for specific moves
- Test material advantage calculation with specific captured piece sets

**Controller Layer Unit Tests:**
- Test game initialization creates correct starting state
- Test turn switching after valid moves
- Test game over detection with specific end states

### Property-Based Testing Approach

The chess game will use **Hypothesis** (Python's property-based testing library) to verify universal properties across many randomly generated inputs.

**Configuration:**
- Each property-based test will run a minimum of 100 iterations
- Tests will use custom generators for valid chess positions, moves, and game states

**Property Test Implementation:**
- Each property-based test MUST be tagged with a comment referencing the correctness property from this design document
- Tag format: `# Feature: chess-game-improvements, Property {number}: {property_text}`
- Each correctness property will be implemented by a SINGLE property-based test

**Model Layer Property Tests:**

*Property 1: Board flip rotation invariant*
- Generate random valid moves
- Execute move and verify rotation changes by 180 degrees

*Property 2: Board orientation preserves game logic*
- Generate random board states and rotation angles
- Verify legal moves are identical regardless of orientation

*Property 3: Coordinate transformation consistency*
- Generate random screen positions and rotation angles
- Verify round-trip transformation preserves position

*Property 13: Move validation completeness*
- Generate random invalid moves (wrong piece movement, capturing own pieces, out of bounds)
- Verify all are rejected

*Property 14: King safety enforcement*
- Generate random moves that would leave king in check
- Verify all are rejected and board unchanged

*Property 15: Check escape requirement*
- Generate random board states with check
- Verify all legal moves remove check

*Property 16: Pawn promotion execution*
- Generate random pawn moves to final rank
- Verify pawn is replaced with queen

*Property 20: Castling legality*
- Generate random board states
- Verify castling is only legal when all conditions are met

*Property 21: Castling execution correctness*
- Generate random valid castling moves
- Verify both pieces end in correct positions

*Property 22: En passant legality*
- Generate random board states with potential en passant
- Verify en passant is only legal when conditions are met

*Property 23: En passant execution correctness*
- Generate random valid en passant captures
- Verify captured pawn removed from correct square

**View Layer Property Tests:**

*Property 4: Legal moves highlight completeness*
- Generate random piece selections
- Verify highlighted squares match legal moves

*Property 7: Algebraic notation correctness*
- Generate random valid moves
- Verify algebraic notation correctly represents the move

*Property 12: Material advantage calculation*
- Generate random sets of captured pieces
- Verify material calculation uses correct values

**Integration Property Tests:**

*Property 8: Move history chronological ordering*
- Generate random sequences of valid moves
- Verify history maintains chronological order

*Property 9: Move attribution correctness*
- Generate random sequences of valid moves
- Verify player attribution alternates correctly

*Property 10: Capture tracking accuracy*
- Generate random capture moves
- Verify captured pieces appear in correct list

*Property 17: Turn indicator accuracy*
- Generate random valid moves
- Verify turn indicator updates correctly

*Property 19: Stalemate detection*
- Generate random board states with no legal moves and no check
- Verify stalemate is detected

### Test Organization

```
tests/
├── unit/
│   ├── model/
│   │   ├── test_board.py
│   │   ├── test_pieces.py
│   │   ├── test_move_validator.py
│   │   ├── test_game_state.py
│   │   └── test_move_history.py
│   ├── view/
│   │   ├── test_board_renderer.py
│   │   ├── test_ui_renderer.py
│   │   └── test_layout_manager.py
│   └── controller/
│       └── test_game_controller.py
├── property/
│   ├── test_board_properties.py
│   ├── test_move_properties.py
│   ├── test_special_moves_properties.py
│   └── test_game_flow_properties.py
└── integration/
    └── test_full_game.py
```

### Testing Guidelines

- Unit tests focus on specific examples and edge cases
- Property tests verify universal rules across many inputs
- Integration tests verify complete game flows
- All tests should be independent and repeatable
- Tests should not depend on timing or animation completion
- Model tests should not require pygame initialization

## Implementation Notes

### Board Flipping Implementation

The board flip will be implemented as a visual transformation only:

1. **Rotation State**: Track current rotation angle (0° or 180°)
2. **Coordinate Transformation**: All rendering uses transformed coordinates based on rotation
3. **Input Transformation**: Mouse clicks are transformed back to board coordinates
4. **Animation**: Smooth interpolation between rotation states over 500ms
5. **Game Logic Independence**: All game logic operates on untransformed board coordinates

### Move Validation Optimization

To maintain performance:

1. **Caching**: Cache legal moves for the selected piece until the board state changes
2. **Incremental Updates**: Only recalculate affected pieces after a move
3. **Early Termination**: Stop checking moves once a legal move is found (for check/checkmate detection)
4. **Lazy Evaluation**: Only calculate legal moves when needed (piece selection or validation)

### Algebraic Notation Generation

Standard algebraic notation rules:

- Piece moves: `Nf3` (piece letter + destination)
- Pawn moves: `e4` (destination only)
- Captures: `Nxf3` or `exd5` (x indicates capture)
- Castling: `O-O` (kingside) or `O-O-O` (queenside)
- Check: `+` suffix
- Checkmate: `#` suffix
- Disambiguation: Add file, rank, or both if multiple pieces can move to same square

### Special Moves Implementation

**Castling:**
- Validate: King and rook haven't moved, no pieces between, not in/through/into check
- Execute: Move king 2 squares toward rook, move rook to square king crossed
- Update: Mark both pieces as having moved

**En Passant:**
- Track: Store last move in game state
- Validate: Opponent pawn just moved 2 squares, landing adjacent to player's pawn
- Execute: Move pawn diagonally, remove opponent's pawn from its current square
- Timing: Only valid immediately after the 2-square pawn move

**Pawn Promotion:**
- Detect: Pawn reaches opposite end (row 0 or 7)
- Execute: Replace pawn with queen automatically
- Future: Could add UI for piece selection (queen, rook, bishop, knight)

### Performance Considerations

**Target Performance:**
- 60 FPS rendering
- < 50ms input response
- < 100ms move validation
- < 500ms board flip animation

**Optimization Strategies:**
- Use dirty rectangles for partial screen updates
- Cache rendered pieces
- Minimize board state copies
- Use efficient data structures (lists for board, not dictionaries)
- Profile and optimize hot paths (move validation, rendering)

### Future Extensibility

The architecture supports future enhancements:

- **AI Opponent**: Add AI player that implements same interface as human player
- **Network Play**: Add network layer that synchronizes game state
- **Move Replay**: Use move history to replay games
- **Save/Load**: Serialize game state to file
- **Different Time Controls**: Add chess clocks and time management
- **Piece Themes**: Support different piece image sets
- **Board Themes**: Support different color schemes
- **Sound Effects**: Add audio feedback for moves, captures, check
- **Move Hints**: Highlight suggested moves for beginners
- **Analysis Mode**: Allow stepping through move history

## File Structure

```
code/
├── chess.py                 # Main entry point (refactored)
├── model/
│   ├── __init__.py
│   ├── game_state.py       # GameState class
│   ├── board.py            # Board class
│   ├── pieces.py           # All Piece classes
│   ├── move_validator.py   # MoveValidator class
│   ├── move_history.py     # MoveHistory class
│   └── data_models.py      # Position, MoveRecord, etc.
├── view/
│   ├── __init__.py
│   ├── board_renderer.py   # BoardRenderer class
│   ├── ui_renderer.py      # UIRenderer class
│   ├── animation_manager.py # AnimationManager class
│   └── layout_manager.py   # LayoutManager class
├── controller/
│   ├── __init__.py
│   └── game_controller.py  # GameController class
└── constants.py            # Shared constants (colors, sizes, etc.)

images/                      # Existing piece images (unchanged)
├── bB.png
├── bK.png
├── ...

tests/                       # Test files (as outlined above)
├── unit/
├── property/
└── integration/
```

## Migration Strategy

To migrate from the existing monolithic `chess.py` to the new architecture:

1. **Phase 1: Extract Model**
   - Create model classes
   - Move game logic from Chess class to model
   - Keep existing rendering temporarily

2. **Phase 2: Extract View**
   - Create view classes
   - Move rendering from Chess class to view
   - Keep existing event handling temporarily

3. **Phase 3: Extract Controller**
   - Create controller class
   - Move event handling to controller
   - Wire up MVC components

4. **Phase 4: Add New Features**
   - Implement board flipping
   - Add move highlighting
   - Add move history display
   - Add captured pieces display

5. **Phase 5: Polish**
   - Add animations
   - Optimize performance
   - Add special moves (castling, en passant)
   - Final testing and bug fixes

Each phase should maintain a working game, allowing for incremental development and testing.
