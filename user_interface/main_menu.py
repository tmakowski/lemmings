import pygame
import sys
import os

from classes.objects import MenuButton
from user_interface.menu_start_load import submenu
from global_variables import BLOCK_DEFAULT_SIZE, INTERFACE_BUTTONS, INTERFACE_DEFAULT_SIZE,\
    INTERFACE_TEXT_COLOR, INTERFACE_BACKGROUND_COLOR, SOUND_MENU


def menu_main(sound=True):
    # Setting top-left corner of a window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

    # Initializing pygame and a screen
    pygame.init()
    size = (width, height) = INTERFACE_DEFAULT_SIZE
    screen = pygame.display.set_mode(size)

    # Basic visual settings
    block_size = BLOCK_DEFAULT_SIZE
    button_font = pygame.font.SysFont('Verdana', block_size)
    text_color = INTERFACE_TEXT_COLOR
    background_color = INTERFACE_BACKGROUND_COLOR

    # Playing the music
    if sound and not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(SOUND_MENU)
        pygame.mixer.music.play()

    # Creating the buttons

    button_start = MenuButton(0, 200, block_size, length_x=5, length_y=2, img=INTERFACE_BUTTONS,
                              text_arg="Start game", text_color_arg=text_color, text_font_arg=button_font)

    button_load = MenuButton(0, 300, block_size, length_x=5, length_y=2, img=INTERFACE_BUTTONS,
                             text_arg="Load game", text_color_arg=text_color, text_font_arg=button_font)

    button_sound = MenuButton(0, 410, block_size, length_x=5, length_y=1, img=INTERFACE_BUTTONS,
                              text_arg="Toggle sound", text_color_arg=text_color, text_font_arg=button_font)

    button_exit = MenuButton(0, height - 80, block_size, length_x=3, length_y=1.5, img=INTERFACE_BUTTONS,
                             text_arg="Exit", text_color_arg=text_color, text_font_arg=button_font)

    # Packing the buttons to a list and centering them
    buttons = [button_start, button_load, button_sound, button_exit]
    for button in buttons:
        button.center(width)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # For each click...
            if event.type == pygame.MOUSEBUTTONUP:

                # Reading position of the click
                click_position = pygame.mouse.get_pos()

                # Performing an action corresponding to clicked button
                for button in buttons:
                    if button.rect.collidepoint(click_position):

                        if button == button_start:
                            submenu("start", sound)

                        elif button == button_load:
                            submenu("load", sound)

                        elif button == button_sound:
                            pygame.mixer.music.stop()
                            menu_main(not sound)

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
