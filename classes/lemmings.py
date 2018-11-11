"""
File containing classes for all lemming types. That is:
    - lemming
To keep in mind: the lemmings' graphics should be 1px smaller than the image canvas. Eg. 9x9 px lemming on 10x10 px image
"""
import pygame

BLOCK_SIZE = 1


class Lemming:
    """
    This class is going to represent each lemming.
    """
    #global BLOCK_SIZE

    def __init__(self, position_x, position_y):
        """
        Creates new lemming at (x, y)
        """
        # Assigning the image to the lemming
        self.image = pygame.image.load("graphics/lemming.png").convert()

        # Creating pygame rect object based on image provided above
        self.rect = self.image.get_rect(x=position_x, y=position_y)

        # Setting movement direction for the lemming
        self.dirX = 0
        self.dirY = 1

        # Fall counter
        self.fall = 0

        # Death flag
        self.dead = 0

    def __del__(self):
        # Deleting all lemming's parameters
        del self.image
        del self.rect
        del self.dirX
        del self.dirY
        del self.fall
        # The sad news:
        self.dead = 1
        return None

    def move(self):
        # Importing the information about block sze
        global BLOCK_SIZE

        # Moving the lemming in it is current X-axis direction by the block size
        self.rect.x += self.dirX*BLOCK_SIZE

        # Moving the lemming down if it is falling and counting how many block it have fell down
        self.rect.y += self.dirY*BLOCK_SIZE
        self.fall += self.dirY
        return self

    def collision_walls(self, walls):
        """
        Checks if the lemming collided with any of the walls.
        If it did then it's X-axis movement direction gets changed.
        """
        if self.rect.collidelist(walls) != -1:
            self.dirX *= -1
        return self

    def collision_floors(self, floors):
        """
        Checks if the lemming collides with any of the floors in the list.
        If it does then it's checked if it just hit the surface or not. If not - nothing happens.
        """
        if self.rect.collidelist(floors) != -1:
            if self.fall > 60:
                self.__del__()
            elif self.fall > 0:
                self.dirX = 1
                self.dirY = 0
                self.fall = 0
        else:   # if the lemming does not collide with any of the floors
            self.dirX = 0
            self.dirY = 1
        return self


class LemmingStopper (Lemming):
    """
    # This extended class is going to represent the lemming with a stopper function.
    """
