import pygame
import pygame_gui
import yaml
from background import Background
from pygame_gui import UIManager
import numpy as np
from menu import Menu

# import logging
# import os
# from datetime import datetime
# import platform



with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]

# set up logging
# if not os.path.exists("logging"):
#     os.makedirs("logging")
# now = datetime.now().strftime("%Y%m%d@%H:%M:%S")
# printable_now = datetime.now().strftime("%Y%m%d at %H:%M:%S")
# logging.basicConfig(filename=os.path.join('logging', f'debug[{now}].log'), encoding='utf-8', level=logging.INFO,format='%(message)s')



is_running = False
pygame.init()
pygame.display.set_caption("Simultaneous Exchange Project")

# set up the GUI
window_surface = pygame.display.set_mode((screen_width, screen_height))
background = pygame.Surface((screen_width, screen_height))
background.fill(pygame.Color("#A5AAAF"))
default_manager = UIManager(
    (screen_width, screen_height)
)

default_manager.preload_fonts([{'name': 'fira_code', 'point_size': 14, 'style': 'bold_italic'},{'name': 'fira_code', 'point_size': 14, 'style': 'italic'},{'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])

# start in-game clock
clock = pygame.time.Clock()
is_running = True

# logging.info(f"Welcome to the Simulex debugging logs. These logs recorded on a {platform.system()} {platform.release()} on {printable_now}")

# ------------
# INITIAL MENU
# ------------

# create initial menu
menu = Menu(default_manager, background)

# while loop to display the menu
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        # if the user closes the game window
        if event.type == pygame.QUIT:
            is_running = False

        # if the user clicks on any GUI button
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            menu.button_pressed(event)

        default_manager.process_events(event)
    
    if menu.update(): # returns True is the user has clicked on the Start button to start the game
        break
    default_manager.update(time_delta)

    # update the GUI
    window_surface.blit(background, (0, 0))
    default_manager.draw_ui(window_surface)
    pygame.display.update()

default_manager.clear_and_reset()


# ------------
#     GAME
# ------------

# stores the level module files 
path_level_modules = ["level_modules/level_module_1.json", "level_modules/level_module_2.json","level_modules/level_module_3.json"]
bg = Background()
bg.init_class(default_manager, path_level_modules)

# while loop to display the game
while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        # if the user closes the game window
        if event.type == pygame.QUIT:
            is_running = False

        # if the user clicks on any GUI button
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            bg.button_pressed(event)

        default_manager.process_events(event)

    default_manager.update(time_delta)

    # update the GUI
    window_surface.blit(background, (0, 0))
    default_manager.draw_ui(window_surface)

    pygame.display.update()
