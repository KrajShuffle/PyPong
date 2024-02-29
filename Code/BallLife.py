import pygame
import numpy as np

class BallLife:
    def __init__(self, rect, ball_velocity, ball_spscalar, ball_maxspeed):
        self.rect = rect
        self.vel_x = ball_velocity[0]
        self.vel_y = ball_velocity[1]
        self.mxspd = ball_maxspeed
        self.spinc = ball_spscalar

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

    def movex(self):
        self.rect.x += self.vel_x

    def movey(self):
        self.rect.y += self.vel_y

    def flip_velx(self):
        self.vel_x *= -1

    def flip_vely(self):
        self.vel_y *= -1

    def paddle_collide(self):
        if np.abs(self.vel_x) < self.mxspd:
            if self.vel_x < 0:
                self.vel_x -= self.spinc
            else:
                self.vel_x += self.spinc
        if np.abs(self.vel_y) < self.mxspd:
            if self.vel_y < 0:
                self.vel_y -= self.spinc
            else:
                self.vel_y += self.spinc

    def vertical_paddle_collide(self, paddle):
        if self.vel_y < 0: # Moving Upward
            self.rect.top = max(paddle.bottom, self.rect.top)
        else: # Moving Downward
            self.rect.top = min(paddle.top, self.rect.top)
