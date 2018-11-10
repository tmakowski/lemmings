"""
File containing classes for all lemming types. That is:
    - lemming

"""
import pygame


class Lemming:
    """
    This class is going to represent each lemming.
    """
    def __init__(self, position_x, position_y, direction_x=None):
        """
        Creates new lemming at (x, y)
        """
        # Assigning the image to the lemming
        self.image = pygame.image.load("graphics/lemming.png").convert()

        # Creating pygame rect object based on image provided above
        self.rect = self.image.get_rect(x=position_x, y=position_y)

        # Setting movement direction for the lemming
        if direction_x is None:
            self.dirX = 1
        else:
            self.dirX = direction_x

    # def __del__(self):


    def move(self):
        # sprawdzić, czy natrafi na ścianę
        self.rect.x += self.dirX
        return self

    def collision(self):
        self.dirX *= -1
        return self


class LemmingStopper (Lemming):
    """
    # This extended class is going to represent the lemming with a stopper function.
    """
