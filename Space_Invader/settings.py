"""
settings.py — Central configuration for Space Invaders.
All constants, colors, paths, and tuning values live here.
"""

import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")

# Individual asset paths
PLAYER_IMG = os.path.join(IMAGES_DIR, "tinyShip1.png")
ENEMY_IMG = os.path.join(IMAGES_DIR, "tinyShip9.png")
SHOOTING_ENEMY_IMG = os.path.join(IMAGES_DIR, "tinyShip7.png")
FAST_ENEMY_IMG = os.path.join(IMAGES_DIR, "tinyShip4.png")
TANK_ENEMY_IMG = os.path.join(IMAGES_DIR, "tinyShip14.png")
ZIGZAG_ENEMY_IMG = os.path.join(IMAGES_DIR, "tinyShip12.png")
POWERUP_IMG = os.path.join(IMAGES_DIR, "tinyShip6.png")
SHIELD_IMG = os.path.join(IMAGES_DIR, "Round_Shield.png")

BULLET_IMG = os.path.join(IMAGES_DIR, "bullet.png")
ENEMY_BULLET_IMG = os.path.join(IMAGES_DIR, "bomb.png")
EXPLOSION_IMG = os.path.join(IMAGES_DIR, "explode.png")
BACKGROUND_IMG = os.path.join(IMAGES_DIR, "Background.png")
ICON_IMG = os.path.join(IMAGES_DIR, "Game_Icon.png")

# Sprite Info (width, height)
PLAYER_FRAME_SIZE = (24, 27)
ENEMY_FRAME_SIZE = (34, 31)
SHOOTING_ENEMY_FRAME_SIZE = (46, 36)
FAST_ENEMY_FRAME_SIZE = (28, 23)
TANK_ENEMY_FRAME_SIZE = (52, 32)
ZIGZAG_ENEMY_FRAME_SIZE = (26, 27)
POWERUP_FRAME_SIZE = (40, 22)

SPRITE_SCALE = 2  # Scale up the tiny pixel art

# ---------------------------------------------------------------------------
# Screen
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Space Invaders"

# ---------------------------------------------------------------------------
# Colors (R, G, B)
# ---------------------------------------------------------------------------
COLOR_BG = (0, 0, 35)
COLOR_FLASH = (161, 13, 54)
COLOR_OVERLAY = (0, 0, 0)
COLOR_OVERLAY_ALPHA = 180
COLOR_GAME_OVER = (255, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_SCORE = (255, 165, 0)
COLOR_SUBTITLE = (200, 200, 200)
COLOR_WAVE_TEXT = (0, 255, 200)
COLOR_SHIELD = (0, 150, 255, 120)

# Power-up colors
COLOR_POWERUP_DOUBLESHOT = (255, 200, 0)
COLOR_POWERUP_RAPIDFIRE = (0, 200, 255)
COLOR_POWERUP_SHIELD = (0, 150, 255)
COLOR_POWERUP_EXTRALIFE = (0, 255, 100)
COLOR_POWERUP_BOMB = (255, 50, 50)

# Enemy tint colors (applied as fallback sprite colors)
COLOR_FAST_ENEMY = (0, 220, 80)
COLOR_TANK_ENEMY = (200, 50, 50)
COLOR_SHOOTER_ENEMY = (200, 100, 255)
COLOR_ZIGZAG_ENEMY = (255, 200, 0)

# ---------------------------------------------------------------------------
# Player
# ---------------------------------------------------------------------------
PLAYER_START_X = 370
PLAYER_START_Y = 480
PLAYER_SPEED = 5
PLAYER_WIDTH = 64          # approximate sprite width

# ---------------------------------------------------------------------------
# Enemies — Base
# ---------------------------------------------------------------------------
ENEMY_SPEED = 3
ENEMY_DROP = 40            # pixels to descend when hitting a wall
ENEMY_SPAWN_Y_MIN = 50
ENEMY_SPAWN_Y_MAX = 150
ENEMY_GAME_OVER_Y = 440    # if enemy reaches this Y → lose a life
REGULAR_ENEMY_SCORE = 1
REGULAR_ENEMY_HP = 1

# ---------------------------------------------------------------------------
# Enemy Types
# ---------------------------------------------------------------------------
# FastEnemy
FAST_ENEMY_SPEED = 6
FAST_ENEMY_HP = 1
FAST_ENEMY_SCORE = 2

# TankEnemy
TANK_ENEMY_SPEED = 1.5
TANK_ENEMY_HP = 3
TANK_ENEMY_SCORE = 5

# ShooterEnemy
SHOOTER_ENEMY_SPEED = 2
SHOOTER_ENEMY_HP = 2
SHOOTER_ENEMY_SCORE = 4
SHOOTER_FIRE_INTERVAL = 2000   # ms between shots

# ZigZagEnemy
ZIGZAG_ENEMY_SPEED = 4
ZIGZAG_ENEMY_HP = 1
ZIGZAG_ENEMY_SCORE = 3
ZIGZAG_AMPLITUDE = 3          # pixels of random direction jitter
ZIGZAG_CHANGE_CHANCE = 5      # % chance per frame to change direction

# ---------------------------------------------------------------------------
# Bullets
# ---------------------------------------------------------------------------
BULLET_SPEED = 10
ENEMY_BULLET_SPEED = 5
BULLET_OFFSET_X = 16       # center bullet on sprite
BULLET_OFFSET_Y = 10
BULLET_COOLDOWN = 300       # ms between player shots
DOUBLE_SHOT_OFFSET = 20     # horizontal offset for double bullets
MAX_PLAYER_BULLETS = 5      # bullet pool size
MAX_ENEMY_BULLETS = 10      # enemy bullet pool size

# ---------------------------------------------------------------------------
# Collision
# ---------------------------------------------------------------------------
COLLISION_RADIUS = 27

# ---------------------------------------------------------------------------
# Lives / Scoring
# ---------------------------------------------------------------------------
STARTING_LIVES = 3
MAX_LIVES = 5
LIFE_LOST_FLASH_MS = 250   # red flash duration

# ---------------------------------------------------------------------------
# Explosion
# ---------------------------------------------------------------------------
EXPLOSION_DURATION_MS = 400

# ---------------------------------------------------------------------------
# HUD positions
# ---------------------------------------------------------------------------
HUD_X = 10
HUD_Y = 10

# ---------------------------------------------------------------------------
# Wave System
# ---------------------------------------------------------------------------
WAVE_TRANSITION_DELAY = 2000    # ms to show "WAVE X" text
BOSS_WAVE_INTERVAL = 4          # every Nth wave is a boss wave

# ---------------------------------------------------------------------------
# Power-Ups
# ---------------------------------------------------------------------------
POWERUP_DROP_CHANCE = 15        # % chance on enemy death
POWERUP_FALL_SPEED = 2
POWERUP_DURATION = 8000         # ms for timed power-ups (DoubleShot, RapidFire)
POWERUP_SIZE = 24               # sprite size (square)

# ---------------------------------------------------------------------------
# Dynamic Difficulty
# ---------------------------------------------------------------------------
DIFFICULTY_SPEED_SCALE = 0.15   # +15% speed per wave
DIFFICULTY_FIRE_RATE_SCALE = 0.10  # +10% fire rate per wave

# ---------------------------------------------------------------------------
# Sprite boundary (screen_width - sprite_width)
# ---------------------------------------------------------------------------
SPRITE_MAX_X = SCREEN_WIDTH - PLAYER_WIDTH  # 736
