"""
File containing classes for all lemming types. That is:
    - lemming

"""
import pygame


class Lemming:
    """
    This class is going to represent each lemming.
    """
    def __init__(self, position_x, position_y, direction_x=None, direction_y=None):
        """
        Creates new lemming at (x, y)
        """
        # Assigning the image to the lemming
        self.image = pygame.image.load("graphics/lemming.png").convert()

        # Creating pygame rect object based on image provided above
        self.rect = self.image.get_rect(x=position_x, y=position_y)

        # Setting movement direction for the lemming
        # if direction_x is None and direction_y is None:
        self.dirX = 0
        self.dirY = 1
        #
        #else
        #    self.dirX = direction_x

        # Fall counter
        self.fall = 0
        self.dead = 0

    def __del__(self):
        del self.image
        del self.rect
        del self.dirX
        del self.dirY
        del self.fall
        self.dead = 1
        # self.image = None
        # self.rect = None
        # self.dirX = None
        # self.dirY = None
        # self.fall = None
        return None

    def move(self):
        # sprawdzić, czy natrafi na ścianę
        self.rect.x += self.dirX

        self.rect.y += self.dirY
        self.fall += self.dirY
        return self

    def collision_walls(self, walls):
        """
        Checks if the lemming collided with any of the walls.
        If it did then it's X-axis movement direction gets changed.
        """
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.dirX *= -1
                return self

    def collision_floors(self, floors):
        """
        Checks if the lemming collides with any of the floor parts.
        If it does then nothing happens and if it does not then it's begins to fall down.
        """
        for floor in floors:
            if self.rect.colliderect(floor.rect):
                if self.fall > 60:
                    self.__del__()
                    return self
                elif self.fall > 0:
                    self.dirX = 1
                    self.dirY = 0
                    self.fall = 0
                    return self
                #
                #    del self


class LemmingStopper (Lemming):
    """
    # This extended class is going to represent the lemming with a stopper function.
    """
