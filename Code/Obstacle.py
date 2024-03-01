import pygame
import numpy as np
import random
class Obstacle:
    def __init__(self, rect, obs_width, obs_height, obs_velocity, screen_height):
        self.rect = rect
        self.width = obs_width
        self.height = obs_height
        self.vel_x = obs_velocity[0]
        self.vel_y = obs_velocity[1]
        self.screen_height = screen_height

    @property
    def pos_x(self):
        return self.rect.left

    @pos_x.setter
    def pos_x(self, value):
        self.rect.left = value

    @property
    def pos_y(self):
        return self.rect.top
    @pos_y.setter
    def pos_y(self, value):
        self.rect.top = value
    def movex(self, wall_thickness, ball_radius, paddle_xpos):
        x_min = (wall_thickness + (2 * ball_radius))
        x_max = paddle_xpos - (self.width + ball_radius)
        if (self.rect.x < x_max) and (self.rect.x > x_min):
            self.rect.x += self.vel_x
        else:
            self.flip_velx()
            self.rect.x += self.vel_x
    def movey(self, wall_thickness, ball_radius):
        y_min = (wall_thickness + (2 * ball_radius))
        y_max = (self.screen_height - wall_thickness - (1.5 * self.height))
        if (self.rect.y < y_max) and (self.rect.y > y_min) :
            self.rect.y += self.vel_y
        else:
            self.flip_vely()
            self.rect.y += self.vel_y
    def flip_velx(self):
        self.vel_x *= -1
    def flip_vely(self):
        self.vel_y *= -1