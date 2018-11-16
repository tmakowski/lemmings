"""
File containing main lemming class and it's subclasses.
"""
import pygame

from global_variables import LEMMING_DEFAULT_SPEED, LEMMING_FALL_THRESHOLD,\
    LEMMING_GRAPHICS_DEFAULT, LEMMING_GRAPHICS_DEAD, LEMMING_GRAPHICS_STOPPER, LEMMING_GRAPHICS_ANTIGRAVITY


class Lemming:
    """
    This is a main lemming class which represents a lemming with no special abilities
    """
    def __init__(self, position_x, position_y, block_size, img_arg=None,
                 direction_x=None, direction_y=None, fall_arg=None,
                 dead_arg=None, remove_arg=None, speed_arg=None, unstuck_arg=None,
                 lemming_arg=None, attribute_dict=None):
        """
        Creates new lemming at position (x, y) counting from top left corner of the map with selected graphics and stats.
        """
        if lemming_arg is None and attribute_dict is None:
            # Assigning the image to the lemming
            self.image_name = LEMMING_GRAPHICS_DEFAULT if img_arg is None else img_arg
            self.image = pygame.transform.scale(
                            pygame.image.load(self.image_name),
                            (block_size, block_size))

            # Creating the hitbox
            self.rect = self.image.get_rect(x=position_x, y=position_y)

            # Setting movement direction for the lemming
            self.dirX = 1 if direction_x is None else direction_x
            self.dirY = 1 if direction_y is None else direction_y

            # Fall counter
            self.fall = 0 if fall_arg is None else fall_arg

            # Death & removal flags
            self.dead = 0 if dead_arg is None else dead_arg
            self.remove = 0 if remove_arg is None else remove_arg

            # Speed (added for later use)
            self.speed = LEMMING_DEFAULT_SPEED if speed_arg is None else speed_arg

            # Collision grace period after falling (used for stopper lemmings collisions)
            self.unstuck = 0 if unstuck_arg is None else unstuck_arg

        # If we provided lemming to base on then we take it's attributes over defaults
        elif attribute_dict is None:
            if img_arg is None:
                self.image_name = lemming_arg.image_name
                self.image = lemming_arg.image
            else:
                self.image_name = img_arg
                self.image = pygame.transform.scale(
                    pygame.image.load(self.image_name),
                    (block_size, block_size))

            self.rect = self.image.get_rect(x=position_x, y=position_y)

            self.dirX = lemming_arg.dirX if direction_x is None else direction_x
            self.dirY = lemming_arg.dirY if direction_y is None else direction_y

            self.fall = lemming_arg.fall if fall_arg is None else fall_arg

            self.dead = lemming_arg.dead if dead_arg is None else dead_arg
            self.remove = lemming_arg.remove if remove_arg is None else remove_arg

            self.speed = lemming_arg.speed if speed_arg is None else speed_arg

            self.unstuck = lemming_arg.unstuck if unstuck_arg is None else unstuck_arg

        # Creating lemming based on the attribute dictionary
        else:
            for (attr, value) in attribute_dict.items():
                setattr(self, attr, value)
            self.image = pygame.transform.scale(
                    pygame.image.load(self.image_name),
                    (block_size, block_size))
            self.rect = self.image.get_rect(x=position_x, y=position_y)

    def __del__(self, img=LEMMING_GRAPHICS_DEAD):
        """
        Lemming destructor... or lemming killer? Whatever. You get the point.
        """
        # Changing image to the dead version
        self.image = pygame.transform.scale(
                        pygame.image.load(img),
                        (self.image.get_rect().width, self.image.get_rect().height))

        # Stopping the lemming's movement (so that we can display it's dead version for a while)
        self.speed = 0

        # Delivering the sad news:
        self.dead = 1
        return None

    def __dir__(self):
        """
        Lemmings' attributes. (rect left out)
        """
        return ["image_name", "dirX", "dirY", "fall", "dead", "remove", "speed", "unstuck"]

    def __str__(self):
        """
        Prints a list of [class, dictionary] where the dictionary contains each attribute and it's value.
        """
        attribute_dict = {}
        for attr in self.__dir__():
            attribute_dict[attr] = getattr(self, attr)
        return [self.__class__.__name__, (self.rect.x, self.rect.y), attribute_dict.__str__()].__str__()

    def on_click(self, click_position, objects_dictionarized, lemmings):
        pass

    def move(self):
        """
        Function used to move lemmings in their current movement direction by their speed value.
        Note: if lemming falls then it does not move along the X-axis
        """
        if self.dirY == 0:

            # Moving the lemming in it is current X-axis direction by the block size
            self.rect.x += self.dirX * self.speed
        else:

            # Moving the lemming down if it is falling and counting for how many frames it has been falling
            self.rect.y += self.dirY * self.speed
            self.fall += self.dirY * self.speed
        return self

    def collision_lemmings(self, lemmings):
        pass

    def collision_objects(self, dict_objects):
        """
        One method to rule them all! Function calls collision method for each object type in dict_objects.
        """
        for key in dict_objects.keys():

            # Walls and floors are handled below
            if key in ["Wall", "Floor", "Stoppers", "Buttons", "MenuButtons"]:
                continue

            method = getattr(self, "collision_" + key.lower())
            method(dict_objects[key])

        # Treating walls as a floors to avoid some shenanigans (we want lemmings to step off of the top of the walls)
        self.collision_floor(dict_objects["Wall"]+dict_objects["Floor"]+dict_objects["Stoppers"])

        return self

    # Not used
    def collision_wall(self, walls):
        """
        Checks if the lemming collided with any of the walls.
        If it did then it's X-axis movement direction gets changed.
        """
        if self.rect.collidelist(walls) != -1:
            self.dirX *= -1
        return self

    def collision_floor(self, floors):
        """
        Checks if the lemming has a floor under it's feet. If it doesn't then the lemming starts to fall.
        If it is falling and touches the floor then we perform check whether the fall distance wasn't too big.
        """
        # Check if lemming is touching the floor on the floor
        if self.rect.collidelist(floors) != -1:

            # Check if the lemming has passed the fall threshold
            if self.fall > LEMMING_FALL_THRESHOLD * self.image.get_rect().height:
                self.__del__()

            # Check if it was falling at all
            elif self.fall > 0:

                # If it was falling, then stop the fall and reset the fall counter
                self.dirY = 0
                self.fall = 0

            # Colliding the lemming with the sides of the floors/walls that are not directly below him
            if self.rect.collidelist([floor for floor in floors if abs(self.rect.bottom-floor.rect.top) > 1]) != -1:
                self.dirX *= -1
        else:

            # If the lemming slipped of the floor then make it start falling
            self.dirY = 1

        return self

    def collision_entrance(self, entrances):
        pass

    def collision_exit(self, exits):
        """
        Method marks the lemming as a one that safely left through exit and increases the counter of said exit
        """
        for obj_exit in exits:
            if (self.rect.colliderect(obj_exit.rect) and
                    self.rect.left == obj_exit.rect.left and
                    self.rect.right == obj_exit.rect.right and
                    self.rect.top == obj_exit.rect.top and
                    self.rect.bottom == obj_exit.rect.bottom):
                obj_exit.lemming_exit_number += 1
                self.remove = 1
                break
        return self

    def collision_water(self, waters):
        """
        Method to kill lemmings on contact with water
        """
        for water in waters:
            if (self.rect.colliderect(water.rect) and
                    self.rect.left == water.rect.left and
                    self.rect.right == water.rect.right and
                    self.rect.top == water.rect.top and
                    self.rect.bottom == water.rect.bottom):
                self.__del__()
                break
        return self

    def boundary_check(self, level_size):
        if (self.rect.right > level_size[0] or
                self.rect.left < 0):
            self.dirX *= -1
        if (self.rect.bottom > level_size[1] or
                self.rect.top < 0):
            self.dirY *= -1


class LemmingStopper (Lemming):
    """
    # This extended class is going to represent the lemming with a stopper function.
    """
    def __init__(self, lemming_arg, objects_dictionarized, attribute_dict=None, img_arg=LEMMING_GRAPHICS_STOPPER):
        """
        This constructor creates a stopper lemming in place of the other
        """
        super(self.__class__, self).__init__(lemming_arg.rect.x, lemming_arg.rect.y,
                                             block_size=lemming_arg.image.get_rect().height,
                                             img_arg=img_arg, speed_arg=0,
                                             lemming_arg=lemming_arg, attribute_dict=attribute_dict)
        lemming_arg.remove = 1

        objects_dictionarized["Stoppers"].append(self)

    def on_click(self, click_position, objects_dictionarized, lemmings):
        if self.rect.collidepoint(click_position):
            lemmings.append(Lemming(self.rect.x, self.rect.y, self.rect.height, img_arg=LEMMING_GRAPHICS_DEFAULT,
                                    speed_arg=1, lemming_arg=self))
            objects_dictionarized["Stoppers"].remove(self)
            self.remove = 1
        return lemmings, objects_dictionarized

    def collision_lemmings(self, lemmings):
        pass

    def collision_floor(self, floors):
        super(self.__class__, self).collision_floor([obj for obj in floors if obj != self])


class LemmingAntiGravity (Lemming):
    def __init__(self, lemming_arg, objects_dictionarized, attribute_dict=None, img_arg=LEMMING_GRAPHICS_ANTIGRAVITY):
        """
        This constructor creates a stopper lemming in place of the other
        """
        super(self.__class__, self).__init__(lemming_arg.rect.x, lemming_arg.rect.y,
                                             block_size=lemming_arg.image.get_rect().height,
                                             img_arg=img_arg,
                                             lemming_arg=lemming_arg, attribute_dict=attribute_dict)
        lemming_arg.remove = 1
        self.rect.y -= 2
        self.fall -= 2

    def on_click(self, click_position, objects_dictionarized, lemmings):
        if self.rect.collidepoint(click_position):
            lemmings.append(Lemming(self.rect.x, self.rect.y+2, self.rect.height, img_arg=LEMMING_GRAPHICS_DEFAULT,
                                    fall_arg=0, lemming_arg=self))
            self.remove = 1

    def collision_floor(self, floors):
        """
        Checks if the lemming has a floor under it's feet. If it doesn't then the lemming starts to fall.
        If it is falling and touches the floor then we perform check whether the fall distance wasn't too big.
        """
        # Check if lemming is touching the floor on the floor
        if self.rect.collidelist(floors) != -1:

            # Check if the lemming has passed the fall threshold
            if -self.fall > LEMMING_FALL_THRESHOLD * self.image.get_rect().height:
                self.__del__()

            # Check if it was falling at all
            elif -self.fall > 0:

                # If it was falling, then stop the fall and reset the fall counter
                self.dirY = 0
                self.fall = 0

            # Colliding the lemming with the sides of the floors/walls that are not directly below him
            if self.rect.collidelist([floor for floor in floors if abs(self.rect.top-floor.rect.bottom) > 1]) != -1:
                self.dirX *= -1

        else:
            # If the lemming slipped of the floor then make it start falling
            self.dirY = -1

        return self
