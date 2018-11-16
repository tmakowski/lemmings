import pygame
import sys
import os

from classes.objects import MenuButton
from user_interface.menu_start_load import submenu
from global_variables import BLOCK_DEFAULT_SIZE, INTERFACE_BUTTONS, INTERFACE_DEFAULT_SIZE,\
    INTERFACE_TEXT_COLOR, INTERFACE_BACKGROUND_COLOR


# Initialization of stuff
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

# Initializing pygame and a screen
pygame.init()
size = (width, height) = INTERFACE_DEFAULT_SIZE
screen = pygame.display.set_mode(size)

# Basic settings used below
block_size = BLOCK_DEFAULT_SIZE
button_font = pygame.font.SysFont('Verdana', block_size)
text_color = INTERFACE_TEXT_COLOR
background_color = INTERFACE_BACKGROUND_COLOR

# Creating the buttons
button_start = MenuButton(0, 200, block_size, length_x=5, length_y=2, img=INTERFACE_BUTTONS,
                          text_arg="Start game", text_color_arg=text_color, text_font_arg=button_font)

button_load = MenuButton(0, 350, block_size, length_x=5, length_y=2, img=INTERFACE_BUTTONS,
                         text_arg="Load game", text_color_arg=text_color, text_font_arg=button_font)

button_exit = MenuButton(0, 500, block_size, length_x=5, length_y=2, img=INTERFACE_BUTTONS,
                         text_arg="Exit", text_color_arg=text_color, text_font_arg=button_font)


# Packing the buttons to a list and creating dictionary for their uses
buttons = [button_start, button_load, button_exit]
for button in buttons:
    button.center(width)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:

            # Reading position of the click
            click_position = pygame.mouse.get_pos()

            # Performing action for each of the clicked buttons
            for button in buttons:
                if button.rect.collidepoint(click_position):

                    # Responding with desired action
                    if button == button_start:
                        submenu("start")
                    elif button == button_load:
                        submenu("load")
                    else:
                        sys.exit()

    # Filling background
    screen.fill(background_color)

    # Displaying buttons and their's texts
    for button in buttons:
        screen.blit(button.image, button.rect)
        screen.blit(button.text, button.text_rect)

    # Updating the display
    pygame.display.flip()

