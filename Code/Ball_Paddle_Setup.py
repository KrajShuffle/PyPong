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
import numpy as np
from cvzone.HandTrackingModule import  HandDetector

# Initialize
pygame.init()

# Create Window/Display
width, height = 1280, 720
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong Life")

# Initialize clock for FPS
fps = 30
clock = pygame.time.Clock()

# Webcam Settings
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
# Define webcam's separate window
cv2.namedWindow("Camera Feed", cv2.WINDOW_NORMAL)

# Define colors
white = (255,255,255)
green = (0, 255, 0)

# Define the ball & ball velocity
ball_radius = 20
ball_pos = [(width // 2), (height // 2)]
ball_vel = [1, 1]

# Define paddle and location
paddle_width = 40
paddle_height = 100
paddle_speed = 4
paddle_pos = [(width - 280), (height // 2)]
paddle_rect = pygame.Rect(paddle_pos[0], paddle_pos[1], paddle_width, paddle_height)

# Define the walls and their location
wall_thickness = 20
top_wall = pygame.Rect(0,0, width, wall_thickness)
bottom_wall = pygame.Rect(0,height - wall_thickness, width, wall_thickness)
left_wall = pygame.Rect(0, wall_thickness, wall_thickness, height - (2 * wall_thickness))
walls = [top_wall, bottom_wall, left_wall]

# Main Loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_UP):
                paddle_rect.y -= paddle_speed
            elif(event.key == pygame.K_DOWN):
                paddle_rect.y += paddle_speed


    # Apply Logic
    # Update game state
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # Wall Ball collision

    # Rect Definition always from top left corner & always updating based on new ball position
    ball_rect = pygame.Rect(ball_pos[0] - ball_radius, ball_pos[1] - ball_radius, (2 * ball_radius), (2 * ball_radius))

    # Ball Collision with top and bottom walls
    for wall_rect in walls[:2]:
        if ball_rect.colliderect(wall_rect):
            ball_vel[1] *= -1

    # Ball Collision with left wall
    if ball_rect.colliderect(left_wall):
        ball_vel[0] *= -1

    if ball_rect.colliderect((paddle_rect)):
        ball_vel[0] *= -1

    # if ball is about to exceed left or right most bounds; kept since don't have paddle in place
    if ((ball_pos[0] - ball_radius) <= 0) or ((ball_pos[0] + ball_radius) >= width):
        ball_vel[0] *= -1


    # Draw objects on screen
    window.fill((0, 0, 0))  # black screen
    pygame.draw.circle(window, white, ball_pos, ball_radius) # white ball
    pygame.draw.rect(window, green, paddle_rect)
    for wall in walls:
        pygame.draw.rect(window, white, wall)

    # Creating and loading in webcam image
    ret, frame = cap.read()
    # If not reading, kill game
    if not ret:
        break

    # flip camera output so its more inituitive to user
    cor_frame_orient = cv2.flip(frame, 1)
    cv2.imshow('Camera Feed', cor_frame_orient) # Display output in separate window

    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)