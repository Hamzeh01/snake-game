"""
This module contains the base game entities and their behaviors.
"""

from dataclasses import dataclass
from typing import List, Tuple
import random


@dataclass
class Point:
    """Represents a point in 2D space."""

    x: int
    y: int

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y


class Snake:
    """Represents the snake entity in the game."""

    def __init__(self, start_position: Point, initial_length: int = 3):
        """Initialize the snake with a starting position and length."""
        self.body: List[Point] = []
        self.direction = Point(1, 0)  # Start moving right

        # Create initial snake body
        for i in range(initial_length):
            self.body.append(Point(start_position.x - i, start_position.y))

    def move(self, grow: bool = False) -> None:
        """Move the snake in the current direction."""
        new_head = Point(
            self.body[0].x + self.direction.x, self.body[0].y + self.direction.y
        )
        self.body.insert(0, new_head)
        if not grow:
            self.body.pop()

    def change_direction(self, new_direction: Point) -> None:
        """Change the snake's direction if it's valid."""
        # Prevent 180-degree turns
        if (new_direction.x != -self.direction.x or new_direction.x == 0) and (
            new_direction.y != -self.direction.y or new_direction.y == 0
        ):
            self.direction = new_direction

    @property
    def head(self) -> Point:
        """Get the snake's head position."""
        return self.body[0]

    def check_collision(self, point: Point) -> bool:
        """Check if the snake collides with a point."""
        return (
            point in self.body[1:]
        )  # Exclude head to prevent self-collision on first check


class Food:
    """Represents the food entity in the game."""

    def __init__(self, position: Point):
        """Initialize food with a position."""
        self.position = position

    @classmethod
    def spawn(cls, grid_size: Tuple[int, int], snake_body: List[Point]):
        """Spawn food at a random position that doesn't overlap with the snake."""
        while True:
            position = Point(
                random.randint(0, grid_size[0] - 1), random.randint(0, grid_size[1] - 1)
            )
            if position not in snake_body:
                return cls(position)
