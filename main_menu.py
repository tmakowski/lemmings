import pygame
import sys
# import time
from classes.objects import Floor, MenuButton
from global_variables import BLOCK_SIZE


pygame.init()
# pygame.font.init()

size = (width, height) = (480, 600)
screen = pygame.display.set_mode(size)
myfont = pygame.font.SysFont('Comic Sans MS', 32)

button1 = Floor(100, 50, length_x=5)
button2 = Floor(300, 50, length_y=5)
button_exit = MenuButton(width/2 - 5*BLOCK_SIZE/2, 100, length_x=5, length_y=2, img="graphics/water.png",
                         action_arg="exit", text_arg="Exit", text_color_arg=(250, 100, 6), text_font_arg=myfont)
button_start = MenuButton(width/2 - 5*BLOCK_SIZE/2, 500, length_x=5, length_y=2, img="graphics/water.png",
                          action_arg="start", text_arg="Start game", text_color_arg=(250, 100, 6), text_font_arg=myfont)

buttons = [button1, button2, button_exit, button_start]

from level_runner import run_level
button_to_action_dict = {"exit": sys.exit, "start": run_level}


# Settings

lemmings_spawn_number = 5                       # setting number of lemmings to spawn
lemmings_spawn_rate = 100                       # setting number of frames between lemming spawns
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "WS     F           W",
    "W      F           W",
    "WFFFFF F           W",
    "W      F           W",
    "WF  FFFF           W",
    "W  W               W",
    "W                  W",
    "WFFFFFF            W",
    "W                  W",
    "W S F  F           W",
    "W FFF    F         W",
    "W      EF          W",
    "WFFFwwwwF          W",
    "WFFFFFFFFFFFFFFFFFFW"]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:

            # Reading position of the click
            click_pos = pygame.mouse.get_pos()

            # Performing action for each of the clicked buttons
            for button in buttons:
                if type(button) == MenuButton and button.action == "start":
                    button_to_action_dict[button.action](level, lemmings_spawn_number, lemmings_spawn_rate)
                elif button.rect.collidepoint(click_pos):
                    button_to_action_dict[button.action]()

            #clicked_buttons = [button for button in buttons if butt.rect.collidepoint(click_pos)]

            #for button in clicked_buttons

    screen.fill((153, 153, 153))
    for obj in buttons:
        screen.blit(obj.image, obj.rect)
#        screen.blit(textsurface, obj.rect)
    screen.blit(button_exit.image, button_exit.rect)
    screen.blit(button_exit.text, button_exit.text_rect)

    pygame.display.flip()

