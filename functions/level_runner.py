from itertools import chain
import pygame
import sys
import time

import classes.lemmings
from functions.level_utilities import level_load_save, level_save, level_create
from global_variables import BLOCK_DEFAULT_SIZE, LEVEL_DEATH_FRAMES, LEVEL_FRAME_TIME


def level_run(block_size=None, level_slot=None, save_slot=None):
    # Level startup
    pygame.init()

    if save_slot is None:
        lemmings, objects_dictionarized, stats, interface = level_create(level_slot, new_block_size=block_size)
    else:
        lemmings, objects_dictionarized, stats, interface = level_load_save(save_slot, new_block_size=block_size)

    if block_size is None:
        block_size = stats["Block_size"]
    else:
        stats["Block_size"] = block_size
    lemmings_spawn_number = stats["Lemmings_spawn_number"]
    lemmings_spawn_rate = stats["Lemmings_spawn_rate"]
    level_width = stats["Level_width"]

    level_size = (int(block_size * level_width), int(0.5 * block_size * level_width))
    screen = pygame.display.set_mode(level_size)  # setting screen of the globally set size

    frames_elapsed = 0
    method_to_use = None
    text_font = pygame.font.Font(None, block_size)
    text_color = (255, 255, 255)

    while True:

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
            # lem.collision_lemmings(lemmings)

            lem.boundary_check(level_size)

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
        for obj in lemmings + list(chain.from_iterable(objects_dictionarized.values())):
            screen.blit(obj.image, obj.rect)

        for button in objects_dictionarized["Buttons"]:
            if button.image_name2 is not None:
                screen.blit(button.image2, button.rect2)
            screen.blit(*button.charges_to_text(stats, text_font, text_color))

        clock_text = text_font.render(interface["Time_left"]+str(round(stats["Timer"], 1)), True, text_color)
        screen.blit(clock_text, interface["Clock_position"])

        # Changing display to show drawn objects
        pygame.display.flip()

    # System stuff
        # Setting custom pause between frames
        dt = interface["Clock"].tick(1 / LEVEL_FRAME_TIME) / 1000
        stats["Timer"] -= dt
        frames_elapsed += 1
        time.sleep(LEVEL_FRAME_TIME * (BLOCK_DEFAULT_SIZE/block_size))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exec(open("./main_menu.py").read())
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                click_position = pygame.mouse.get_pos()

                for button in objects_dictionarized["Buttons"]:
                    if button.rect.collidepoint(click_position):
                        if (button.class_name is not None and
                                stats["Class_list"][button.class_name] > 0 and
                                method_to_use is None):
                            method_to_use = getattr(classes.lemmings, button.class_name)
                            break
                        elif button.class_name is not None:
                            method_to_use = None
                        # jakiś efekt kliknięcia    def __str__(self):

                if method_to_use is not None:
                    for lem in lemmings:
                        if lem.rect.collidepoint(click_position):
                            lemmings.append(method_to_use(lemming_arg=lem, objects_dictionarized=objects_dictionarized))

                            stats["Class_list"][method_to_use.__name__] -= 1
                            method_to_use = None
                            level_save(1, lemmings, objects_dictionarized, stats)
                            # wyłączyć efekt kliknięcia
                            break
                    continue

                for lem in lemmings:
                    lem.on_click(click_position, objects_dictionarized, lemmings)

        # Check for level end
        if frames_elapsed > lemmings_spawn_rate:
            if (max(stats["Timer"], 0) == 0 or
                    (lemmings == [] and frames_elapsed > lemmings_spawn_rate * (lemmings_spawn_number+1))):
                pass
                # LEVEL END
