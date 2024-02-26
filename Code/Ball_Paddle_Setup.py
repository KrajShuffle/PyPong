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
#cap = cv2.VideoCapture(0)
#cap.set(3, width)
#cap.set(4, height)

# Define the ball & ball movement
ball_radius = 20
ball_pos = [(width // 2), (height // 2)]
ball_vel = [1, 1]


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
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    # if ball is about to exceed left or right most bounds
    if ((ball_pos[0] - ball_radius) <= 0) or ((ball_pos[0] + ball_radius) >= width):
        ball_vel[0] *= -1
    if(((ball_pos[1] - ball_radius) <= 0) or ((ball_pos[1] + ball_radius) >= height)):
        ball_vel[1] *= -1

    # Draw objects on screen
    window.fill((0, 0, 0))  # black screen
    pygame.draw.circle(window, (255,255,255), ball_pos, ball_radius)



    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)