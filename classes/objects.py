from classes.lemmings import *


class Wall:
    def __init__(self, position_x, position_y):
        self.image = pygame.image.load("graphics/wall.png").convert()
        self.rect = self.image.get_rect(x=position_x, y=position_y)
