"""
This module contains the base game entities and their behaviors.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Union
import random


# Constants for directions
DIRECTION_RIGHT = (1, 0)
DIRECTION_LEFT = (-1, 0)
DIRECTION_UP = (0, -1)
DIRECTION_DOWN = (0, 1)

# Game configuration constants
DEFAULT_SNAKE_LENGTH = 3
MAX_FOOD_SPAWN_ATTEMPTS = 100


@dataclass(frozen=True)
class Point:
    """Represents an immutable point in 2D space with enhanced functionality."""

    x: int
    y: int

    def __add__(self, other: Union[Point, Tuple[int, int]]) -> Point:
        """Add two points or a point and a tuple."""
        if isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1])
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        """Check equality with another Point."""
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        """Make Point hashable for use in sets."""
        return hash((self.x, self.y))

    def is_within_bounds(self, width: int, height: int) -> bool:
        """Check if point is within given bounds."""
        return 0 <= self.x < width and 0 <= self.y < height


class Snake:
    """Represents the snake entity with improved OOP principles and validation."""

    def __init__(self, start_position: Point, initial_length: int = DEFAULT_SNAKE_LENGTH) -> None:
        """Initialize the snake with a starting position and length."""
        if initial_length < 1:
            raise ValueError("Initial length must be at least 1")
        
        self._body: List[Point] = []
        self._direction = Point(*DIRECTION_RIGHT)  # Start moving right

        # Create initial snake body
        for i in range(initial_length):
            self._body.append(Point(start_position.x - i, start_position.y))

    @property
    def body(self) -> List[Point]:
        """Get the snake's body segments."""
        return self._body.copy()  # Return a copy to prevent external modification

    @property
    def head(self) -> Point:
        """Get the snake's head position."""
        return self._body[0]

    @property
    def direction(self) -> Point:
        """Get the current direction."""
        return self._direction

    def move(self, grow: bool = False) -> None:
        """Move the snake in the current direction."""
        new_head = self.head + self._direction
        self._body.insert(0, new_head)
        
        if not grow:
            self._body.pop()

    def change_direction(self, new_direction: Point) -> bool:
        """
        Change the snake's direction if it's valid.
        Returns True if direction was changed, False otherwise.
        """
        # Prevent 180-degree turns (moving directly opposite to current direction)
        if self._is_opposite_direction(new_direction):
            return False
        
        self._direction = new_direction
        return True

    def _is_opposite_direction(self, new_direction: Point) -> bool:
        """Check if the new direction is opposite to current direction."""
        return (self._direction.x == -new_direction.x and self._direction.x != 0) or \
               (self._direction.y == -new_direction.y and self._direction.y != 0)

    def has_self_collision(self) -> bool:
        """Check if the snake's head collides with its body."""
        return self.head in self._body[1:]  # Exclude head from collision check

    def check_collision(self, point: Point) -> bool:
        """Check if the snake collides with a specific point."""
        return point in self._body[1:]  # Exclude head to prevent self-collision on first check

    def __len__(self) -> int:
        """Return the length of the snake."""
        return len(self._body)


class Food:
    """Represents the food entity with optimized spawning algorithm."""

    def __init__(self, position: Point) -> None:
        """Initialize food with a position."""
        self.position = position

    @classmethod
    def spawn(
        cls, 
        grid_size: Tuple[int, int], 
        snake_body: List[Point], 
        obstacles: Union[set, List[Tuple[int, int]], None] = None
    ) -> 'Food':
        """
        Spawn food at a random position using an optimized algorithm.
        
        Args:
            grid_size: Tuple of (width, height) for the game grid
            snake_body: List of points occupied by the snake
            obstacles: Set or list of obstacle positions (x, y) tuples
            
        Returns:
            Food instance at a valid position
        """
        if obstacles is None:
            obstacles = set()
        
        # Convert obstacles to set of tuples for efficient lookup
        obstacle_set = set()
        if obstacles:
            if isinstance(obstacles, (list, tuple)):
                obstacle_set = set(obstacles)
            else:
                obstacle_set = obstacles

        # Calculate available positions more efficiently
        total_positions = grid_size[0] * grid_size[1]
        occupied_positions = len(snake_body) + len(obstacle_set)
        
        if occupied_positions >= total_positions:
            # Fallback: find any position not on snake (ignore obstacles if needed)
            return cls._find_fallback_position(grid_size, snake_body)
        
        # Use optimized spawning for better performance
        if occupied_positions < total_positions * 0.5:  # Less than 50% occupied
            return cls._random_spawn(grid_size, snake_body, obstacle_set)
        else:
            return cls._systematic_spawn(grid_size, snake_body, obstacle_set)

    @classmethod
    def _random_spawn(
        cls, 
        grid_size: Tuple[int, int], 
        snake_body: List[Point], 
        obstacles: set
    ) -> 'Food':
        """Random spawning for sparse grids."""
        snake_positions = {(point.x, point.y) for point in snake_body}
        
        for _ in range(MAX_FOOD_SPAWN_ATTEMPTS):
            position = Point(
                random.randint(0, grid_size[0] - 1), 
                random.randint(0, grid_size[1] - 1)
            )
            pos_tuple = (position.x, position.y)
            
            if pos_tuple not in snake_positions and pos_tuple not in obstacles:
                return cls(position)
        
        # Fallback if random attempts fail
        return cls._find_fallback_position(grid_size, snake_body)

    @classmethod
    def _systematic_spawn(
        cls, 
        grid_size: Tuple[int, int], 
        snake_body: List[Point], 
        obstacles: set
    ) -> 'Food':
        """Systematic spawning for dense grids."""
        snake_positions = {(point.x, point.y) for point in snake_body}
        
        # Create list of all available positions
        available_positions = []
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                pos_tuple = (x, y)
                if pos_tuple not in snake_positions and pos_tuple not in obstacles:
                    available_positions.append(Point(x, y))
        
        if available_positions:
            return cls(random.choice(available_positions))
        
        # Ultimate fallback
        return cls._find_fallback_position(grid_size, snake_body)

    @classmethod
    def _find_fallback_position(cls, grid_size: Tuple[int, int], snake_body: List[Point]) -> 'Food':
        """Find any position not occupied by snake as ultimate fallback."""
        snake_positions = {(point.x, point.y) for point in snake_body}
        
        for x in range(grid_size[0]):
            for y in range(grid_size[1]):
                if (x, y) not in snake_positions:
                    return cls(Point(x, y))
        
        # If somehow all positions are occupied (shouldn't happen in normal gameplay)
        return cls(Point(0, 0))
