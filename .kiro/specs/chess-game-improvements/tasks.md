# Implementation Plan

- [x] 1. Set up project structure and data models




  - Create directory structure for model, view, and controller components
  - Implement Position dataclass with algebraic notation conversion
  - Implement MoveRecord dataclass for move history tracking
  - Implement CapturedPieces dataclass for tracking captures
  - Create constants.py with shared constants (colors, sizes, piece values)
  - _Requirements: 5.1, 5.5_





- [ ] 2. Implement core model layer - Board and Piece classes

  - Create abstract Piece base class with color, position, and has_moved attributes
  - Implement Board class with 8x8 grid and piece management methods


  - Implement get_piece, set_piece, move_piece, find_king, get_all_pieces methods
  - Implement board copy method for move simulation
  - _Requirements: 5.1, 6.1_

- [ ] 3. Implement piece movement rules

  - Implement Pawn class with forward movement and diagonal capture logic
  - Implement Rook class with horizontal and vertical movement
  - Implement Knight class with L-shaped movement
  - Implement Bishop class with diagonal movement
  - Implement Queen class combining rook and bishop movement
  - Implement King class with one-square movement in any direction
  - _Requirements: 6.1, 6.4_

- [ ]* 3.1 Write property test for basic piece movement validation
  - **Property 13: Move validation completeness**
  - **Validates: Requirements 6.1**

- [ ] 4. Implement MoveValidator class





  - Create MoveValidator with is_legal_move method
  - Implement validation for piece-specific movement rules
  - Implement validation to prevent capturing own pieces
  - Implement validation for out-of-bounds moves
  - Implement would_leave_in_check method using board simulation
  - _Requirements: 6.1, 6.2_

- [ ]* 4.1 Write property test for king safety enforcement
  - **Property 14: King safety enforcement**
  - **Validates: Requirements 6.2**




- [ ] 5. Implement check and checkmate detection

  - Implement is_under_attack method in MoveValidator
  - Implement is_in_check method in GameState
  - Implement get_legal_moves method that filters moves leaving king in check
  - Implement is_checkmate method checking for no legal moves while in check
  - Implement is_stalemate method checking for no legal moves without check
  - _Requirements: 6.2, 6.3, 7.5_

- [ ]* 5.1 Write property test for check escape requirement
  - **Property 15: Check escape requirement**
  - **Validates: Requirements 6.3**



- [ ]* 5.2 Write property test for stalemate detection
  - **Property 19: Stalemate detection**
  - **Validates: Requirements 7.5**

- [ ] 6. Implement pawn promotion




  - Add pawn promotion detection in GameState.make_move
  - Automatically promote pawns reaching opposite end to queens
  - Update board with promoted piece
  - _Requirements: 6.4, 6.5_


- [ ]* 6.1 Write property test for pawn promotion execution
  - **Property 16: Pawn promotion execution**
  - **Validates: Requirements 6.5**

- [x] 7. Implement special moves - Castling






  - Add castling validation in MoveValidator.can_castle
  - Check king and rook haven't moved using has_moved attribute
  - Check no pieces between king and rook
  - Check king not in check, not moving through check, not into check
  - Implement castling execution moving both king and rook
  - Update has_moved flags for both pieces
  - _Requirements: 8.1, 8.2, 8.5_

- [ ]* 7.1 Write property test for castling legality
  - **Property 20: Castling legality**

  - **Validates: Requirements 8.1, 8.5**

- [ ]* 7.2 Write property test for castling execution correctness
  - **Property 21: Castling execution correctness**
  - **Validates: Requirements 8.2**
-

- [x] 8. Implement special moves - En Passant





  - Add last_move tracking to GameState
  - Implement is_en_passant_legal in MoveValidator
  - Check for pawn on correct rank with opponent pawn that just moved 2 squares
  - Implement en passant execution removing captured pawn from correct square
  - _Requirements: 8.3, 8.4_

- [ ]* 8.1 Write property test for en passant legality


  - **Property 22: En passant legality**
  - **Validates: Requirements 8.3**

- [ ]* 8.2 Write property test for en passant execution correctness
  - **Property 23: En passant execution correctness**
  - **Validates: Requirements 8.4**
-

- [x] 9. Implement MoveHistory class





  - Create MoveHistory class with moves list
  - Implement add_move method
  - Implement to_algebraic_notation method for standard chess notation
  - Handle piece moves, pawn moves, captures, castling, check, checkmate
  - Implement disambiguation for multiple pieces moving to same square
  - Implement get_formatted_history for display
  - _Requirements: 3.1, 3.2, 3.4_

- [ ]* 9.1 Write property test for algebraic notation correctness
  - **Property 7: Algebraic notation correctness**
  - **Validates: Requirements 3.1**


- [ ]* 9.2 Write property test for move history chronological ordering
  - **Property 8: Move history chronological ordering**
  - **Validates: Requirements 3.2**

- [ ]* 9.3 Write property test for move attribution correctness
  - **Property 9: Move attribution correctness**
  - **Validates: Requirements 3.4**
-

- [x] 10. Implement GameState class





  - Create GameState with board, current_turn, move_history, captured_pieces
  - Implement make_move method coordinating validation and execution
  - Update captured_pieces when pieces are captured
  - Update check_status after each move
  - Detect checkmate and stalemate conditions
  - Switch turns after successful moves


  - _Requirements: 5.1, 5.4, 7.2_

- [ ]* 10.1 Write property test for capture tracking accuracy
  - **Property 10: Capture tracking accuracy**
  - **Validates: Requirements 4.1**

- [ ]* 10.2 Write property test for turn indicator accuracy
  - **Property 17: Turn indicator accuracy**


  - **Validates: Requirements 7.2**

- [x] 12. Implement LayoutManager for screen organization




  - Create LayoutManager class with screen dimensions
  - Calculate board_rect for centered board display
  - Calculate move_history_rect for right panel
  - Calculate captured_pieces_rect for side panels
  - Calculate status_rect for turn and check indicators
  - Implement transform_coordinates for rotation handling
  - _Requirements: 5.2, 1.5_
-

- [x] 13. Implement BoardRenderer class





  - Create BoardRenderer with screen and piece images
  - Implement draw_squares for checkerboard pattern
  - Implement draw_pieces rendering all pieces with rotation
  - Implement highlight_square for selected piece
  - Implement highlight_legal_moves with different colors for captures
  - Implement get_board_position converting screen to board coordinates
  - Implement get_screen_position converting board to screen coordinates
  - Handle coordinate transformation based on board_orientation
  - _Requirements: 1.2, 1.5, 2.1, 2.2, 2.3, 5.2_

- [ ]* 13.1 Write property test for coordinate transformation consistency
  - **Property 3: Coordinate transformation consistency**

  - **Validates: Requirements 1.5**

- [ ]* 13.2 Write property test for legal moves highlight completeness
  - **Property 4: Legal moves highlight completeness**
  - **Validates: Requirements 2.1**

- [ ]* 13.3 Write property test for capture move visual distinction
  - **Property 5: Capture move visual distinction**
  - **Validates: Requirements 2.2**

- [ ]* 13.4 Write property test for selected piece highlighting
  - **Property 6: Selected piece highlighting**
  - **Validates: Requirements 2.3**

- [x] 14. Implement UIRenderer class






  - Create UIRenderer with screen and fonts
  - Implement render_move_history displaying moves in panel with scrolling
  - Implement render_captured_pieces showing grouped pieces by type
  - Implement calculate_material_advantage using standard piece values
  - Implement render_turn_indicator showing current player
  - Implement render_check_indicator for check warnings






  - Implement render_game_over for checkmate and stalemate
  - _Requirements: 3.2, 3.3, 4.2, 4.3, 4.4, 4.5, 5.2, 7.1, 7.2, 7.3, 7.4_

- [ ]* 14.1 Write property test for captured pieces grouping
  - **Property 11: Captured pieces grouping**
  - **Validates: Requirements 4.2**

- [ ]* 14.2 Write property test for material advantage calculation
  - **Property 12: Material advantage calculation**




  - **Validates: Requirements 4.4, 4.5**

- [ ]* 14.3 Write property test for check indicator display
  - **Property 18: Check indicator display**
  - **Validates: Requirements 7.3**
- [x] 15. Implement AnimationManager class




- [ ] 15. Implement AnimationManager class


  - Create AnimationManager with active_animations list
  - Implement start_board_flip creating rotation animation
  - Implement update method advancing animations by delta_time
  - Use easing function for smooth rotation (ease-in-out)
  - Implement get_current_rotation returning interpolated angle

  - Implement is_animating checking for active animations
  - Target 500ms duration for board flip
  - _Requirements: 1.1, 1.4_

- [ ]* 15.1 Write property test for board flip rotation invariant
  - **Property 1: Board flip rotation invariant**
  - **Validates: Requirements 1.1**

-

- [x] 16. Implement GameController class




  - Create GameController initializing all components
  - Implement main run loop with event handling
  - Implement handle_mouse_click for piece selection and moves
  - Implement select_piece caching legal moves
  - Implement attempt_move validating and executing moves





  - Implement execute_move updating game state and triggering board flip
  - Implement flip_board starting animation
  - Implement update method for animations
  - Implement render method coordinating all rendering
  - _Requirements: 5.3, 5.4, 9.1, 9.2_

- [ ]* 16.1 Write property test for board orientation preserves game logic
  - **Property 2: Board orientation preserves game logic**
  - **Validates: Requirements 1.2**




- [ ] 17. Refactor main entry point


  - Update chess.py to use new GameController
  - Keep Menu class for main menu
  - Wire up Play button to start GameController



  - Maintain existing menu functionality
  - _Requirements: 5.3_

- [ ] 18. Add visual polish and final touches


  - Add last move highlighting (origin and destination squares)




  - Add hover effects for legal move squares
  - Ensure smooth 60 FPS rendering
  - Add keyboard shortcuts (ESC for menu, F for fullscreen)
  - Test and adjust colors for better visibility
  - _Requirements: 2.4, 2.5, 9.2, 9.4_

- [ ] 20. Integration testing and bug fixes


  - Test complete game flows from start to checkmate
  - Test all special moves in real game scenarios
  - Test board flipping with various game states
  - Test UI responsiveness and layout on different screen sizes
  - Fix any bugs discovered during integration testing
  - _Requirements: All_
