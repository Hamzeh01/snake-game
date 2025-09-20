"""
Test cases for different game modes.
"""

import unittest

from snake_game.entities import Food, Point, Snake
from snake_game.game_modes import ChallengeMode, ClassicMode, TimedMode


class TestClassicMode(unittest.TestCase):
    """Test cases for the ClassicMode class."""

    def setUp(self):
        """Set up test cases."""
        self.grid_size = (10, 10)
        self.mode = ClassicMode(self.grid_size)
        self.snake = Snake(Point(5, 5))
        self.food = Food(Point(7, 5))

    def test_wall_collision(self):
        """Test wall collision detection."""
        # In ClassicMode, there are no wall collisions due to wraparound
        # Move snake to wall position and verify wraparound behavior
        wall_snake = Snake(Point(-1, 5))
        continue_game, _ = self.mode.update(wall_snake, self.food)

        # Should continue game and wrap around
        self.assertTrue(continue_game)
        # After wraparound, snake head should be at right edge
        self.assertEqual(wall_snake.head.x, self.grid_size[0] - 1)

    def test_self_collision(self):
        """Test self collision detection."""
        # Create self collision by manually setting body positions
        collision_snake = Snake(Point(5, 5))
        collision_snake._body = [Point(5, 5), Point(5, 5)]
        continue_game, message = self.mode.update(collision_snake, self.food)
        self.assertFalse(continue_game)
        self.assertEqual(message, "Self collision!")

    def test_food_collision(self):
        """Test food collision detection and scoring."""
        # Move snake to food
        food_snake = Snake(self.food.position)
        continue_game, message = self.mode.update(food_snake, self.food)
        self.assertTrue(continue_game)
        self.assertEqual(message, "Food eaten!")
        self.assertEqual(self.mode.score, 1)


class TestTimedMode(unittest.TestCase):
    """Test cases for the TimedMode class."""

    def setUp(self):
        """Set up test cases."""
        self.grid_size = (10, 10)
        self.mode = TimedMode(self.grid_size, time_limit=5)
        self.snake = Snake(Point(5, 5))
        self.food = Food(Point(7, 5))

    def test_time_limit(self):
        """Test time limit functionality."""
        # Set time remaining to 0 to trigger timeout
        self.mode._time_remaining = 0
        continue_game, message = self.mode.update(self.snake, self.food)
        self.assertFalse(continue_game)
        self.assertEqual(message, "Time's up!")


class TestChallengeMode(unittest.TestCase):
    """Test cases for the ChallengeMode class."""

    def setUp(self):
        """Set up test cases."""
        self.grid_size = (10, 10)
        self.mode = ChallengeMode(self.grid_size)
        self.snake = Snake(Point(5, 5))
        self.food = Food(Point(7, 5))

    def test_speed_increase(self):
        """Test speed increase after eating food."""
        initial_speed = self.mode.get_speed()

        # Simulate eating food
        food_snake = Snake(self.food.position)
        self.mode.update(food_snake, self.food)

        # Check speed increase
        self.assertGreater(self.mode.get_speed(), initial_speed)


if __name__ == "__main__":
    unittest.main()
