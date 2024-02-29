"""
Pygame Template

    Import Pygame
    Initialize Pygame
    Create Pygame display
    Initialize clock for FPS

    Loop
        Get Events
            if quit:
                quit pygame
        Apply Logic of Game
        Update display/window
        Set FPS

"""
# Import
import pygame
import cv2
from Paddle import Paddle
from BallLife import BallLife
from GameMetrics import GameMetrics
import numpy as np
from cvzone.HandTrackingModule import HandDetector

# Initialize
pygame.init()

# Create Window/Display
screen_width, height = 1280 - 100, 720
game_window = pygame.display.set_mode((screen_width, height))
pygame.display.set_caption("Pong Life")

# Initialize clock for FPS
fps = 60
clock = pygame.time.Clock()

# Webcam Settings
cap = cv2.VideoCapture(0)
cap.set(3, screen_width)
cap.set(4, height)

# Defining HandDetector
hand_detect = HandDetector(maxHands= 1)

# Define colors
white = (255,255,255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
blue = (0, 0, 255)

# Load Game Font & lives
titlefont = pygame.font.Font("../Game Assets/Cabal-w5j3.ttf", 50)
game_lives = 3

# Load Game Images
heart_img = pygame.image.load("../Game Assets/heart48x48.png").convert_alpha()
life_appear = [True] * game_lives
start_life_pos = 950
life_pos = start_life_pos


# Define the ball & ball velocity
ball_radius = 20
ball_center = [(screen_width // 2) -50, (height // 2)]
ball_vel = [4, 4]
ball_speedinc = 2
ball_maxspeed = int(fps / 2) - 1

ball_rect = pygame.Rect(ball_center[0] - ball_radius, ball_center[1] - ball_radius, (2 * ball_radius), (2 * ball_radius))
ball = BallLife(ball_rect, ball_vel, ball_speedinc, ball_maxspeed)
# Define paddle and location
paddle_width = 40
paddle_height = 100
paddle_pos = [(screen_width - 225), (height // 2)]
paddle = Paddle(paddle_pos[0], paddle_pos[1],paddle_width, paddle_height)

# Define the walls and their location
wall_thickness = 60
top_wall = pygame.Rect(0,0, screen_width, wall_thickness)
bottom_wall = pygame.Rect(0,height - wall_thickness, screen_width, wall_thickness)
left_wall = pygame.Rect(0, wall_thickness, wall_thickness, height - (2 * wall_thickness))

# List of rects
walls = [top_wall, bottom_wall, left_wall]
rects = [top_wall, bottom_wall, left_wall, paddle.rect]

# Initialize Game
game_stats = GameMetrics(game_lives, wall_thickness, height, screen_width)

# Define collision detection test
def collide_test(ball, rects):
    collided_rects = []
    for rect in rects:
        if ball.colliderect(rect):
            collided_rects.append(rect)
    return collided_rects

def move_ball(ball, coltargets):
    # Move the ball vertically
    ball.rect.y += ball.vel_y
    collide_rects_y = collide_test(ball.rect, coltargets)
    for obj in collide_rects_y:
        if ball.vel_y > 0:
            ball.rect.bottom = obj.top
            if obj == paddle.rect:
                paddle.vert_collision_response(ball)
                ball.paddle_collide()
                game_stats.increment_score(ball, paddle.rect)
        elif ball.vel_y < 0:
            ball.rect.top = obj.bottom
            if obj == paddle.rect:
                paddle.vert_collision_response(ball)
                ball.paddle_collide()
                game_stats.increment_score(ball, paddle.rect)
        ball.flip_vely()

    # Move the ball horizontally
    ball.rect.x += ball.vel_x
    collide_rects_x = collide_test(ball.rect, coltargets)
    for obj in collide_rects_x:  # for each object collided with ball in collide_rects_x
        if ball.vel_x > 0:
            ball.rect.right = obj.left
            if obj == paddle.rect:
                ball.paddle_collide()
                game_stats.increment_score(ball, paddle.rect)
        elif ball.vel_x < 0:
            ball.rect.left = obj.right
            if obj == paddle.rect:
                ball.paddle_collide()
                game_stats.increment_score(ball, paddle.rect)
        ball.flip_velx()

# Main Loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    # Update game state
    move_ball(ball, rects)

    # if ball is about to exceed left or right most bounds; kept for testing game
    if ((ball.pos_x - ball_radius) <= 0) or ((ball.pos_x + ball_radius) >= screen_width):
        # Reinitialize ball at original position
        ball_rect = pygame.Rect(ball_center[0] - ball_radius, ball_center[1] - ball_radius, (2 * ball_radius),
                                (2 * ball_radius))
        ball = BallLife(ball_rect, ball_vel, ball_speedinc, ball_maxspeed)
        # Game Penalty Actions
        game_stats.bad_hit_detector()
        game_stats.decrement_lives() # 3 to 0
        life_appear[game_stats.lives] = False


    # Creating and loading in webcam image
    success, img = cap.read()
    cor_img_orient = cv2.flip(img, 1)
    hands, img_drawn = hand_detect.findHands(cor_img_orient, flipType= False)
    paddle.update_paddle_y(hands, height, wall_thickness, 3)
    img_drawn = np.rot90(img_drawn)
    RGB_img = cv2.cvtColor(img_drawn, cv2.COLOR_BGR2RGB)


    # If not reading, kill game
    if not success:
        break

    # Draw objects on screen
    # Initial base black background
    black_bg = pygame.Surface((screen_width, height))  # base background with how big it is
    black_bg.fill(black) # Filling base background with black

    # Overlaid Transparent Camera Feed
    RGB_surface = pygame.surfarray.make_surface(RGB_img)
    RGB_surface = pygame.transform.flip(RGB_surface, True, False) # Flip to Correct Orientation
    cam_surface = pygame.Surface((screen_width, height), pygame.SRCALPHA) # Transparent Canvas
    cam_surface.set_alpha(128) # Setting Transparency of cam_surface
    cam_surface.blit(RGB_surface,(0, 0)) # Where it starts from is second input


    # Overlaid Elements in Order
    game_window.blit(black_bg, (0, 0))  # Adding black background as the base
    game_window.blit(cam_surface, (0, 0)) # Adding transparent Canvas on top of black bg
    pygame.draw.circle(game_window, white,
                       [ball.pos_x + ball_radius, ball.pos_y + ball_radius], ball_radius)  # white ball
    pygame.draw.rect(game_window, green, paddle.rect)
    for wall in walls:
        pygame.draw.rect(game_window, white, wall)

    # Text and Images
    gameTitle = titlefont.render("Pong Game", False, black)
    game_window.blit(gameTitle, (wall_thickness, 0))
    scoreLabel = titlefont.render("Score: " + str(game_stats.score), False, blue)
    game_window.blit(scoreLabel, (wall_thickness + 575, 0))

    for logical in life_appear:
        if logical:
            game_window.blit(heart_img, (life_pos, 12))
        life_pos += 55
    life_pos = start_life_pos # Redefined to prevent displaying outside display

    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)