"""
enemy.py — Enemy entity hierarchy.

Base Enemy class with HP system, plus specialized subclasses:
  FastEnemy, TankEnemy, ShooterEnemy, ZigZagEnemy.
"""

import random
import math
import pygame
from settings import (
    ENEMY_IMG, SHOOTING_ENEMY_IMG, FAST_ENEMY_IMG, TANK_ENEMY_IMG, ZIGZAG_ENEMY_IMG,
    ENEMY_SPEED, ENEMY_DROP, SPRITE_MAX_X,
    ENEMY_SPAWN_Y_MIN, ENEMY_SPAWN_Y_MAX,
    REGULAR_ENEMY_HP, REGULAR_ENEMY_SCORE,
    FAST_ENEMY_SPEED, FAST_ENEMY_HP, FAST_ENEMY_SCORE,
    TANK_ENEMY_SPEED, TANK_ENEMY_HP, TANK_ENEMY_SCORE,
    SHOOTER_ENEMY_SPEED, SHOOTER_ENEMY_HP, SHOOTER_ENEMY_SCORE,
    SHOOTER_FIRE_INTERVAL,
    ZIGZAG_ENEMY_SPEED, ZIGZAG_ENEMY_HP, ZIGZAG_ENEMY_SCORE,
    ZIGZAG_AMPLITUDE, ZIGZAG_CHANGE_CHANCE,
    COLOR_FAST_ENEMY, COLOR_TANK_ENEMY,
    COLOR_SHOOTER_ENEMY, COLOR_ZIGZAG_ENEMY,
    ENEMY_FRAME_SIZE, FAST_ENEMY_FRAME_SIZE, TANK_ENEMY_FRAME_SIZE,
    SHOOTING_ENEMY_FRAME_SIZE, ZIGZAG_ENEMY_FRAME_SIZE,
    SPRITE_SCALE
)
from utils.helpers import load_spritesheet


# ======================================================================
# Base Enemy
# ======================================================================

class Enemy:
    """Standard alien enemy with HP system."""

    def __init__(self, speed: float = ENEMY_SPEED, hp: int = REGULAR_ENEMY_HP,
                 score_value: int = REGULAR_ENEMY_SCORE,
                 image_path: str = ENEMY_IMG,
                 frame_size: tuple = ENEMY_FRAME_SIZE,
                 state_indices: dict = None,
                 fallback_color: tuple = (255, 0, 255)):
        
        if state_indices is None:
            state_indices = {'idle': 0}
            
        raw_frames = load_spritesheet(image_path, frame_size[0], frame_size[1], fallback_color=fallback_color)
        self.frames = []
        for frame in raw_frames:
            w, h = frame.get_size()
            scaled = pygame.transform.scale(frame, (w * SPRITE_SCALE, h * SPRITE_SCALE))
            self.frames.append(scaled)
            
        self.state_frames = {}
        for state, idx in state_indices.items():
            if idx < len(self.frames):
                self.state_frames[state] = self.frames[idx]
            else:
                self.state_frames[state] = self.frames[-1]

        self.current_state = 'idle' if 'idle' in self.state_frames else list(self.state_frames.keys())[0]
        self.image = self.state_frames[self.current_state]

        self.x: float = 0
        self.y: float = 0
        self.base_speed: float = speed
        self.speed: float = speed
        self.drop: float = ENEMY_DROP
        self.hp: int = hp
        self.max_hp: int = hp
        self.score_value: int = score_value
        self.alive: bool = True
        self.respawn()

    def respawn(self):
        """Place at a random position in the spawn zone and restore HP."""
        self.x = random.randint(0, SPRITE_MAX_X)
        self.y = random.randint(ENEMY_SPAWN_Y_MIN, ENEMY_SPAWN_Y_MAX)
        self.hp = self.max_hp
        self.alive = True

    def hit(self) -> bool:
        """Take 1 damage. Return True if this kill destroys the enemy."""
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def apply_difficulty(self, multiplier: float):
        """Scale speed by the difficulty multiplier."""
        self.speed = self.base_speed * multiplier

    def update(self):
        """Move horizontally; bounce off walls and drop down."""
        if not self.alive:
            return
        self.x += self.speed
        if self.x <= 0:
            self.speed = abs(self.speed)
            self.y += self.drop
        elif self.x >= SPRITE_MAX_X:
            self.speed = -abs(self.speed)
            self.y += self.drop

    def draw(self, surface: pygame.Surface):
        """Render the enemy sprite."""
        if self.alive:
            surface.blit(self.image, (self.x, self.y))
            # HP bar for multi-HP enemies
            if self.max_hp > 1:
                self._draw_hp_bar(surface)

    def _draw_hp_bar(self, surface: pygame.Surface):
        """Draw a small HP bar above the sprite."""
        bar_width = 40
        bar_height = 4
        bar_x = self.x + 12
        bar_y = self.y - 6
        fill = int(bar_width * (self.hp / self.max_hp))
        pygame.draw.rect(surface, (60, 60, 60), (bar_x, bar_y, bar_width, bar_height))
        color = (0, 255, 0) if self.hp > 1 else (255, 80, 0)
        pygame.draw.rect(surface, color, (bar_x, bar_y, fill, bar_height))


# ======================================================================
# FastEnemy
# ======================================================================

class FastEnemy(Enemy):
    """Moves at double speed, low health."""

    def __init__(self):
        super().__init__(
            speed=FAST_ENEMY_SPEED,
            hp=FAST_ENEMY_HP,
            score_value=FAST_ENEMY_SCORE,
            image_path=FAST_ENEMY_IMG,
            frame_size=FAST_ENEMY_FRAME_SIZE,
            state_indices={'idle': 0, 'attack': 1, 'move': 2},
            fallback_color=COLOR_FAST_ENEMY,
        )
        self.current_state = 'move'
        self.image = self.state_frames[self.current_state]


# ======================================================================
# TankEnemy
# ======================================================================

class TankEnemy(Enemy):
    """Slow-moving, high HP — needs multiple hits to destroy."""

    def __init__(self):
        super().__init__(
            speed=TANK_ENEMY_SPEED,
            hp=TANK_ENEMY_HP,
            score_value=TANK_ENEMY_SCORE,
            image_path=TANK_ENEMY_IMG,
            frame_size=TANK_ENEMY_FRAME_SIZE,
            state_indices={'attack': 0, 'idle': 1},
            fallback_color=COLOR_TANK_ENEMY,
        )
        # Tank enemy tint and scale
        for state, frame in self.state_frames.items():
            self.state_frames[state] = self._make_tank_sprite(frame)
        self.image = self.state_frames[self.current_state]

    @staticmethod
    def _make_tank_sprite(surface: pygame.Surface) -> pygame.Surface:
        # Scale up 1.3×
        w, h = surface.get_size()
        scaled = pygame.transform.scale(surface, (int(w * 1.3), int(h * 1.3)))
        return scaled


# ======================================================================
# ShooterEnemy
# ======================================================================

class ShooterEnemy(Enemy):
    """Fires bullets at timed intervals. Replaces the old ShootingEnemy."""

    def __init__(self):
        super().__init__(
            speed=SHOOTER_ENEMY_SPEED,
            hp=SHOOTER_ENEMY_HP,
            score_value=SHOOTER_ENEMY_SCORE,
            image_path=SHOOTING_ENEMY_IMG,
            frame_size=SHOOTING_ENEMY_FRAME_SIZE,
            state_indices={'move': 0, 'attack': 1, 'idle': 2},
            fallback_color=COLOR_SHOOTER_ENEMY,
        )
        self.current_state = 'move'
        self.image = self.state_frames[self.current_state]
        self._last_shot_time: int = 0
        self._fire_interval: int = SHOOTER_FIRE_INTERVAL
        self.base_fire_interval: int = SHOOTER_FIRE_INTERVAL

    def apply_difficulty(self, multiplier: float):
        """Scale speed and fire rate."""
        super().apply_difficulty(multiplier)
        self._fire_interval = max(400, int(self.base_fire_interval / multiplier))

    def should_shoot(self) -> bool:
        """Return True if enough time has passed since the last shot."""
        if not self.alive:
            return False
        now = pygame.time.get_ticks()
        
        # Briefly show attack frame
        if now - self._last_shot_time < 200:
            self.image = self.state_frames.get('attack', self.image)
        else:
            self.image = self.state_frames.get('move', self.image)

        if now - self._last_shot_time >= self._fire_interval:
            self._last_shot_time = now
            return True
        return False

    def respawn(self):
        super().respawn()
        self._last_shot_time = pygame.time.get_ticks()


# ======================================================================
# ZigZagEnemy
# ======================================================================

class ZigZagEnemy(Enemy):
    """Moves in unpredictable zigzag patterns."""

    def __init__(self):
        super().__init__(
            speed=ZIGZAG_ENEMY_SPEED,
            hp=ZIGZAG_ENEMY_HP,
            score_value=ZIGZAG_ENEMY_SCORE,
            image_path=ZIGZAG_ENEMY_IMG,
            frame_size=ZIGZAG_ENEMY_FRAME_SIZE,
            state_indices={'move': 0, 'attack': 1, 'idle': 2},
            fallback_color=COLOR_ZIGZAG_ENEMY,
        )
        self.current_state = 'move'
        self.image = self.state_frames[self.current_state]
        self._zigzag_dir: int = random.choice([-1, 1])

    def update(self):
        if not self.alive:
            return
        # Random direction changes
        if random.randint(0, 100) < ZIGZAG_CHANGE_CHANCE:
            self._zigzag_dir *= -1

        self.x += self.speed * self._zigzag_dir
        self.y += 0.3  # slow constant descent

        # Bounce off walls
        if self.x <= 0:
            self.x = 0
            self._zigzag_dir = 1
        elif self.x >= SPRITE_MAX_X:
            self.x = SPRITE_MAX_X
            self._zigzag_dir = -1

    def respawn(self):
        super().respawn()
        self._zigzag_dir = random.choice([-1, 1])
