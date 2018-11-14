import pygame
import sys
import time

from classes.lemmings import Lemming
from level_generator import generate_level
from global_variables import BLOCK_SIZE,\
    LEVEL_SIZE, LEVEL_DEATH_FRAMES, LEVEL_FRAME_TIME


level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W      W           W",
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
dict_objects = generate_level(level)            # generating objects based on the level visualization

# Testing only: initializing objects
lemmings = [Lemming(BLOCK_SIZE, BLOCK_SIZE)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

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
        lem.collision(dict_objects)

        # Moving the lemming
        lem.move()


# Drawing the frame
    # Filling background
    screen.fill((0, 0, 0))

    # Drawing all objects
    for obj in lemmings+dict_objects.values():
        screen.blit(obj.image, obj.rect)

    # Changing display to show drawn objects
    pygame.display.flip()


# System stuff
    # Setting custom pause between frames
    time.sleep(LEVEL_FRAME_TIME)
