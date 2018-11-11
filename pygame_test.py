from classes import *
import sys
import time
# import pygame
pygame.init()

size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)

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

    # Filling background
    screen.fill(black)
    # Drawing objects
    for obj in lemmings+walls+floors:
        screen.blit(obj.image, obj.rect)
    # Changing display to show drawn objects
    pygame.display.flip()
    time.sleep(0.005)
