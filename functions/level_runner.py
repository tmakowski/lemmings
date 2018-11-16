from itertools import chain
import pygame
import sys
import time

import classes.lemmings
from functions.level_utilities import level_generate, level_interface, level_import_layout, level_load_save, level_save
from global_variables import LEVEL_DEATH_FRAMES, LEVEL_FRAME_TIME
# from classes.lemmings import *


def level_run(lemmings_spawn_number, lemmings_spawn_rate, block_size, level_file=None, save_slot=None):
    # Level startup
    pygame.init()
    level_width = 54
    level_size = (int(block_size * level_width), int(0.5 * block_size * level_width))
    screen = pygame.display.set_mode(level_size)                    # setting screen of the globally set size
    if save_slot is None:
        lemmings = []                                     # initializing a list for lemmings if those weren't provided
        level = level_import_layout(level_file)                    # importing level layout
        objects_dictionarized = level_generate(level, block_size)  # generating objects based on the level visualization
        objects_dictionarized["Stoppers"] = []
    else:
        lemmings, objects_dictionarized = level_load_save(save_slot, block_size)
        lemmings_spawn_number = 0 # should be read

    #
    interface = level_interface(block_size, level_size)
    # usuwać klucz Stoppers na końcu!!

    method_to_use = None
    dev_timer = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exec(open("./main_menu.py").read())
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                click_position = pygame.mouse.get_pos()
                clicked = [s for s in lemmings if s.rect.collidepoint(click_position)]

                for button in interface["Buttons"]:
                    if button.rect.collidepoint(click_position):
                        if button.class_name is not None:
                            method_to_use = getattr(classes.lemmings, button.class_name)
                            break
                        # jakiś efekt kliknięcia
                        else:
                            obj_dict = objects_dictionarized.copy()
                            obj_dict.pop("Stoppers")
                            level_save(3, lemmings, obj_dict)
                            del obj_dict

                if method_to_use is not None:
                    for lem in lemmings:
                        if lem.rect.collidepoint(click_position):
                            lemmings.append(method_to_use(lemming_arg=lem, objects_dictionarized=objects_dictionarized))
                            method_to_use = None
                            # charges -= 1
                            # wyłączyć efekt kliknięcia
                            break

    # Spawning lemmings
        for obj_entrance in objects_dictionarized["Entrance"]:
            obj_entrance.spawn(lemmings, spawn_rate=lemmings_spawn_rate, spawn_number=lemmings_spawn_number)

    # Performing actions for each lemming
        for lem in lemmings:

            # Check if the lemming is dead
            if lem.dead > 0:

                # Deleting the lemming after it's dead version has been displayed long enough
                if lem.dead > LEVEL_DEATH_FRAMES:
                    lemmings.remove(lem)

                # Increasing the dead-lemming frame counter
                lem.dead += 1
                continue

            # Colliding the lemming with each type of objects
            lem.collision_objects(objects_dictionarized)

            # Collides lemmings with one another
            lem.collision_lemmings(lemmings)

            # Removing lemmings that made it to the exit or got upgraded to different type
            if lem.remove == 1:
                lemmings.remove(lem)
                continue

            # Moving the lemming
            lem.move()

    # Drawing the frame
        # Filling background
        screen.fill((0, 0, 0))

        # Drawing lemmings and all objects
        for obj in (lemmings
                    + list(chain.from_iterable(objects_dictionarized.values()))
                    + interface["Buttons"]):
            screen.blit(obj.image, obj.rect)

        # Changing display to show drawn objects
        pygame.display.flip()

    # System stuff
        # Setting custom pause between frames
        time.sleep(LEVEL_FRAME_TIME)

        dev_timer += 1
        if lemmings == [] and dev_timer > lemmings_spawn_rate:
            for obj_exit in objects_dictionarized["Exit"]:
                print("Uwaga, uwaga, tyle lemingów wyszło:", obj_exit.lemming_exit_number)
            exec(open("./main_menu.py").read())
            sys.exit()
