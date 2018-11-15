from itertools import chain
import pygame
import sys
import time

from level_generator import generate_level
from global_variables import BLOCK_SIZE,\
    LEVEL_SIZE, LEVEL_DEATH_FRAMES, LEVEL_FRAME_TIME


# Settings
lemmings_spawn_number = 5                       # setting number of lemmings to spawn
lemmings_spawn_rate = 100                       # setting number of frames between lemming spawns
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
    "W S W              W",
    "W FFF              W",
    "W      E           W",
    "WFFFww             W",
    "WFFFFFFFFFFFFFFFFFFW"]


# Level startup
pygame.init()
screen = pygame.display.set_mode(LEVEL_SIZE)    # setting screen of the globally set size
objects_dictionarized = generate_level(level)   # generating objects based on the level visualization
lemmings = []                                   # initializing a list for lemmings
dev_timer = 0


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

        # Checking if lemming has left via any of the exits
        if lem.exit == 1:
            lemmings.remove(lem)
            continue

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

    dev_timer += 1
    if lemmings == [] and dev_timer > lemmings_spawn_rate:
        for obj_exit in objects_dictionarized["Exit"]:
            print("Uwaga, uwaga, tyle lemingów wyszło:", obj_exit.lemming_exit_number)
        sys.exit()
