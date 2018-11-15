import pygame
import sys
import os

from classes.objects import MenuButton
from level_runner import level_run
from global_variables import BLOCK_SIZE


# Initialization of stuff
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)
pygame.init()
size = (width, height) = (480, 600)
screen = pygame.display.set_mode(size)
button_font = pygame.font.SysFont('Verdana', 32)

# Creating the buttons
button_start = MenuButton(width/2 - 8*BLOCK_SIZE/2, 500, length_x=5, length_y=2, img="graphics/water.png",
                          text_arg="Start game", text_color_arg=(250, 100, 6), text_font_arg=button_font)

button_exit = MenuButton(width/2 - 8*BLOCK_SIZE/2, 100, length_x=5, length_y=2, img="graphics/water.png",
                         text_arg="Exit", text_color_arg=(250, 100, 6), text_font_arg=button_font)

# Packing the buttons to a list and craeting dictionary for their uses
# buttons = [button_start, button_exit]
button_exit.center(width)
button_to_action_dict = {button_exit: sys.exit, button_start: level_run}


# Settings

lemmings_spawn_number = 5                       # setting number of lemmings to spawn
lemmings_spawn_rate = 100                       # setting number of frames between lemming spawns

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:

            # Reading position of the click
            click_pos = pygame.mouse.get_pos()

            # Performing action for each of the clicked buttons
            for button in button_to_action_dict.keys():
                if button.rect.collidepoint(click_pos):

                    if button == button_start:
                        button_to_action_dict[button]("level.txt", lemmings_spawn_number, lemmings_spawn_rate, "lemmings.txt")
                    else:
                        button_to_action_dict[button]()

    # Filling background
    screen.fill((253, 153, 153))

    # Displaying buttons and their's texts
    for button in button_to_action_dict.keys():
        screen.blit(button.image, button.rect)
        screen.blit(button.text, button.text_rect)

    # Updating the display
    pygame.display.flip()

