import pygame
class Paddle:
    """
    Class defining paddle movement within game
    """
    def __init__(self, pos_x, pos_y, pd_width, pd_height):
        """
        Initialize a paddle object
        :param pos_x: initial x position of paddle
        :param pos_y: initial y position of paddle
        :param pd_width: paddle width
        :param pd_height: paddle height
        """
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pd_width = pd_width
        self.pd_height = pd_height
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.pd_width, self.pd_height)
        self.can_move = True # Flag to prevent accidental ball-paddle overlap after initial collision
        self.time_pause = 500 # Prevent external hand position input for 500 milliseconds
        self.pause_initial_time = 0
        self.max_velocity = 20 # Max velocity paddle can travel
        self.velocity = 0 # Placeholder variable to calculate actual velocities
    def vert_collision_response(self, ball):
        """
        Used to prevent ball and paddle overlap from happening post-collision
        Prevents detection of multiple erroneous collisions
        :param ball: ball object from BallLife class
        :return: None
        """
        self.can_move = False # Prevent hand input to guide paddle movement
        self.pause_initial_time = pygame.time.get_ticks() # Record current time
        # Overlap Area Height between the ball and paddle
        # Prevent multiple collisions since ball cannot move far enough in next step without still being in the paddle
        overlap_height = self.rect.clip(ball.rect).height
        # Depending on where ball is (above or below paddle), shift paddle back by distance overlapped with ball
        if ball.vel_y > 0:
            self.rect.y += overlap_height
        else:
            self.rect.y -= overlap_height

    def update_paddle_y(self,hands, game_height, wall_thickness):
        """
        Update paddle position based on hand position provided
        :param hands: list of dictionaries containing distinct x & y coordinates mapped on hand
        :param game_height: screen display height
        :param wall_thickness: wall thickness
        :return: None
        """
        current_time = pygame.time.get_ticks() # Get current time
        # If pause is done, switch flag to enable hand guided paddle position
        if (current_time - self.pause_initial_time) >= self.time_pause:
            self.can_move = True

        # If paddle can move, and hand coordinates are retrieved
        if (hands and self.can_move):
            hand = hands[0] # One hand so only one dictionary mapping within list
            x_9, y_9 = hand['lmList'][9]  # Middle Finger MCP
            x_0, y_0 = hand['lmList'][0]  # Wrist

            # Mapping from approximately palm of hand to center of paddle
            yhand_cam = int(((y_9 + y_0) / 2) - (self.pd_height / 2))

            # Determine max y and min y distance paddle can travel
            max_bottom = game_height - (wall_thickness + self.pd_height)
            max_top = wall_thickness
            # If hand position within bounds defined by max and min y, paddle can travel
            if ((yhand_cam < max_bottom) & (yhand_cam > max_top)):
                # Calculate current velocity
                new_velocity = yhand_cam - self.rect.y

                # Check if current velocity is smaller in magnitude than max velocity
                # Assign that velocity value to self.velocity to update paddle position
                if new_velocity < 0: # Address case where velocity is negative
                    self.velocity = max(new_velocity, -1 * self.max_velocity)
                else: # Address case where velocity is positive
                    self.velocity = min(new_velocity, self.max_velocity)
                self.rect.y += self.velocity # Move paddle by velocity

            # If hand is below bottom bounds
            elif yhand_cam > max_bottom:
                # Gradually move paddle down till directly above bottom wall
                self.rect.y = min(self.rect.y + self.max_velocity, max_bottom)

            # If hand is above top bounds
            elif yhand_cam < max_top:
                # Gradually move paddle up till directly below top wall
                self.rect.y = max(self.rect.y - self.max_velocity, max_top)
