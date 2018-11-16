#
BLOCK_DEFAULT_SIZE = 32

#
LEVEL_WIDTH = 54    # value in blocks
LEVEL_SIZE = (int(BLOCK_DEFAULT_SIZE * LEVEL_WIDTH), int(0.5 * BLOCK_DEFAULT_SIZE * LEVEL_WIDTH))
LEVEL_DEATH_FRAMES = 30
LEVEL_FRAME_TIME = 0.005

#
LEMMING_FALL_THRESHOLD = 5
LEMMING_DEFAULT_SPEED = 1
LEMMING_GRAPHICS_DEFAULT = "graphics/lemming2.png"
LEMMING_GRAPHICS_DEAD = "graphics/lemming_dead.png"
LEMMING_GRAPHICS_STOPPER = "graphics/lemming_stopper.png"
LEMMING_GRAPHICS_ANTIGRAVITY = "graphics/exit.png"

#
OBJECT_DICT = {"F": "Floor",
               "W": "Wall",
               "S": "Entrance",
               "E": "Exit",
               "w": "Water"}
OBJECT_GRAPHICS_FLOOR = "graphics/floor.png"
OBJECT_GRAPHICS_WALL = "graphics/wall.png"
OBJECT_GRAPHICS_ENTRANCE = "graphics/entrance.png"
OBJECT_GRAPHICS_EXIT = "graphics/exit.png"
OBJECT_GRAPHICS_WATER = "graphics/water.png"

CLASS_TO_GRAPHICS_DICT = {
    "LemmingStopper": LEMMING_GRAPHICS_STOPPER,
    "LemmingAntiGravity": LEMMING_GRAPHICS_ANTIGRAVITY}

#
SAVE_PATH = "./saves/save"
SAVE_LEMMINGS = "lemmings.txt"
SAVE_OBJECTS = "objects.txt"
SAVE_STATS = "stats.txt"

LEVEL_PATH = "./levels/level"
LEVEL_LAYOUT = "level.txt"

INTERFACE_BAR = "graphics/exit.png"
INTERFACE_BUTTONS = "graphics/water.png"
INTERFACE_DEFAULT_SIZE = (480, 960)
INTERFACE_TEXT_COLOR = (250, 100, 6)
