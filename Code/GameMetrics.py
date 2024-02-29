import pygame

class GameMetrics:
    def __init__(self, game_hscore):
        self.score = 0
        self.lives = 3
        self.game_hscore = game_hscore
    def increment_score(self):
        self.score += 10
    def decrement_lives(self):
        self.lives -= 1
    def reset_game(self):
        self.score = 0
        self.lives = 3
