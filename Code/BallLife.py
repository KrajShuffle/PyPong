import numpy as np

class BallLife:
    """
    Class defining ball movement in game
    """
    def __init__(self, rect, ball_velocity, ball_spscalar, ball_maxspeed):
        """
        Initialize the ball object from BallLife class
        :param rect: rect object representing ball
        :param ball_velocity: ball initial velocity
        :param ball_spscalar: ball speed increase value
        :param ball_maxspeed: ball max speed
        """
        self.rect = rect
        self.vel_x = ball_velocity[0]
        self.vel_y = ball_velocity[1]
        self.mxspd = ball_maxspeed
        self.spinc = ball_spscalar
        self.threshold = 10 # Velocity Threshold to Reset Ball Speed by reset_drop
        self.reset_drop = 6 # Speed drop decrease amount

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
        """
        Move ball in x direction by taking current x position and adding velocity
        :return: None
        """
        self.rect.x += self.vel_x

    def movey(self):
        """
        Move ball in y direction by taking current y position and adding velocity
        :return: None
        """
        self.rect.y += self.vel_y

    def flip_velx(self):
        """
        Flip the x-direction the ball will now travel
        :return: None
        """
        self.vel_x *= -1

    def flip_vely(self):
        """
        Flip the y-direction the ball will now travel
        :return: None
        """
        self.vel_y *= -1

    def paddle_collide(self):
        """
        If ball collides with ball, increase the speed value by 2 in both directions
        Only while current ball speed is less than max ball speed allowed
        :return: None
        """
        if np.abs(self.vel_x) < self.mxspd: # Check if current speed less than max
            if self.vel_x < 0: # Account for x velocity between negative
                self.vel_x -= self.spinc
            else: # x velocity is positive
                self.vel_x += self.spinc
        if np.abs(self.vel_y) < self.mxspd:
            if self.vel_y < 0: # Account for y velocity between negative
                self.vel_y -= self.spinc
            else: # y velocity is positive
                self.vel_y += self.spinc

    def reset_game_velocity(self):
        """
        Only while current ball speed is less than max ball speed allowed
        If ball speed exceeds threshold, decrease the speed value by 6 in both directions
        Else return speed at [6,6]
        :return: Adjusted Speed used when ball is reinitialized
        """
        if np.abs(self.vel_x) > self.threshold:
            new_vel = [self.vel_x - self.reset_drop, self.vel_x - self.reset_drop]
        else:
            new_vel = [self.reset_drop, self.reset_drop]
        return new_vel

