"""
utils/helpers.py — Utility functions for safe asset loading.
"""

import os
import sys
import pygame


def load_image(path: str, fallback_size: tuple = (64, 64),
               fallback_color: tuple = (255, 0, 255)) -> pygame.Surface:
    """Load an image from *path*. If the file is missing or corrupt,
    return a brightly-colored placeholder surface so the game doesn't crash."""
    try:
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Asset not found: {path}")
        image = pygame.image.load(path).convert_alpha()
        return image
    except (pygame.error, FileNotFoundError) as exc:
        print(f"[WARNING] Could not load image '{path}': {exc}")
        surface = pygame.Surface(fallback_size, pygame.SRCALPHA)
        surface.fill(fallback_color)
        return surface


def resource_path(relative_path: str) -> str:
    """Resolve a path relative to the project root. Works for both
    development and PyInstaller-bundled executables."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    # Go up one level from utils/ to the project root
    base = os.path.dirname(base)
    return os.path.join(base, relative_path)

def load_spritesheet(path: str, frame_width: int, frame_height: int, padding_x: int = 1,
                     fallback_color: tuple = (255, 0, 255)) -> list[pygame.Surface]:
    """Load an image and slice it horizontally into a list of animation frames."""
    sheet = load_image(path, fallback_size=(frame_width, frame_height), fallback_color=fallback_color)
    sheet_width, sheet_height = sheet.get_size()
    
    frames = []
    x = 0
    # Fallback case
    if sheet_width == frame_width and sheet_height == frame_height and not os.path.isfile(path):
        return [sheet]

    while x + frame_width <= sheet_width:
        rect = pygame.Rect(x, 0, frame_width, frame_height)
        frame = pygame.Surface(rect.size, pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), rect)
        frames.append(frame)
        x += frame_width + padding_x

    if not frames:
        frames.append(sheet)
        
    return frames
