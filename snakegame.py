import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)

# Game settings
BLOCK_SIZE = 20
SNAKE_SPACING = 2  

# Fonts
font_style = pygame.font.SysFont("acme", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

def display_score(score):
    value = score_font.render("Score: " + str(score), True, WHITE)
    screen.blit(value, [10, 10])

def draw_snake(snake_list):
    for segment in snake_list:
        pygame.draw.rect(screen, RED, [segment[0] + SNAKE_SPACING // 2, segment[1] + SNAKE_SPACING // 2,
                                       BLOCK_SIZE - SNAKE_SPACING, BLOCK_SIZE - SNAKE_SPACING])

def message(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3 + y_offset])

def game_loop(speed):
    game_over = False
    game_close = False

    x, y = WIDTH // 2, HEIGHT // 2
    x_change, y_change = 0, 0

    snake_list = []
    snake_length = 1

    food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
    food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0

    while not game_over:
        while game_close:
            screen.fill(BLACK)
            message("You lost! Press C to Play Again or Q to Quit.", RED)
            display_score(snake_length - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x_change == 0:
                    x_change = -BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_RIGHT and x_change == 0:
                    x_change = BLOCK_SIZE
                    y_change = 0
                elif event.key == pygame.K_UP and y_change == 0:
                    x_change = 0
                    y_change = -BLOCK_SIZE
                elif event.key == pygame.K_DOWN and y_change == 0:
                    x_change = 0
                    y_change = BLOCK_SIZE

        # Move the snake to the opposite side if it crosses the boundaries
        x = (x + x_change) % WIDTH
        y = (y + y_change) % HEIGHT

        screen.fill(BLACK)
        pygame.draw.rect(screen, GREEN, [food_x, food_y, BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x, y]
        snake_list.append(snake_head)
        if len(snake_list) > snake_length:
            del snake_list[0]

        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_list)
        display_score(snake_length - 1)

        pygame.display.update()

        if x == food_x and y == food_y:
            food_x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
            food_y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
            snake_length += 1

        clock.tick(speed)

    pygame.quit()
    quit()

def main_menu():
    menu = True
    while menu:
        screen.fill(BLACK)
        message("Welcome to Snake Game!", WHITE, y_offset=-50)
        message("Press 1 for Level 1 (Slow)", GREEN, y_offset=0)
        message("Press 2 for Level 2 (Medium)", GREEN, y_offset=30)
        message("Press 3 for Level 3 (Fast)", GREEN, y_offset=60)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    menu = False  # Exit the menu loop
                    game_loop(10)  # Level 1 speed
                elif event.key == pygame.K_2:
                    menu = False  # Exit the menu loop
                    game_loop(15)  # Level 2 speed
                elif event.key == pygame.K_3:
                    menu = False  # Exit the menu loop
                    game_loop(20)  # Level 3 speed

# Start the game
main_menu()
