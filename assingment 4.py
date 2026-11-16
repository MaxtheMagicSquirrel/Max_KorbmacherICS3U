
import pygame
#Start Pygame#

pygame.init()
#Set up the game window#

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dungeon Escape")
COLOURS

BLACK = (15, 15, 20)
DARK_GREY = (40, 40, 50)
GREY = (100, 100, 110)
BLUE = (0, 100, 255)
RED = (220, 40, 40)
GREEN = (0, 220, 80)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
#PLAYER SETTINGS#

player_size = 28
player_speed = 3
player_health = 10
player_rect = pygame.Rect(40, 40, player_size, player_size)
#SHOOTING SETTINGS#

bullet_speed = 8
shoot_delay = 250
bullets = []
#ENEMY SETTINGS#

enemy_size = 28
enemy_speed = 1
enemies = []
#POWER-UP SETTINGS#

powerup_rect = None
speed_boost_end = 0
#GAME SETTINGS#

level = 1
game_state = "menu"
#Create a clock to control the game speed#

clock = pygame.time.Clock()
#Create fonts#

title_font = pygame.font.SysFont(None, 64)
game_font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)
#Remember the direction the player is facing#

facing_x = 1
facing_y = 0
#Keep track of shooting and damage#

last_shot_time = 0
last_damage_time = 0
#Keep the game running#

running = True

#FUNCTIONS#

def create_level(level_number):
#Creates the walls, enemies, exit and power-up for each level.#
# Create the walls list
walls = []
# LEVEL 1 - THE FORGOTTEN DUNGEON
if level_number == 1:
# Create the maze walls
walls = [
pygame.Rect(150, 0, 20, 350),
pygame.Rect(300, 200, 20, 400),
pygame.Rect(450, 0, 20, 350),
pygame.Rect(600, 0, 20, 400)
]
# Create the enemies
enemies = [
pygame.Rect(230, 100, enemy_size, enemy_size),
pygame.Rect(520, 470, enemy_size, enemy_size)
]
# Create the exit
exit_rect = pygame.Rect(735, 520, 40, 40)
# Create the speed power-up
powerup = pygame.Rect(350, 80, 24, 24)
# LEVEL 2 - THE DEEP CATACOMBS
    else:
# Create the maze walls
walls = [
pygame.Rect(130, 0, 20, 320),
pygame.Rect(260, 220, 20, 380),
pygame.Rect(390, 0, 20, 320),
pygame.Rect(520, 220, 20, 380),
pygame.Rect(650, 0, 20, 420)
]
# Create more enemies
enemies = [
pygame.Rect(220, 100, enemy_size, enemy_size),
pygame.Rect(340, 460, enemy_size, enemy_size),
pygame.Rect(470, 100, enemy_size, enemy_size),
pygame.Rect(600, 480, enemy_size, enemy_size)
]
# Create the exit
exit_rect = pygame.Rect(735, 520, 40, 40)
# Create the speed power-up
powerup = pygame.Rect(430, 470, 24, 24)
return walls, enemies, exit_rect, powerup

def draw_text(message, font, colour, x, y):
#Displays text on the game screen#
text_image = font.render(message, True, colour)
screen.blit(text_image, (x, y))

def draw_walls(walls):
#Draws all the walls stored in the walls list.#
    for wall in walls:
pygame.draw.rect(screen, GREY, wall)

def draw_player(player_rect):
#Draws the blue player character on the screen.#
pygame.draw.rect(screen, BLUE, player_rect)

def draw_enemies(enemies):
#Draws all the red enemies on the screen.#
for enemy in enemies:
pygame.draw.rect(screen, RED, enemy)

def draw_game(walls, enemies, exit_rect, powerup, player_rect,
bullets, player_health, level_number, speed_boost_active):
#Draws the game, including the maze, player and enemies.#
# Draw the dungeon background
screen.fill(DARK_GREY)
# Draw the maze walls
draw_walls(walls)
# Draw the exit
pygame.draw.rect(screen, GREEN, exit_rect)
# Draw the power-up if it still exists
if powerup is not None:
pygame.draw.circle(screen, YELLOW, powerup.center, 12)
# Draw the enemies
draw_enemies(enemies)
# Draw the bullets
for bullet in bullets:
pygame.draw.rect(screen, YELLOW, bullet[0])
# Draw the player
draw_player(player_rect)
# Display the player's health and current level
draw_text("Health: " + str(player_health), game_font, WHITE, 10, 10)
draw_text("Level: " + str(level_number), game_font, WHITE, 10, 45)
# Display the speed boost message
if speed_boost_active:
draw_text("SPEED BOOST!", small_font, YELLOW, 650, 15)
# Display the controls
draw_text("Move: WASD / Arrows", small_font, WHITE, 10, 565)
draw_text("Shoot: SPACE", small_font, WHITE, 620, 565)

def move_player(player_rect, keys, walls, speed, facing_x, facing_y):
#Moves the player while preventing movement through walls.#
# Remember the original horizontal position
old_x = player_rect.x
# Move horizontally
if keys[pygame.K_LEFT] or keys[pygame.K_a]:
player_rect.x -= speed
facing_x = -1
facing_y = 0
if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
player_rect.x += speed
facing_x = 1
facing_y = 0
# Check for horizontal wall collisions
for wall in walls:
if player_rect.colliderect(wall):
player_rect.x = old_x
# Remember the original vertical position
old_y = player_rect.y
# Move vertically
if keys[pygame.K_UP] or keys[pygame.K_w]:
player_rect.y -= speed
facing_x = 0
facing_y = -1
if keys[pygame.K_DOWN] or keys[pygame.K_s]:
player_rect.y += speed
facing_x = 0
facing_y = 1
# Check for vertical wall collisions
for wall in walls:
if player_rect.colliderect(wall):
player_rect.y = old_y
# Keep the player inside the game window
if player_rect.left < 0:
player_rect.left = 0
if player_rect.right > SCREEN_WIDTH:
player_rect.right = SCREEN_WIDTH
if player_rect.top < 0:
player_rect.top = 0
if player_rect.bottom > SCREEN_HEIGHT:
player_rect.bottom = SCREEN_HEIGHT
return player_rect, facing_x, facing_y

def move_enemies(enemies, player_rect, walls, speed):
#Moves enemies toward the player while checking wall collisions.#
for enemy in enemies:
# Move toward the player horizontally
old_x = enemy.x
if enemy.centerx < player_rect.centerx:
enemy.x += speed
elif enemy.centerx > player_rect.centerx:
enemy.x -= speed
# Stop the enemy if it hits a wall
for wall in walls:
if enemy.colliderect(wall):
enemy.x = old_x
# Move toward the player vertically
old_y = enemy.y
if enemy.centery < player_rect.centery:
enemy.y += speed
elif enemy.centery > player_rect.centery:
enemy.y -= speed
# Stop the enemy if it hits a wall
for wall in walls:
if enemy.colliderect(wall):
enemy.y = old_y
# Keep enemies inside the game window
if enemy.left < 0:
enemy.left = 0
if enemy.right > SCREEN_WIDTH:
enemy.right = SCREEN_WIDTH
if enemy.top < 0:
enemy.top = 0
if enemy.bottom > SCREEN_HEIGHT:
enemy.bottom = SCREEN_HEIGHT

def update_bullets(bullets, enemies, walls):
#Moves bullets and checks if they hit a wall or enemy.#
remaining_bullets = []
defeated_enemies = []
for bullet in bullets:
# Move the bullet in its shooting direction
bullet[0].x += bullet[1] * bullet_speed
bullet[0].y += bullet[2] * bullet_speed
bullet_active = True
# Check if the bullet leaves the screen
if (bullet[0].right < 0 or bullet[0].left > SCREEN_WIDTH
or bullet[0].bottom < 0 or bullet[0].top > SCREEN_HEIGHT):
bullet_active = False
# Check if the bullet hits a wall
for wall in walls:
if bullet[0].colliderect(wall):
bullet_active = False
# Check if the bullet hits an enemy
for enemy in enemies:
if bullet[0].colliderect(enemy):
defeated_enemies.append(enemy)
bullet_active = False
break
# Keep bullets that have not hit anything
if bullet_active:
remaining_bullets.append(bullet)
# Remove enemies after checking all bullets
for enemy in defeated_enemies:
if enemy in enemies:
enemies.remove(enemy)
return remaining_bullets, enemies

Create the first level

walls, enemies, exit_rect, powerup_rect = create_level(level)

#MAIN GAME LOOP#

while running:
# Check the current time
current_time = pygame.time.get_ticks()
# Check for events
for event in pygame.event.get():
if event.type == pygame.QUIT:
running = False
# Check for keyboard presses
if event.type == pygame.KEYDOWN:
# Start the game
if game_state == "menu" and event.key == pygame.K_RETURN:
game_state = "playing"
# Restart the game
if game_state == "game_over" and event.key == pygame.K_r:
level = 1
player_health = 10
player_rect = pygame.Rect(40, 40, player_size, player_size)
walls, enemies, exit_rect, powerup_rect = create_level(level)
enemy_speed = 1
bullets = []
speed_boost_end = 0
last_damage_time = 0
last_shot_time = 0
facing_x = 1
facing_y = 0
game_state = "playing"
# Play again after winning
if game_state == "victory" and event.key == pygame.K_r:
level = 1
player_health = 10
player_rect = pygame.Rect(40, 40, player_size, player_size)
walls, enemies, exit_rect, powerup_rect = create_level(level)
enemy_speed = 1
bullets = []
speed_boost_end = 0
last_damage_time = 0
last_shot_time = 0
facing_x = 1
facing_y = 0
game_state = "playing"
# Quit from the end screens
if event.key == pygame.K_q:
if game_state == "game_over" or game_state == "victory":
running = False
# GAMEPLAY
if game_state == "playing":
# Check which keys are being pressed
keys = pygame.key.get_pressed()
# Check if the speed boost is active
if current_time < speed_boost_end:
current_speed = 5
speed_boost_active = True
else:
current_speed = player_speed
speed_boost_active = False
# Move the player
player_rect, facing_x, facing_y = move_player(
player_rect, keys, walls, current_speed, facing_x, facing_y
)
# Move the enemies
move_enemies(enemies, player_rect, walls, enemy_speed)
# Shoot bullets while space is held
if keys[pygame.K_SPACE]:
if current_time - last_shot_time >= shoot_delay:
# Create a bullet in the direction the player is facing
bullet_rect = pygame.Rect(
player_rect.centerx - 4,
player_rect.centery - 4,
8,
8
)
bullets.append([bullet_rect, facing_x, facing_y])
last_shot_time = current_time
# Update the bullets
bullets, enemies = update_bullets(bullets, enemies, walls)
# Check if an enemy touches the player
for enemy in enemies:
if player_rect.colliderect(enemy):
# Damage the player once per second
if current_time - last_damage_time >= 1000:
player_health -= 1
last_damage_time = current_time
break
# Check if the player has run out of health
if player_health <= 0:
game_state = "game_over"
# Check if the player collects the speed power-up
if powerup_rect is not None:
if player_rect.colliderect(powerup_rect):
speed_boost_end = current_time + 5000
powerup_rect = None
# Check if the player reaches the exit
if player_rect.colliderect(exit_rect):
# Move to level 2
if level == 1:
level = 2
enemy_speed = 2
walls, enemies, exit_rect, powerup_rect = create_level(level)
player_rect = pygame.Rect(40, 40, player_size, player_size)
bullets = []
speed_boost_end = 0
last_damage_time = current_time
# Finish the game
else:
game_state = "victory"
# Draw the game
draw_game(
walls, enemies, exit_rect, powerup_rect, player_rect,
bullets, player_health, level, speed_boost_active
)
# START MENU
elif game_state == "menu":
screen.fill(BLACK)
draw_text("DUNGEON ESCAPE", title_font, BLUE, 175, 170)
draw_text("Explore the dungeon and find the exit!", game_font, WHITE, 150, 260)
draw_text("Avoid monsters and use SPACE to shoot.", game_font, WHITE, 150, 310)
draw_text("Press ENTER to start", game_font, GREEN, 260, 400)
# GAME OVER SCREEN
elif game_state == "game_over":
screen.fill(BLACK)
draw_text("GAME OVER", title_font, RED, 275, 200)
draw_text("You ran out of health!", game_font, WHITE, 270, 280)
draw_text("Press R to restart", game_font, GREEN, 290, 370)
draw_text("Press Q to quit", game_font, WHITE, 310, 420)
# VICTORY SCREEN
elif game_state == "victory":
screen.fill(BLACK)
draw_text("YOU ESCAPED!", title_font, GREEN, 235, 200)
draw_text("You conquered both dungeons!", game_font, WHITE, 220, 280)
draw_text("Press R to play again", game_font, GREEN, 260, 370)
draw_text("Press Q to quit", game_font, WHITE, 310, 420)
# Update the display
pygame.display.flip()
# Limit the game to 60 FPS
clock.tick(60)

#Close Pygame#

pygame.quit()