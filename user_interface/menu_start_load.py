import pygame
import sys
import os

from classes.objects import MenuButton
from functions.level_runner import level_run
from global_variables import BLOCK_DEFAULT_SIZE, INTERFACE_BUTTONS, INTERFACE_DEFAULT_SIZE,\
    INTERFACE_TEXT_COLOR, INTERFACE_BACKGROUND_COLOR, SAVE_PATH, SAVE_LEMMINGS, SAVE_OBJECTS, SAVE_STATS


def submenu(mode, sound):
    from user_interface.main_menu import menu_main

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

    # Creating the buttons
    buttons = []
    if mode == "start":
        max_slot = 5   # number of levels

        # Creating and aligning a button for each level
        for i in range(max_slot):
            # buttons.append(MenuButton(0, 50 + (i % (max_slot//2)) * 80, block_size, length_x=5, length_y=2,
            buttons.append(MenuButton(0, 50 + i * 80, block_size, length_x=5, length_y=2,
                                      img=INTERFACE_BUTTONS,
                                      text_arg="Level " + str(i + 1),
                                      text_color_arg=text_color,
                                      text_font_arg=button_font))

            # Splitting buttons into two rows
            # if i < max_slot // 2:
            #     buttons[i].center(width // 2)
            # else:
            #     buttons[i].center(3 * (width // 2))
            buttons[i].center(width)

    else:
        max_slot = 3        # number of save slots
        save_slots = []     # list of the non-empty save slots' indexes

        # Creating and aligning a button for each save that has all needed files
        for i in range(max_slot):

            # Check for the files
            save_path = SAVE_PATH + str(i+1) + "/"
            if (os.path.isfile(save_path + SAVE_LEMMINGS)
                    and os.path.isfile(save_path + SAVE_OBJECTS)
                    and os.path.isfile(save_path + SAVE_STATS)):
                text = "Load save "
                save_slots.append(i)
            else:
                text = "Empty "

            # Button creation
            buttons.append(MenuButton(0, 50 + i * 140, block_size, length_x=5, length_y=2,
                                      img=INTERFACE_BUTTONS,
                                      text_arg=text + str(i + 1),
                                      text_color_arg=text_color,
                                      text_font_arg=button_font))
            buttons[len(buttons)-1].center(width // 2)

        # For each non-empty save showing it's screen if it's present
        for i in range(max_slot):

            # Existence check
            img_path = SAVE_PATH + str(i+1) + "/frame.png"

            # Creation of the previews
            if os.path.isfile(img_path):
                buttons.append(MenuButton(width, 50 + i * 140, block_size, length_x=6, length_y=3,
                                          img=img_path,
                                          text_arg="",
                                          text_color_arg=text_color,
                                          text_font_arg=button_font))
                buttons[len(buttons)-1].center(3 * (width // 2))

    # Addition of a back button aligned to center
    buttons.append(MenuButton(0, height-80, block_size, length_x=3, length_y=1.5, img=INTERFACE_BUTTONS,
                              text_arg="Back", text_color_arg=text_color, text_font_arg=button_font))
    buttons[-1].center(width)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # For each click...
            if event.type == pygame.MOUSEBUTTONUP:

                # Reading position of the click
                click_position = pygame.mouse.get_pos()

                # Either starting a level (i+1) or loading the save (i+1)
                for i in range(max_slot):

                    # Collision (click) check
                    if buttons[i].rect.collidepoint(click_position):
                        pygame.mixer.music.fadeout(1000)
                        if mode == "start":
                            level_run(level_slot=i+1, sound_arg=sound)

                        else:
                            # Checking if save slot is non-empty
                            if i in save_slots:
                                level_run(save_slot=i+1, sound_arg=sound)

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

