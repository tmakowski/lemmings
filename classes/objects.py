import pygame
from global_variables import BLOCK_SIZE,\
    OBJECT_GRAPHICS_FLOOR, OBJECT_GRAPHICS_WALL


class Floor:
    """
    Parent class for all objects' classes.
    """
    def __init__(self, position_x, position_y, length_x=None, length_y=None, img=OBJECT_GRAPHICS_FLOOR):
        """
        Creates new floor at position (x, y) that can be stretched by providing length_x/_y factors.
        """
        # Default values for scaling
        if length_x is None:
            length_x = 1
        if length_y is None:
            length_y = 1

        # Scaling and loading the image
        self.image = pygame.transform.scale(
                        pygame.image.load(img),
                        (BLOCK_SIZE * length_x, BLOCK_SIZE * length_y))

        # Creating the hitbox
        self.rect = self.image.get_rect(x=position_x, y=position_y)


class Wall (Floor):
    """
    Subclass representing walls.
    """
    def __init__(self, position_x, position_y, length_x=None, length_y=None):
        """
        Calls the constructor from parent class (Floor) with image representing a wall.
        """
        super(self.__class__, self).__init__(position_x, position_y, length_x, length_y, img=OBJECT_GRAPHICS_WALL)
