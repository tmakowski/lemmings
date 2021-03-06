#
BLOCK_DEFAULT_SIZE = 32

#
LEVEL_WIDTH = 54    # value in blocks
LEVEL_SIZE = (int(BLOCK_DEFAULT_SIZE * LEVEL_WIDTH), int(0.5 * BLOCK_DEFAULT_SIZE * LEVEL_WIDTH))
LEVEL_DEATH_FRAMES = 30
LEVEL_FRAME_TIME = 0.0001

#
LEMMING_FALL_THRESHOLD = 5
LEMMING_DEFAULT_SPEED = 1
LEMMING_GRAPHICS_DEFAULT = "graphics/lemming.png"
LEMMING_GRAPHICS_DEAD = "graphics/lemming_dead.png"
LEMMING_GRAPHICS_STOPPER = "graphics/lemming_stopper.png"
LEMMING_GRAPHICS_ANTIGRAVITY = "graphics/lemming_antigravity.png"

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
SOUND_VICTORY = "sound/victory.mp3"
SOUND_DEFEAT = "sound/defeat.ogg"
SOUND_MENU = "sound/menu_theme.mp3"

#
SAVE_PATH = "./saves/save"
SAVE_LEMMINGS = "lemmings.txt"
SAVE_OBJECTS = "objects.txt"
SAVE_STATS = "stats.txt"

LEVEL_PATH = "./levels/level"
LEVEL_LAYOUT = "level.txt"
LEVEL_BACKGROUND_COLOR = (46, 49, 49)
LEVEL_TEXT_COLOR = (245, 229, 27)

INTERFACE_LEVEL_BAR = "graphics/level_bar.png"
INTERFACE_LEVEL_EXIT = "graphics/level_exit.png"
INTERFACE_LEVEL_SAVE = "graphics/level_save_"
INTERFACE_LEVEL_PAUSE = "graphics/level_pause.png"
INTERFACE_BUTTONS = "graphics/level_bar.png"
INTERFACE_DEFAULT_SIZE = (480, 600)
INTERFACE_TEXT_COLOR = (245, 229, 27)
INTERFACE_BACKGROUND_COLOR = (56, 59, 59)
