import pygame
import sys
import os

from classes.objects import MenuButton
from functions.level_runner import level_run
from global_variables import BLOCK_DEFAULT_SIZE, INTERFACE_BUTTONS, INTERFACE_DEFAULT_SIZE,\
    INTERFACE_TEXT_COLOR, INTERFACE_BACKGROUND_COLOR, SAVE_PATH, SAVE_LEMMINGS, SAVE_OBJECTS, SAVE_STATS


def end_screen(stats):
    from user_interface.main_menu import menu_main

    # Setting top-left corner of a window
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

    # Initializing pygame and a screen
    pygame.init()
    size = (width, height) = stats["Level_size"]
    screen = pygame.display.set_mode(size)

    # Basic visual settings
    block_size = BLOCK_DEFAULT_SIZE
    button_font = pygame.font.SysFont('Verdana', block_size)
    text_color = INTERFACE_TEXT_COLOR
    background_color = INTERFACE_BACKGROUND_COLOR

    # Read level stats
    lemmings_win_threshold = stats["Lemmings_win_threshold"]
    lemmings_spawned = stats["Lemmings_spawned"]
    lemmings_exit = stats["Lemmings_exit"]
    victory = True if lemmings_exit >= lemmings_win_threshold else False

    # Creating the buttons
    buttons = []
    if victory:
        button_text = "Next level"
    else:
        button_text = "Retry"

    buttons.append(MenuButton(0, height - 80, block_size, length_x=5, length_y=2,
                              img=INTERFACE_BUTTONS,
                              text_arg=button_text,
                              text_color_arg=text_color,
                              text_font_arg=button_font))

    buttons[-1].center(3 * (width // 2))

    # Addition of a back button aligned to 1/4 of the screen
    buttons.append(MenuButton(0, height-80, block_size, length_x=5, length_y=2,
                              img=INTERFACE_BUTTONS,
                              text_arg="Main menu",
                              text_color_arg=text_color,
                              text_font_arg=button_font))

    buttons[-1].center(width // 2)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # For each click...
            if event.type == pygame.MOUSEBUTTONUP:

                # Reading position of the click
                click_position = pygame.mouse.get_pos()

                # Either starting the same level or next one
                if buttons[0].rect.collidepoint(click_position):

                    if victory:
                        level_run(level_slot=stats["Level_slot"]+1)

                    else:
                        level_run(evel_slot=stats["Level_slot"])

                # Separate action for back button which returns to main menu
                if buttons[-1].rect.collidepoint(click_position):
                    menu_main()

        # Filling background
        screen.fill(background_color)

        # Displaying buttons and their's texts
        for button in buttons:
            screen.blit(button.image, button.rect)
            screen.blit(button.text, button.text_rect)

        # Updating the display
        pygame.display.flip()
