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
enemies = pygame.sprite.Group()  # Use a sprite group for enemies

def create_enemy():
    enemy = pygame.image.load("enemy.png")
    enemy = pygame.transform.scale(enemy, (ENEMY_SIZE, ENEMY_SIZE))
    enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
    enemy_y = random.randint(50, 200)
    enemies.add(enemy, x=enemy_x, y=enemy_y)

for _ in range(ENEMY_COUNT):
    create_enemy()

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
        screen.blit(enemy.image, enemy.rect.topleft)
        enemy.rect.y += ENEMY_SPEED

        if enemy.rect.y > HEIGHT:
            enemy.rect.x = random.randint(0, WIDTH - ENEMY_SIZE)
            enemy.rect.y = random.randint(50, 200)

        if player.colliderect(enemy.rect):
            running = False

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
        bullet.y -= bullet_speed

        if bullet.y < 0:
            bullets.remove(bullet)

        if pygame.sprite.spritecollide(bullet, enemies, True):
            bullets.remove(bullet)
            create_enemy()  # Create a new enemy
            score += 1
            explosion_sound.play()  # Play explosion sound

    if len(enemies) == 0:
        ENEMY_COUNT += 1
        for _ in range(ENEMY_COUNT):
            create_enemy()

    if keys[pygame.K_SPACE]:
        if len(bullets) < 3:
            bullets.append(pygame.Rect(player_x + PLAYER_SIZE // 2 - 2, player_y, 4, 10))
            laser_sound.play()  # Play laser sound

    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    screen.blit(player, (player_x, player_y))

    pygame.display.update()

pygame.quit()
