"""
This module contains the main game interface and rendering logic.
"""
from __future__ import annotations
from typing import Tuple, Type, Dict, Any
import pygame
from .entities import Snake, Food, Point
from .game_modes import GameMode, ClassicMode, ChallengeMode


# Game configuration constants
DEFAULT_WINDOW_SIZE = (800, 600)
DEFAULT_GRID_SIZE = (20, 15)
DEFAULT_FPS = 10
CELL_PADDING = 1

# Color constants
class Colors:
    """Game color constants."""
    BLACK = (0, 0, 0)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    YELLOW = (255, 255, 0)

# Pygame key constants 
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT


class GameRenderer:
    """Handles the rendering of game elements with improved organization."""

    def __init__(self, window_size: Tuple[int, int], grid_size: Tuple[int, int]) -> None:
        """Initialize the renderer with window and grid sizes."""
        # Ensure pygame and font module are initialized
        if not pygame.get_init():
            pygame.init()
        if not pygame.font.get_init():
            pygame.font.init()
            
        self._window_size = window_size
        self._grid_size = grid_size
        self._cell_size = self._calculate_cell_size()

        # Initialize colors
        self._colors: Dict[str, Tuple[int, int, int]] = {
            'background': Colors.BLACK,
            'snake': Colors.GREEN,
            'food': Colors.RED,
            'text': Colors.WHITE,
            'obstacle': Colors.GRAY
        }

        # Initialize Pygame display
        self._screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        pygame.display.set_caption("Snake Game")
        self._font = pygame.font.Font(None, 36)

    def _calculate_cell_size(self) -> Tuple[int, int]:
        """Calculate the size of each grid cell."""
        return (
            self._window_size[0] // self._grid_size[0],
            self._window_size[1] // self._grid_size[1]
        )

    def handle_resize(self, new_size: Tuple[int, int]) -> None:
        """Handle window resize event."""
        self._window_size = new_size
        self._cell_size = self._calculate_cell_size()
        self._screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)

    def _draw_rect_at_grid_position(self, position: Point, color: Tuple[int, int, int]) -> None:
        """Draw a rectangle at the given grid position."""
        pygame.draw.rect(
            self._screen,
            color,
            (
                position.x * self._cell_size[0],
                position.y * self._cell_size[1],
                self._cell_size[0] - CELL_PADDING,
                self._cell_size[1] - CELL_PADDING
            )
        )

    def draw_snake(self, snake: Snake) -> None:
        """Draw the snake on the screen."""
        for segment in snake.body:
            self._draw_rect_at_grid_position(segment, self._colors['snake'])

    def draw_food(self, food: Food) -> None:
        """Draw the food on the screen."""
        self._draw_rect_at_grid_position(food.position, self._colors['food'])

    def draw_obstacles(self, obstacles: set) -> None:
        """Draw obstacles on the screen."""
        for obstacle_x, obstacle_y in obstacles:
            obstacle_pos = Point(obstacle_x, obstacle_y)
            self._draw_rect_at_grid_position(obstacle_pos, self._colors['obstacle'])

    def _draw_text_at_position(self, text: str, position: Tuple[int, int]) -> None:
        """Draw text at the specified position."""
        text_surface = self._font.render(text, True, self._colors['text'])
        self._screen.blit(text_surface, position)

    def _center_text(self, text_surface: pygame.Surface) -> Tuple[int, int]:
        """Calculate position to center text on screen."""
        center_x = self._window_size[0] // 2 - text_surface.get_width() // 2
        center_y = self._window_size[1] // 2 - text_surface.get_height() // 2
        return center_x, center_y

    def draw_score(self, score: int) -> None:
        """Draw the score on the screen."""
        self._draw_text_at_position(f"Score: {score}", (10, 10))

    def draw_mode_info(self, info: str) -> None:
        """Draw mode-specific information on the screen."""
        if info:
            self._draw_text_at_position(info, (10, 50))

    def draw_start_screen(self) -> None:
        """Draw the start screen."""
        title_text = self._font.render("Snake Game", True, self._colors['text'])
        start_text = self._font.render("Press SPACE to Start", True, self._colors['text'])
        
        title_x, title_y = self._center_text(title_text)
        start_x, start_y = self._center_text(start_text)
        
        self._screen.blit(title_text, (title_x, title_y - 30))
        self._screen.blit(start_text, (start_x, start_y + 30))

    def draw_game_over(self, final_score: int, mode_name: str = "") -> None:
        """Draw the game over screen."""
        texts = [
            ("Game Over!", 0),
            (f"Final Score: {final_score}", 40),
            (f"Mode: {mode_name}", 70) if mode_name else None,
            ("Press R to Restart", 100),
            ("Press M for Main Menu", 130),
            ("Press Q to Quit", 160)
        ]

        center_x = self._window_size[0] // 2
        base_y = self._window_size[1] // 2 - 90

        for text_info in texts:
            if text_info is None:
                continue
            text, y_offset = text_info
            text_surface = self._font.render(text, True, self._colors['text'])
            text_x = center_x - text_surface.get_width() // 2
            self._screen.blit(text_surface, (text_x, base_y + y_offset))

    def fill_background(self) -> None:
        """Fill the screen with background color."""
        self._screen.fill(self._colors['background'])

    def update_display(self) -> None:
        """Update the display."""
        pygame.display.flip()

class Game:
    """Main game class with enhanced architecture and error handling."""

    def __init__(
        self, 
        window_size: Tuple[int, int] = DEFAULT_WINDOW_SIZE, 
        grid_size: Tuple[int, int] = DEFAULT_GRID_SIZE
    ) -> None:
        """Initialize the game with window and grid sizes."""
        self._window_size = window_size
        self._grid_size = grid_size
        self._renderer = GameRenderer(window_size, grid_size)
        self._clock = pygame.time.Clock()
        
        # Game state
        self._running = True
        self._game_started = False
        self._return_to_menu = False
        
        # Game entities
        self._snake: Snake
        self._food: Food
        self._game_mode: GameMode
        
        # Initialize with default mode
        self.reset_game(ClassicMode)

    @property
    def running(self) -> bool:
        """Check if the game is running."""
        return self._running

    @property
    def return_to_menu(self) -> bool:
        """Check if should return to menu."""
        return self._return_to_menu

    def reset_game(self, mode_class: Type[GameMode]) -> None:
        """Reset the game state with the specified game mode."""
        start_pos = Point(self._grid_size[0] // 4, self._grid_size[1] // 2)
        self._snake = Snake(start_pos)
        self._food = Food.spawn(self._grid_size, self._snake.body)
        self._game_mode = mode_class(self._grid_size)
        self._running = True
        self._game_started = False
        self._return_to_menu = False

    def _handle_direction_input(self, key: int) -> None:
        """Handle direction key presses."""
        direction_map = {
            K_UP: Point(0, -1),
            K_DOWN: Point(0, 1),
            K_LEFT: Point(-1, 0),
            K_RIGHT: Point(1, 0)
        }
        if key in direction_map:
            self._snake.change_direction(direction_map[key])

    def handle_input(self) -> None:
        """Handle user input with improved event processing."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.VIDEORESIZE:
                self._renderer.handle_resize((event.w, event.h))
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown_event(event.key)

    def _handle_keydown_event(self, key: int) -> None:
        """Handle keydown events."""
        if key == pygame.K_r and self._game_mode.game_over:
            self.reset_game(type(self._game_mode))
        elif key == pygame.K_m and self._game_mode.game_over:
            self._return_to_menu = True
            self._running = False
        elif key == pygame.K_q and self._game_mode.game_over:
            self._running = False
        elif key == pygame.K_SPACE and not self._game_started:
            self._game_started = True
        elif self._game_started and not self._game_mode.game_over:
            self._handle_direction_input(key)

    def update(self) -> None:
        """Update game state with improved logic."""
        if not self._game_started:
            return
            
        if not self._game_mode.game_over:
            # Move snake
            self._snake.move(grow=False)
            
            # Check game rules
            continue_game, message = self._game_mode.update(self._snake, self._food)
            
            if message and "Food eaten!" in message:
                self._snake.move(grow=True)
                # Pass obstacles if available when spawning new food
                obstacles = getattr(self._game_mode, 'obstacles', None)
                self._food = Food.spawn(self._grid_size, self._snake.body, obstacles)
            
            if not continue_game:
                self._game_mode.game_over = True

    def render(self) -> None:
        """Render the game state with improved organization."""
        self._renderer.fill_background()
        
        if self._game_started:
            self._renderer.draw_snake(self._snake)
            self._renderer.draw_food(self._food)
            self._renderer.draw_score(self._game_mode.score)
            
            # Draw mode-specific info
            mode_info = self._game_mode.get_mode_info()
            self._renderer.draw_mode_info(mode_info)
            
            # Draw obstacles for Challenge mode
            if hasattr(self._game_mode, 'get_obstacles'):
                self._renderer.draw_obstacles(self._game_mode.get_obstacles())
            
            if self._game_mode.game_over:
                mode_name = type(self._game_mode).__name__.replace('Mode', ' Mode')
                self._renderer.draw_game_over(self._game_mode.score, mode_name)
        else:
            self._renderer.draw_start_screen()
        
        self._renderer.update_display()

    def _calculate_fps(self, base_fps: int) -> int:
        """Calculate FPS based on game mode."""
        if isinstance(self._game_mode, ChallengeMode) and hasattr(self._game_mode, 'get_speed'):
            return int(base_fps * self._game_mode.get_speed())
        return base_fps

    def run(self, fps: int = DEFAULT_FPS) -> bool:
        """Main game loop with improved structure."""
        while self._running:
            self.handle_input()
            self.update()
            self.render()
            
            # Adjust speed based on game mode
            current_fps = self._calculate_fps(fps)
            self._clock.tick(current_fps)

        # Don't quit pygame here, let main() handle it
        return self._return_to_menu  # Return True if should return to menu
