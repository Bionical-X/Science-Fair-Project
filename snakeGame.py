import pygame
import random

class Game:
    def __init__(self, width, height):
        pygame.display.set_Caption("SnakeGame")
        self.game_width = width
        self.game_height = height
        self.gameDisplay = pygame.display.set_mode((width, height + 60))
        #self.bg = pygame.image.load("img/background.png")
        self.crash = False
        self.player = Player(self)
        self.food = Food()
        self.score = 0
