"""
The purpose of this module is translating text visualization of the map to the proper objects.
"""
import pygame
import classes.objects
from classes.lemmings import Lemming
from global_variables import OBJECT_DICT, SAVE_PATH, SAVE_LEMMINGS, SAVE_OBJECTS, SAVE_STATS, LEVEL_PATH, LEVEL_LAYOUT, \
    CLASS_TO_GRAPHICS_DICT, INTERFACE_LEVEL_BAR, INTERFACE_LEVEL_EXIT, INTERFACE_LEVEL_SAVE, INTERFACE_LEVEL_PAUSE

code_to_class_dict = dict([
    (code, getattr(classes.objects, class_name))
    for (code, class_name)
    in OBJECT_DICT.items()
])


def level_generate(level_layout, block_size):
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
            objects.append(code_to_class_dict[code](block_size * offset_x, block_size * offset_y, block_size=block_size))

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
    objects_dictionarized["Stoppers"] = []
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


def level_load_lemmings(file_name, block_size, objects_dictionarized, stats=None, path="./"):
    """
    Function creates list of lemmings based on a file provided
    """
    lemmings = []
    block_size_scaling = 1 if stats is None else block_size / stats["Block_size"]
    with open(path + file_name, "r") as f:
        for line in f:
            # Reading the line as a list
            lem_input = eval(line.encode('utf-8'))

            # Reading the attributes
            class_name = lem_input[0]
            position_x, position_y = lem_input[1]
            attribute_dict = eval(lem_input[2])

            # Creating output lemming
            lem_output = Lemming(position_x=int(position_x * block_size_scaling),
                                 position_y=int(position_y * block_size_scaling),
                                 block_size=block_size, attribute_dict=attribute_dict)

            # Either adding the lemming to a pool or converting it to a specific type first
            if class_name == "Lemming":
                lemmings.append(lem_output)
            else:
                lemmings.append(getattr(classes.lemmings, class_name)
                                (lemming_arg=lem_output, objects_dictionarized=objects_dictionarized,
                                 attribute_dict=attribute_dict))
    return lemmings


def level_load_objects(file_name, block_size, stats=None, path="./"):
    """
    Function creates list of objects based on file input (at the end we sort objects to dictionary).
    """
    objects = []
    block_size_scaling = 1 if stats is None else block_size/stats["Block_size"]
    with open(path + file_name, "r") as f:
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
                (position_x=int(position_x * block_size_scaling),
                 position_y=int(position_y * block_size_scaling),
                 block_size=block_size, attribute_dict=attribute_dict))

    return sort_objects_to_dict(objects)


def level_load_stats(file_name, path="./"):
    stats = ""
    with open(path + file_name, "r") as f:
        # stats = eval(f.readline().encode('utf-8'))
        for line in f:
            stats += line.rstrip()
        stats = eval(stats.encode('utf-8'))
    return stats


def level_load_save(save_slot, new_block_size=None, path=None):
    """
    Loads objects and lemmings from files
    """
    if path is None:
        path = SAVE_PATH + str(save_slot) + "/"

    stats = level_load_stats(SAVE_STATS, path)

    block_size = stats["Block_size"] if new_block_size is None else new_block_size
    objects_dictionarized = level_load_objects(SAVE_OBJECTS, block_size, stats, path)

    lemmings = level_load_lemmings(SAVE_LEMMINGS, block_size, objects_dictionarized, stats, path)

    objects_dictionarized, stats, interface = level_interface(stats, objects_dictionarized, block_size)

    return lemmings, objects_dictionarized, stats, interface


def level_save(save_slot, lemmings, objects_dictionarized, stats, screen, path=None):
    if path is None:
        path = SAVE_PATH + str(save_slot) + "/"

    with open(path + SAVE_OBJECTS, "w") as f:
        for obj_type in [value for (key, value) in objects_dictionarized.items() if key != "Stoppers"]:
            for obj in obj_type:
                print(obj, file=f)

    with open(path + SAVE_LEMMINGS, "w") as f:
        for lem in lemmings:
            print(lem, file=f)

    with open(path + SAVE_STATS, "w") as f:
        print(stats, file=f)

    pygame.image.save(screen, path + "frame.png")


def level_interface(stats, objects_dictionarized, block_size):
    # block_size = stats["Block_size"] if new_block_size is None else new_block_size
    ui_height = stats["Ui_height"]
    level_width = stats["Level_width"]
    ui_start = (0.5 * level_width - ui_height) * block_size
    stats["Level_size"] = (int(block_size * level_width), int(0.5 * block_size * level_width))

    objects_dictionarized["MenuButtons"] = [
        classes.objects.LevelInterfaceButton(position_x=(level_width - ui_height) * block_size,
                                             position_y=ui_start,
                                             block_size=block_size,
                                             length_x=ui_height, length_y=ui_height,
                                             img=INTERFACE_LEVEL_EXIT),
        classes.objects.LevelInterfaceButton(position_x=(level_width - 6 * ui_height) * block_size,
                                             position_y=ui_start,
                                             block_size=block_size,
                                             length_x=ui_height, length_y=ui_height,
                                             img=INTERFACE_LEVEL_PAUSE)
    ]

    for i in [1, 2, 3]:
        objects_dictionarized["MenuButtons"].append(
            classes.objects.LevelInterfaceButton(position_x=(level_width - (1 + i * 1.25) * ui_height) * block_size,
                                                 position_y=ui_start,
                                                 block_size=block_size,
                                                 length_x=ui_height, length_y=ui_height,
                                                 img=INTERFACE_LEVEL_SAVE))

    objects_dictionarized["MenuButtons"].append(classes.objects.LevelInterfaceButton(position_x=0,
                                                position_y=(ui_start - block_size),
                                                 block_size=block_size,
                                                 length_x=level_width, length_y=1,
                                                 img=INTERFACE_LEVEL_BAR))

    offset_x = 0
    objects_dictionarized["Buttons"] = []
    for (class_name, charges) in stats["Class_list"].items():
        objects_dictionarized["Buttons"].append(
            classes.objects.LevelInterfaceButton(position_x=offset_x * (ui_height + 0.5) * block_size,
                                                 position_y=ui_start, block_size=block_size,
                                                 length_x=ui_height, length_y=ui_height,
                                                 class_name_arg=class_name,
                                                 img2=CLASS_TO_GRAPHICS_DICT[class_name]))
        offset_x += 1

    interface = {
        "Clock": pygame.time.Clock(),
        "Clock_position": (block_size, ui_start - 0.8 * block_size),
        "Time_left": "Time left: "}
    return objects_dictionarized, stats, interface


def level_create(level_slot, new_block_size=None, path=None):
    if path is None:
        path = LEVEL_PATH + str(level_slot) + "/"

    stats = level_load_stats(SAVE_STATS, path)

    level = level_import_layout(path + LEVEL_LAYOUT)
    block_size = stats["Block_size"] if new_block_size is None else new_block_size
    objects_dictionarized = level_generate(level, block_size)

    lemmings = []

    objects_dictionarized, stats, interface = level_interface(stats, objects_dictionarized, block_size)

    return lemmings, objects_dictionarized, stats, interface
