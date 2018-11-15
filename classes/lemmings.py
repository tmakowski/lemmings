"""
File containing main lemming class and it's subclasses.
"""
import pygame

from global_variables import BLOCK_SIZE,\
    LEMMING_DEFAULT_SPEED, LEMMING_FALL_THRESHOLD,\
    LEMMING_GRAPHICS_DEFAULT, LEMMING_GRAPHICS_DEAD, LEMMINGS_GRAPHICS_STOPPER


class Lemming:
    """
    This is a main lemming class which represents a lemming with no special abilities
    """
    def __init__(self, position_x, position_y, img=LEMMING_GRAPHICS_DEFAULT,
                 direction_x=1, direction_y=1, fall_arg=0,
                 dead_arg=0, remove_arg=0,
                 speed_arg=LEMMING_DEFAULT_SPEED):
        """
        Creates new lemming at position (x, y) counting from top left corner of the map with selected graphics.
        """
        # Assigning the image to the lemming
        self.image = pygame.transform.scale(
                        pygame.image.load(img),
                        (BLOCK_SIZE, BLOCK_SIZE))

        # Creating the hitbox
        self.rect = self.image.get_rect(x=position_x, y=position_y)

        # Setting movement direction for the lemming
        self.dirX = direction_x
        self.dirY = direction_y

        # Fall counter
        self.fall = fall_arg

        # Death & removal flags
        self.dead = dead_arg
        self.remove = remove_arg

        # Speed (added for later use)
        self.speed = speed_arg

    def __del__(self, img=LEMMING_GRAPHICS_DEAD):
        """
        Lemming destructor... or lemming killer? Whatever. You get the point.
        """
        # Changing image to the dead version
        self.image = pygame.transform.scale(
                        pygame.image.load(img),
                        (BLOCK_SIZE, BLOCK_SIZE))

        # Stopping the lemming's movement (so that we can display it's dead version for a while)
        self.speed = 0

        # Delivering the sad news:
        self.dead = 1
        return None

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
            if key in ["Wall", "Floor"]:
                continue

            method = getattr(self, "collision_" + key.lower())
            method(dict_objects[key])

        # Treating walls as a floors to avoid some shenanigans (we want lemmings to step off of the top of the walls)
        self.collision_floor(dict_objects["Wall"]+dict_objects["Floor"])

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
            if self.fall > LEMMING_FALL_THRESHOLD * BLOCK_SIZE:
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


class LemmingStopper (Lemming):
    """
    # This extended class is going to represent the lemming with a stopper function.
    """
    def __init__(self, lemming, img=LEMMINGS_GRAPHICS_STOPPER):
        """
        This constructor creates a stopper lemming in place of the other
        """
        super(self.__class__, self).__init__(position_x=lemming.rect.x, position_y=lemming.rect.y, img=img,
                                             direction_x=lemming.dirX, direction_y=lemming.dirY, fall_arg=lemming.fall,
                                             dead_arg=lemming.dead, remove_arg=lemming.remove,
                                             speed_arg=0)
        lemming.remove = 1

    def collision_lemmings(self, lemmings):
        for lem in lemmings:
            if self.rect.colliderect(lem.rect):
                lem.dirX *= -1
