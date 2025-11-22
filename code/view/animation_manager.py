"""
AnimationManager for handling smooth animations in the chess game.

This module provides animation support for board flipping and other visual effects.
"""

import time
from dataclasses import dataclass
from typing import List


@dataclass
class Animation:
    """Represents a single animation."""
    start_time: float
    duration: float  # in seconds
    start_value: float
    end_value: float
    animation_type: str  # 'board_flip', etc.
    
    def get_progress(self, current_time: float) -> float:
        """Get animation progress from 0.0 to 1.0."""
        elapsed = current_time - self.start_time
        if elapsed >= self.duration:
            return 1.0
        return elapsed / self.duration
    
    def is_complete(self, current_time: float) -> bool:
        """Check if animation is complete."""
        return (current_time - self.start_time) >= self.duration


class AnimationManager:
    """
    Manages smooth animations for board flipping and piece movement.
    
    The AnimationManager handles timing, interpolation, and easing for all
    visual animations in the chess game. It supports multiple concurrent
    animations and provides smooth transitions using easing functions.
    """
    
    def __init__(self):
        """Initialize the AnimationManager with an empty animation list."""
        self.active_animations: List[Animation] = []
        self.current_rotation: float = 0.0
    
    def start_board_flip(self, from_angle: float, to_angle: float, 
                        duration_ms: int = 500):
        """
        Start a board flip animation.
        
        Args:
            from_angle: Starting rotation angle in degrees (0 or 180)
            to_angle: Ending rotation angle in degrees (0 or 180)
            duration_ms: Animation duration in milliseconds (default: 500)
        """
        # Clear any existing board flip animations
        self.active_animations = [
            anim for anim in self.active_animations 
            if anim.animation_type != 'board_flip'
        ]
        
        # Create new board flip animation
        animation = Animation(
            start_time=time.time(),
            duration=duration_ms / 1000.0,  # Convert to seconds
            start_value=from_angle,
            end_value=to_angle,
            animation_type='board_flip'
        )
        
        self.active_animations.append(animation)
        self.current_rotation = from_angle
    
    def update(self, delta_time: float) -> bool:
        """
        Update all active animations.
        
        Args:
            delta_time: Time elapsed since last update in seconds (not used directly,
                       we use absolute time for more accurate animations)
        
        Returns:
            True if any animations are still active, False otherwise
        """
        current_time = time.time()
        
        # Update current rotation based on active board flip animation
        for animation in self.active_animations:
            if animation.animation_type == 'board_flip':
                progress = animation.get_progress(current_time)
                # Apply ease-in-out easing function
                eased_progress = self._ease_in_out(progress)
                # Interpolate between start and end values
                self.current_rotation = (
                    animation.start_value + 
                    (animation.end_value - animation.start_value) * eased_progress
                )
        
        # Remove completed animations
        self.active_animations = [
            anim for anim in self.active_animations 
            if not anim.is_complete(current_time)
        ]
        
        return len(self.active_animations) > 0
    
    def get_current_rotation(self) -> float:
        """
        Get the current board rotation angle.
        
        Returns:
            Current rotation angle in degrees (0-180)
        """
        return self.current_rotation
    
    def is_animating(self) -> bool:
        """
        Check if any animations are currently active.
        
        Returns:
            True if animations are active, False otherwise
        """
        return len(self.active_animations) > 0
    
    def _ease_in_out(self, t: float) -> float:
        """
        Apply ease-in-out easing function for smooth animation.
        
        This creates a smooth acceleration at the start and deceleration at the end,
        making the animation feel more natural and polished.
        
        Args:
            t: Progress value from 0.0 to 1.0
        
        Returns:
            Eased progress value from 0.0 to 1.0
        """
        if t < 0.5:
            # Ease in: accelerate (quadratic)
            return 2 * t * t
        else:
            # Ease out: decelerate (quadratic)
            return 1 - 2 * (1 - t) * (1 - t)
