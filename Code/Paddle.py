import pygame
class Paddle:
    def __init__(self, pos_x, pos_y, pd_width, pd_height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pd_width = pd_width
        self.pd_height = pd_height
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.pd_width, self.pd_height)
        self.can_move = True
        self.time_pause = 500
        self.pause_initial_time = 0
        self.max_velocity = 18
        self.velocity = 0
        self.wiggle_room = 15
    def vert_collision_response(self, ball):
        self.can_move = False
        self.pause_initial_time = pygame.time.get_ticks()
        # Overlap Area Height between the ball and paddle
        # Prevent multiple collisions since ball cannot move far enough in next step without still being in the paddle
        overlap_height = self.rect.clip(ball.rect).height
        if ball.vel_y > 0:
            self.rect.y += overlap_height
        else:
            self.rect.y -= overlap_height

    def update_paddle_y(self,hands, game_height, wall_thickness):
        current_time = pygame.time.get_ticks()
        if (current_time - self.pause_initial_time) >= self.time_pause:
            self.can_move = True
        if (hands and self.can_move):
            hand = hands[0]
            x_9, y_9 = hand['lmList'][9]  # Middle Finger MCP
            x_0, y_0 = hand['lmList'][0]  # Wrist
            # Mapping from approximately palm of hand to center of paddle
            yhand_cam = int(((y_9 + y_0) / 2) - (self.pd_height / 2))
            max_bottom = game_height - (wall_thickness + self.pd_height)
            max_top = wall_thickness
            if ((yhand_cam < max_bottom) & (yhand_cam > max_top)):
                new_velocity = yhand_cam - self.rect.y
                if new_velocity < 0:
                    self.velocity = max(new_velocity, -1 * self.max_velocity)
                else:
                    self.velocity = min(new_velocity, self.max_velocity)
                self.rect.y += self.velocity
            if not (yhand_cam < max_bottom):
                self.rect.y = max_bottom
            if not((yhand_cam - self.wiggle_room) > max_top):
                self.rect.y = max_top
