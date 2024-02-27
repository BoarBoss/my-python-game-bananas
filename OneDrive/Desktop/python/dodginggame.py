import pygame
import cv2
import random
import math
import time

# Initialize Pygame
pygame.init()

# Constants
PLAYER_SIZE = 70
ENEMY_SIZE = 40
BULLET_SIZE = 10
PLAYER_BULLET_SIZE = 30
FPS = 60
BACKGROUND_SPEED = 0  # Adjust the background scroll speed
FIRING_RATE = 0.5  # Adjust the firing rate in seconds

# Colors
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)  # New color for enemies
BLUE = (0, 0, 255)  # Color for the health bar
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
ORINGE = (255, 165, 0)
BROWN = (139, 69, 19)

# Create the game window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Shooting Game")

# Load Player image
image_path = "C:/Users/judew/Downloads/player.png"
Player_image = pygame.image.load(image_path)
Player_image = pygame.transform.scale(Player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Load enemy image
enemy_image_path = "C:/Users/judew/Downloads/enemies.png"
enemy_image = pygame.image.load(enemy_image_path)
enemy_image = pygame.transform.scale(enemy_image, (ENEMY_SIZE, ENEMY_SIZE))

# Load tree image
tree_image_path = "C:/Users/judew/Downloads/tree.png"
tree_image = pygame.image.load(tree_image_path)
tree_image = pygame.transform.scale(tree_image, (100, 120))  # Adjust size as needed

# Load enemy bullet image
enemy_bullet_image_path = "C:/Users/judew/Downloads/enemy_bullet.png"
enemy_bullet_image = pygame.image.load(enemy_bullet_image_path)
enemy_bullet_image = pygame.transform.scale(enemy_bullet_image, (BULLET_SIZE, BULLET_SIZE))

# Load grass image
grass_image_path = "C:/Users/judew/Downloads/grass.jpg"
grass_image = pygame.image.load(grass_image_path)
grass_image = pygame.transform.scale(grass_image, (WIDTH, HEIGHT))

# Load bullet image
bullet_image_path = "C:/Users/judew/Downloads/bullets.png"
bullet_image = pygame.image.load(bullet_image_path)
bullet_image = pygame.transform.scale(bullet_image, (PLAYER_BULLET_SIZE, PLAYER_BULLET_SIZE))

# Load background music
pygame.mixer.music.load("C:/Users/judew/Downloads/y2mate.com_-_Ghost_Fight.mp3")
pygame.mixer.music.set_volume(0.5)  # Adjust the volume as needed
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Clock to control the frame rate
clock = pygame.time.Clock()

# Map definition ('x' for trees, ' ' for empty space, and 'p' for player spawn)
game_map = [
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "x    x                                                                                                              x",
    "x    x      x                                                                                                       x",
    "x       x       x              x                                                                                    x",
    "x                 x                                                                                                 x",
    "x      x                  x                                                                                         x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                    x              x",
    "x                                                                             x                                     x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                        x                          x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                        x                                                                          x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                x              xp                                                                  x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "x                                                                                                                   x",
    "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
]

# Second Map definition ('y' for additional obstacles)
second_map = [
    "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
    "y    y                                                                                                              y",
    "y    y      y                                                                                                       y",
    "y       y       y              y                                                                                    y",
    "y                 y                                                                                                 y",
    "y      y                  y                                                                                         y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                    y              y",
    "y                                                                             y                                     y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                        y                          y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y      y         y         y         y         y        y        y                                                  y",
    "y                                                                                                                    y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "y                                                                                                                   y",
    "yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy",
]

# Calculate the width and height for the inventory grid
inventory_width = 5  # Adjust the width of the inventory grid
inventory_height = 3  # Adjust the height of the inventory grid
inventory_cell_size = 50  # Adjust the size of each cell as needed
inventory_margin = 10  # Adjust the margin between cells as needed

# Initialize player health
player_health = 100

# Background position
bg_x = 1
bg_y = 1

# Bullets
bullets = []

# Grass pattern
grass_pattern = ['gggg']

# Orange Dots
orange_dots = []

# Enemies
enemies = []

trees = []

# Enemy Bullets
enemy_bullets = []

# Black Enemies
black_enemies = []

# Background position for grass
grass_bg_x = 0

# Function to move grass based on scrolling background
def move_grass(scroll_speed):
    global grass_bg_x
    grass_bg_x -= scroll_speed
    if grass_bg_x <= -WIDTH:
        grass_bg_x = 0

# Function to move the background based on player movement
def move_background(scroll_speed):
    global bg_x, bg_y
    bg_x -= scroll_speed
    if bg_x <= -WIDTH:
        bg_x = 0

# Function to move trees based on scrolling background
def move_trees(scroll_speed):
    for i in range(len(trees)):
        trees[i] = (trees[i][0] - scroll_speed, trees[i][1])

# Function to draw both maps
def draw_maps(map1, map2, player_x, player_y):
    global grass_bg_x
    for row_index, (row1, row2) in enumerate(zip(map1, map2)):
        for col_index, (tile1, tile2) in enumerate(zip(row1, row2)):
            if tile1 == 'x':
                tree_x = col_index * 100 - player_x
                tree_y = row_index * 120 - player_y
                screen.blit(tree_image, (tree_x, tree_y))
            elif tile1 == 'p':
                player_x = col_index * 100
                player_y = row_index * 120
                screen.blit(Player_image, (player_x, player_y))
            elif tile2 == 'y':
                obstacle_x = col_index * 100 - player_x
                obstacle_y = row_index * 120 - player_y
                screen.blit(grass_image, (obstacle_x, obstacle_y))

# Function to find player spawn position on the map
def find_player_spawn_position(map_data):
    for row_index, row in enumerate(map_data):
        for col_index, tile in enumerate(row):
            if tile == 'p':
                return col_index * 100, row_index * 120  # Assuming each tile is 100x120
    return 0, 0  # Default position if 'p' is not found

# Player health
player_health = 100

# Initialize player image
Player_image = pygame.transform.scale(Player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Background position
bg_x = 0
bg_y = 0

# Bullets
bullets = []

# Orange Dots
orange_dots = []

# Enemies
enemies = []

trees = []

# Enemy Bullets
enemy_bullets = []

# Black Enemies
black_enemies = []

# draw map
def draw_map(map_data):
    for row_index, row in enumerate(map_data):
        for col_index, tile in enumerate(row):
            if tile == 'x':
                screen.blit(tree_image, (col_index * 100, row_index * 120))
            elif tile == 'p':
                player_x = col_index * 100
                player_y = row_index * 120
                screen.blit(Player_image, (player_x, player_y))

def check_tree_collisions_enemy_bullet(rect, trees):
    for tree_pos in trees:
        tree_rect = pygame.Rect(tree_pos[0], tree_pos[1], 100, 120)  # Adjust the rect size based on the tree image
        if rect.colliderect(tree_rect):
            return True  # Collision detected with a tree
    return False

# Function to generate random trees
def generate_random_trees(player_x, player_y):
    trees = []
    for x in range(0, WIDTH, 100):
        for y in range(0, HEIGHT, 100):
            if (x, y) != (player_x, player_y) and random.randint(1, 10) == 1:
                trees.append((x - player_x, y - player_y))
    return trees

# Function to generate random enemy positions avoiding trees
def generate_random_enemy_positions(num_enemies, trees):
    enemy_positions = []
    while len(enemy_positions) < num_enemies:
        x = random.randint(0, WIDTH - ENEMY_SIZE)
        y = random.randint(0, HEIGHT - ENEMY_SIZE)
        enemy_rect = pygame.Rect(x, y, ENEMY_SIZE, ENEMY_SIZE)
        collides_with_tree = any(enemy_rect.colliderect(pygame.Rect(tree[0], tree[1], 100, 120)) for tree in trees)
        if not collides_with_tree:
            enemy_positions.append((x, y))
    return enemy_positions

# Function to draw the map with trees and grass background
def draw_map(map_data, player_x, player_y):
    global grass_bg_x
    for row_index, row in enumerate(map_data):
        for col_index, tile in enumerate(row):
            if tile == 'x':
                tree_x = col_index * 100 - player_x
                tree_y = row_index * 120 - player_y
                screen.blit(tree_image, (tree_x, tree_y))
            elif tile == 'p':
                player_x = col_index * 100
                player_y = row_index * 120
                screen.blit(Player_image, (player_x, player_y))
    
    # Draw grass background
    for i, grass_row in enumerate(grass_pattern):
        for j, grass_tile in enumerate(grass_row):
            grass_x = j * WIDTH - player_x - grass_bg_x
            grass_y = i * HEIGHT - player_y
            screen.blit(grass_image, (grass_x, grass_y))

def check_tree_collisions_enemy_bullet(rect, trees):
    for tree_pos in trees:
        tree_rect = pygame.Rect(tree_pos[0], tree_pos[1], 100, 120)  # Adjust the rect size based on the tree image
        if rect.colliderect(tree_rect):
            return True  # Collision detected with a tree
    return False

# Function to move enemies towards the player avoiding trees
def move_enemy_towards_player(enemy, trees):

    # Check if enough time has passed since the last enemy shot
    if time.time() - enemy.get('last_shot_time', 0) > FIRING_RATE:
        # Calculate the angle between enemy and player
        dx, dy = player_x - enemy['x'] - ENEMY_SIZE // 2, player_y - enemy['y'] - ENEMY_SIZE // 2
        angle = math.atan2(dy, dx)

        # Create an enemy bullet at the enemy's position with speed based on the angle
        enemy_bullet = {'x': enemy['x'] + ENEMY_SIZE // 2 - BULLET_SIZE // 2,
                        'y': enemy['y'] + ENEMY_SIZE // 2 - BULLET_SIZE // 2,
                        'speed': 5,  # Adjust the bullet speed as needed
                        'angle': angle}
        enemy_bullets.append(enemy_bullet)

        # Update the last shot time
        enemy['last_shot_time'] = time.time()

# Function to check collisions with trees
def check_tree_collisions(rect, trees):
    for tree_pos in trees:
        tree_rect = pygame.Rect(tree_pos[0], tree_pos[1], 100, 120)
        if rect.colliderect(tree_rect):
            return True  # Collision detected with a tree
    return False

# Initialize player spawn position
player_x, player_y = find_player_spawn_position(game_map)

# Initial tree generation
trees = generate_random_trees(player_x, player_y)

# Font for rendering text
font = pygame.font.Font(None, 50)

# Initialize variables for firing rate control
shoot_timer = 0
can_shoot = True

# Create the game window
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()

pygame.display.set_caption("Shooting Game")

# Function to draw the player
def draw_player(x, y):
    screen.blit(Player_image, (x, y))

# Calculate the width of the game area (excluding the inventory)
game_area_width = WIDTH - (inventory_width * (inventory_cell_size + inventory_margin)) - inventory_margin

# Position the game area and inventory
game_area_x = WIDTH // 2 - PLAYER_SIZE // 2  # Center the player on the screen initially
inventory_x = WIDTH - (inventory_width * (inventory_cell_size + inventory_margin))

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # 1 represents the left mouse button
            # Set the can_shoot flag to True when the left mouse button is pressed
            can_shoot = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:  # 1 represents the left mouse button
            # Reset the shoot timer and set can_shoot to False when the left mouse button is released
            shoot_timer = 0
            can_shoot = False

    # Check if the left mouse button is held down and enough time has passed since the last shot
    if pygame.mouse.get_pressed()[0] and can_shoot:
        # Calculate the angle between player and cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx, dy = mouse_x - player_x - PLAYER_SIZE // 2, mouse_y - player_y - PLAYER_SIZE // 2
        angle = math.atan2(dy, dx)

        # Replace the drawing code for player bullets
        bullets.append({'image': bullet_image, 'x': player_x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                        'y': player_y + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                        'speed': 10,
                        'angle': angle})

        # Reset the shoot timer and set can_shoot to False
        shoot_timer = 0
        can_shoot = False

        # Create a bullet at the player's position with speed based on the angle
        bullet = {'x': player_x + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                  'y': player_y + PLAYER_SIZE // 2 - BULLET_SIZE // 2,
                  'speed': 10,
                  'angle': angle}
        bullets.append(bullet)

    # Move the player with w, a, s, d keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and player_x > 0:
        player_x -= 10
        move_background(-BACKGROUND_SPEED)  # Move the background left when player moves left
    if keys[pygame.K_d] and player_x < game_area_width - PLAYER_SIZE:
        player_x += 10
        move_background(BACKGROUND_SPEED)  # Move the background right when player moves right
    if keys[pygame.K_w] and player_y > 0:
        player_y -= 10
    if keys[pygame.K_s] and player_y < HEIGHT - PLAYER_SIZE:
        player_y += 10
    
    

    # Move bullets based on angle
    for bullet in bullets:
        bullet['x'] += bullet['speed'] * math.cos(bullet['angle'])
        bullet['y'] += bullet['speed'] * math.sin(bullet['angle'])

        # Check for collisions with trees
        bullet_rect = pygame.Rect(bullet['x'], bullet['y'], BULLET_SIZE, BULLET_SIZE)
        if check_tree_collisions(bullet_rect, trees):
            bullets.remove(bullet)  # Remove the bullet if it collides with a tree

    # Move enemy bullets based on angle
    for enemy_bullet in enemy_bullets:
        enemy_bullet['x'] += enemy_bullet['speed'] * math.cos(enemy_bullet['angle'])
        enemy_bullet['y'] += enemy_bullet['speed'] * math.sin(enemy_bullet['angle'])

        # Check for collisions with trees
        enemy_bullet_rect = pygame.Rect(enemy_bullet['x'], enemy_bullet['y'], BULLET_SIZE, BULLET_SIZE)
        if check_tree_collisions_enemy_bullet(enemy_bullet_rect, trees):
            enemy_bullets.remove(enemy_bullet)  # Remove the bullet if it collides with a tree

    # Move enemies towards the player
    for enemy in enemies:
        dx, dy = player_x - enemy['x'] - ENEMY_SIZE // 2, player_y - enemy['y'] - ENEMY_SIZE // 2
        angle = math.atan2(dy, dx)
        new_enemy_x = enemy['x'] + 2 * math.cos(angle)
        new_enemy_y = enemy['y'] + 2 * math.sin(angle)
        enemy_rect = pygame.Rect(new_enemy_x, new_enemy_y, ENEMY_SIZE, ENEMY_SIZE)
        if not check_tree_collisions(enemy_rect, trees):
            enemy['x'] = new_enemy_x
            enemy['y'] = new_enemy_y

    # Check for collisions with trees
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    if check_tree_collisions(player_rect, trees):
        # Move the player back to the previous position to prevent walking through trees
        if keys[pygame.K_a] and player_x > 0:
            player_x += 10
        if keys[pygame.K_d] and player_x < WIDTH - PLAYER_SIZE:
            player_x -= 10
        if keys[pygame.K_w] and player_y > 0:
            player_y += 10
        if keys[pygame.K_s] and player_y < HEIGHT - PLAYER_SIZE:
            player_y -= 10

        # Check for collisions with trees
        bullet_rect = pygame.Rect(bullet['x'], bullet['y'], BULLET_SIZE, BULLET_SIZE)
        if check_tree_collisions(bullet_rect, trees):
            bullets.remove(bullet)  # Remove the bullet if it collides with a tree
    
    # Draw the enemy bullets
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, YELLOW, (enemy_bullet['x'], enemy_bullet['y'], BULLET_SIZE, BULLET_SIZE))

    # Check for collisions between enemy bullets and player
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for enemy_bullet in enemy_bullets:
        enemy_bullet_rect = pygame.Rect(enemy_bullet['x'], enemy_bullet['y'], BULLET_SIZE, BULLET_SIZE)
        if player_rect.colliderect(enemy_bullet_rect):
            enemy_bullets.remove(enemy_bullet)
            player_health -= 10  # Adjust the damage value as needed
            if player_health <= 0:
                print("Game Over!")
                running = False

            enemy_bullet = {'x': enemy['x'] + ENEMY_SIZE // 2 - BULLET_SIZE // 2,
                            'y': enemy['y'] + ENEMY_SIZE // 2 - BULLET_SIZE // 2,
                            'speed': 5,  # Adjust the bullet speed as needed
                            'angle': angle}
            enemy_bullets.append(enemy_bullet)

    # Spawn black enemy bullets randomly
    for black_enemy in black_enemies:
        if random.randint(1, 20) < 3:  # Adjust the probability as needed
            dx, dy = player_x - black_enemy['x'] - ENEMY_SIZE // 2, player_y - black_enemy['y'] - ENEMY_SIZE // 2
            angle = math.atan2(dy, dx)

            black_enemy_bullet = {'x': black_enemy['x'] + ENEMY_SIZE // 2 - BULLET_SIZE // 2,
                                  'y': black_enemy['y'] + ENEMY_SIZE // 2 - BULLET_SIZE // 2,
                                  'speed': 50,  # Adjust the bullet speed for black enemies
                                  'angle': angle}
            enemy_bullets.append(black_enemy_bullet)
    
    # Move bullets based on angle
    for bullet in bullets:
        bullet['x'] += bullet['speed'] * math.cos(bullet['angle'])
        bullet['y'] += bullet['speed'] * math.sin(bullet['angle'])

    # Spawn enemies randomly
    if random.randint(1, 500) < 6:
        enemy_positions = generate_random_enemy_positions(1, trees)
        for position in enemy_positions:
            enemy = {'x': position[0], 'y': position[1], 'health': 100}
            enemies.append(enemy)

    # spawn black enemies randomly
    if random.randint(1, 1000) < 2:
        black_enemy = {'x': random.randint(0, WIDTH - ENEMY_SIZE), 'y': random.randint(0, HEIGHT - ENEMY_SIZE), 'health': 100}
        black_enemies.append(black_enemy)

    # enemies towards the player
    for enemy in enemies:
        # Calculate the movement direction
        dx, dy = player_x - enemy['x'] - ENEMY_SIZE // 2, player_y - enemy['y'] - ENEMY_SIZE // 2
        angle = math.atan2(dy, dx)
    
        # Check for collisions with trees
        new_enemy_x = enemy['x'] + 2 * math.cos(angle)
        new_enemy_y = enemy['y'] + 2 * math.sin(angle)
        # update enemy position only if there is no collision with trees
        enemy_rect = pygame.Rect(new_enemy_x, new_enemy_y, ENEMY_SIZE, ENEMY_SIZE)
        if not check_tree_collisions(enemy_rect, trees):
            # Update enemy position only if there is no collision with trees
            enemy['x'] = new_enemy_x
            enemy['y'] = new_enemy_y

    # Check for collisions with black enemies
    for black_enemy in black_enemies:
        black_enemy_rect = pygame.Rect(black_enemy['x'], black_enemy['y'], ENEMY_SIZE, ENEMY_SIZE)
        if player_rect.colliderect(black_enemy_rect):
            black_enemies.remove(black_enemy)

    # Check for collisions with black enemies
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet['x'], bullet['y'], BULLET_SIZE, BULLET_SIZE)
        for black_enemy in black_enemies:
            black_enemy_rect = pygame.Rect(black_enemy['x'], black_enemy['y'], ENEMY_SIZE, ENEMY_SIZE)
            if bullet_rect.colliderect(black_enemy_rect):
                # Remove the bullet and reduce black enemy health on collision
                bullets.remove(bullet)
                black_enemy['health'] -= 20
                if black_enemy['health'] <= 0:
                    black_enemies.remove(black_enemy)

    # Check for collisions with enemies
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy['x'], enemy['y'], ENEMY_SIZE, ENEMY_SIZE)
        if player_rect.colliderect(enemy_rect):
            enemies.remove(enemy)

    # Check for collisions with enemies
    player_rect = pygame.Rect(player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy['x'], enemy['y'], ENEMY_SIZE, ENEMY_SIZE)
        if player_rect.colliderect(enemy_rect):
            player_health -= 10
            if player_health <= 0:
                print("Game Over!")
                running = False

    # Check for collisions with bullets
    for bullet in bullets:
        bullet_rect = pygame.Rect(bullet['x'], bullet['y'], BULLET_SIZE, BULLET_SIZE)
        for enemy in enemies:
            enemy_rect = pygame.Rect(enemy['x'], enemy['y'], ENEMY_SIZE, ENEMY_SIZE)
            if bullet_rect.colliderect(enemy_rect):
                # Remove the bullet and reduce enemy health on collision
                bullets.remove(bullet)
                enemy['health'] -= 33.4
                if enemy['health'] <= 0:
                    # Check if a weapon should be dropped (10% chance)
                    if random.random() < 0.1:
                        # Add the position of the defeated enemy to the list
                        orange_dots.append({'x': enemy['x'], 'y': enemy['y']})
                enemies.remove(enemy)

    # Move trees based on scrolling background
    move_trees(BACKGROUND_SPEED)

    # Draw the scrolling background with grass image
    screen.blit(grass_image, (bg_x, bg_y))
    screen.blit(grass_image, (bg_x + WIDTH, bg_y))

    # Draw the maps
    draw_maps(game_map, second_map, player_x, player_y)

    # Update the background position for scrolling effect
    bg_x -= BACKGROUND_SPEED
    if bg_x <= -WIDTH:
        bg_x = 0

    # Draw the player at the updated position
    draw_player(WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2)

    # Draw the trees
    for tree_pos in trees:
        screen.blit(tree_image, (tree_pos[0], tree_pos[1]))

    # Draw the enemies
    for enemy in enemies:
        screen.blit(enemy_image, (enemy['x'] - player_x + game_area_x, enemy['y'] - player_y + HEIGHT // 2))

        # Draw the health bar above each enemy
        pygame.draw.rect(screen, BLACK, (enemy['x'] - player_x + game_area_x, enemy['y'] - player_y + HEIGHT // 2 - 10, ENEMY_SIZE, 5))
        pygame.draw.rect(screen, RED, (enemy['x'] - player_x + game_area_x, enemy['y'] - player_y + HEIGHT // 2 - 10, (enemy['health'] / 100) * ENEMY_SIZE, 5))

    # Draw the black enemies
    for black_enemy in black_enemies:
        pygame.draw.rect(screen, BLACK, (black_enemy['x'] - player_x + game_area_x, black_enemy['y'] - player_y + HEIGHT // 2, ENEMY_SIZE, ENEMY_SIZE))

        # Draw the health bar above each black enemy
        pygame.draw.rect(screen, WHITE, (black_enemy['x'] - player_x + game_area_x, black_enemy['y'] - player_y + HEIGHT // 2 - 10, ENEMY_SIZE, 5))
        pygame.draw.rect(screen, RED, (black_enemy['x'] - player_x + game_area_x, black_enemy['y'] - player_y + HEIGHT // 2 - 10, (black_enemy['health'] / 100) * ENEMY_SIZE, 5))


    # Draw the bullets
    for bullet in bullets:
        rotated_bullet = pygame.transform.rotate(bullet_image, math.degrees(-bullet['angle']))
        rotated_bullet_rect = rotated_bullet.get_rect(center=(bullet['x'] + BULLET_SIZE // 2 - player_x + game_area_x,
                                                              bullet['y'] + BULLET_SIZE // 2 - player_y + HEIGHT // 2))
        screen.blit(rotated_bullet, rotated_bullet_rect.topleft)

        # Calculate the position to blit the rotated bullet image
        rotated_bullet_rect = rotated_bullet.get_rect(center=(bullet['x'] + BULLET_SIZE // 2 - player_x + game_area_x, bullet['y'] + BULLET_SIZE // 2 - player_y + HEIGHT // 2))

        # Blit the rotated bullet image onto the screen
        screen.blit(rotated_bullet, rotated_bullet_rect.topleft)

    # Draw the health bar for the player
    pygame.draw.rect(screen, RED, (10, 10, player_health, 20))

    # Draw the enemy bullets
    for enemy_bullet in enemy_bullets:
        pygame.draw.rect(screen, YELLOW, (enemy_bullet['x'] - player_x + game_area_x, enemy_bullet['y'] - player_y + HEIGHT // 2, BULLET_SIZE, BULLET_SIZE))

    # Render and display the health text
    health_text = font.render(f'Health: {player_health}', True, WHITE)
    screen.blit(health_text, (10, 40))

    # Update the displayd
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()