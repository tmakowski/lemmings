import pygame
from global_variables import *


class Wall:
    def __init__(self, position_x, position_y):
        self.image = pygame.transform.scale(
                        pygame.image.load("graphics/wall.png").convert(),
                        (BLOCK_SIZE, BLOCK_SIZE))
        self.rect = self.image.get_rect(x=position_x, y=position_y)


class Floor:
    def __init__(self, position_x, position_y, length_x=None):
        if length_x is None:
            length_x = 1
        self.image = pygame.transform.scale(
                        pygame.image.load('graphics/floor.png').convert(),
                        (BLOCK_SIZE*length_x, BLOCK_SIZE))
        self.rect = self.image.get_rect(x=position_x, y=position_y)
