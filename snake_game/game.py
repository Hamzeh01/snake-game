"""
This module contains the main game interface and rendering logic.
"""
from typing import Tuple, Type
import pygame
from .entities import Snake, Food, Point
from .game_modes import GameMode, ClassicMode, ChallengeMode

# Use key constants directly from the pygame module; some type checkers don't expose them via pygame.locals
K_UP = pygame.K_UP
K_DOWN = pygame.K_DOWN
K_LEFT = pygame.K_LEFT
K_RIGHT = pygame.K_RIGHT

# Initialize Pygame
pygame.init()  # type: ignore[attr-defined]

class GameRenderer:
    """Handles the rendering of game elements."""

    def __init__(self, window_size: Tuple[int, int], grid_size: Tuple[int, int]):
        """Initialize the renderer with window and grid sizes."""
        self.window_size = window_size
        self.grid_size = grid_size
        self.cell_size = (
            window_size[0] // grid_size[0],
            window_size[1] // grid_size[1]
        )

        # Initialize colors
        self.colors = {
            'background': (0, 0, 0),
            'snake': (0, 255, 0),
            'food': (255, 0, 0),
            'text': (255, 255, 255),
            'obstacle': (128, 128, 128)  # Gray for obstacles
        }

        # Initialize Pygame and create window
        pygame.init()  # type: ignore[attr-defined]
        self.screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)  # type: ignore[attr-defined]
        pygame.display.set_caption("Snake Game")
        self.font = pygame.font.Font(None, 36)

    def handle_resize(self, new_size: Tuple[int, int]):
        """Handle window resize event."""
        self.window_size = new_size
        self.cell_size = (
            new_size[0] // self.grid_size[0],
            new_size[1] // self.grid_size[1]
        )
        self.screen = pygame.display.set_mode(new_size, pygame.RESIZABLE)  # type: ignore[attr-defined]

    def draw_snake(self, snake: Snake):
        """Draw the snake on the screen."""
        for segment in snake.body:
            pygame.draw.rect(
                self.screen,
                self.colors['snake'],
                (
                    segment.x * self.cell_size[0],
                    segment.y * self.cell_size[1],
                    self.cell_size[0] - 1,
                    self.cell_size[1] - 1
                )
            )

    def draw_food(self, food: Food):
        """Draw the food on the screen."""
        pygame.draw.rect(
            self.screen,
            self.colors['food'],
            (
                food.position.x * self.cell_size[0],
                food.position.y * self.cell_size[1],
                self.cell_size[0] - 1,
                self.cell_size[1] - 1
            )
        )

    def draw_score(self, score: int):
        """Draw the score on the screen."""
        score_text = self.font.render(f"Score: {score}", True, self.colors['text'])
        self.screen.blit(score_text, (10, 10))

    def draw_mode_info(self, info: str):
        """Draw mode-specific information on the screen."""
        if info:
            info_text = self.font.render(info, True, self.colors['text'])
            self.screen.blit(info_text, (10, 50))

    def draw_obstacles(self, obstacles):
        """Draw obstacles on the screen."""
        for obstacle_pos in obstacles:
            pygame.draw.rect(
                self.screen,
                self.colors['obstacle'],
                (
                    obstacle_pos[0] * self.cell_size[0],
                    obstacle_pos[1] * self.cell_size[1],
                    self.cell_size[0] - 1,
                    self.cell_size[1] - 1
                )
            )

    def draw_start_screen(self):
        """Draw the start screen."""
        title_text = self.font.render("Snake Game", True, self.colors['text'])
        start_text = self.font.render("Press SPACE to Start", True, self.colors['text'])
        
        center_x = self.window_size[0] // 2
        center_y = self.window_size[1] // 2
        
        self.screen.blit(title_text, 
                        (center_x - title_text.get_width() // 2, 
                         center_y - 30))
        self.screen.blit(start_text, 
                        (center_x - start_text.get_width() // 2, 
                         center_y + 30))

    def draw_game_over(self, final_score: int, mode_name: str = ""):
        """Draw the game over screen."""
        game_over_text = self.font.render("Game Over!", True, self.colors['text'])
        score_text = self.font.render(f"Final Score: {final_score}", True, self.colors['text'])
        if mode_name:
            mode_text = self.font.render(f"Mode: {mode_name}", True, self.colors['text'])
        restart_text = self.font.render("Press R to Restart", True, self.colors['text'])
        menu_text = self.font.render("Press M for Main Menu", True, self.colors['text'])
        quit_text = self.font.render("Press Q to Quit", True, self.colors['text'])

        center_x = self.window_size[0] // 2
        center_y = self.window_size[1] // 2

        self.screen.blit(game_over_text, 
                        (center_x - game_over_text.get_width() // 2, 
                         center_y - 90))
        self.screen.blit(score_text, 
                        (center_x - score_text.get_width() // 2, 
                         center_y - 50))
        if mode_name:
            self.screen.blit(mode_text, 
                            (center_x - mode_text.get_width() // 2, 
                             center_y - 20))
        self.screen.blit(restart_text, 
                        (center_x - restart_text.get_width() // 2, 
                         center_y + 10))
        self.screen.blit(menu_text, 
                        (center_x - menu_text.get_width() // 2, 
                         center_y + 40))
        self.screen.blit(quit_text, 
                        (center_x - quit_text.get_width() // 2, 
                         center_y + 70))

class Game:
    """Main game class that coordinates all game components."""

    def __init__(self, window_size: Tuple[int, int] = (800, 600), 
                 grid_size: Tuple[int, int] = (20, 15)):
        """Initialize the game with window and grid sizes."""
        self.window_size = window_size
        self.grid_size = grid_size
        self.renderer = GameRenderer(window_size, grid_size)
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_started = False
        self.return_to_menu = False  # New flag for returning to menu
        self.food = None
        self.reset_game(ClassicMode)
        pygame.init()  # type: ignore[attr-defined]

    def reset_game(self, mode_class: Type[GameMode]):
        """Reset the game state with the specified game mode."""
        start_pos = Point(self.grid_size[0] // 4, self.grid_size[1] // 2)
        self.snake = Snake(start_pos)
        self.food = Food.spawn(self.grid_size, self.snake.body)
        self.game_mode = mode_class(self.grid_size)
        self.running = True
        self.game_started = False
        self.return_to_menu = False

    def handle_input(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.VIDEORESIZE:
                self.renderer.handle_resize((event.w, event.h))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game_mode.game_over:
                    self.reset_game(type(self.game_mode))
                elif event.key == pygame.K_m and self.game_mode.game_over:
                    self.return_to_menu = True
                    self.running = False
                elif event.key == pygame.K_q and self.game_mode.game_over:
                    self.running = False
                elif event.key == pygame.K_SPACE and not self.game_started:
                    self.game_started = True
                elif self.game_started and not self.game_mode.game_over:
                    self._handle_direction_input(event.key)

    def _handle_direction_input(self, key):
        direction_map = {
            K_UP: Point(0, -1),
            K_DOWN: Point(0, 1),
            K_LEFT: Point(-1, 0),
            K_RIGHT: Point(1, 0)
        }
        if key in direction_map:
            self.snake.change_direction(direction_map[key])

    def update(self):
        """Update game state."""
        if not self.game_started:
            self.renderer.draw_start_screen()
            return
            
        if not self.game_mode.game_over:
            # Move snake
            self.snake.move(grow=False)
            
            # Check game rules
            continue_game, message = self.game_mode.update(self.snake, self.food)
            
            if message and "Food eaten!" in message:
                self.snake.move(grow=True)
                # Pass obstacles if available when spawning new food
                obstacles = getattr(self.game_mode, 'obstacles', None)
                self.food = Food.spawn(self.grid_size, self.snake.body, obstacles)
            
            if not continue_game:
                self.game_mode.game_over = True

    def render(self):
        """Render the game state."""
        self.renderer.screen.fill(self.renderer.colors['background'])
        
        if self.game_started:
            self.renderer.draw_snake(self.snake)
            self.renderer.draw_food(self.food)
            self.renderer.draw_score(self.game_mode.get_score())
            
            # Draw mode-specific info
            mode_info = self.game_mode.get_mode_info()
            self.renderer.draw_mode_info(mode_info)
            
            # Draw obstacles for Challenge mode
            if hasattr(self.game_mode, 'get_obstacles'):
                self.renderer.draw_obstacles(self.game_mode.get_obstacles())
            
            if self.game_mode.game_over:
                mode_name = type(self.game_mode).__name__.replace('Mode', ' Mode')
                self.renderer.draw_game_over(self.game_mode.get_score(), mode_name)
        else:
            self.renderer.draw_start_screen()
        
        pygame.display.flip()

    def run(self, fps: int = 10):
        """Main game loop."""
        while self.running:
            self.handle_input()
            self.update()
            self.render()
            
            # Adjust speed based on game mode
            current_fps = fps
            if isinstance(self.game_mode, ChallengeMode) and hasattr(self.game_mode, 'get_speed'):
                current_fps = int(fps * self.game_mode.get_speed())
            
            self.clock.tick(current_fps)

        pygame.quit()
        return self.return_to_menu  # Return True if should return to menu
