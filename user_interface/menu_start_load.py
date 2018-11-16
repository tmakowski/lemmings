import pygame
import sys
import os

from classes.objects import MenuButton
from functions.level_runner import level_run
from global_variables import BLOCK_DEFAULT_SIZE, INTERFACE_BUTTONS, INTERFACE_DEFAULT_SIZE,\
    INTERFACE_TEXT_COLOR, INTERFACE_BACKGROUND_COLOR, SAVE_PATH, SAVE_LEMMINGS, SAVE_OBJECTS, SAVE_STATS


def submenu(mode):
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
    buttons = []
    if mode == "start":
        max_slot = 10
        for i in range(max_slot):
            buttons.append(MenuButton(0, 50 + (i % (max_slot//2)) * 80, block_size, length_x=5, length_y=2,
                                      img=INTERFACE_BUTTONS,
                                      text_arg="Level " + str(i + 1),
                                      text_color_arg=text_color,
                                      text_font_arg=button_font))
            if i < max_slot // 2:
                buttons[i].center(width // 2)
            else:
                buttons[i].center(3 * (width // 2))

    else:
        max_slot = 3
        save_slots = []
        for i in range(max_slot):
            save_path = SAVE_PATH + str(i+1) + "/"
            if (os.path.isfile(save_path + SAVE_LEMMINGS)
                    and os.path.isfile(save_path + SAVE_OBJECTS)
                    and os.path.isfile(save_path + SAVE_STATS)):
                text = "Load save "
                save_slots.append(i)
            else:
                text = "Empty "

            buttons.append(MenuButton(0, 50 + i * 140, block_size, length_x=5, length_y=2,
                                      img=INTERFACE_BUTTONS,
                                      text_arg=text + str(i + 1),
                                      text_color_arg=text_color,
                                      text_font_arg=button_font))
            buttons[len(buttons)-1].center(width // 2)

        for i in range(max_slot):
            img_path = SAVE_PATH + str(i+1) + "/frame.png"
            if os.path.isfile(img_path):
                buttons.append(MenuButton(width, 50 + i * 140, block_size, length_x=6, length_y=3,
                                          img=img_path,
                                          text_arg="",
                                          text_color_arg=text_color,
                                          text_font_arg=button_font))
                buttons[len(buttons)-1].center(3 * (width // 2))

    # Back button
    buttons.append(MenuButton(0, height-80, block_size, length_x=3, length_y=1.5, img=INTERFACE_BUTTONS,
                              text_arg="Back", text_color_arg=text_color, text_font_arg=button_font))
    buttons[-1].center(width)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:

                # Reading position of the click
                click_position = pygame.mouse.get_pos()

                # Performing action for each of the clicked buttons
                for i in range(max_slot):
                    if buttons[i].rect.collidepoint(click_position):
                        if mode == "start":
                            level_run(level_slot=i+1)
                        else:
                            if i in save_slots:
                                level_run(save_slot=i+1)

                if buttons[-1].rect.collidepoint(click_position):
                    exec(open("./main_menu.py").read())

        # Filling background
        screen.fill(background_color)

        # Displaying buttons and their's texts
        for button in buttons:
            screen.blit(button.image, button.rect)
            screen.blit(button.text, button.text_rect)

        # Updating the display
        pygame.display.flip()

