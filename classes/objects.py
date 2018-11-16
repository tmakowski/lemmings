import pygame

from classes.lemmings import Lemming
from global_variables import \
    OBJECT_GRAPHICS_FLOOR, OBJECT_GRAPHICS_WALL, OBJECT_GRAPHICS_ENTRANCE, OBJECT_GRAPHICS_EXIT, OBJECT_GRAPHICS_WATER,\
    INTERFACE_BUTTONS


class Floor:
    """
    Parent class for all objects' classes.
    """
    def __init__(self, position_x, position_y, block_size, length_x=None, length_y=None,
                 img=OBJECT_GRAPHICS_FLOOR,
                 attribute_dict=None):
        """
        Creates new floor at position (x, y) that can be stretched by providing length_x/_y factors.
        """
        if attribute_dict is None:
            # Values for scaling
            self.length_x = 1 if length_x is None else length_x
            self.length_y = 1 if length_y is None else length_y

            # Scaling and loading the image
            self.image_name = img
            self.image = pygame.transform.scale(
                            pygame.image.load(self.image_name),
                            (int(block_size * self.length_x), int(block_size * self.length_y)))

            # Creating the hitbox
            self.rect = self.image.get_rect(x=position_x, y=position_y)

        # Used during reading from file
        else:
            for (attr, value) in attribute_dict.items():
                setattr(self, attr, value)
            self.image = pygame.transform.scale(
                    pygame.image.load(self.image_name),
                    (block_size * self.length_x, block_size * self.length_y))
            self.rect = self.image.get_rect(x=position_x, y=position_y)

    def __dir__(self):
        """
        Floors' and it derivatives attributes.
        """
        return ["image_name", "length_x", "length_y"]

    def __str__(self):
        """
        Prints a list of [class, dictionary] where the dictionary contains each attribute and it's value.
        """
        attribute_dict = {}
        for attr in self.__dir__():
            attribute_dict[attr] = getattr(self, attr)
        return [self.__class__.__name__, (self.rect.x, self.rect.y), attribute_dict.__str__()].__str__()


class Wall (Floor):
    """
    Subclass representing the walls.
    """
    def __init__(self, position_x, position_y, block_size, length_x=None, length_y=None,
                 img=OBJECT_GRAPHICS_WALL,
                 attribute_dict=None):
        """
        Calls the constructor from parent class (Floor) with an image representing a wall.
        """
        super(self.__class__, self).__init__(position_x, position_y, block_size,
                                             length_x, length_y, img, attribute_dict)


class Entrance (Floor):
    """
    Subclass representing the level entrance.
    """
    def __init__(self, position_x, position_y, block_size, length_x=None, length_y=None,
                 img=OBJECT_GRAPHICS_ENTRANCE,
                 attribute_dict=None):
        """
        Calls the constructor of the parent class (Floor) with an image representing an entrance.
        Additionally we set a timer and counter variables used during lemmings' spawning.
        """
        super(self.__class__, self).__init__(position_x, position_y, block_size,
                                             length_x, length_y, img, attribute_dict)
        if attribute_dict is None:
            # Used to count frames between next lemmings spawns
            self.spawn_timer = 0

            # Counts how many lemmings were spawned
            self.spawn_counter = 0

    def __dir__(self):
        """
        Exit's attributes.
        """
        return ["image_name", "length_x", "length_y", "spawn_timer", "spawn_counter"]

    def spawn(self, lemmings, spawn_rate, spawn_number, lem_type=Lemming):
        """
        Method used to spawn lemmings at a set spawn rate and of the chosen lemming type.
        """
        self.spawn_timer += 1

        # If the spawn counter reaches provided threshold then spawn a lemming and reset the counter
        if self.spawn_timer == spawn_rate and self.spawn_counter < spawn_number:
            lemmings.append(lem_type(self.rect.x, self.rect.y, block_size=self.image.get_rect().height))
            self.spawn_counter += 1
            self.spawn_timer = 0


class Exit (Floor):
    def __init__(self, position_x, position_y, block_size, length_x=None, length_y=None,
                 img=OBJECT_GRAPHICS_EXIT,
                 attribute_dict=None):
        """
        Calls the constructor of the parent class (Floor) with an image representing an entrance.
        Additionally we set a counter for how many lemmings made it to that exit
        """
        super(self.__class__, self).__init__(position_x, position_y, block_size,
                                             length_x, length_y, img, attribute_dict)
        if attribute_dict is None:
            # Counts how many lemmings left through that exit
            self.lemming_exit_number = 0

    def __dir__(self):
        """
        Exit's attributes.
        """
        return ["image_name", "length_x", "length_y", "lemming_exit_number"]


class Water (Floor):
    def __init__(self, position_x, position_y, block_size, length_x=None, length_y=None,
                 img=OBJECT_GRAPHICS_WATER,
                 attribute_dict=None):
        """
        Calls the constructor of the parent class (Floor) with an image representing a water.
        """
        super(self.__class__, self).__init__(position_x, position_y, block_size,
                                             length_x, length_y, img, attribute_dict)


class MenuButton (Floor):
    """
    Class representing
    """
    def __init__(self, position_x, position_y, block_size, img, text_arg, text_font_arg, text_color_arg,
                 length_x=None, length_y=None):
        """
        Calls the constructor from parent class (Floor) with a selected image.
        """
        super(self.__class__, self).__init__(position_x, position_y, block_size, length_x, length_y, img)

        # Saving the text
        self.text = text_font_arg.render(text_arg, True, text_color_arg)

        # Text's rectangle centered in the button's rectangle
        self.text_rect = self.text.get_rect(center=(self.rect.x + self.rect.width/2,
                                                    self.rect.y + self.rect.height/2))

    def center(self, width):
        """
        Aligns the button to the center of a window.
        """
        self.rect.x = (width - self.rect.width)/2
        self.text_rect.x = (width - self.text_rect.width)/2
        return self


class LevelInterfaceButton (Floor):
    def __init__(self, position_x, position_y, block_size, length_x=None, length_y=None,
                 img=INTERFACE_BUTTONS, img2=None,
                 class_name_arg=None,
                 attribute_dict=None):
        super(self.__class__, self).__init__(position_x, position_y, block_size,
                                             length_x, length_y, img, attribute_dict)

        self.class_name = class_name_arg

        self.image_name2 = img if img2 is None else img2
        self.image2 = pygame.transform.scale(
            pygame.image.load(self.image_name2),
            (int(0.75 * block_size * self.length_x), int(0.75 * block_size * self.length_y)))

        self.rect2 = self.image2.get_rect(center=(self.rect.x + 0.5 * self.image.get_rect().width,
                                                  self.rect.y + 0.5 * self.image.get_rect().height))

    def __dir__(self):
        return ["image_name", "length_x", "length_y", "class_name", "image_name2"]

    def charges_to_text(self, stats, text_font_arg, text_color_arg):
        if self.class_name is None:
            charges = ""
        else:
            charges = stats["Class_list"][self.class_name]

        text_ = text_font_arg.render(str(charges), True, text_color_arg)
        text_rect = text_.get_rect(center=(self.rect.x + self.rect.width / 2,
                                           self.rect.y + self.rect.height / 2))
        return text_, text_rect


class TextBox:
    def __init__(self, position_x, position_y, text_arg, text_font_arg, text_color_arg):
        self.text = text_font_arg.render(text_arg, True, text_color_arg)
        self.rect = self.text.get_rect(x=position_x, y=position_y)

    def center(self, width):
        """
        Aligns the button to the center of a window.
        """
        self.rect.x = (width - self.rect.width)/2
        return self
