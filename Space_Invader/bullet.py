"""
bullet.py — Bullet pool systems for player and enemies.

Uses object pools to efficiently manage multiple simultaneous bullets
for DoubleShot power-up and multiple ShooterEnemies.
"""

import pygame
from settings import (
    BULLET_IMG, ENEMY_BULLET_IMG,
    BULLET_SPEED, ENEMY_BULLET_SPEED,
    BULLET_OFFSET_X, BULLET_OFFSET_Y,
    PLAYER_START_Y, SCREEN_HEIGHT,
    BULLET_COOLDOWN, DOUBLE_SHOT_OFFSET,
    MAX_PLAYER_BULLETS, MAX_ENEMY_BULLETS,
)
from utils.helpers import load_image


# ======================================================================
# Single bullet entity (internal)
# ======================================================================

class _BulletEntity:
    """A single bullet instance used internally by pools."""
    __slots__ = ("x", "y", "speed", "active", "going_up")

    def __init__(self, speed: float, going_up: bool = True):
        self.x: float = 0
        self.y: float = 0
        self.speed: float = speed
        self.active: bool = False
        self.going_up: bool = going_up

    def activate(self, x: float, y: float):
        self.x = x
        self.y = y
        self.active = True

    def update(self):
        if not self.active:
            return
        if self.going_up:
            self.y -= self.speed
            if self.y <= 0:
                self.active = False
        else:
            self.y += self.speed
            if self.y > SCREEN_HEIGHT:
                self.active = False

    def reset(self):
        self.active = False


# ======================================================================
# Player Bullet Pool
# ======================================================================

class BulletPool:
    """Pool of player bullets. Supports single and double shot."""

    def __init__(self):
        self.image = load_image(BULLET_IMG, fallback_size=(8, 16))
        self._pool = [_BulletEntity(BULLET_SPEED, going_up=True)
                      for _ in range(MAX_PLAYER_BULLETS)]
        self._last_fire_time: int = 0
        self._cooldown: int = BULLET_COOLDOWN
        self.base_cooldown: int = BULLET_COOLDOWN

    @property
    def active_bullets(self) -> list[_BulletEntity]:
        return [b for b in self._pool if b.active]

    def set_rapid_fire(self, enabled: bool):
        """Halve cooldown when rapid fire is active."""
        self._cooldown = self.base_cooldown // 2 if enabled else self.base_cooldown

    def fire(self, player_x: float, player_y: float, double_shot: bool = False) -> bool:
        """Fire one or two bullets from the player's position."""
        now = pygame.time.get_ticks()
        if now - self._last_fire_time < self._cooldown:
            return False  # cooldown not elapsed

        # Find free bullets
        free = [b for b in self._pool if not b.active]
        if not free:
            return False  # pool exhausted

        self._last_fire_time = now

        if double_shot and len(free) >= 2:
            free[0].activate(player_x - DOUBLE_SHOT_OFFSET // 2, player_y)
            free[1].activate(player_x + DOUBLE_SHOT_OFFSET // 2, player_y)
        else:
            free[0].activate(player_x, player_y)
            
        return True

    def update(self):
        for b in self._pool:
            b.update()

    def draw(self, surface: pygame.Surface):
        for b in self._pool:
            if b.active:
                surface.blit(self.image, (b.x + BULLET_OFFSET_X,
                                          b.y + BULLET_OFFSET_Y))

    def reset(self):
        for b in self._pool:
            b.reset()
        self._last_fire_time = 0
        self._cooldown = self.base_cooldown


# ======================================================================
# Enemy Bullet Pool
# ======================================================================

class EnemyBulletPool:
    """Pool of enemy bombs. Multiple shooters can fire simultaneously."""

    def __init__(self):
        self.image = load_image(ENEMY_BULLET_IMG, fallback_size=(16, 16))
        self._pool = [_BulletEntity(ENEMY_BULLET_SPEED, going_up=False)
                      for _ in range(MAX_ENEMY_BULLETS)]

    @property
    def active_bullets(self) -> list[_BulletEntity]:
        return [b for b in self._pool if b.active]

    def fire(self, enemy_x: float, enemy_y: float):
        """Launch a bomb from an enemy position."""
        for b in self._pool:
            if not b.active:
                b.activate(enemy_x, enemy_y)
                return
        # Pool full — silently skip

    def update(self):
        for b in self._pool:
            b.update()

    def draw(self, surface: pygame.Surface):
        for b in self._pool:
            if b.active:
                surface.blit(self.image, (b.x + BULLET_OFFSET_X,
                                          b.y + BULLET_OFFSET_Y))

    def reset(self):
        for b in self._pool:
            b.reset()
