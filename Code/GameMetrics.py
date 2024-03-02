import pygame
import numpy as np
class GameMetrics:
    """
    Class for Tracking Score, Penalties, & Detecting Bad Paddle Hits Used in Game
    Main object stores these metrics and helps compute score adjustments
    """
    def __init__(self, game_lives,  wall_thickness, screen_height, screen_width):
        self.score = 0
        self.base_score = 10
        self.lives = game_lives
        self.contact_time = np.inf # Initially set to infinite to prevent point loss on game load
        self.ball_velx = 0
        self.ball_vely = 0
        self.paddle_center = [0,0]
        self.wall_thickness = wall_thickness
        self.screen_height = screen_height
        self.screen_width = screen_width
        self.sound_hurt = pygame.mixer.Sound("../Game Assets/hurt.ogg")
        self.sound_gain = pygame.mixer.Sound("../Game Assets/paddle.ogg")
        self.unit_match = 38 # Conversion Value used to compare ball max travel and actual distance
    def increment_score(self, pong_ball, paddle, old_velocity):
        """

        :param pong_ball: Retrieve ball object to get x & y velocity ball will now travel with
        :param paddle: Retrieve paddle position to determine max distance ball can travel
        :param old_velocity: Retrieve velocity of ball upon impact to calculate score increase
        :return:
        """
        if np.abs(old_velocity) <= 9: # if ball contact velocity between 0 and 9
            self.score += (self.base_score)
        elif 10 <= np.abs(old_velocity) <= 19: # if ball contact velocity between 10 and 19
            self.score += (self.base_score * 2)
        elif np.abs(old_velocity) >= 20:
            self.score += (self.base_score * 3) # if ball contact velocity between 10 and 19
        self.sound_gain.play()
        self.contact_time = pygame.time.get_ticks() # Get time of impact
        self.ball_velx = pong_ball.vel_x
        self.ball_vely = pong_ball.vel_y
        self.paddle_center = [paddle.centerx, paddle.centery]
    def decrement_lives(self):
        """
        If ball goes out of bounds, reduce num of lives and play sound
        :return:
        """
        self.lives -= 1
        self.sound_hurt.play()
    def decrement_score(self):
        """
        If a bad hit between ball and paddle is detected, reduce total score
        :return:
        """
        self.score -= self.base_score * 2
    def bad_hit_detector(self):
        """
        Detect if bad contact of paddle with ball resulted in lost life
        If so, conduct appropriate point adjustment
        :return:
        """
        current_time = pygame.time.get_ticks()
        # Compute Distance of paddle to either top or bottom wall
        vertical_distance = 0
        center_topwall_distance = self.paddle_center[1] - self.wall_thickness
        center_botwall_distance = ((self.screen_height - self.wall_thickness) - self.paddle_center[1])
        # Compare computed distances to determine longest vertical path
        if (center_topwall_distance > center_botwall_distance):
            vertical_distance = center_topwall_distance
        else:
            vertical_distance = center_botwall_distance

        # Compute max distance traveled if ball just went up to the wall and then right
        # Also convert computed distance to approx same units used in game
        max_distance = (vertical_distance + (self.screen_width - self.paddle_center[0])) * self.unit_match

        # Compute approximate distance ball would travel if it was a bad hit
        # bad hit only possible if ball bounces off top or bottom part of paddle to boundary
        diagonal_speed = np.sqrt((self.ball_vely **2) + (self.ball_velx ** 2))
        distance_traveled = ((current_time - self.contact_time) * diagonal_speed)

        # If actual distance traveled by ball is less than max distance ball could travel
        if(distance_traveled <= max_distance):
            self.decrement_score() # Decrement score since highly likely its a bad hit
