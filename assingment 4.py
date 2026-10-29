import pygame, random

pygame.init()

# Create the game window
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Very Gut Pie Gaming Project")

# Set up our colours
SKY_BLUE = (135, 206, 235)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
# Create the maze walls
walls = [
    pygame.Rect(100, 0, 20, 300),
    pygame.Rect(200, 100, 20, 300),
    pygame.Rect(300, 0, 20, 250),
    pygame.Rect(400, 100, 20, 300),
    pygame.Rect(500, 0, 20, 250)
]


# Store the player's and enemy's starting position
player_x = 375
player_y = 275
enemy_x = 100
enemy_y = 200

#Draw the bullet on top of the player
bullet_x = player_x
bullet_y = player_y
bullet_speed = 111  # Increased speed so it doesn't move at a crawl
bullet_active = False

# NEW: the bullet's own direction (locked in when fired)
bullet_dx = 0
bullet_dy = 0

# NEW: remembers which way the player last moved
facing_x = 0
facing_y = -1  # player starts facing up

# Control how many pixels the square moves each frame
speed = 7
enemy_speed = 1.5

# Keep the game running
running = True

# Add a clock to regulate frame rate (prevents the game from running too fast)
clock = pygame.time.Clock()

while running:

    # Check for events, including closing the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check which keyboard keys are being pressed
    keys = pygame.key.get_pressed()

    # NEW: update the facing direction (True counts as 1, False as 0)
    dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
    dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
    if dx != 0 or dy != 0:  # only update when the player is actually moving
        facing_x = dx
        facing_y = dy

    # Move left by decreasing the X position
    if keys[pygame.K_LEFT]:
        player_x = player_x - speed

    # Move right by increasing the X position
    if keys[pygame.K_RIGHT]:
        player_x = player_x + speed

    # Move up by decreasing the Y position
    if keys[pygame.K_UP]:
        player_y = player_y - speed

    # Move down by increasing the Y position
    if keys[pygame.K_DOWN]:
        player_y = player_y + speed

    # Move the enemy toward the player
    if enemy_x < player_x:
        enemy_x += enemy_speed
    elif enemy_x > player_x:
        enemy_x -= enemy_speed
    if enemy_y < player_y:
        enemy_y += enemy_speed
    elif enemy_y > player_y:
        enemy_y -= enemy_speed

    # 1. HANDLE INPUT (Only handles the initial trigger)
    if keys[pygame.K_SPACE]:
        if not bullet_active:
            # Reset bullet position to the player's position when fired
            bullet_x = player_x + 17  # roughly centres the bullet on the player
            bullet_y = player_y + 17
            # NEW: lock in the direction the player is facing
            bullet_dx = facing_x * bullet_speed
            bullet_dy = facing_y * bullet_speed
            bullet_active = True

    # 2. UPDATE BULLET POSITION
    if bullet_active:
        # NEW: keep moving in the direction chosen when fired
        bullet_x += bullet_dx
        bullet_y += bullet_dy

        # Check boundaries (If it goes off-screen, deactivate it)
        if bullet_x >= 800 or bullet_y >= 600 or bullet_y <= 0 or bullet_x <= 0:
            bullet_active = False


    screen.fill(SKY_BLUE)

    # Now draw the bullet if it's active
    if bullet_active:
        pygame.draw.rect(screen, BLUE, (bullet_x, bullet_y, 15, 15))  # Small 15x15 bullet

    # 1. Create rectangle objects for both the player and the enemy
    player_rect = pygame.Rect(player_x, player_y, 50, 50)
    enemy_rect = pygame.Rect(enemy_x, enemy_y, 30, 30)
    bullet_rect = pygame.Rect(bullet_x, bullet_y, 15, 15)

    # 2. Check if the rectangles overlap (collision)
    if player_rect.colliderect(enemy_rect):
        running = False  # Ends the game loop

    # NEW: only count a hit if the bullet is active, and remove it on impact
    if bullet_active and bullet_rect.colliderect(enemy_rect):
        enemy_x = random.randint(0,800)
        enemy_y = random.randint(0,600)
        bullet_active = False

    # Draw the player and enemy on top of the background
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 50))
    pygame.draw.rect(screen, RED, (enemy_x, enemy_y, 30, 30))

    # Show the updated screen
    pygame.display.flip()

    # Cap the game at 60 frames per second
    clock.tick(60)

pygame.quit()