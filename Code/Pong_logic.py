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
#game_prop = 2/3
screen_width = 1280
game_width, height = screen_width, 720
window = pygame.display.set_mode((game_width, height))
pygame.display.set_caption("Pong Life")

# Initialize clock for FPS
fps = 60
clock = pygame.time.Clock()

# Webcam Settings
#cam_prop = 1 - game_prop
cap = cv2.VideoCapture(0)
cap.set(3, int(screen_width))
cap.set(4, height)
# Define webcam's separate window
cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

# Defining HandDetector
hand_detect = HandDetector(maxHands= 1)

# Define colors
white = (255,255,255)
green = (0, 255, 0)

# Define the ball & ball velocity
ball_radius = 20
ball_pos = [(game_width // 2), (height // 2)]
ball_vel = [2, 3]
ball_speedinc = 2
ball_maxspeed = int(fps / 2) - 1
ball = Ball(ball_pos, ball_radius, ball_vel, ball_speedinc, ball_maxspeed)

# Define paddle and location
paddle_width = 40
paddle_height = 100
paddle_pos = [(game_width - 120), (height // 2)]
paddle = Paddle(paddle_pos[0], paddle_pos[1],paddle_width, paddle_height)

# Define the walls and their location
wall_thickness = 40
top_wall = pygame.Rect(0,0, game_width, wall_thickness)
bottom_wall = pygame.Rect(0,height - wall_thickness, game_width, wall_thickness)
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
    if ((ball.pos_x - ball_radius) <= 0) or ((ball.pos_x + ball_radius) >= game_width):
        ball.flip_velx()

    # Draw objects on screen
    window.fill((0, 0, 0))  # black screen
    pygame.draw.circle(window, white, [ball.pos_x, ball.pos_y], ball.radius) # white ball
    pygame.draw.rect(window, green, paddle.rect)
    for wall in walls:
        pygame.draw.rect(window, white, wall)

    # Creating and loading in webcam image
    success, img = cap.read()
    cor_img_orient = cv2.flip(img, 1)
    hands, img_drawn = hand_detect.findHands(cor_img_orient, flipType= False)
    paddle.update_paddle_y(hands)

    # If not reading, kill game
    if not success:
        break

    # flip camera output so its more intuitive to user
    cv2.imshow('Camera Feed', img_drawn) # Display output in separate window

    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)