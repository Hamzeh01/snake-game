"""
Main entry point for the Snake Game.
"""

import sys
import pygame
from snake_game.game import Game
from snake_game.game_modes import ClassicMode, TimedMode, ChallengeMode


def show_mode_selection():
    """Show game mode selection screen."""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game - Mode Selection")
    font = pygame.font.Font(None, 36)

    modes = {
        0: ("Classic Mode", ClassicMode),
        1: ("Timed Mode", TimedMode),
        2: ("Challenge Mode", ChallengeMode),
    }

    selected = 0

    while True:
        screen.fill((0, 0, 0))

        title = font.render("Select Game Mode", True, (255, 255, 255))
        screen.blit(title, (300, 100))

        for i, (mode_name, _) in modes.items():
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = font.render(mode_name, True, color)
            screen.blit(text, (300, 200 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(modes)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(modes)
                elif event.key == pygame.K_RETURN:
                    return modes[selected][1]


def main():
    """Run the main game."""
    while True:
        selected_mode = show_mode_selection()
        if selected_mode is None:  # User closed the mode selection
            break
            
        game = Game()
        game.reset_game(selected_mode)
        return_to_menu = game.run()
        
        if not return_to_menu:  # User chose to quit instead of return to menu
            break


if __name__ == "__main__":
    main()
