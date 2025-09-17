#!/usr/bin/env python3
"""
Test script to verify the font initialization fix.
"""

import pygame
import sys
import os

# Add the snake_game package to Python path
sys.path.insert(0, os.path.dirname(__file__))

def test_font_initialization():
    """Test that font initialization works correctly."""
    print("Testing font initialization fix...")
    
    try:
        # Initialize pygame
        pygame.init()
        print("✓ pygame.init() successful")
        
        # Check if font module is initialized
        if pygame.font.get_init():
            print("✓ Font module initialized")
        else:
            print("! Font module not initialized, initializing...")
            pygame.font.init()
            print("✓ Font module manually initialized")
        
        # Try to create a font object
        font = pygame.font.Font(None, 36)
        print("✓ Font object created successfully")
        
        # Try to render text
        text_surface = font.render("Test Text", True, (255, 255, 255))
        print("✓ Text rendered successfully")
        
        # Test the game imports
        from snake_game.game import Game
        from snake_game.game_modes import ClassicMode
        print("✓ Game modules imported successfully")
        
        # Test game creation (but don't run the game loop)
        game = Game()
        print("✓ Game instance created successfully")
        
        game.reset_game(ClassicMode)
        print("✓ Game reset with ClassicMode successful")
        
        pygame.quit()
        print("✓ All tests passed!")
        
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Font Initialization Test")
    print("=" * 30)
    success = test_font_initialization()
    print("=" * 30)
    if success:
        print("Result: PASS - Font initialization working correctly")
    else:
        print("Result: FAIL - Font initialization needs more work")