"""
This module contains different game modes and their specific rules.
"""

from __future__ import annotations

import random
import time
from abc import ABC, abstractmethod
from typing import Optional, Tuple

from .entities import Food, Point, Snake

# Game mode constants
DEFAULT_TIME_LIMIT = 30
CHALLENGE_SPEED_INCREMENT = 0.15
OBSTACLE_FREQUENCY = 3


class GameMode(ABC):
    """Abstract base class for different game modes with enhanced structure."""

    def __init__(self, grid_size: Tuple[int, int]) -> None:
        """Initialize the game mode."""
        self._grid_size = grid_size
        self._score = 0
        self._game_over = False

    @property
    def grid_size(self) -> Tuple[int, int]:
        """Get the grid size."""
        return self._grid_size

    @property
    def score(self) -> int:
        """Get the current score."""
        return self._score

    @property
    def game_over(self) -> bool:
        """Check if the game is over."""
        return self._game_over

    @game_over.setter
    def game_over(self, value: bool) -> None:
        """Set the game over state."""
        self._game_over = value

    def _wrap_around_movement(self, snake: Snake) -> None:
        """Handle wraparound movement for the snake."""
        head = snake.head
        # Create a new head position with wrapped coordinates
        wrapped_x = head.x % self._grid_size[0]
        wrapped_y = head.y % self._grid_size[1]

        # Update the head position directly in the snake's body
        snake._body[0] = Point(wrapped_x, wrapped_y)

    def _increment_score(self, amount: int = 1) -> None:
        """Increment the score by the specified amount."""
        self._score += amount

    @abstractmethod
    def update(self, snake: Snake, food: Food) -> Tuple[bool, Optional[str]]:
        """Update game state and return if the game should continue."""
        pass

    @abstractmethod
    def get_mode_info(self) -> str:
        """Return mode-specific information to display."""
        pass


class ClassicMode(GameMode):
    """Classic snake game mode - grow longer with each food eaten, with wraparound movement."""

    def update(self, snake: Snake, food: Food) -> Tuple[bool, Optional[str]]:
        """Update classic mode state."""
        # Handle wraparound movement
        self._wrap_around_movement(snake)

        # Check self collision (only collision that ends the game in classic mode)
        if snake.has_self_collision():
            return False, "Self collision!"

        # Check food collision
        if snake.head == food.position:
            self._increment_score()
            return True, "Food eaten!"

        return True, None

    def get_mode_info(self) -> str:
        """Return mode-specific information."""
        return f"Classic Mode - Score: {self._score}"


class TimedMode(GameMode):
    """Timed mode - collect as much food as possible within the time limit."""

    def __init__(
        self, grid_size: Tuple[int, int], time_limit: int = DEFAULT_TIME_LIMIT
    ) -> None:
        """Initialize timed mode with a time limit in seconds."""
        super().__init__(grid_size)
        self._time_limit = time_limit
        self._time_remaining = float(time_limit)
        self._last_update: Optional[float] = None
        self._bonus_points = 0

    @property
    def time_remaining(self) -> float:
        """Get the remaining time."""
        return self._time_remaining

    @property
    def bonus_points(self) -> int:
        """Get the bonus points earned."""
        return self._bonus_points

    def _update_timer(self) -> None:
        """Update the game timer."""
        current_time = time.time()

        if self._last_update is None:
            self._last_update = current_time
        else:
            elapsed = current_time - self._last_update
            self._time_remaining = max(0, self._time_remaining - elapsed)
            self._last_update = current_time

    def _calculate_time_bonus(self) -> int:
        """Calculate bonus points based on remaining time."""
        return int((self._time_remaining / self._time_limit) * 10)

    def update(self, snake: Snake, food: Food) -> Tuple[bool, Optional[str]]:
        """Update timed mode state."""
        self._update_timer()

        if self._time_remaining <= 0:
            return False, "Time's up!"

        # Handle wraparound movement
        self._wrap_around_movement(snake)

        # Check self collision
        if snake.has_self_collision():
            return False, "Self collision!"

        # Check food collision
        if snake.head == food.position:
            # Base points plus bonus for remaining time
            time_bonus = self._calculate_time_bonus()
            total_points = 1 + time_bonus
            self._increment_score(total_points)
            self._bonus_points += time_bonus
            return True, f"Food eaten! +{total_points} points!"

        return True, None

    def get_mode_info(self) -> str:
        """Return mode-specific information."""
        return f"Timed Mode - Score: {self._score} | Time: {int(self._time_remaining)}s"


class ChallengeMode(GameMode):
    """Challenge mode - no wraparound, obstacles appear, and speed increases."""

    def __init__(self, grid_size: Tuple[int, int]) -> None:
        """Initialize challenge mode."""
        super().__init__(grid_size)
        self._speed_multiplier = 1.0
        self._obstacles: set = set()
        self._foods_eaten = 0

    @property
    def speed_multiplier(self) -> float:
        """Get the current speed multiplier."""
        return self._speed_multiplier

    @property
    def obstacles(self) -> set:
        """Get the current obstacles."""
        return self._obstacles.copy()

    def get_obstacles(self) -> set:
        """Return the current obstacles (for backward compatibility)."""
        return self._obstacles

    def get_speed(self) -> float:
        """Return the current speed multiplier (for backward compatibility)."""
        return self._speed_multiplier

    def _is_wall_collision(self, snake: Snake) -> bool:
        """Check if snake collided with walls."""
        head = snake.head
        return (
            head.x < 0
            or head.x >= self._grid_size[0]
            or head.y < 0
            or head.y >= self._grid_size[1]
        )

    def _is_obstacle_collision(self, snake: Snake) -> bool:
        """Check if snake collided with obstacles."""
        head_pos = (snake.head.x, snake.head.y)
        return head_pos in self._obstacles

    def _add_obstacle(self, snake_body: list) -> None:
        """Add a random obstacle to the game."""
        snake_positions = {(point.x, point.y) for point in snake_body}
        available_positions = []

        # Find all available positions
        for x in range(self._grid_size[0]):
            for y in range(self._grid_size[1]):
                pos = (x, y)
                if pos not in snake_positions and pos not in self._obstacles:
                    available_positions.append(pos)

        # Add obstacle if position available
        if available_positions:
            obstacle_pos = random.choice(available_positions)
            self._obstacles.add(obstacle_pos)

    def _increase_difficulty(self, snake_body: list) -> None:
        """Increase game difficulty by adding speed and obstacles."""
        self._foods_eaten += 1
        self._speed_multiplier += CHALLENGE_SPEED_INCREMENT

        # Add obstacle every OBSTACLE_FREQUENCY foods eaten
        if self._foods_eaten % OBSTACLE_FREQUENCY == 0:
            self._add_obstacle(snake_body)

    def update(self, snake: Snake, food: Food) -> Tuple[bool, Optional[str]]:
        """Update challenge mode state."""
        # NO wraparound in challenge mode - check wall collision
        if self._is_wall_collision(snake):
            return False, "Wall collision!"

        # Check self collision
        if snake.has_self_collision():
            return False, "Self collision!"

        # Check obstacle collision
        if self._is_obstacle_collision(snake):
            return False, "Obstacle collision!"

        # Check food collision
        if snake.head == food.position:
            self._increment_score()
            self._increase_difficulty(snake.body)
            return True, "Food eaten!"

        return True, None

    def get_mode_info(self) -> str:
        """Return mode-specific information."""
        return (
            f"Challenge Mode - Score: {self._score} | "
            f"Speed: {self._speed_multiplier:.1f}x | "
            f"Obstacles: {len(self._obstacles)}"
        )
