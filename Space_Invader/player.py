"""
player.py — Player spaceship entity with power-up support.
"""

import pygame
from settings import (
    PLAYER_IMG, PLAYER_START_X, PLAYER_START_Y,
    PLAYER_SPEED, SPRITE_MAX_X, POWERUP_DURATION,
    COLOR_SHIELD, PLAYER_FRAME_SIZE, SPRITE_SCALE, SHIELD_IMG
)
from utils.helpers import load_spritesheet, load_image


class Player:
    """Represents the player's spaceship with power-up state."""

    def __init__(self):
        # Load animated frames and scale
        raw_frames = load_spritesheet(PLAYER_IMG, PLAYER_FRAME_SIZE[0], PLAYER_FRAME_SIZE[1])
        self.frames = []
        for frame in raw_frames:
            w, h = frame.get_size()
            scaled = pygame.transform.scale(frame, (w * SPRITE_SCALE, h * SPRITE_SCALE))
            self.frames.append(scaled)

        self.frame_idle = self.frames[0] if len(self.frames) > 0 else raw_frames[0]
        self.frame_attack = self.frames[1] if len(self.frames) > 1 else self.frame_idle
        self.frame_move = self.frames[2] if len(self.frames) > 2 else self.frame_idle
        
        self.image = self.frame_idle
        self._attack_expire = 0
        
        # Load shield image
        raw_shield_frames = load_spritesheet(SHIELD_IMG, 64, 64, padding_x=0)
        self.shield_frames = []
        for frame in raw_shield_frames:
            scaled_shield = pygame.transform.scale(frame, (80, 80))
            self.shield_frames.append(scaled_shield)
            
        self.x: float = PLAYER_START_X
        self.y: float = PLAYER_START_Y
        self.speed: float = PLAYER_SPEED
        self.dx: float = 0  # current horizontal velocity

        # Power-up state
        self.shielded: bool = False
        self.double_shot: bool = False
        self.rapid_fire: bool = False
        self._powerup_timers: dict[str, int] = {}  # name → expire_tick

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------

    def move_left(self):
        self.dx = -self.speed

    def move_right(self):
        self.dx = self.speed

    def stop(self):
        self.dx = 0

    def play_attack_anim(self):
        self._attack_expire = pygame.time.get_ticks() + 150

    def update(self):
        """Move the player and update power-up timers."""
        self.x += self.dx
        self.x = max(0, min(self.x, SPRITE_MAX_X))
        
        # Determine current frame
        if pygame.time.get_ticks() < self._attack_expire:
            self.image = self.frame_attack
        elif self.dx != 0:
            self.image = self.frame_move
        else:
            self.image = self.frame_idle
            
        self._update_powerups()

    # ------------------------------------------------------------------
    # Power-ups
    # ------------------------------------------------------------------

    def activate_powerup(self, name: str, duration: int = POWERUP_DURATION):
        """Activate a timed power-up."""
        expire = pygame.time.get_ticks() + duration
        self._powerup_timers[name] = expire
        if name == "double_shot":
            self.double_shot = True
        elif name == "rapid_fire":
            self.rapid_fire = True

    def activate_shield(self):
        """Shield lasts until a hit absorbs it (not time-based)."""
        self.shielded = True

    def absorb_hit(self) -> bool:
        """If shielded, absorb the hit. Return True if absorbed."""
        if self.shielded:
            self.shielded = False
            return True
        return False

    def _update_powerups(self):
        now = pygame.time.get_ticks()
        expired = [k for k, v in self._powerup_timers.items() if now >= v]
        for name in expired:
            del self._powerup_timers[name]
            if name == "double_shot":
                self.double_shot = False
            elif name == "rapid_fire":
                self.rapid_fire = False

    def get_active_powerups(self) -> list[str]:
        """Return names of currently active timed power-ups."""
        names = list(self._powerup_timers.keys())
        if self.shielded:
            names.append("shield")
        return names

    # ------------------------------------------------------------------
    # Drawing
    # ------------------------------------------------------------------

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.x, self.y))
        # Shield glow
        if self.shielded and self.shield_frames:
            # Animate the shield frames based on time (e.g., 10 frames per second)
            frame_idx = (pygame.time.get_ticks() // 100) % len(self.shield_frames)
            current_shield = self.shield_frames[frame_idx]
            
            # Center the shield (which is 80x80) over the player (which is 48x54)
            # dx = (80 - 48) / 2 = 16
            # dy = (80 - 54) / 2 = 13
            sx = self.x - 16
            sy = self.y - 13
            surface.blit(current_shield, (sx, sy))

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self):
        self.x = PLAYER_START_X
        self.y = PLAYER_START_Y
        self.dx = 0
        self.shielded = False
        self.double_shot = False
        self.rapid_fire = False
        self._powerup_timers.clear()
