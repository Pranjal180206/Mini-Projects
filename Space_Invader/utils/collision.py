"""
utils/collision.py — Collision detection utilities.
"""

import math


def distance_collision(x1: float, y1: float,
                       x2: float, y2: float,
                       threshold: float = 27) -> bool:
    """Return True if the Euclidean distance between two points
    is less than *threshold*."""
    dx = x1 - x2
    dy = y1 - y2
    return (dx * dx + dy * dy) < (threshold * threshold)


def rect_collision(rect1: "pygame.Rect", rect2: "pygame.Rect") -> bool:
    """Return True if two pygame Rects overlap."""
    return rect1.colliderect(rect2)
