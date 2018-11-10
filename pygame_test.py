from classes import *
import sys
import pygame
pygame.init()

size = width, height = 320, 240
black = 0, 0, 0
screen = pygame.display.set_mode(size)

lem1 = Lemming(20, 20)
lem2 = Lemming(150, 84, -1)
lemmings = [lem1, lem2]
walls = [Wall(250, 0), Wall(250, 64)]


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for lem in lemmings:
        for wall in walls:
            if lem.rect.colliderect(wall.rect):
                lem.collision()
                break   # break is necessary to avoid double collision resulting in going through walls

    # X-axis boundary check
    for lem in lemmings:
        if lem.rect.left < 0 or lem.rect.right > width:
            lem.collision()

    # Moving each lemming
    for lem in lemmings:
        lem.move()


    # Filling background
    screen.fill(black)
    # Displaying all lemmings
    for lem in lemmings:
        screen.blit(lem.image, lem.rect)
    # Displaying all walls
    # for wall in walls:
    #     screen.blit(wall.image, wall.rect)
    test1 = pygame.transform.rotate(walls[0].image, 30)
    test2 = test1.get_rect(x=walls[0].rect.x, y=walls[0].rect.y)
    screen.blit(test1, test2)
    screen.blit(walls[1].image, walls[1].rect)
    pygame.display.flip()
