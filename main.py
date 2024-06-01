import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Human and Automated Squares")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

# Square properties
square_size = 50

# Movement speed
move_speed = 10
auto_speed = 20

# Font for displaying text
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

def check_collision(x1, y1, x2, y2, size):
    return x1 < x2 + size and x1 + size > x2 and y1 < y2 + size and y1 + size > y2

def reset_game():
    x_human = WIDTH // 2
    y_human = HEIGHT // 2
    speed_x_human = 0
    speed_y_human = 0

    x_auto_1 = WIDTH // 4
    y_auto_1 = HEIGHT // 2

    x_auto_2 = WIDTH // 4
    y_auto_2 = HEIGHT // 3

    speed_x_auto_1 = auto_speed
    speed_y_auto_1 = auto_speed

    speed_x_auto_2 = auto_speed
    speed_y_auto_2 = -auto_speed

    start_ticks = pygame.time.get_ticks()

    return x_human, y_human, speed_x_human, speed_y_human, x_auto_1, y_auto_1, x_auto_2, y_auto_2, speed_x_auto_1, speed_y_auto_1, speed_x_auto_2, speed_y_auto_2, start_ticks

# Initialize game state
x_human, y_human, speed_x_human, speed_y_human, x_auto_1, y_auto_1, x_auto_2, y_auto_2, speed_x_auto_1, speed_y_auto_1, speed_x_auto_2, speed_y_auto_2, start_ticks = reset_game()

# Main game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                speed_x_human = -move_speed
            elif event.key == pygame.K_RIGHT:
                speed_x_human = move_speed
            elif event.key == pygame.K_UP:
                speed_y_human = -move_speed
            elif event.key == pygame.K_DOWN:
                speed_y_human = move_speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                speed_x_human = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                speed_y_human = 0

    # Move the human-controlled square
    x_human += speed_x_human
    y_human += speed_y_human

    # Keep the human-controlled square within the screen boundaries
    if x_human < 0:
        x_human = 0
    elif x_human + square_size > WIDTH:
        x_human = WIDTH - square_size
    if y_human < 0:
        y_human = 0
    elif y_human + square_size > HEIGHT:
        y_human = HEIGHT - square_size

    # Move the automated square
    x_auto_1 += speed_x_auto_1
    y_auto_1 += speed_y_auto_1

    x_auto_2 += speed_x_auto_2
    y_auto_2 += speed_y_auto_2

    # Bounce the automated square off the edges
    if x_auto_1 < 0 or x_auto_1 + square_size > WIDTH:
        speed_x_auto_1 = -speed_x_auto_1
    if y_auto_1 < 0 or y_auto_1 + square_size > HEIGHT:
        speed_y_auto_1 = -speed_y_auto_1

    if x_auto_2 < 0 or x_auto_2 + square_size > WIDTH:
        speed_x_auto_2 = -speed_x_auto_2
    if y_auto_2 < 0 or y_auto_2 + square_size > HEIGHT:
        speed_y_auto_2 = -speed_y_auto_2

    # Check for collision
    if check_collision(x_human, y_human, x_auto_1, y_auto_1, square_size) or check_collision(x_human, y_human, x_auto_2, y_auto_2, square_size):
        # Calculate survival time
        survival_time = (pygame.time.get_ticks() - start_ticks) / 1000

        # Display "You Lose" message and survival time
        screen.fill(WHITE)
        text = font.render('You Lose', True, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
        screen.blit(text, text_rect)

        time_text = small_font.render(f'Survival Time: {survival_time:.2f} seconds', True, BLACK)
        time_rect = time_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 20))
        screen.blit(time_text, time_rect)

        pygame.display.flip()
        pygame.time.wait(3000)  # Wait for 3 seconds before restarting the game

        # Reset the game
        x_human, y_human, speed_x_human, speed_y_human, x_auto_1, y_auto_1, x_auto_2, y_auto_2, speed_x_auto_1, speed_y_auto_1, speed_x_auto_2, speed_y_auto_2, start_ticks = reset_game()
        continue

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the human-controlled square
    pygame.draw.rect(screen, RED, (x_human, y_human, square_size, square_size))

    # Draw the automated square
    pygame.draw.rect(screen, BLUE, (x_auto_1, y_auto_1, square_size, square_size))

    pygame.draw.rect(screen, GREEN, (x_auto_2, y_auto_2, square_size, square_size))

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)

pygame.quit()
sys.exit()
