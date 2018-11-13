import pygame
from global_variables import *


class Floor:
    def __init__(self, position_x, position_y, length_x=None, length_y=None, img="graphics/floor.png"):
        # Default values for scaling
        if length_x is None:
            length_x = 1
        if length_y is None:
            length_y = 1

        # Scaling of the image
        self.image = pygame.transform.scale(
                        pygame.image.load(img).convert(),
                        (BLOCK_SIZE * length_x, BLOCK_SIZE * length_y))

        # Creating the hitbox
        self.rect = self.image.get_rect(x=position_x, y=position_y)


class Wall (Floor):
    def __init__(self, position_x, position_y, length_x=None, length_y=None):
        super(self.__class__, self).__init__(position_x, position_y, length_x, length_y, img="graphics/wall.png")
