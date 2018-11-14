"""
File containing main lemming class and it's subclasses.
"""
import pygame

from global_variables import BLOCK_SIZE,\
    LEMMING_DEFAULT_SPEED, LEMMING_FALL_THRESHOLD,\
    LEMMING_GRAPHICS_DEFAULT, LEMMING_GRAPHICS_DEAD


class Lemming:
    """
    This is a main lemming class which represents a lemming with no special abilities
    """
    def __init__(self, position_x, position_y, img=LEMMING_GRAPHICS_DEFAULT):
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
        self.dirX = 1
        self.dirY = 1

        # Fall counter
        self.fall = 0

        # Death flag
        self.dead = 0

        # Speed (added for later use)
        self.speed = LEMMING_DEFAULT_SPEED

    def __del__(self):
        """
        Lemming destructor... or lemming killer? Whatever. You get the point.
        """
        # Changing image to the dead version
        self.image = pygame.transform.scale(
                        pygame.image.load(LEMMING_GRAPHICS_DEAD),
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

    def collision(self, dict_objects):
        """
        One method to rule them all! Function calls collision method for each object type in dict_objects.
        """
        for key in dict_objects.keys():
            method = getattr(self, "collision_" + key.lower())
            method(dict_objects[key])
        return self

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
        else:

            # If the lemming slipped of the floor then make it start falling
            self.dirY = 1
        return self

    def collision_entrance(self, entrance):
        pass


class LemmingStopper (Lemming):
    """
    # This extended class is going to represent the lemming with a stopper function.
    """
