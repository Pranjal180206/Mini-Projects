import pygame
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, TITLE, FPS,
    COLOR_BG, COLOR_WHITE, COLOR_SCORE, COLOR_SUBTITLE
)
import sys

def show_menu(screen, clock, font, big_font):
    """
    Displays the Main Menu. Connects directly to the event loop.
    Returns:
        True if the player pressed ENTER to start the game.
        False if the player pressed ESC or closed the window to quit.
    """
    menu_running = True
    start_game = False

    while menu_running:
        screen.fill(COLOR_BG)

        # Title
        title_surf = big_font.render(TITLE, True, COLOR_SCORE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        screen.blit(title_surf, title_rect)

        # Start instruction
        start_surf = font.render(f"Press ENTER to Start", True, COLOR_WHITE)
        start_rect = start_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(start_surf, start_rect)
        
        # Quit instruction
        exit_surf = font.render(f"Press ESC to Exit", True, COLOR_SUBTITLE)
        exit_rect = exit_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
        screen.blit(exit_surf, exit_rect)

        pygame.display.update()
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    start_game = True
                    menu_running = False
                elif event.key == pygame.K_ESCAPE:
                    menu_running = False

        clock.tick(FPS)

    return start_game
