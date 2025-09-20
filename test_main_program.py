#!/usr/bin/env python3
"""
Simple test to verify the main program works without font errors.
This will test the menu without requiring user interaction.
"""

import os
import sys

import pygame

# Add the snake_game package to Python path
sys.path.insert(0, os.path.dirname(__file__))


def test_main_program():
    """Test the main program flow."""
    print("Testing main program font initialization...")

    try:
        # Import main components
        from main import ModeSelectionMenu
        from snake_game.game_modes import ClassicMode

        # Initialize pygame (like main() does)
        pygame.init()
        print("✓ Pygame initialized in main")

        # Create menu (this should not cause font errors)
        menu = ModeSelectionMenu()
        print("✓ Menu created successfully")

        # Verify font is available
        if pygame.font.get_init():
            print("✓ Font module available in menu")
        else:
            print("✗ Font module not available")
            return False

        # Simulate menu selection (manually return ClassicMode)
        selected_mode = ClassicMode
        print("✓ Mode selection simulated")

        # Test game creation after menu
        from snake_game.game import Game

        game = Game()
        game.reset_game(selected_mode)
        print("✓ Game created after menu selection")

        # Clean up
        pygame.quit()
        print("✓ Clean shutdown successful")

        return True

    except Exception as e:
        print(f"✗ Error occurred: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    print("Main Program Font Test")
    print("=" * 30)
    success = test_main_program()
    print("=" * 30)
    if success:
        print("Result: PASS - Main program working correctly")
        print("The font not initialized error should be fixed!")
    else:
        print("Result: FAIL - Still has issues")
