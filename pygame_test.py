from classes import *
import sys
import time
# import pygame

# Initialization
pygame.init()

# Defining size and screen
size = width, height = 320, 240
screen = pygame.display.set_mode(size)

# Testing only: initializing objects
lemmings = [Lemming(20, 20), Lemming(150, 84)]
walls = [Wall(250, 0), Wall(250, 64)]
floors = [Floor(0, 200), Floor(100, 200), Floor(0, 200), Floor(0,100)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Lemming exit check

    # Moving each lemming
    for lem in lemmings:
        lem.collision_walls(walls)
        lem.collision_floors(floors)

        if lem.dead == 1:
            lemmings.remove(lem)
            break

        ### To be removed:
        if lem.rect.left < 0 or lem.rect.right > width:
            lem.dirX *= -1
        ######
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
    time.sleep(0.005)
