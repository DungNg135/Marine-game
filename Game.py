import pygame  # type: ignore
import sys
import os
import random

print(pygame.__version__)  # Print pygame version to verify installation

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Marine Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# File paths
fish_img_path = os.path.join(os.getcwd(), "fish.png")
background_image_path = os.path.join(os.getcwd(), "background.jpg")
bottle_img_path = os.path.join(os.getcwd(), "bottle.png")
plastic_bag_img_path = os.path.join(os.getcwd(), "plastic.png")

# Load assets
try:
    fish_img = pygame.image.load(fish_img_path)
    fish_img = pygame.transform.scale(fish_img, (50, 50))  # Scale fish image

    background_jpg = pygame.image.load(background_image_path)
    background_width = background_jpg.get_width()
    background_height = background_jpg.get_height()

    bottle_img = pygame.image.load(bottle_img_path)
    bottle_img = pygame.transform.scale(bottle_img, (40, 80))  # Resize bottle

    plastic_img = pygame.image.load(plastic_bag_img_path)
    plastic_img = pygame.transform.scale(plastic_img, (40, 80))  # Resize plastic bag

except FileNotFoundError as e:
    print(f"Error loading assets: {e}")
    sys.exit()

# Variables for fish and background
character_x, character_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
character_speed = 5
background_x = 0
background_y = 0
scroll_speed = 5

# Obstacles: Separate lists for bottles and plastic bags
bottle_positions = []  # Stores positions of bottles
plastic_positions = []  # Stores positions of plastic bags

bottle_spawn_time = 60  # Spawn a new bottle every 60 frames
plastic_spawn_time = 90  # Spawn a new plastic bag every 90 frames
obstacle_speed = 7
max_bottles = 4  # Maximum number of bottles on screen
max_plastics = 3  # Maximum number of plastic bags on screen

# Health system
max_hearts = 5
hearts = max_hearts

# Game loop
clock = pygame.time.Clock()
frame_count = 0
running = True

while running:
    # Clear screen
    screen.fill(WHITE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Character movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        background_x -= scroll_speed
    if keys[pygame.K_LEFT]:
        background_x += scroll_speed
    if keys[pygame.K_DOWN]:
        character_y += character_speed
    if keys[pygame.K_UP]:
        character_y -= character_speed

    # Draw background (loop for continuous scrolling)
    for x_offset in range(-1, 2):  # Draw multiple copies horizontally
        for y_offset in range(-1, 2):  # Draw multiple copies vertically
            screen.blit(
                background_jpg,
                (
                    (background_x % background_width) + x_offset * background_width,
                    (background_y % background_height) + y_offset * background_height,
                ),
            )

    # Spawn new bottles
    if frame_count % bottle_spawn_time == 0 and len(bottle_positions) < max_bottles:
        bottle_y = random.randint(0, SCREEN_HEIGHT - bottle_img.get_height())
        bottle_positions.append([0, bottle_y])  # Add bottle at x=0, random y

    # Spawn new plastic bags
    if frame_count % plastic_spawn_time == 0 and len(plastic_positions) < max_plastics:
        plastic_y = random.randint(0, SCREEN_HEIGHT - plastic_img.get_height())
        plastic_positions.append([0, plastic_y])  # Add plastic bag at x=0, random y

    # Move bottles and check for collisions
    for bottle in bottle_positions[:]:  # Use a copy of the list to iterate safely
        bottle[0] += obstacle_speed  # Move bottle to the right
        screen.blit(bottle_img, (bottle[0], bottle[1]))  # Draw bottle

        # Check for collision with the fish
        fish_rect = pygame.Rect(
            character_x - fish_img.get_width() // 2,
            character_y - fish_img.get_height() // 2,
            fish_img.get_width(),
            fish_img.get_height(),
        )
        bottle_rect = pygame.Rect(bottle[0], bottle[1], bottle_img.get_width(), bottle_img.get_height())
        if fish_rect.colliderect(bottle_rect):
            hearts -= 1  # Lose a heart
            bottle_positions.remove(bottle)  # Remove the bottle after collision

    # Move plastic bags and check for collisions
    for plastic in plastic_positions[:]:  # Use a copy of the list to iterate safely
        plastic[0] += obstacle_speed  # Move plastic bag to the right
        screen.blit(plastic_img, (plastic[0], plastic[1]))  # Draw plastic bag

        # Check for collision with the fish
        plastic_rect = pygame.Rect(plastic[0], plastic[1], plastic_img.get_width(), plastic_img.get_height())
        if fish_rect.colliderect(plastic_rect):
            hearts -= 1  # Lose a heart
            plastic_positions.remove(plastic)  # Remove the plastic bag after collision

    # Remove off-screen obstacles
    bottle_positions = [b for b in bottle_positions if b[0] < SCREEN_WIDTH]
    plastic_positions = [p for p in plastic_positions if p[0] < SCREEN_WIDTH]

    # Draw fish (main character)
    screen.blit(fish_img, (character_x - fish_img.get_width() // 2, character_y - fish_img.get_height() // 2))

    # Draw hearts (health system)
    for i in range(hearts):
        pygame.draw.circle(screen, RED, (20 + i * 30, 20), 10)

    # Check if the player has lost
    if hearts <= 0:
        print("Game Over!")
        running = False

    # Update display
    pygame.display.flip()

    # Frame rate
    clock.tick(30)
    frame_count += 1

# Quit Pygame
pygame.quit()
sys.exit()


