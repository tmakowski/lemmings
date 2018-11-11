import pygame
# from classes.lemmings import Lemming


class Wall:
    def __init__(self, position_x, position_y):
        self.image = pygame.image.load("graphics/wall.png").convert()
        self.rect = self.image.get_rect(x=position_x, y=position_y)


class Floor:
    def __init__(self, position_x, position_y):
        # pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(pygame.image.load('graphics/wall.png').convert(), 90)
        self.rect = self.image.get_rect(x=position_x, y=position_y)
