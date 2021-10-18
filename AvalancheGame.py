import pygame
import sys
import random

pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Screen color
black_color = (0,0,0)

# Player model specifications
white_color = (255,250,250)
player_pos_x = 400
player_pos_y = 500
player_size = 50

# Falling block specifications
red_color = (255,0,0)
block_size = 50
block_pos_x = random.randint(0, SCREEN_WIDTH-block_size)
block_pos_y = 0
block_speed = 3
block_list = [[block_pos_x, block_pos_y]]

# Game Stats
score = 0
diff = ""

GAME_OVER = False

frame_rate = pygame.time.Clock()

font = pygame.font.SysFont("monospace", 35)

# Creates new blocks for draw_functions 
def drop_blocks(block_list):
    stagger = random.random()
    if len(block_list) < 10 and stagger < 0.1:
        x_value = random.randint(0,SCREEN_WIDTH-block_size)
        y_value = 0
        block_list.append([x_value, y_value])

# Draws the falling blocks on the screen
def draw_blocks(block_list):
    for block in block_list:
            pygame.draw.rect(screen, red_color, (block[0], block[1], block_size, block_size))


# Uses 4 test cases to determine whether a block has collided with player
def detect_collision(player_pos_x, player_pos_y, block_pos_x, block_pos_y):
    player_x = player_pos_x
    player_y = player_pos_y
    block_x = block_pos_x
    block_y = block_pos_y

    if (block_x >= player_x and block_x < (player_x + player_size)) or (player_x >= block_x and player_x < (block_x + block_size)):
        if (block_y >= player_y and block_y < (player_y + player_size)) or (player_y >= block_y and player_y < (block_y + block_size)):
            return True
    return False

# Updating falling block positions
def update_block_positions(block_list, score):
    for index, block in enumerate(block_list):
        if block[1] >= 0 and block[1] < SCREEN_HEIGHT:
            block[1] += block_speed
        else:
            block_list.pop(index)
            score += 1
    return score

# Uses detect_collision to check for collision in every iteration
def collision_check(block_list, player_pos_x, player_pos_y):
    for block in block_list:
        if detect_collision(block[0], block[1], player_pos_x, player_pos_y):
            return True
    return False

# Increases block falling speeds as score increases
def level(score, block_speed):
    block_speed = score/10 + 2
    return block_speed

# General difficulty of game
def difficulty(score, diff):
    if score < 20:
        diff = "Easy"
    elif score < 40:
        diff = "Medium"
    elif score < 60:
        diff = "Hard"
    elif score < 80:
        diff = "Insane"
    else:
        diff = "Goodbye"
    return diff

while not GAME_OVER:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        # User input changes player model position
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_pos_x -= 50
            elif event.key == pygame.K_RIGHT:
                player_pos_x += 50


    screen.fill(black_color)

    
    drop_blocks(block_list)
    score = update_block_positions(block_list, score)
    block_speed = level(score, block_speed)
    
    # Prints score and difficulty on screen
    score_text = "Score: " + str(score)
    label = font.render(score_text, 1, white_color)
    screen.blit(label, (SCREEN_WIDTH-300, SCREEN_HEIGHT-40))
    diff_text = "Difficulty: " + difficulty(score, diff)
    diff_label = font.render(diff_text, 1, white_color)
    screen.blit(diff_label, (SCREEN_WIDTH-800, SCREEN_HEIGHT-40))
   
    if collision_check(block_list, player_pos_x, player_pos_y):
        GAME_OVER = True
        break
    draw_blocks(block_list)
    pygame.draw.rect(screen, white_color, (player_pos_x, player_pos_y, player_size, player_size))
    frame_rate.tick(60)
    pygame.display.update()

# Final Message
print("GAME OVER!")
print("SCORE: " + str(score))