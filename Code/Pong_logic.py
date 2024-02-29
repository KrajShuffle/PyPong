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
from Ball import Ball
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
green = (0, 255, 0)
black = (0, 0, 0)

# Define the ball & ball velocity
ball_radius = 20
ball_pos = [(screen_width // 2), (height // 2)]
ball_vel = [4, 4]
ball_speedinc = 2
ball_maxspeed = int(fps / 2) - 1
ball = Ball(ball_pos, ball_radius, ball_vel, ball_speedinc, ball_maxspeed)

# Define paddle and location
paddle_width = 40
paddle_height = 100
paddle_pos = [(screen_width - 150), (height // 2)]
paddle = Paddle(paddle_pos[0], paddle_pos[1],paddle_width, paddle_height)

# Define the walls and their location
wall_thickness = 40
top_wall = pygame.Rect(0,0, screen_width, wall_thickness)
bottom_wall = pygame.Rect(0,height - wall_thickness, screen_width, wall_thickness)
left_wall = pygame.Rect(0, wall_thickness, wall_thickness, height - (2 * wall_thickness))

# List of rects
walls = [top_wall, bottom_wall, left_wall]
rects = [top_wall, bottom_wall, left_wall, paddle.rect]

# Define collision detection test
def collide_test(ball, rects):
    collided_rects = []
    for rect in rects:
        if ball.colliderect(rect):
            collided_rects.append(rect)
    return collided_rects

def move_ball(ball, coltargets):
    ball.movex()
    collide_rects_x = collide_test(ball.rect, coltargets)
    if len(collide_rects_x) != 0:
        if paddle.rect in collide_rects_x:
            ball.paddle_collide()

        ball.flip_velx()
        ball.movex()
    ball.movey()
    collide_rects_y = collide_test(ball.rect, coltargets)
    if len(collide_rects_y) != 0:
        if paddle.rect in collide_rects_y:
            paddle.vert_collision_response(ball)
            ball.vertical_paddle_collide(paddle.rect)
            ball.paddle_collide()
        ball.flip_vely()
        ball.movey()


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
        ball.flip_velx()


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
    pygame.draw.circle(game_window, white, [ball.pos_x, ball.pos_y], ball.radius)  # white ball
    pygame.draw.rect(game_window, green, paddle.rect)
    for wall in walls:
        pygame.draw.rect(game_window, white, wall)

    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)