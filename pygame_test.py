from classes.lemmings import *
from classes.objects import *
import sys, pygame
pygame.init()

size = width, height = 320, 240
# speed = [2, 2]
black = 0, 0, 0

screen = pygame.display.set_mode(size)

# ball = pygame.image.load("graphics/lemming.png")
# ballrect = ball.get_rect()
lem1 = Lemming(20, 20)
lem2 = Lemming(150, 84, -1)
lemmings = [lem1, lem2]
walls = [Wall(250, 0), Wall(250, 64)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

#    ballrect = ballrect.move(speed)
#    if ballrect.left < 0 or ballrect.right > width:
#        speed[0] = -speed[0]
#    if ballrect.top < 0 or ballrect.bottom > height:
#        speed[1] = -speed[1]
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
    for wall in walls:
        screen.blit(wall.image, wall.rect)
    pygame.display.flip()
