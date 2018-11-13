"""
File containing classes for all lemming types. That is:
    - lemming
To keep in mind: the lemmings' graphics should be 1px smaller than the image canvas. Eg. 9x9 px lemming on 10x10 px image
"""
import pygame
from global_variables import *


class Lemming:
    """
    This class is going to represent a regular lemming.
    """
    def __init__(self, position_x, position_y):
        """
        Creates new lemming at position (x, y) counting from top left corner of the map.
        """
        # Assigning the image to the lemming
        self.image = pygame.transform.scale(
                        pygame.image.load("graphics/lemming2.png"),
                        (BLOCK_SIZE, BLOCK_SIZE))

        # Creating pygame rect object based on image provided above
        self.rect = self.image.get_rect(x=position_x, y=position_y)

        # Setting movement direction for the lemming
        self.dirX = 1
        self.dirY = 1

        # Fall counter
        self.fall = 0

        # Death flag
        self.dead = 0

    def __del__(self):
        """
        Lemming destructor... or lemming killer? Whatever. You get the point.
        """
        self.image = pygame.transform.scale(
                        pygame.image.load("graphics/lemming_dead.png"),
                        (BLOCK_SIZE, BLOCK_SIZE))

        # Stopping the lemming's movement
        self.dirX = 0
        self.dirY = 0

        # Delivering the sad news:
        self.dead = 1
        return None

    def move(self):
        """
        Function used to move lemmings in their current movement direction.
        """
        if self.dirY == 0:
            # Moving the lemming in it is current X-axis direction by the block size
            self.rect.x += self.dirX
        else:
            # Moving the lemming down if it is falling and counting how many block it have fell down
            self.rect.y += self.dirY
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
        Checks if the lemming has a floor under it's feet. If it doesn't then the lemming starts to fall.
        """
        # Check if lemming is touching the floor on the floor
        if self.rect.collidelist(floors) != -1:
            # Check if the lemming has passed the fall threshold
            if self.fall > LEMMING_FALL_THRESHOLD*BLOCK_SIZE:
                self.__del__()
            # Check if it was falling at all
            elif self.fall > 0:
                # If it was falling, then stop the fall and reset the fall counter
                self.dirY = 0
                self.fall = 0
        else:
            # If the lemming slipped of the floor then make it start falling
            self.dirY = 1
        return self


class LemmingStopper (Lemming):
    """
    # This extended class is going to represent the lemming with a stopper function.
    """
