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

explosionImg = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\explode.png")

background = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\Background.png")

# Player setup
playerImg = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\Player.png")
playerX = 370
playerY = 480
playerX_changed = 0

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return distance < 27  # value for sensitivity

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
enemyImg = []
enemyX = []
enemyY = []
enemyX_changed = []
enemyY_changed = []
num_of_enemies = 7
explosions = []

shooting_enemy_visible = True
shooting_enemy_respawn_time = 0
shooting_enemy_respawn_delay = 5000  # milliseconds

shooting_enemyImg = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\space-ship.png")
shooting_enemyX = random.randint(0, 736)
shooting_enemyY = random.randint(50, 150)
shooting_enemyX_change = 2
shooting_enemyY_change = 40

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\Alien.png"))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 150))
    enemyX_changed.append(3)
    enemyY_changed.append(40)

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Enemy bullet setup
enemy_bulletImg = pygame.image.load("C:\\Users\\Pranj\\Git\\Space_Invaders\\images\\bomb.png")
enemy_bulletX = shooting_enemyX
enemy_bulletY = shooting_enemyY
enemy_bulletY_change = 5
enemy_bullet_state = "ready"

def draw_shooting_enemy(x, y):
    screen.blit(shooting_enemyImg, (x, y))

def fire_enemy_bullet(x, y):
    global enemy_bullet_state
    enemy_bullet_state = "fire"
    screen.blit(enemy_bulletImg, (x + 16, y + 20))

def fire_enemy_bullet(x, y):
    global enemy_bullet_state
    enemy_bullet_state = "fire"
    screen.blit(enemy_bulletImg, (x + 16, y + 10))

def isPlayerHit(playerX, playerY, bulletX, bulletY):
    distance = math.sqrt((playerX - bulletX) ** 2 + (playerY - bulletY) ** 2)
    return distance < 27

# Score setup
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 165, 0))
    screen.blit(score, (x, y))
    lives_text = font.render("Lives : " + str(lives), True, (255, 255, 255))
    screen.blit(lives_text, (x, y + 30))

score_value = 0

lives = 3
life_lost = False
life_lost_time = 0

# Pause setup
paused = False
pause_font = pygame.font.Font(None, 64)

font = pygame.font.Font(None, 32) 
over_font = pygame.font.Font(None, 64)
textX = 10
textY = 10

# Game Over setup
def game_over_text():
    # Semi-transparent black overlay
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(180)  # 0 is fully transparent, 255 is fully opaque
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    # Big red text
    died_text = over_font.render("YOU DIED", True, (255, 0, 0))
    screen.blit(died_text, (270, 250))  # Centered

    # Small retry text
    retry_text = font.render("Press 'R' to Restart", True, (255, 255, 255))
    screen.blit(retry_text, (280, 320))

game_over = False 

# Restart setup
def reset_game():
    global playerX, playerY, playerX_changed
    global bulletX, bulletY, bullet_state
    global enemyX, enemyY, enemyX_changed, enemyY_changed
    global score_value, game_over
    global lives 

    playerX = 370
    playerY = 480
    playerX_changed = 0

    bulletX = 0
    bulletY = playerY
    bullet_state = "ready"

    enemyX = []
    enemyY = []
    enemyX_changed = []
    enemyY_changed = []

    for i in range(num_of_enemies):
        enemyX.append(random.randint(0, 736))
        enemyY.append(random.randint(50, 150))
        enemyX_changed.append(3)
        enemyY_changed.append(40)

    score_value = 0
    lives = 3
    game_over = False

# Clock for FPS control
clock = pygame.time.Clock()

# Game loop
running = True
while running:

    # Red flash for 300ms
    if life_lost and pygame.time.get_ticks() - life_lost_time < 250:
        screen.fill((161, 13, 54))  # Red flash
    else:
        screen.fill((0, 0, 35))
        screen.blit(background, (0, 0))
        if life_lost:
            life_lost = False


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Restart after game over
        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused



        if not game_over:
            # Key press events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    playerX_changed = -5
                if event.key == pygame.K_RIGHT:
                    playerX_changed = 5
                if event.key == pygame.K_SPACE:
                    if bullet_state == "ready":
                        bulletX = playerX
                        bulletY = playerY
                        fireBullet(bulletX, bulletY)

            # Key release events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    playerX_changed = 0

    if not paused and not game_over:
    # Player movement, enemy movement, bullet updates
    # Collision checks, etc.
        # Player movement
        playerX += playerX_changed
        playerX = max(0, min(playerX, 736))

        # Bullet movement
        if bulletY <= 0:
            bulletY = 480
            bullet_state = "ready"
        if bullet_state == "fire":
            fireBullet(bulletX, bulletY)
            bulletY -= bulletY_changed

        # Collision with shooting enemy
        if shooting_enemy_visible and isCollision(shooting_enemyX, shooting_enemyY, bulletX, bulletY):
            bulletY = 480
            bullet_state = "ready"
            score_value += 5  # Reward more for shooting enemy
            shooting_enemy_visible = False
            shooting_enemy_respawn_time = pygame.time.get_ticks()

       # Show or respawn shooting enemy
        current_time = pygame.time.get_ticks()
        if not shooting_enemy_visible and current_time - shooting_enemy_respawn_time >= shooting_enemy_respawn_delay:
            shooting_enemyX = random.randint(0, 736)
            shooting_enemyY = random.randint(50, 150)
            shooting_enemy_visible = True

        if shooting_enemy_visible:
            # Movement
            shooting_enemyX += shooting_enemyX_change
            if shooting_enemyX <= 0 or shooting_enemyX >= 736:
                shooting_enemyX_change *= -1
                shooting_enemyY += shooting_enemyY_change

            # Random shoot
            if enemy_bullet_state == "ready" and random.randint(0, 100) < 2:
                enemy_bulletX = shooting_enemyX
                enemy_bulletY = shooting_enemyY
                fire_enemy_bullet(enemy_bulletX, enemy_bulletY)

            screen.blit(shooting_enemyImg, (shooting_enemyX, shooting_enemyY))

        # Enemy bullet movement
        if enemy_bullet_state == "fire":
            fire_enemy_bullet(enemy_bulletX, enemy_bulletY)
            enemy_bulletY += enemy_bulletY_change
            if enemy_bulletY > 600:
                enemy_bullet_state = "ready"
        
        # Check collision between enemy bullet and player
        if isPlayerHit(playerX, playerY, enemy_bulletX, enemy_bulletY):
            enemy_bullet_state = "ready"
            lives -= 1
            life_lost = True
            life_lost_time = pygame.time.get_ticks()
            if lives <= 0:
                game_over = True

    # Enemy movement, game over check, collision, and drawing
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_changed[i]
        if enemyX[i] <= 0:
            enemyX_changed[i] = 3
            enemyY[i] += enemyY_changed[i]
        elif enemyX[i] >= 736:
            enemyX_changed[i] = -3
            enemyY[i] += enemyY_changed[i]

        # Game Over check
        if enemyY[i] > 440:
            lives -= 1
            if lives == 0:
                game_over = True
            else:
                enemyX[i] = random.randint(0, 736)
                enemyY[i] = random.randint(50, 150)
                life_lost = True
                life_lost_time = pygame.time.get_ticks()

        # Collision check
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            explosions.append((enemyX[i], enemyY[i], pygame.time.get_ticks()))
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 150)

        # Drawing game elements
        enemy(enemyX[i], enemyY[i], i)
        draw_shooting_enemy(shooting_enemyX, shooting_enemyY)
    show_score(textX, textY)
    player(playerX, playerY)
    
    if paused and not game_over:
        pause_text = over_font.render("PAUSED", True, (255, 255, 255))
        screen.blit(pause_text, (300, 250))

        resume_text = font.render("Press 'P' to Resume", True, (200, 200, 200))
        screen.blit(resume_text, (280, 320))

    elif game_over:
        game_over_text()
        show_score(textX, textY)

    # Show or respawn shooting enemy
    current_time = pygame.time.get_ticks()
    if not shooting_enemy_visible and current_time - shooting_enemy_respawn_time >= shooting_enemy_respawn_delay:
        shooting_enemyX = random.randint(0, 736)
        shooting_enemyY = random.randint(50, 150)
        shooting_enemy_visible = True

    pygame.display.update()
    clock.tick(60)
