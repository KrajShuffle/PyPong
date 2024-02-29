import pygame
import numpy as np
class GameMetrics:
    def __init__(self, game_lives,  wall_thickness, screen_height, screen_width):
        self.score = 0
        self.base_score = 10
        self.score_multi = [1,2,3]
        self.lives = game_lives
        self.contact_time = 0
        self.ball_velx = 0
        self.ball_vely = 0
        self.paddle_center = [0,0]
        self.wall_thickness = wall_thickness
        self.screen_height = screen_height
        self.screen_width = screen_width
    def increment_score(self, pong_ball, paddle, old_velocity):
        if np.abs(old_velocity) <= 9:
            self.score += (self.base_score)
        elif 10 <= np.abs(old_velocity) <= 19:
            self.score += (self.base_score * 2)
        elif np.abs(old_velocity) >= 20:
            self.score += (self.base_score * 3)
        self.contact_time = pygame.time.get_ticks() # Get time of impact
        self.ball_velx = pong_ball.vel_x
        self.ball_vely = pong_ball.vel_y
        self.paddle_center = [paddle.centerx, paddle.centery]
    def decrement_lives(self):
        self.lives -= 1
    def decrement_score(self):
        self.score -= self.base_score * 2
    def bad_hit_detector(self):
        current_time = pygame.time.get_ticks()
        # Determine Largest Vertical Distance
        vertical_distance = 0
        center_topwall_distance = self.paddle_center[1] - self.wall_thickness
        center_botwall_distance = ((self.screen_height - self.wall_thickness) - self.paddle_center[1])
        if (center_topwall_distance > center_botwall_distance):
            vertical_distance = center_topwall_distance
        else:
            vertical_distance = center_botwall_distance
        # Compute max distance traveled if ball just went up to the wall and then right
        max_distance = vertical_distance + (self.screen_width - self.paddle_center[0])
        # Compute approximate distance ball would travel if it was a bad hit
        # bad hit only possible if ball bounces off top or bottom part of paddle to boundary
        diagonal_speed = np.sqrt((self.ball_vely **2) + (self.ball_velx ** 2))
        distance_traveled = (current_time - self.contact_time) / diagonal_speed

        if(distance_traveled <= max_distance):
            self.decrement_score()
    def reset_game(self):
        self.score = 0
        self.lives = 3
