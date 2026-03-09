"""
powerup.py — Power-up system.

Power-ups drop from destroyed enemies with a random chance,
fall downward, and apply effects when collected by the player.
"""

import random
import pygame
from settings import (
    POWERUP_FALL_SPEED, POWERUP_SIZE, POWERUP_DURATION,
    POWERUP_DROP_CHANCE, SCREEN_HEIGHT, MAX_LIVES,
    COLOR_POWERUP_DOUBLESHOT, COLOR_POWERUP_RAPIDFIRE,
    COLOR_POWERUP_SHIELD, COLOR_POWERUP_EXTRALIFE, COLOR_POWERUP_BOMB,
    COLLISION_RADIUS,
    POWERUP_IMG, POWERUP_FRAME_SIZE, SPRITE_SCALE
)
from utils.collision import distance_collision
from utils.helpers import load_spritesheet


# ======================================================================
# Base PowerUp
# ======================================================================

class PowerUp:
    """Base class for all power-ups."""

    label: str = "?"
    color: tuple = (255, 255, 255)

    def __init__(self, x: float, y: float):
        self.x: float = x
        self.y: float = y
        self.speed: float = POWERUP_FALL_SPEED
        self.active: bool = True
        self.size: int = POWERUP_SIZE
        # Build sprite
        self.image = self._make_sprite()
        self.size = max(self.image.get_width(), self.image.get_height())

    def _make_sprite(self) -> pygame.Surface:
        """Render a colored ship sprite with a letter label."""
        raw_frames = load_spritesheet(POWERUP_IMG, POWERUP_FRAME_SIZE[0], POWERUP_FRAME_SIZE[1])
        base_frame = raw_frames[0]
        w, h = base_frame.get_size()
        surf = pygame.transform.scale(base_frame, (w * SPRITE_SCALE, h * SPRITE_SCALE)).copy()
        
        # Apply additive tint
        tint = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        tint.fill((*self.color, 120))
        surf.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        
        # Label
        font = pygame.font.Font(None, 24)
        text = font.render(self.label, True, (255, 255, 255))
        tx = (surf.get_width() - text.get_width()) // 2
        ty = (surf.get_height() - text.get_height()) // 2
        
        # Dark outline for text
        outline = font.render(self.label, True, (0, 0, 0))
        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            surf.blit(outline, (tx + dx, ty + dy))
            
        surf.blit(text, (tx, ty))
        return surf

    def update(self):
        if self.active:
            self.y += self.speed
            if self.y > SCREEN_HEIGHT:
                self.active = False

    def draw(self, surface: pygame.Surface):
        if self.active:
            surface.blit(self.image, (self.x, self.y))

    def collides_with_player(self, player_x: float, player_y: float, player_w: float, player_h: float) -> bool:
        if not self.active:
            return False
            
        pu_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        pl_rect = pygame.Rect(player_x, player_y, player_w, player_h)
        return pu_rect.colliderect(pl_rect)

    def apply(self, player, game_manager):
        """Override in subclasses to apply the effect."""
        raise NotImplementedError


# ======================================================================
# Concrete Power-Ups
# ======================================================================

class DoubleShotPowerUp(PowerUp):
    label = "D"
    color = COLOR_POWERUP_DOUBLESHOT

    def apply(self, player, game_manager):
        player.activate_powerup("double_shot", POWERUP_DURATION)


class RapidFirePowerUp(PowerUp):
    label = "R"
    color = COLOR_POWERUP_RAPIDFIRE

    def apply(self, player, game_manager):
        player.activate_powerup("rapid_fire", POWERUP_DURATION)
        game_manager.bullet_pool.set_rapid_fire(True)


class ShieldPowerUp(PowerUp):
    label = "S"
    color = COLOR_POWERUP_SHIELD

    def apply(self, player, game_manager):
        player.activate_shield()


class ExtraLifePowerUp(PowerUp):
    label = "+"
    color = COLOR_POWERUP_EXTRALIFE

    def apply(self, player, game_manager):
        if game_manager.lives < MAX_LIVES:
            game_manager.lives += 1


class BombPowerUp(PowerUp):
    label = "B"
    color = COLOR_POWERUP_BOMB

    def apply(self, player, game_manager):
        """Destroy all alive enemies on screen."""
        for enemy in game_manager.wave_manager.enemies:
            if enemy.alive:
                game_manager.explosions.append(
                    (enemy.x, enemy.y, pygame.time.get_ticks()))
                game_manager.score += enemy.score_value
                enemy.alive = False


# ======================================================================
# Utility
# ======================================================================

_POWERUP_TYPES = [
    DoubleShotPowerUp,
    RapidFirePowerUp,
    ShieldPowerUp,
    ExtraLifePowerUp,
    BombPowerUp,
]


def maybe_spawn_powerup(x: float, y: float) -> PowerUp | None:
    """Roll a random chance; if it succeeds, return a random PowerUp."""
    if random.randint(1, 100) <= POWERUP_DROP_CHANCE:
        cls = random.choice(_POWERUP_TYPES)
        return cls(x, y)
    return None
