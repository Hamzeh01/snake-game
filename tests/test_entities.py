"""
Test cases for the snake game entities.
"""
import unittest
from snake_game.entities import Point, Snake, Food

class TestPoint(unittest.TestCase):
    """Test cases for the Point class."""

    def test_point_equality(self):
        """Test point equality comparison."""
        p1 = Point(1, 2)
        p2 = Point(1, 2)
        p3 = Point(2, 1)
        
        self.assertEqual(p1, p2)
        self.assertNotEqual(p1, p3)

class TestSnake(unittest.TestCase):
    """Test cases for the Snake class."""

    def setUp(self):
        """Set up test cases."""
        self.start_pos = Point(5, 5)
        self.snake = Snake(self.start_pos)

    def test_initial_snake_creation(self):
        """Test snake initialization."""
        self.assertEqual(len(self.snake.body), 3)
        self.assertEqual(self.snake.head, self.start_pos)
        self.assertEqual(self.snake.direction, Point(1, 0))

    def test_snake_movement(self):
        """Test snake movement."""
        initial_head = self.snake.head
        self.snake.move()
        
        # Test normal movement
        self.assertEqual(self.snake.head, Point(initial_head.x + 1, initial_head.y))
        self.assertEqual(len(self.snake.body), 3)

        # Test growing
        self.snake.move(grow=True)
        self.assertEqual(len(self.snake.body), 4)

    def test_direction_change(self):
        """Test snake direction changes."""
        # Test valid direction change
        self.snake.change_direction(Point(0, 1))
        self.assertEqual(self.snake.direction, Point(0, 1))

        # Test invalid direction change (180 degrees)
        self.snake.change_direction(Point(0, -1))
        self.assertEqual(self.snake.direction, Point(0, 1))

    def test_collision_detection(self):
        """Test snake collision detection."""
        # Test with check_collision method directly  
        snake = Snake(Point(5, 5))
        
        # Test collision with a body segment position
        body_segment_pos = Point(4, 5)  # This is where second segment is initially
        self.assertTrue(snake.check_collision(body_segment_pos))
        
        # Test no collision with head position
        self.assertFalse(snake.check_collision(snake.head))

class TestFood(unittest.TestCase):
    """Test cases for the Food class."""

    def test_food_spawn(self):
        """Test food spawning."""
        grid_size = (10, 10)
        snake_body = [Point(5, 5), Point(5, 6), Point(5, 7)]
        
        food = Food.spawn(grid_size, snake_body)
        
        # Test food position is within grid
        self.assertTrue(0 <= food.position.x < grid_size[0])
        self.assertTrue(0 <= food.position.y < grid_size[1])
        
        # Test food doesn't spawn on snake
        self.assertNotIn(food.position, snake_body)

if __name__ == '__main__':
    unittest.main()
