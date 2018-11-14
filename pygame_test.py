from itertools import chain
import pygame
import sys
import time

from classes.lemmings import Lemming
from level_generator import generate_level
from global_variables import BLOCK_SIZE,\
    LEVEL_SIZE, LEVEL_DEATH_FRAMES, LEVEL_FRAME_TIME


level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WS     W           W",
    "W      W           W",
    "WFFFFF W           W",
    "W      W           W",
    "WF FFFFF           W",
    "W                  W",
    "W                  W",
    "WFFFFFF            W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "W                  W",
    "WFFFFFFFFFFFFFFFFFFW"]


# Level startup
pygame.init()
screen = pygame.display.set_mode(LEVEL_SIZE)    # setting screen of the globally set size
objects_dictionarized = generate_level(level)   # generating objects based on the level visualization
lemmings = []
lemmings_spawn_number = 5
lemmings_spawn_rate = 100
# Testing only: initializing objects
# lemmings = [Lemming(BLOCK_SIZE, BLOCK_SIZE)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

# Spawning lemmings
    for obj_entrance in objects_dictionarized["Entrance"]:
        obj_entrance.spawn(lemmings, spawn_rate=lemmings_spawn_rate, spawn_number=lemmings_spawn_number)

# Performing actions for each lemming
    for lem in lemmings:

        # Check if the lemming is dead
        if lem.dead > 0:

            # Deleting the lemming after it's dead version has been displayed long enough
            if lem.dead > LEVEL_DEATH_FRAMES:
                lemmings.remove(lem)

            # Increasing the dead-lemming frame counter
            lem.dead += 1
            continue

        # Colliding the lemming with each type of objects
        lem.collision(objects_dictionarized)

        # Moving the lemming
        lem.move()


# Drawing the frame
    # Filling background
    screen.fill((0, 0, 0))

    # Drawing lemmings and all objects
    for obj in lemmings+list(chain.from_iterable(objects_dictionarized.values())):
        screen.blit(obj.image, obj.rect)

    # Changing display to show drawn objects
    pygame.display.flip()


# System stuff
    # Setting custom pause between frames
    time.sleep(LEVEL_FRAME_TIME)
