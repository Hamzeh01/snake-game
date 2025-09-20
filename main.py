"""
Main entry point for the Snake Game with enhanced user interface.
"""

from __future__ import annotations

import sys
from typing import Dict, Optional, Tuple, Type

import pygame

from snake_game.game import Game
from snake_game.game_modes import ChallengeMode, ClassicMode, GameMode, TimedMode

# UI Configuration Constants
WINDOW_SIZE = (800, 600)
FONT_SIZE = 36
BACKGROUND_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 255, 255)
HIGHLIGHT_COLOR = (255, 255, 0)
MENU_START_Y = 200
MENU_ITEM_HEIGHT = 50


class ModeSelectionMenu:
    """Handles the game mode selection interface with improved organization."""

    def __init__(self) -> None:
        """Initialize the mode selection menu."""
        # Don't initialize pygame here if it's already initialized
        if not pygame.get_init():
            pygame.init()
        self._screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Snake Game - Mode Selection")
        self._font = pygame.font.Font(None, FONT_SIZE)
        self._clock = pygame.time.Clock()

        self._modes: Dict[int, Tuple[str, Type[GameMode]]] = {
            0: ("Classic Mode", ClassicMode),
            1: ("Timed Mode", TimedMode),
            2: ("Challenge Mode", ChallengeMode),
        }

        self._selected_index = 0
        self._running = True

    def _draw_title(self) -> None:
        """Draw the menu title."""
        title_text = self._font.render("Select Game Mode", True, TEXT_COLOR)
        title_x = WINDOW_SIZE[0] // 2 - title_text.get_width() // 2
        self._screen.blit(title_text, (title_x, 100))

    def _draw_mode_options(self) -> None:
        """Draw the mode selection options."""
        for i, (mode_name, _) in self._modes.items():
            color = HIGHLIGHT_COLOR if i == self._selected_index else TEXT_COLOR
            text_surface = self._font.render(mode_name, True, color)

            text_x = WINDOW_SIZE[0] // 2 - text_surface.get_width() // 2
            text_y = MENU_START_Y + i * MENU_ITEM_HEIGHT

            self._screen.blit(text_surface, (text_x, text_y))

    def _draw_instructions(self) -> None:
        """Draw usage instructions."""
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER to select",
            "Press ESC to quit",
        ]

        start_y = MENU_START_Y + len(self._modes) * MENU_ITEM_HEIGHT + 50
        font_small = pygame.font.Font(None, 24)

        for i, instruction in enumerate(instructions):
            text_surface = font_small.render(instruction, True, TEXT_COLOR)
            text_x = WINDOW_SIZE[0] // 2 - text_surface.get_width() // 2
            text_y = start_y + i * 25
            self._screen.blit(text_surface, (text_x, text_y))

    def _handle_navigation(self, key: int) -> None:
        """Handle menu navigation."""
        if key == pygame.K_UP:
            self._selected_index = (self._selected_index - 1) % len(self._modes)
        elif key == pygame.K_DOWN:
            self._selected_index = (self._selected_index + 1) % len(self._modes)

    def _handle_selection(self) -> Optional[Type[GameMode]]:
        """Handle mode selection."""
        return self._modes[self._selected_index][1]

    def _handle_events(self) -> Optional[Type[GameMode]]:
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
                return None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self._running = False
                    return None
                elif event.key in (pygame.K_UP, pygame.K_DOWN):
                    self._handle_navigation(event.key)
                elif event.key == pygame.K_RETURN:
                    self._running = False
                    return self._handle_selection()
        return "continue"  # Special value to continue the loop

    def show(self) -> Optional[Type[GameMode]]:
        """Show the mode selection menu and return the selected mode."""
        while self._running:
            self._screen.fill(BACKGROUND_COLOR)

            self._draw_title()
            self._draw_mode_options()
            self._draw_instructions()

            pygame.display.flip()

            result = self._handle_events()
            if result != "continue":
                # Don't quit pygame here, just return the result
                return result

            self._clock.tick(60)  # 60 FPS for smooth menu experience

        # Don't quit pygame here either
        return None


def show_mode_selection() -> Optional[Type[GameMode]]:
    """Show game mode selection screen with improved interface."""
    menu = ModeSelectionMenu()
    return menu.show()


def main() -> None:
    """Run the main game with enhanced error handling and flow control."""
    # Initialize pygame once at the start
    pygame.init()

    try:
        while True:
            selected_mode = show_mode_selection()
            if selected_mode is None:  # User closed the mode selection or quit
                break

            # Initialize and run the game
            game = Game()
            game.reset_game(selected_mode)
            return_to_menu = game.run()

            if not return_to_menu:  # User chose to quit instead of return to menu
                break

    except KeyboardInterrupt:
        print("\nGame interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback

        traceback.print_exc()
    finally:
        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    main()
