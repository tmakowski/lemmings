import pygame
import sys
import os

from classes.objects import MenuButton
from functions.level_runner import level_run
from global_variables import BLOCK_DEFAULT_SIZE, INTERFACE_BUTTONS, INTERFACE_DEFAULT_SIZE, INTERFACE_TEXT_COLOR


# Initialization of stuff
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

# Initializing pygame and a screen
pygame.init()
size = (width, height) = INTERFACE_DEFAULT_SIZE
screen = pygame.display.set_mode(size)

# Basic settings used below
screen_color = (253, 153, 153)
block_size = BLOCK_DEFAULT_SIZE
button_font = pygame.font.SysFont('Verdana', block_size)
text_color = INTERFACE_TEXT_COLOR

# Creating the buttons
buttons = []
for i in range(10):
    buttons.append(MenuButton(0, 50 + i*80, block_size, length_x=5, length_y=2, img=INTERFACE_BUTTONS,
                              text_arg="Level "+str(i+1), text_color_arg=text_color, text_font_arg=button_font))

buttons.append(MenuButton(0, 75 + len(buttons)*80, block_size, length_x=3, length_y=1.5, img=INTERFACE_BUTTONS,
                          text_arg="Back", text_color_arg=text_color, text_font_arg=button_font))

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
            for i in range(0, 10):
                if buttons[i].rect.collidepoint(click_position):
                    level_run(level_slot=i+1)

            if buttons[-1].rect.collidepoint(click_position):
                exec(open("./main_menu.py").read())

    # Filling background
    screen.fill((253, 153, 153))

    # Displaying buttons and their's texts
    for button in buttons:
        screen.blit(button.image, button.rect)
        screen.blit(button.text, button.text_rect)

    # Updating the display
    pygame.display.flip()

