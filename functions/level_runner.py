from itertools import chain
import pygame
import sys
import time

import classes.lemmings
from functions.level_utilities import level_load_save, level_save, level_create
from global_variables import BLOCK_DEFAULT_SIZE, LEVEL_DEATH_FRAMES, LEVEL_FRAME_TIME,\
    LEVEL_BACKGROUND_COLOR, LEVEL_TEXT_COLOR


def level_run(sound_arg, block_size=None, level_slot=None, save_slot=None):
    from user_interface.main_menu import menu_main
    from user_interface.level_end_screen import end_screen

    # Level startup
    pygame.init()

    # Either loading or creating lemmings and objects, reading stats and creating interface
    if save_slot is None:
        lemmings, objects_dictionarized, stats, interface = level_create(level_slot, new_block_size=block_size)
    else:
        lemmings, objects_dictionarized, stats, interface = level_load_save(save_slot, new_block_size=block_size)

    # Setting variables based on stats entries
    if block_size is None:
        block_size = stats["Block_size"]

    else:
        # If main level-running procedure had block size provided then we save that
        stats["Block_size"] = block_size

    lemmings_spawn_number = stats["Lemmings_spawn_number"]  # How many lemmings are to spawn by each entrance
    lemmings_spawn_rate = stats["Lemmings_spawn_rate"]      # How many frames there will be between next spawns

    # Based on the width we set level window size and then create a screen
    level_size = stats["Level_size"]
    screen = pygame.display.set_mode(level_size)  # setting screen of the globally set size

    # Settings for the clock's appearance
    text_font = pygame.font.Font(None, block_size)
    text_color = LEVEL_TEXT_COLOR

    method_to_use = None    # Variable used to change types of lemmings
    pause = False           # Flag which can be changed by pressing right button

    while True:
        if not pause:
            # Moving clock forward and reducing the timer
            dt = interface["Clock"].tick(1 / LEVEL_FRAME_TIME) / 1000
            stats["Timer"] -= dt

            # Swapping to a new frame with small delay (by default 200 frames per second)
            stats["Frames_elapsed"] += 1
            time.sleep(LEVEL_FRAME_TIME * (BLOCK_DEFAULT_SIZE / block_size))

            # Spawning lemmings from each entrance
            for obj_entrance in objects_dictionarized["Entrance"]:
                obj_entrance.spawn(lemmings, spawn_rate=lemmings_spawn_rate, spawn_number=lemmings_spawn_number)

            # For each lemming...
            for lem in lemmings:

                # Check if it's dead
                if lem.dead > 0:

                    # If it has been dead for a while, we finally remove him
                    if lem.dead > LEVEL_DEATH_FRAMES:
                        lemmings.remove(lem)

                    # It's dead attribute serves as a counter for displaying the dead state
                    lem.dead += 1
                    continue

                # We collide the lemming with each object of each type
                lem.collision_objects(objects_dictionarized)

                # We don't let the lemming leave escape the window
                lem.boundary_check(level_size)

                # Removing lemming if it was marked for removal (e.g. lemming made it to the exit, got upgraded)
                if lem.remove == 1:
                    lemmings.remove(lem)
                    continue

                # Moving the lemming
                lem.move()

        # Filling background
        screen.fill(LEVEL_BACKGROUND_COLOR)

        # Drawing lemmings and all objects (interface included)
        for obj in lemmings + list(chain.from_iterable(objects_dictionarized.values())):
            screen.blit(obj.image, obj.rect)

        # For interface buttons we additionally:
        for button in objects_dictionarized["Buttons"]:

            # Display the button's second image which represents the lemming type
            if button.image_name2 is not None:
                screen.blit(button.image2, button.rect2)

            # Display the remaining charges for given lemming type
            screen.blit(*button.charges_to_text(stats, text_font, text_color))

        # Drawing clock
        clock_text = text_font.render(interface["Time_left"]+str(round(stats["Timer"], 1)), True, text_color)
        screen.blit(clock_text, interface["Clock_position"])

        # Changing display to reflect the changes
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            # For each click...
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Reading position of the click
                click_position = pygame.mouse.get_pos()

                # Exit to main menu button
                if objects_dictionarized["MenuButtons"][0].rect.collidepoint(click_position):
                    menu_main(sound_arg)

                # Pause button
                if objects_dictionarized["MenuButtons"][1].rect.collidepoint(click_position):
                    pause = not pause

                # Save1, Save2 & Save3 buttons
                for i in [2, 3, 4]:
                    if objects_dictionarized["MenuButtons"][i].rect.collidepoint(click_position):
                        level_save(5 - i, lemmings, objects_dictionarized, stats, screen)

                # For each type change button which was clicked on
                for button in objects_dictionarized["Buttons"]:
                    if button.rect.collidepoint(click_position):

                        # If there is no method then we create new method
                        if (stats["Class_list"][button.class_name] > 0 and
                                method_to_use is None):

                            method_to_use = getattr(classes.lemmings, button.class_name)
                            # efekt zaznaczenia
                            break

                        # If there is a method "deselect" it
                        else:
                            method_to_use = None
                            # efekt odanzcaenia

                # For each lemming that was clicked we either apply the method or execute lemming's on-click method
                for lem in lemmings:

                    # Type application
                    if method_to_use is not None:
                        if lem.rect.collidepoint(click_position):

                            # Changing lemming type to the selected one and adding it back to the lemming pool
                            lemmings.append(method_to_use(lemming_arg=lem, objects_dictionarized=objects_dictionarized))

                            # Decreasing the number of charges
                            stats["Class_list"][method_to_use.__name__] -= 1

                            # "Deselecting"the method
                            method_to_use = None
                            # wyłączyć efekt kliknięcia

                            # Leaving the lemming loop to ensure that only one lemming was changed
                            break
                    else:

                        # For special types it's going to remove the type and revert lemming back to normal
                        lem.on_click(click_position, objects_dictionarized, lemmings)

        # Level end check, proceed only if each entrance spawned maximum number of lemmings
        if stats["Frames_elapsed"] > lemmings_spawn_rate * (lemmings_spawn_number+1):

            # End of time or end of living lemmings
            if max(stats["Timer"], 0) == 0 or lemmings == []:

                # Count how many lemmings were spawned
                stats["Lemmings_spawned"] = lemmings_spawn_number * len(objects_dictionarized["Entrance"])

                # Count how many lemmings made it to exits
                for obj_exit in objects_dictionarized["Exit"]:
                    stats["Lemmings_exit"] += obj_exit.lemming_exit_number

                end_screen(stats, sound_arg)
