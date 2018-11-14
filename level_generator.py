"""
The purpose of this module is translating text visualization of the map to the proper objects.
"""
import classes.objects
from global_variables import BLOCK_SIZE, OBJECT_DICT

code_to_class_dict = dict([
    (code, getattr(classes.objects, class_name))
    for (code, class_name)
    in zip(OBJECT_DICT.keys(), OBJECT_DICT.values())
])


def generate_level(level_layout):
    """
    This function creates objects used in the level based in visualization of the level layout.
    """
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
            objects.append(code_to_class_dict[code](BLOCK_SIZE * offset_x, BLOCK_SIZE * offset_y))

        # Moving to the next line
        offset_y += 1
    return sort_objects_to_dict(objects)


def sort_objects_to_dict(objects):
    """
    This function generates dictionary for 'object name: list of objects with class' name == object name'.
    """
    objects_dictionarized = {}
    for class_name in OBJECT_DICT.values():
        objects_dictionarized[class_name] = [obj for obj in objects if obj.__class__.__name__ == class_name]
    return objects_dictionarized
