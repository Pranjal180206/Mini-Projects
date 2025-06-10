import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen setup
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Game icon and background
icon = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\Game_Icon.png")
pygame.display.set_icon(icon)

background = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\Background.png")

# Player setup
playerImg = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\Player.png")
playerX = 370
playerY = 480
playerX_changed = 0

def player(x, y):
    screen.blit(playerImg, (x, y))

# Bullet setup
bulletImg = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\bullet.png")
bulletX = 0
bulletY = playerY
bulletY_changed = 10
bullet_state = "ready"

def fireBullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

# Enemy setup
enemyImg = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\Alien.png")
enemyX = random.randint(0, 736)
enemyY = random.randint(50, 150)
enemyX_changed = 3
enemyY_changed = 40

def enemy(x, y):
    screen.blit(enemyImg, (x, y))

# Clock for FPS control
clock = pygame.time.Clock()

# Game loop
running = True
while running:

    screen.fill((0, 0, 35))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Key press events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_changed = -5
            if event.key == pygame.K_RIGHT:
                playerX_changed = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    bulletY = playerY  # Reset bullet Y when firing
                    fireBullet(bulletX, bulletY)

        # Key release events
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_changed = 0

    # Player movement
    playerX += playerX_changed
    playerX = max(0, min(playerX, 736))  # Keep player within bounds

    # Enemy movement
    enemyX += enemyX_changed
    if enemyX <= 0:
        enemyX_changed = 3
        enemyY += enemyY_changed
    elif enemyX >= 736:
        enemyX_changed = -3
        enemyY += enemyY_changed

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
    if bullet_state == "fire":
        fireBullet(bulletX, bulletY)
        bulletY -= bulletY_changed

    # Drawing player and enemy
    player(playerX, playerY)
    enemy(enemyX, enemyY)

    pygame.display.update()
    clock.tick(60)  # Limit to 60 FPS
