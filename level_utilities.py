"""
The purpose of this module is translating text visualization of the map to the proper objects.
"""
import classes.objects
from classes.lemmings import Lemming
from global_variables import BLOCK_SIZE, OBJECT_DICT

code_to_class_dict = dict([
    (code, getattr(classes.objects, class_name))
    for (code, class_name)
    in OBJECT_DICT.items()
])


def level_generate(level_layout):
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


def level_import_layout(file_name, path="./"):
    """
    Function reads layout from file and returns a list with one layout line per element.
    """
    layout = []
    with open(path+file_name, "r") as f:
        for line in f:
            layout.append(line.strip())
    return layout


def level_load_lemmings(file_name, path="./"):
    """
    Function creates list of lemmings based on a file provided
    """
    lemmings = []
    with open(path+file_name, "r") as f:
        for line in f:
            # Reading the line as a list
            lem_input = eval(line.encode('utf-8'))

            # Reading the attributes
            class_name = lem_input[0]
            position_x, position_y = lem_input[1]
            attribute_dict = eval(lem_input[2])

            # Creating output lemming
            lem_output = Lemming(position_x=position_x, position_y=position_y, attribute_dict=attribute_dict)

            # Either adding the lemming to a pool or converting it to a specific type first
            if class_name == "Lemming":
                lemmings.append(lem_output)
            else:
                lemmings.append(getattr(classes.lemmings, class_name)(lemming_arg=lem_output))
    return lemmings

def level_load_objects(file_name, path="./"):
    """
    Function creates list of objects based on file input (at the end we sort objects to dictionary).
    """
    objects = []
    with open(path+file_name, "r") as f:
        for line in f:
            # Reading the line as a list
            obj_input = eval(line.encode('utf-8'))

            # Reading the attributes
            class_name = obj_input[0]
            position_x, position_y = obj_input[1]
            attribute_dict = eval(obj_input[2])

            # Creating output lemming
            objects.append(
                getattr(classes.objects, class_name)
                (position_x=position_x, position_y=position_y, attribute_dict=attribute_dict))

    return objects
