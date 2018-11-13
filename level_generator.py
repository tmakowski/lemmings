"""
The purpose of this module is translating text visualization of the map to the proper objects.
"""
from classes.objects import *
from global_variables import *


DICT_CODE_TO_OBJ = {"W": Wall, "F": Floor}


def generate_level(level_layout):
    # Variables initialization
    objects = []
    offset_y = 0
    for line in level_layout:
        # Variable used to place objects correctly
        offset_x = -1
        for code in line:
            # Increasing the offset from the edge
            offset_x += 1

            # Skipping the code if it represents empty space
            if code == " ":
                continue

            # Creating the objects
            objects.append(DICT_CODE_TO_OBJ[code](BLOCK_SIZE * offset_x, BLOCK_SIZE * offset_y))

        # Moving to the next line
        offset_y += 1
    return objects
