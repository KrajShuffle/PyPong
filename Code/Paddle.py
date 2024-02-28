import pygame
class Paddle:
    def __init__(self, pos_x, pos_y, pd_width, pd_height):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pd_width = pd_width
        self.pd_height = pd_height
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.pd_width, self.pd_height)
    def update_paddle_y(self,hands):
        # HandDetector
        if hands:
            hand = hands[0]
            x_9, y_9 = hand['lmList'][9]  # Middle Finger MCP
            x_0, y_0 = hand['lmList'][0]  # Wrist
            # Mapping from approximately hand palm to center of paddle
            self.rect.y = int(((y_9 + y_0) / 2) - (self.pd_height / 2))
