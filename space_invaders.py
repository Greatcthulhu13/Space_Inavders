import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame mixer
pygame.mixer.init()

# Load background music for the main menu
menu_music = pygame.mixer.Sound("invaders_from_space.ogg")
menu_music.set_volume(0.5)  # Adjust volume as needed

# Load background music for the game
game_music = pygame.mixer.Sound("fighting_aliens.ogg")
game_music.set_volume(1)  # Adjust volume as needed

# Load audio files
explosion_sound = pygame.mixer.Sound("explosion.ogg")
laser_sound = pygame.mixer.Sound("laser.ogg")

# Constants
WIDTH, HEIGHT = 1000, 800
PLAYER_SIZE = 100
ENEMY_SIZE = 65
PLAYER_SPEED = 2
ENEMY_SPEED = 1
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

# Initialize leaderboard as a global variable
leaderboard = []

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

def load_leaderboard():
    try:
        with open("leaderboard.txt", "r") as file:
            leaderboard = [line.strip() for line in file if line.strip()]
            leaderboard = [int(score) for score in leaderboard]
            leaderboard.sort(reverse=True)
            return leaderboard
    except FileNotFoundError:
        return []

def save_leaderboard(leaderboard):
    with open("leaderboard.txt", "w") as file:
        for score in leaderboard:
            file.write(str(score) + "\n")

def update_leaderboard(score, leaderboard):
    leaderboard.append(score)
    leaderboard.sort(reverse=True)
    leaderboard = leaderboard[:5]  # Keep only the top 5 scores
    save_leaderboard(leaderboard)
    return leaderboard

def draw_leaderboard(leaderboard):
    font = pygame.font.Font(None, 36)
    leaderboard_title = font.render("Leaderboard", True, WHITE)
    screen.blit(leaderboard_title, (10, 10))
    y_offset = 50
    for i, score in enumerate(leaderboard, start=1):
        score_text = font.render(f"{i}. {score}", True, WHITE)
        screen.blit(score_text, (10, y_offset))
        y_offset += 30

def main_menu():
    menu_music.play(-1)  # Start playing menu music in a loop
    global leaderboard  # Declare leaderboard as a global variable
    leaderboard = load_leaderboard()
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        title_text = font.render("Space Invaders", True, WHITE)
        start_text = font.render("Press SPACE to Start", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(start_text, (WIDTH // 2 - 120, HEIGHT // 2))
        draw_leaderboard(leaderboard)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_music.stop()  # Stop menu music
                    return

main_menu()

game_music.play(-1)  # Start playing game music in a loop

for _ in range(ENEMY_COUNT):
    create_enemy()

# Game Loop
running = True
game_over = False  # New variable to track game over state
score = 0
font = pygame.font.Font(None, 36)

while running:
    if game_over:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over", True, WHITE)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
        screen.blit(score_text, (WIDTH // 2 - 60, HEIGHT // 2))
        pygame.display.update()

        leaderboard = update_leaderboard(score, leaderboard)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    else:
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
                game_over = True  # Set game over state

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
