import pygame

from classes.lemmings import Lemming
from global_variables import BLOCK_SIZE,\
    OBJECT_GRAPHICS_FLOOR, OBJECT_GRAPHICS_WALL, OBJECT_GRAPHICS_ENTRANCE, OBJECT_GRAPHICS_EXIT, OBJECT_GRAPHICS_WATER


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
                        (int(BLOCK_SIZE * length_x), int(BLOCK_SIZE * length_y)))

        # Creating the hitbox
        self.rect = self.image.get_rect(x=position_x, y=position_y)


class Wall (Floor):
    """
    Subclass representing the walls.
    """
    def __init__(self, position_x, position_y, length_x=None, length_y=None, img=OBJECT_GRAPHICS_WALL):
        """
        Calls the constructor from parent class (Floor) with an image representing a wall.
        """
        super(self.__class__, self).__init__(position_x, position_y, length_x, length_y, img)


class Entrance (Floor):
    """
    Subclass representing the level entrance.
    """
    def __init__(self, position_x, position_y, length_x=None, length_y=None, img=OBJECT_GRAPHICS_ENTRANCE):
        """
        Calls the constructor of the parent class (Floor) with an image representing an entrance.
        Additionally we set a timer and counter variables used during lemmings' spawning.
        """
        super(self.__class__, self).__init__(position_x, position_y, length_x, length_y, img)

        # Used to count frames between next lemmings spawns
        self.spawn_timer = 0

        # Counts how many lemmings were spawned
        self.spawn_counter = 0

    def spawn(self, lemmings, spawn_rate, spawn_number, lem_type=Lemming):
        """
        Method used to spawn lemmings at a set spawn rate and of the chosen lemming type.
        """
        self.spawn_timer += 1

        # If the spawn counter reaches provided threshold then spawn a lemming and reset the counter
        if self.spawn_timer == spawn_rate and self.spawn_counter < spawn_number:
            lemmings.append(lem_type(self.rect.x, self.rect.y))
            self.spawn_counter += 1
            self.spawn_timer = 0


class Exit (Floor):
    def __init__(self, position_x, position_y, length_x=None, length_y=None, img=OBJECT_GRAPHICS_EXIT):
        """
        Calls the constructor of the parent class (Floor) with an image representing an entrance.
        Additionally we set a counter for how many lemmings made it to that exit
        """
        super(self.__class__, self).__init__(position_x, position_y, length_x, length_y, img)

        # Counts how many lemmings left through that exit
        self.lemming_exit_number = 0


class Water (Floor):
    def __init__(self, position_x, position_y, length_x=None, length_y=None, img=OBJECT_GRAPHICS_WATER):
        """
        Calls the constructor of the parent class (Floor) with an image representing a water.
        """
        super(self.__class__, self).__init__(position_x, position_y, length_x, length_y, img)


class MenuButton (Floor):
    """
    Class representing
    """
    def __init__(self, position_x, position_y, img, action_arg, text_arg, text_font_arg, text_color_arg,
                 length_x=None, length_y=None):
        """
        Calls the constructor from parent class (Floor) with a selected image.
        """
        super(self.__class__, self).__init__(position_x, position_y, length_x, length_y, img)

        # Saving the text
        self.text = text_font_arg.render(text_arg, False, text_color_arg)

        # self.text.rect = self.text.get_rect(x=int((self.rect.width-self.text.get_rect().width)/2), y=self.rect.y)

        self.text_rect = self.text.get_rect(center=(self.rect.x+self.rect.width/2, self.rect.y+self.rect.height/2))

        # Types like: start, load, save, exit etc.
        self.action = action_arg
