from classes import *
from global_variables import *
import sys
import time
# import pygame

# Initialization
pygame.init()

# Defining screen
screen = pygame.display.set_mode(LEVEL_SIZE)

# Testing only: initializing objects
lemmings = [Lemming(20, 20), Lemming(150, 84)]
#walls = [Wall(250, 0, length_y=5), Wall(250+BLOCK_SIZE*1+1, 0), Wall(250+BLOCK_SIZE*1, BLOCK_SIZE*1),
#         Wall(0, 0), Wall(BLOCK_SIZE, BLOCK_SIZE), Wall(2*BLOCK_SIZE, 0)]
#floors = [Floor(100, 300, 7), Floor(0, 200), Floor(0, 100, 5)]


level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "WFFFFFFFFFFFFFFFFFFW"]
#
from level_generator import *
objects = generate_level(level)
floors = [obj for obj in objects if type(obj) == Floor]
walls = [obj for obj in objects if type(obj) == Wall]
#

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Lemming exit check

    # Moving each lemming
    for lem in lemmings:
        # Check if lemming is dead
        if lem.dead > 0:
            # If it is dead then we display it's dead version for set number of frames and remove it afterwards
            if lem.dead > LEMMING_DEATH_FRAMES:
                lemmings.remove(lem)
            lem.dead += 1
            continue

        lem.collision_walls(walls)
        lem.collision_floors(floors)

        lem.move()

# Drawing the frame
    # Filling background
    screen.fill((0, 0, 0))

    # Drawing all objects
    for obj in objects+lemmings:
        screen.blit(obj.image, obj.rect)

    # Changing display to show drawn objects
    pygame.display.flip()

# System stuff
    # Setting custom pause between frames
    time.sleep(FRAME_TIME)
