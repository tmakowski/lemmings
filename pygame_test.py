from classes import *
from global_variables import *
import sys
import time
# import pygame

# Initialization
pygame.init()

# Defining screen
screen = pygame.display.set_mode(SIZE)

# Testing only: initializing objects
lemmings = [Lemming(20, 20), Lemming(150, 84)]
walls = [Wall(250, 0), Wall(250, 64)]
floors = [Floor(100, 300, 7), Floor(0, 200), Floor(0, 100, 5)]

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
    for obj in lemmings+walls+floors:
        screen.blit(obj.image, obj.rect)

    # Changing display to show drawn objects
    pygame.display.flip()

# System stuff
    # Setting custom pause between frames
    time.sleep(FRAME_TIME)
