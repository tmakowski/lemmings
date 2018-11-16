"""
The purpose of this module is translating text visualization of the map to the proper objects.
"""
import classes.objects
from classes.lemmings import Lemming
from global_variables import OBJECT_DICT, SAVE_PATH, SAVE_LEMMINGS, SAVE_OBJECTS, SAVE_STATS, LEVEL_PATH, LEVEL_LAYOUT,\
    INTERFACE_BAR, CLASS_TO_GRAPHICS_DICT

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


def level_load_lemmings(file_name, block_size, objects_dictionarized, path="./"):
    """
    Function creates list of lemmings based on a file provided
    """
    lemmings = []
    with open(path + file_name, "r") as f:
        for line in f:
            # Reading the line as a list
            lem_input = eval(line.encode('utf-8'))

            # Reading the attributes
            class_name = lem_input[0]
            position_x, position_y = lem_input[1]
            attribute_dict = eval(lem_input[2])

            # Creating output lemming
            lem_output = Lemming(position_x=position_x, position_y=position_y,
                                 block_size=block_size, attribute_dict=attribute_dict)

            # Either adding the lemming to a pool or converting it to a specific type first
            if class_name == "Lemming":
                lemmings.append(lem_output)
            else:
                lemmings.append(getattr(classes.lemmings, class_name)
                                (lemming_arg=lem_output, objects_dictionarized=objects_dictionarized,
                                 attribute_dict=attribute_dict))
    return lemmings


def level_load_objects(file_name, block_size, path="./"):
    """
    Function creates list of objects based on file input (at the end we sort objects to dictionary).
    """
    objects = []
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
                (position_x=position_x, position_y=position_y, block_size=block_size, attribute_dict=attribute_dict))

    return sort_objects_to_dict(objects)


def level_load_stats(file_name, path="./"):
    with open(path + file_name, "r") as f:
        stats = eval(f.readline().encode('utf-8'))

    return stats


def level_load_save(save_slot, path=None):
    """
    Loads objects and lemmings from files
    """
    if path is None:
        path = SAVE_PATH + str(save_slot) + "/"

    stats = level_load_stats(SAVE_STATS, path)

    block_size = stats["Block_size"]
    objects_dictionarized = level_load_objects(SAVE_OBJECTS, block_size, path)
    lemmings = level_load_lemmings(SAVE_LEMMINGS, block_size, objects_dictionarized, path)

    objects_dictionarized = level_interface(stats, objects_dictionarized)

    return lemmings, objects_dictionarized, stats


def level_save(save_slot, lemmings, objects_dictionarized, stats, path=None):
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


def level_interface(stats, objects_dictionarized):
    block_size = stats["Block_size"]
    ui_height = stats["Ui_height"]
    ui_start = (0.5 * stats["Level_width"] - ui_height) * block_size

    objects_dictionarized["Buttons"] = [
        classes.objects.LevelInterfaceButton(position_x=0, position_y=(ui_start - block_size),
                                             block_size=block_size, img=INTERFACE_BAR,
                                             length_x=stats["Level_width"], length_y=1)]

    offset_x = 0
    for class_name in stats["Class_list"]:
        objects_dictionarized["Buttons"].append(
            classes.objects.LevelInterfaceButton(position_x=offset_x * ui_height * (block_size + 1),
                                                 position_y=ui_start, block_size=block_size,
                                                 length_x=ui_height, length_y=ui_height, class_name_arg=class_name,
                                                 img2=CLASS_TO_GRAPHICS_DICT[class_name]))
        offset_x += 1
    return objects_dictionarized


def level_create(level_slot, path=None):
    if path is None:
        path = LEVEL_PATH + str(level_slot) + "/"

    level = level_import_layout(path + LEVEL_LAYOUT)

    stats = level_load_stats(SAVE_STATS, path)
    objects_dictionarized = level_generate(level, stats["Block_size"])
    lemmings = []

    objects_dictionarized = level_interface(stats, objects_dictionarized)

    return lemmings, objects_dictionarized, stats
