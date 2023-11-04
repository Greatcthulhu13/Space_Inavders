import pygame
import random

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load audio files
explosion_sound = pygame.mixer.Sound("explosion.wav")
laser_sound = pygame.mixer.Sound("laser.wav")

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
ENEMY_SIZE = 30
PLAYER_SPEED = 5
ENEMY_SPEED = 3
BULLET_SPEED = 10
ENEMY_COUNT = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Player
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (PLAYER_SIZE, PLAYER_SIZE))
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - PLAYER_SIZE

# Bullets
bullets = []
bullet_speed = BULLET_SPEED

# Enemies
enemies = []
for _ in range(ENEMY_COUNT):
    enemy = pygame.image.load("enemy.png")
    enemy = pygame.transform.scale(enemy, (ENEMY_SIZE, ENEMY_SIZE))
    enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
    enemy_y = random.randint(50, 200)
    enemies.append([enemy, enemy_x, enemy_y])

# Game Loop
running = True
score = 0
font = pygame.font.Font(None, 36)

while running:
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT] and player_x < WIDTH - PLAYER_SIZE:
        player_x += PLAYER_SPEED

    for enemy in enemies:
        screen.blit(enemy[0], (enemy[1], enemy[2]))
        enemy[2] += ENEMY_SPEED

        if enemy[2] > HEIGHT:
            enemy[1] = random.randint(0, WIDTH - ENEMY_SIZE)
            enemy[2] = random.randint(50, 200)

        if player_x < enemy[1] + ENEMY_SIZE and player_x + PLAYER_SIZE > enemy[1] and player_y < enemy[2] + ENEMY_SIZE and player_y + PLAYER_SIZE > enemy[2]:
            running = False

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
        bullet.y -= bullet_speed

        if bullet.y < 0:
            bullets.remove(bullet)

        for enemy in enemies:
            if bullet.colliderect(enemy[1], enemy[2], ENEMY_SIZE, ENEMY_SIZE):
                bullets.remove(bullet)
                enemy[1] = random.randint(0, WIDTH - ENEMY_SIZE)
                enemy[2] = random.randint(50, 200)
                score += 1
                explosion_sound.play()  # Play explosion sound

    if len(enemies) == 0:
        ENEMY_COUNT += 1
        for _ in range(ENEMY_COUNT):
            enemy = pygame.image.load("enemy.png")
            enemy = pygame.transform.scale(enemy, (ENEMY_SIZE, ENEMY_SIZE))
            enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
            enemy_y = random.randint(50, 200)
            enemies.append([enemy, enemy_x, enemy_y])

    if keys[pygame.K_SPACE]:
        if len(bullets) < 3:
            bullets.append(pygame.Rect(player_x + PLAYER_SIZE // 2 - 2, player_y, 4, 10))
            laser_sound.play()  # Play laser sound

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    screen.blit(player, (player_x, player_y))

    pygame.display.update()

pygame.quit()
