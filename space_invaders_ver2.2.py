import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load audio files
explosion_sound = pygame.mixer.Sound("explosion.ogg")
laser_sound = pygame.mixer.Sound("laser.ogg")

# Constants
WIDTH, HEIGHT = 900, 700
PLAYER_SIZE = 100
ENEMY_SIZE = 30
PLAYER_SPEED = 5
ENEMY_SPEED = 3
BULLET_SPEED = 5
ENEMY_COUNT = 5
clock = pygame.time.Clock()

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

    enemy_sprite = pygame.sprite.Sprite()
    enemy_sprite.image = enemy
    enemy_sprite.rect = enemy.get_rect()
    enemy_sprite.rect.x = enemy_x
    enemy_sprite.rect.y = enemy_y
    enemies.add(enemy_sprite)

for _ in range(ENEMY_COUNT):
    create_enemy()

# Game Loop
running = True
score = 0
font = pygame.font.Font(None, 36)


while running:
    screen.fill(BLACK)
    clock.tick(300)

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

        if player.get_rect().colliderect(enemy.rect):
            running = False

    for bullet in bullets:
        pygame.draw.rect(screen, WHITE, bullet)
        bullet.y -= bullet_speed

        if bullet.y < 0:
            bullets.remove(bullet)

        # Create a sprite for the bullet
        bullet_sprite = pygame.sprite.Sprite()
        bullet_sprite.rect = bullet

        # Detect collisions without removing
        collided_enemies = pygame.sprite.spritecollide(bullet_sprite, enemies, False)
        if collided_enemies:
            for enemy in collided_enemies:
                enemies.remove(enemy)
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
