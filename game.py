import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
PLAYER_SPEED = 5
ENEMY_SIZE = 50
ENEMY_SPEED = 2
BULLET_SIZE = 10
BULLET_SPEED = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Load images
player_img = pygame.image.load("player.png")
enemy_img = pygame.image.load("enemy.png")

# Set up player
player_x = WIDTH // 2 - PLAYER_SIZE // 2
player_y = HEIGHT - 2 * PLAYER_SIZE
player_x_change = 0

# Set up enemy
enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
enemy_y = random.randint(50, 150)

# Set up bullet
bullet_x = 0
bullet_y = HEIGHT - PLAYER_SIZE
bullet_x_change = 0
bullet_y_change = -BULLET_SPEED
bullet_state = "ready"  # "ready" means the bullet is ready to fire

# Score
score = 0

# Font
font = pygame.font.Font(None, 36)

# Game over text
game_over_text = font.render("Game Over", True, RED)

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y):
    screen.blit(enemy_img, (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + PLAYER_SIZE // 2 - BULLET_SIZE // 2, y - BULLET_SIZE))

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = ((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2) ** 0.5
    if distance < (ENEMY_SIZE + BULLET_SIZE) / 2:
        return True
    return False

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -PLAYER_SPEED
            if event.key == pygame.K_RIGHT:
                player_x_change = PLAYER_SPEED
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = pygame.mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        # Check for key releases
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Update player's position
    player_x += player_x_change

    # Ensure player doesn't go out of bounds
    if player_x < 0:
        player_x = 0
    elif player_x > WIDTH - PLAYER_SIZE:
        player_x = WIDTH - PLAYER_SIZE

    # Update enemy's position
    enemy_x += ENEMY_SPEED

    # Enemy boundary checking
    if enemy_x < 0:
        enemy_x = 0
        ENEMY_SPEED *= -1
        enemy_y += ENEMY_SIZE
    elif enemy_x > WIDTH - ENEMY_SIZE:
        enemy_x = WIDTH - ENEMY_SIZE
        ENEMY_SPEED *= -1
        enemy_y += ENEMY_SIZE

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y += bullet_y_change

    # Bullet reset
    if bullet_y <= 0:
        bullet_y = HEIGHT - PLAYER_SIZE
        bullet_state = "ready"

    # Collision
    if is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
        explosion_sound = pygame.mixer.Sound("explosion.wav")
        explosion_sound.play()
        bullet_y = HEIGHT - PLAYER_SIZE
        bullet_state = "ready"
        score += 1
        enemy_x = random.randint(0, WIDTH - ENEMY_SIZE)
        enemy_y = random.randint(50, 150)

    # Game Over
    if enemy_y >= HEIGHT - PLAYER_SIZE:
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw player and enemy
    player(player_x, player_y)
    enemy(enemy_x, enemy_y)

    # Draw the score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()

# Quit the game
pygame.quit()
sys.exit()
