import pygame
import numpy as np
class Ball:
    def __init__(self, pos_xy, ball_radius, ball_velocity, ball_spscalar, ball_maxspeed):
        self.pos_x = pos_xy[0]
        self.pos_y = pos_xy[1]
        self.radius = ball_radius
        self.vel_x = ball_velocity[0]
        self.vel_y = ball_velocity[1]
        self.mxspd = ball_maxspeed
        self.spinc = ball_spscalar

    @property
    def pos_x(self):
        return self._pos_x

    @pos_x.setter
    def pos_x(self, value):
        self._pos_x = value

    @property
    def pos_y(self):
        return self._pos_y

    @pos_y.setter
    def pos_y(self, value):
        self._pos_y = value

    @property
    def rect(self):
        return pygame.Rect(self.pos_x - self.radius, self.pos_y - self.radius, (2 * self.radius), (2 * self.radius))
    def movex(self):
        self.pos_x += self.vel_x
    def movey(self):
        self.pos_y += self.vel_y
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
            self.pos_y = max(paddle.bottom, self.pos_y)
        else: # Moving Downward
            self.pos_y = min(paddle.top, self.pos_y)
