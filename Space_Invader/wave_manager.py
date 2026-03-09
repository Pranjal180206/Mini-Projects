"""
wave_manager.py — Wave/level system with dynamic difficulty.

Controls enemy spawning, wave progression, and difficulty scaling.
"""

import pygame
from settings import (
    WAVE_TRANSITION_DELAY, BOSS_WAVE_INTERVAL,
    DIFFICULTY_SPEED_SCALE, DIFFICULTY_FIRE_RATE_SCALE,
)
from enemy import Enemy, FastEnemy, TankEnemy, ShooterEnemy, ZigZagEnemy


# ======================================================================
# Wave Definitions
# ======================================================================

# Hand-crafted waves for the first 4. After that, a formula generates them.
_WAVE_DEFS: dict[int, list[type]] = {
    1: [Enemy] * 5,
    2: [Enemy] * 5 + [FastEnemy] * 2,
    3: [Enemy] * 4 + [FastEnemy] * 2 + [ShooterEnemy] * 2,
    4: [TankEnemy] * 3 + [ShooterEnemy] * 2 + [ZigZagEnemy] * 2,  # boss wave
}


def _generate_wave(wave_number: int) -> list[type]:
    """Generate enemy composition for waves beyond the predefined ones."""
    total = 5 + wave_number
    enemies: list[type] = []

    # Distribute enemy types based on wave number
    n_tanks = min(wave_number // 2, 4)
    n_shooters = min(1 + wave_number // 3, 5)
    n_zigzag = min(wave_number // 2, 4)
    n_fast = min(2 + wave_number // 2, 6)
    n_normal = max(0, total - n_tanks - n_shooters - n_zigzag - n_fast)

    enemies += [TankEnemy] * n_tanks
    enemies += [ShooterEnemy] * n_shooters
    enemies += [ZigZagEnemy] * n_zigzag
    enemies += [FastEnemy] * n_fast
    enemies += [Enemy] * n_normal
    return enemies[:total]  # cap to total


# ======================================================================
# WaveManager
# ======================================================================

class WaveManager:
    """Manages wave progression, enemy lifecycle, and difficulty."""

    def __init__(self):
        self.wave_number: int = 0
        self.enemies: list[Enemy] = []
        self._transition: bool = False
        self._transition_start: int = 0
        self._difficulty: float = 1.0

        # Start wave 1
        self.next_wave()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def wave_cleared(self) -> bool:
        """True when every enemy in the current wave is dead."""
        return all(not e.alive for e in self.enemies)

    @property
    def in_transition(self) -> bool:
        return self._transition

    @property
    def difficulty_multiplier(self) -> float:
        return self._difficulty

    @property
    def is_boss_wave(self) -> bool:
        return self.wave_number % BOSS_WAVE_INTERVAL == 0

    def next_wave(self):
        """Advance to the next wave."""
        self.wave_number += 1
        self._difficulty = 1.0 + (self.wave_number - 1) * DIFFICULTY_SPEED_SCALE
        self._spawn_wave()
        self._transition = True
        self._transition_start = pygame.time.get_ticks()

    def update(self):
        """Update all enemies and check for wave clear."""
        # Transition timer
        if self._transition:
            if pygame.time.get_ticks() - self._transition_start >= WAVE_TRANSITION_DELAY:
                self._transition = False

        # Update enemies
        for enemy in self.enemies:
            enemy.update()

        # Auto-advance when cleared and transition is over
        if self.wave_cleared and not self._transition:
            self.next_wave()

    def reset(self):
        """Reset back to wave 1."""
        self.wave_number = 0
        self.enemies.clear()
        self._transition = False
        self._difficulty = 1.0
        self.next_wave()

    # ------------------------------------------------------------------
    # Internal
    # ------------------------------------------------------------------

    def _spawn_wave(self):
        """Instantiate enemies for the current wave with difficulty applied."""
        if self.wave_number in _WAVE_DEFS:
            types = _WAVE_DEFS[self.wave_number]
        else:
            types = _generate_wave(self.wave_number)

        self.enemies = [cls() for cls in types]

        # Apply difficulty scaling
        for enemy in self.enemies:
            enemy.apply_difficulty(self._difficulty)
