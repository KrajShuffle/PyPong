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
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Main Loop
start = True
while start:
    # Get Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            start = False
            pygame.quit()

    # Apply Logic
    #window.fill((255,255,255))

    # OpenCV
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imgRGB = np.rot90(imgRGB)
    frame = pygame.surfarray.make_surface(imgRGB).convert()
    window.blit(frame,(0,0))

    # Update display
    pygame.display.update()

    # Set FPS
    clock.tick(fps)