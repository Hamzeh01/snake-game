"""
This module contains different game modes and their specific rules.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .entities import Snake, Food

class GameMode(ABC):
    """Abstract base class for different game modes."""

    def __init__(self, grid_size):
        """Initialize the game mode."""
        self.grid_size = grid_size
        self.score = 0
        self.game_over = False

    @abstractmethod
    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update game state and return if the game should continue."""
        raise NotImplementedError

    @abstractmethod
    def get_score(self) -> int:
        """Return the current score."""
        raise NotImplementedError


class ClassicMode(GameMode):
    """Classic snake game mode - grow longer with each food eaten."""

    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update classic mode state."""
        # Check wall collision
        if (
            snake.head.x < 0
            or snake.head.x >= self.grid_size[0]
            or snake.head.y < 0
            or snake.head.y >= self.grid_size[1]
        ):
            return False, "Wall collision!"

        # Check self collision
        if snake.check_collision(snake.head):
            return False, "Self collision!"

        # Check food collision
        if snake.head == food.position:
            self.score += 1
            return True, "Food eaten!"

        return True, None

    def get_score(self) -> int:
        """Return the current score."""
        return self.score


class TimedMode(GameMode):
    """Timed mode - collect as much food as possible within the time limit."""

    def __init__(self, grid_size, time_limit: int = 60):
        """Initialize timed mode with a time limit in seconds."""
        super().__init__(grid_size)
        self.time_limit = time_limit
        self.time_remaining = time_limit
        self.last_update = None

    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update timed mode state."""
        import time

        current_time = time.time()

        if self.last_update is None:
            self.last_update = current_time
        else:
            self.time_remaining -= current_time - self.last_update
            self.last_update = current_time

        if self.time_remaining <= 0:
            return False, "Time's up!"

        # Check wall and self collision
        if (
            snake.head.x < 0
            or snake.head.x >= self.grid_size[0]
            or snake.head.y < 0
            or snake.head.y >= self.grid_size[1]
            or snake.check_collision(snake.head)
        ):
            return False, "Collision!"

        # Check food collision
        if snake.head == food.position:
            self.score += 1
            return True, "Food eaten!"

        return True, None

    def get_score(self) -> int:
        """Return the current score."""
        return self.score


class ChallengeMode(GameMode):
    """Challenge mode - snake moves faster as it grows longer."""

    def __init__(self, grid_size):
        """Initialize challenge mode."""
        super().__init__(grid_size)
        self.speed_multiplier = 1.0

    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update challenge mode state."""
        # Check wall and self collision
        if (
            snake.head.x < 0
            or snake.head.x >= self.grid_size[0]
            or snake.head.y < 0
            or snake.head.y >= self.grid_size[1]
            or snake.check_collision(snake.head)
        ):
            return False, "Collision!"

        # Check food collision
        if snake.head == food.position:
            self.score += 1
            self.speed_multiplier += 0.1  # Increase speed by 10% for each food eaten
            return True, "Food eaten!"

        return True, None

    def get_score(self) -> int:
        """Return the current score."""
        return self.score

    def get_speed(self) -> float:
        """Return the current speed multiplier."""
        return self.speed_multiplier
