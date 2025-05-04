import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Player
player_size = 50
player_x = WIDTH // 2 - player_size // 2
player_y = HEIGHT - player_size - 20
player_speed = 5

# Enemy
enemy_size = 40
enemies = []
enemy_speed = 2
enemy_spawn_rate = 30

# Bullet
bullet_size = 5
bullet_speed = 7
bullets = []

# Game state
score = 0
game_active = True
font = pygame.font.SysFont('Arial', 36)
clock = pygame.time.Clock()

def draw_player(x, y):
    pygame.draw.rect(screen, GREEN, (x, y, player_size, player_size))

def draw_enemy(x, y):
    pygame.draw.rect(screen, RED, (x, y, enemy_size, enemy_size))

def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, (x, y, bullet_size, bullet_size))

def show_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def reset_game():
    global player_x, player_y, enemies, bullets, score, game_active
    player_x = WIDTH // 2 - player_size // 2
    player_y = HEIGHT - player_size - 20
    enemies.clear()
    bullets.clear()
    score = 0
    game_active = True

# Main game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_active:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append([player_x + player_size//2 - bullet_size//2, player_y])
        else:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset_game()
                if event.key == pygame.K_q:
                    running = False
    
    if game_active:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_size:
            player_x += player_speed
        
        # Enemy spawning
        if random.randint(1, enemy_spawn_rate) == 1:
            enemies.append([random.randint(0, WIDTH - enemy_size), -enemy_size])
        
        # Enemy movement
        for enemy in enemies[:]:
            enemy[1] += enemy_speed
            
            # Game over if enemy reaches bottom
            if enemy[1] > HEIGHT:
                game_active = False
            
            # Bullet-enemy collision
            for bullet in bullets[:]:
                if (enemy[0] < bullet[0] < enemy[0] + enemy_size and
                    enemy[1] < bullet[1] < enemy[1] + enemy_size):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    break
        
        # Bullet movement
        for bullet in bullets[:]:
            bullet[1] -= bullet_speed
            if bullet[1] < 0:
                bullets.remove(bullet)
        
        # Drawing
        draw_player(player_x, player_y)
        for enemy in enemies:
            draw_enemy(enemy[0], enemy[1])
        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        show_score()
    else:
        # Game over screen
        game_over_text = font.render("GAME OVER! Press R to restart", True, WHITE)
        quit_text = font.render("Press Q to quit", True, WHITE)
        screen.blit(game_over_text, (WIDTH//2 - 180, HEIGHT//2 - 50))
        screen.blit(quit_text, (WIDTH//2 - 100, HEIGHT//2 + 10))
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - 100, HEIGHT//2 + 50))
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()