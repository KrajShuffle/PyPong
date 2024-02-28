import pygame
class Paddle:
    def __init__(self, pos_x, pos_y, pd_width, pd_height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pd_width = pd_width
        self.pd_height = pd_height
        self.hand_ymax = 1350
        self.hand_ymin = 200
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.pd_width, self.pd_height)
    def update_paddle_y(self,hands, game_height, wall_thickness, wiggle_room):
        # HandDetector
        if hands:
            hand = hands[0]
            x_9, y_9 = hand['lmList'][9]  # Middle Finger MCP
            x_0, y_0 = hand['lmList'][0]  # Wrist
            # Mapping from approximately hand palm to center of paddle
            yhand_cam = int(((y_9 + y_0) / 2))
            max_bottom = game_height - (wall_thickness + wiggle_room + self.pd_height)
            max_top = wall_thickness + wiggle_room
            if ((yhand_cam < self.hand_ymax) & (yhand_cam > self.hand_ymin)):
                # Linear Interpolation of Mapping Hand Y Range to Paddle Y Range
                # Hand Y Range: (200 to 1350)
                # Paddle Y Range (wall_thickness (40) to (game_height (720) - wall_thickness (40) - paddle_height (100))
                self.rect.y = int(yhand_cam *(540 / 1150) + 40 - (108_000 / 1150))
            if not (yhand_cam < self.hand_ymax):
                self.rect.y = max_bottom
            if not(yhand_cam > self.hand_ymin):
                self.rect.y = max_top
