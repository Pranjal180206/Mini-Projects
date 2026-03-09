"""
game_manager.py — Main game orchestrator.

Integrates WaveManager, BulletPools, power-ups, difficulty scaling,
and the full game loop (events → update → draw).
"""

import os
import pygame
from menu import show_menu
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
    ICON_IMG, BACKGROUND_IMG, EXPLOSION_IMG,
    COLOR_BG, COLOR_FLASH, COLOR_OVERLAY, COLOR_OVERLAY_ALPHA,
    COLOR_GAME_OVER, COLOR_WHITE, COLOR_SCORE, COLOR_SUBTITLE,
    COLOR_WAVE_TEXT,
    STARTING_LIVES,
    LIFE_LOST_FLASH_MS, EXPLOSION_DURATION_MS,
    COLLISION_RADIUS, ENEMY_GAME_OVER_Y,
    HUD_X, HUD_Y, WAVE_TRANSITION_DELAY,
    BULLET_OFFSET_X, BULLET_OFFSET_Y,
)
from utils.helpers import load_image
from utils.collision import distance_collision
from player import Player
from enemy import ShooterEnemy
from bullet import BulletPool, EnemyBulletPool
from wave_manager import WaveManager
from powerup import maybe_spawn_powerup, PowerUp


class GameManager:
    """Top-level game controller."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)

        # Window icon
        icon = load_image(ICON_IMG, fallback_size=(32, 32))
        pygame.display.set_icon(icon)

        # Background
        self.background = load_image(BACKGROUND_IMG,
                                     fallback_size=(SCREEN_WIDTH, SCREEN_HEIGHT),
                                     fallback_color=COLOR_BG)
        # Explosion sprite
        self.explosion_img = load_image(EXPLOSION_IMG, fallback_size=(64, 64))

        # Fonts
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 64)
        self.wave_font = pygame.font.Font(None, 80)

        # Clock
        self.clock = pygame.time.Clock()

        # Entities
        self.player = Player()
        self.bullet_pool = BulletPool()
        self.enemy_bullet_pool = EnemyBulletPool()
        self.wave_manager = WaveManager()

        # Power-ups
        self.powerups: list[PowerUp] = []

        # State
        self.state = "MENU"
        self.high_score: int = 0
        self._load_high_score()
        self.score: int = 0
        self.lives: int = STARTING_LIVES
        self.running: bool = True

        # Visual effects
        self.explosions: list[tuple[float, float, int]] = []
        self.life_lost: bool = False
        self.life_lost_time: int = 0

    # ------------------------------------------------------------------
    # High Score
    # ------------------------------------------------------------------

    def _load_high_score(self):
        filename = "highscore.txt"
        if not os.path.exists(filename):
            with open(filename, "w") as f:
                f.write("0")
            self.high_score = 0
        else:
            try:
                with open(filename, "r") as f:
                    content = f.read().strip()
                    self.high_score = int(content) if content else 0
            except ValueError:
                self.high_score = 0

    def _save_high_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open("highscore.txt", "w") as f:
                f.write(str(self.high_score))

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------

    def run(self):
        while self.running:
            if self.state == "MENU":
                start_game = show_menu(self.screen, self.clock, self.font, self.big_font)
                if start_game:
                    self.state = "PLAYING"
                else:
                    self.running = False
            else:
                self._handle_events()
                self._update()
                self._draw()
                pygame.display.update()
                self.clock.tick(FPS)
        pygame.quit()

    # ------------------------------------------------------------------
    # Events
    # ------------------------------------------------------------------

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                self._on_key_down(event.key)
            if event.type == pygame.KEYUP:
                self._on_key_up(event.key)

    def _on_key_down(self, key):
        if self.state == "GAME_OVER":
            if key == pygame.K_r:
                self._reset()
            elif key == pygame.K_ESCAPE:
                self.state = "MENU"
                self._reset()
            return

        if key == pygame.K_p:
            if self.state == "PLAYING":
                self.state = "PAUSED"
            elif self.state == "PAUSED":
                self.state = "PLAYING"
            return
            
        if key == pygame.K_ESCAPE:
            self.state = "MENU"
            self._reset()
            return

        if self.state == "PAUSED":
            return

        if key == pygame.K_LEFT:
            self.player.move_left()
        elif key == pygame.K_RIGHT:
            self.player.move_right()
        elif key == pygame.K_SPACE:
            if self.bullet_pool.fire(self.player.x, self.player.y,
                                  double_shot=self.player.double_shot):
                self.player.play_attack_anim()

    def _on_key_up(self, key):
        if key in (pygame.K_LEFT, pygame.K_RIGHT):
            self.player.stop()

    # ------------------------------------------------------------------
    # Update
    # ------------------------------------------------------------------

    def _update(self):
        if self.state == "PAUSED" or self.state == "GAME_OVER":
            return

        # Player
        self.player.update()

        # Sync rapid-fire state to bullet pool
        self.bullet_pool.set_rapid_fire(self.player.rapid_fire)

        # Player bullets
        self.bullet_pool.update()

        # Wave manager (enemies)
        self.wave_manager.update()

        # Enemy bullets
        self.enemy_bullet_pool.update()

        # ShooterEnemies fire
        for enemy in self.wave_manager.enemies:
            if isinstance(enemy, ShooterEnemy) and enemy.should_shoot():
                self.enemy_bullet_pool.fire(enemy.x, enemy.y)

        # Power-ups fall
        for pu in self.powerups:
            pu.update()

        # --- Collisions ---
        self._check_bullet_vs_enemies()
        self._check_enemy_bullets_vs_player()
        self._check_enemies_reached_bottom()
        self._check_powerup_pickups()

        # Expire old explosions
        now = pygame.time.get_ticks()
        self.explosions = [(x, y, t) for x, y, t in self.explosions
                           if now - t < EXPLOSION_DURATION_MS]

        # Clean up inactive power-ups
        self.powerups = [pu for pu in self.powerups if pu.active]

    # -- Collision helpers --

    def _check_bullet_vs_enemies(self):
        """Player bullets vs all enemies."""
        for bullet in self.bullet_pool.active_bullets:
            bullet_rect = pygame.Rect(bullet.x + BULLET_OFFSET_X, bullet.y + BULLET_OFFSET_Y, 8, 16)
            for enemy in self.wave_manager.enemies:
                if not enemy.alive:
                    continue
                enemy_rect = pygame.Rect(enemy.x, enemy.y, enemy.image.get_width(), enemy.image.get_height())
                if bullet_rect.colliderect(enemy_rect):
                    bullet.reset()
                    killed = enemy.hit()
                    if killed:
                        self.explosions.append(
                            (enemy.x, enemy.y, pygame.time.get_ticks()))
                        self.score += enemy.score_value
                        # Chance to drop power-up
                        pu = maybe_spawn_powerup(enemy.x, enemy.y)
                        if pu:
                            self.powerups.append(pu)
                    break  # this bullet is consumed

    def _check_enemy_bullets_vs_player(self):
        """Enemy bombs vs player."""
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.image.get_width(), self.player.image.get_height())
        # Shrink player hitbox slightly for fairer gameplay
        player_rect.inflate_ip(-12, -12)
        
        for bullet in self.enemy_bullet_pool.active_bullets:
            bullet_rect = pygame.Rect(bullet.x + BULLET_OFFSET_X, bullet.y + BULLET_OFFSET_Y, 16, 16)
            if bullet_rect.colliderect(player_rect):
                bullet.reset()
                if not self.player.absorb_hit():
                    self._lose_life()

    def _check_enemies_reached_bottom(self):
        """Enemies that reach the bottom → player loses a life."""
        for enemy in self.wave_manager.enemies:
            if enemy.alive and enemy.y > ENEMY_GAME_OVER_Y:
                enemy.alive = False
                self._lose_life()

    def _check_powerup_pickups(self):
        """Power-ups colliding with the player."""
        for pu in self.powerups:
            if pu.collides_with_player(self.player.x, self.player.y, self.player.image.get_width(), self.player.image.get_height()):
                pu.apply(self.player, self)
                pu.active = False

    def _lose_life(self):
        self.lives -= 1
        self.life_lost = True
        self.life_lost_time = pygame.time.get_ticks()
        if self.lives <= 0:
            self.lives = 0
            self.state = "GAME_OVER"
            self._save_high_score()

    # ------------------------------------------------------------------
    # Draw
    # ------------------------------------------------------------------

    def _draw(self):
        now = pygame.time.get_ticks()

        # Background (red flash on life lost)
        if self.life_lost and now - self.life_lost_time < LIFE_LOST_FLASH_MS:
            self.screen.fill(COLOR_FLASH)
        else:
            self.screen.fill(COLOR_BG)
            self.screen.blit(self.background, (0, 0))
            if self.life_lost:
                self.life_lost = False

        # Enemies
        for enemy in self.wave_manager.enemies:
            enemy.draw(self.screen)

        # Explosions
        for ex, ey, _ in self.explosions:
            self.screen.blit(self.explosion_img, (ex, ey))

        # Bullets
        self.bullet_pool.draw(self.screen)
        self.enemy_bullet_pool.draw(self.screen)

        # Power-ups
        for pu in self.powerups:
            pu.draw(self.screen)

        # Player
        self.player.draw(self.screen)

        # HUD
        self._draw_hud()

        # Wave transition overlay
        if self.wave_manager.in_transition and self.state != "GAME_OVER":
            self._draw_wave_announcement()

        # Overlays
        if self.state == "PAUSED":
            self._draw_pause_overlay()
        elif self.state == "GAME_OVER":
            self._draw_game_over_overlay()

    def _draw_hud(self):
        # Score
        score_surf = self.font.render(f"Score : {self.score}", True, COLOR_SCORE)
        self.screen.blit(score_surf, (HUD_X, HUD_Y))
        
        # High Score
        high_score_surf = self.font.render(f"High Score : {max(self.score, self.high_score)}", True, COLOR_SCORE)
        self.screen.blit(high_score_surf, (HUD_X, HUD_Y + 30))

        # Lives
        lives_surf = self.font.render(f"Lives : {self.lives}", True, COLOR_WHITE)
        self.screen.blit(lives_surf, (HUD_X, HUD_Y + 60))

        # Wave number (top-right)
        wave_surf = self.font.render(f"Wave {self.wave_manager.wave_number}",
                                     True, COLOR_WAVE_TEXT)
        self.screen.blit(wave_surf, (SCREEN_WIDTH - wave_surf.get_width() - 10,
                                     HUD_Y))

        # Active power-ups (top-right, below wave)
        active = self.player.get_active_powerups()
        if active:
            pu_text = " | ".join(p.replace("_", " ").title() for p in active)
            pu_surf = self.font.render(pu_text, True, COLOR_SUBTITLE)
            self.screen.blit(pu_surf, (SCREEN_WIDTH - pu_surf.get_width() - 10,
                                       HUD_Y + 30))

    def _draw_wave_announcement(self):
        label = "BOSS WAVE" if self.wave_manager.is_boss_wave else "WAVE"
        color = COLOR_GAME_OVER if self.wave_manager.is_boss_wave else COLOR_WAVE_TEXT
        text = f"— {label} {self.wave_manager.wave_number} —"
        surf = self.wave_font.render(text, True, color)
        x = (SCREEN_WIDTH - surf.get_width()) // 2
        self.screen.blit(surf, (x, 260))

    def _draw_pause_overlay(self):
        pause_surf = self.big_font.render("PAUSED", True, COLOR_WHITE)
        resume_surf = self.font.render("Press 'P' to Resume", True, COLOR_SUBTITLE)
        self.screen.blit(pause_surf, (300, 250))
        self.screen.blit(resume_surf, (280, 320))

    def _draw_game_over_overlay(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(COLOR_OVERLAY_ALPHA)
        overlay.fill(COLOR_OVERLAY)
        self.screen.blit(overlay, (0, 0))

        died_surf = self.big_font.render("GAME OVER", True, COLOR_GAME_OVER)
        died_rect = died_surf.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(died_surf, died_rect)

        score_surf = self.font.render(f"Score: {self.score}", True, COLOR_SCORE)
        score_rect = score_surf.get_rect(center=(SCREEN_WIDTH // 2, 260))
        self.screen.blit(score_surf, score_rect)
        
        high_score_surf = self.font.render(f"High Score: {max(self.score, self.high_score)}", True, COLOR_SCORE)
        hs_rect = high_score_surf.get_rect(center=(SCREEN_WIDTH // 2, 300))
        self.screen.blit(high_score_surf, hs_rect)

        wave_surf = self.font.render(f"Reached Wave {self.wave_manager.wave_number}", True, COLOR_WAVE_TEXT)
        w_rect = wave_surf.get_rect(center=(SCREEN_WIDTH // 2, 340))
        self.screen.blit(wave_surf, w_rect)

        retry_surf = self.font.render("Press 'R' to Restart", True, COLOR_WHITE)
        r_rect = retry_surf.get_rect(center=(SCREEN_WIDTH // 2, 390))
        self.screen.blit(retry_surf, r_rect)
        
        esc_surf = self.font.render("Press ESC to Exit", True, COLOR_SUBTITLE)
        e_rect = esc_surf.get_rect(center=(SCREEN_WIDTH // 2, 430))
        self.screen.blit(esc_surf, e_rect)

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def _reset(self):
        self.player.reset()
        self.bullet_pool.reset()
        self.enemy_bullet_pool.reset()
        self.wave_manager.reset()
        self.powerups.clear()
        self.score = 0
        self.lives = STARTING_LIVES
        self.state = "PLAYING"
        self.life_lost = False
        self.explosions.clear()
