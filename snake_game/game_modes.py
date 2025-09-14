"""
This module contains different game modes and their specific rules.
"""

from abc import ABC, abstractmethod
from typing import Optional
import random
from .entities import Snake, Food, Point

class GameMode(ABC):
    """Abstract base class for different game modes."""

    def __init__(self, grid_size):
        """Initialize the game mode."""
        self.grid_size = grid_size
        self.score = 0
        self.game_over = False

    def wrap_around(self, snake: Snake):
        """Handle wraparound movement for the snake."""
        head = snake.head
        head.x = head.x % self.grid_size[0]
        head.y = head.y % self.grid_size[1]

    @abstractmethod
    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update game state and return if the game should continue."""
        raise NotImplementedError

    @abstractmethod
    def get_score(self) -> int:
        """Return the current score."""
        raise NotImplementedError

    def get_mode_info(self) -> str:
        """Return mode-specific information to display."""
        return ""


class ClassicMode(GameMode):
    """Classic snake game mode - grow longer with each food eaten, with wraparound movement."""

    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update classic mode state."""
        # Handle wraparound movement
        self.wrap_around(snake)

        # Check self collision (only collision that ends the game in classic mode)
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

    def get_mode_info(self) -> str:
        """Return mode-specific information."""
        return f"Classic Mode - Score: {self.score}"


class TimedMode(GameMode):
    """Timed mode - collect as much food as possible within the time limit."""

    def __init__(self, grid_size, time_limit: int = 30):
        """Initialize timed mode with a time limit in seconds."""
        super().__init__(grid_size)
        self.time_limit = time_limit
        self.time_remaining = time_limit
        self.last_update = None
        self.bonus_points = 0

    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update timed mode state."""
        import time

        current_time = time.time()

        if self.last_update is None:
            self.last_update = current_time
        else:
            elapsed = current_time - self.last_update
            self.time_remaining = max(0, self.time_remaining - elapsed)
            self.last_update = current_time

        if self.time_remaining <= 0:
            return False, "Time's up!"

        # Handle wraparound movement
        self.wrap_around(snake)

        # Check self collision
        if snake.check_collision(snake.head):
            return False, "Self collision!"

        # Check food collision
        if snake.head == food.position:
            # Base points plus bonus for remaining time
            time_bonus = int(self.time_remaining / self.time_limit * 10)
            self.score += 1 + time_bonus
            self.bonus_points += time_bonus
            return True, f"Food eaten! +{1 + time_bonus} points!"

        return True, None

    def get_score(self) -> int:
        """Return the current score."""
        return self.score

    def get_mode_info(self) -> str:
        """Return mode-specific information."""
        return f"Timed Mode - Score: {self.score} | Time: {int(self.time_remaining)}s"

    def get_score(self) -> int:
        """Return the current score."""
        return self.score


class ChallengeMode(GameMode):
    """Challenge mode - no wraparound, obstacles appear, and speed increases."""

    def __init__(self, grid_size):
        """Initialize challenge mode."""
        super().__init__(grid_size)
        self.speed_multiplier = 1.0
        self.obstacles = set()
        self.foods_eaten = 0

    def _add_obstacle(self, snake_body):
        """Add a random obstacle to the game."""
        max_attempts = 50
        attempts = 0
        while attempts < max_attempts:
            obstacle_pos = Point(
                random.randint(0, self.grid_size[0] - 1),
                random.randint(0, self.grid_size[1] - 1)
            )
            # Ensure obstacle doesn't spawn on snake
            if obstacle_pos not in snake_body and obstacle_pos not in self.obstacles:
                self.obstacles.add((obstacle_pos.x, obstacle_pos.y))
                break
            attempts += 1

    def update(self, snake: Snake, food: Food) -> tuple[bool, Optional[str]]:
        """Update challenge mode state."""
        # NO wraparound in challenge mode - check wall collision
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

        # Check obstacle collision
        if (snake.head.x, snake.head.y) in self.obstacles:
            return False, "Obstacle collision!"

        # Check food collision
        if snake.head == food.position:
            self.score += 1
            self.foods_eaten += 1
            self.speed_multiplier += 0.15  # Increase speed by 15% for each food eaten
            
            # Add obstacle every 3 foods eaten
            if self.foods_eaten % 3 == 0:
                self._add_obstacle(snake.body)
            
            return True, "Food eaten!"

        return True, None

    def get_score(self) -> int:
        """Return the current score."""
        return self.score

    def get_speed(self) -> float:
        """Return the current speed multiplier."""
        return self.speed_multiplier

    def get_mode_info(self) -> str:
        """Return mode-specific information."""
        return f"Challenge Mode - Score: {self.score} | Speed: {self.speed_multiplier:.1f}x | Obstacles: {len(self.obstacles)}"

    def get_obstacles(self):
        """Return the current obstacles."""
        return self.obstacles
