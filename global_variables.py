#
BLOCK_SIZE = 32

#
LEVEL_WIDTH = 20    # value in blocks
LEVEL_SIZE = (int(BLOCK_SIZE * LEVEL_WIDTH), int(0.75 * BLOCK_SIZE * LEVEL_WIDTH))
LEVEL_DEATH_FRAMES = 30
LEVEL_FRAME_TIME = 0.005

#
LEMMING_FALL_THRESHOLD = 5
LEMMING_DEFAULT_SPEED = 1
LEMMING_GRAPHICS_DEFAULT = "graphics/lemming2.png"
LEMMING_GRAPHICS_DEAD = "graphics/lemming_dead.png"

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
