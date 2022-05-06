import pygame
import pygame_gui
import yaml
from background import Background
from information_popup import Information_Popup
from pygame_gui import UIManager
import numpy as np
from menu import Menu
with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]

is_running = False

pygame.init()

pygame.display.set_caption("Simultaneous Exchange Project")

window_surface = pygame.display.set_mode((screen_width, screen_height))

background = pygame.Surface((screen_width, screen_height))
background.fill(pygame.Color("#A5AAAF"))
default_manager = UIManager(
    (screen_width, screen_height)
) #, 'source/window.json')

default_manager.preload_fonts([{'name': 'fira_code', 'point_size': 14, 'style': 'bold_italic'},{'name': 'fira_code', 'point_size': 14, 'style': 'italic'},{'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])

clock = pygame.time.Clock()
is_running = True

# create and display the menu
menu = Menu(default_manager, background)

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            menu.button_pressed(event)

        default_manager.process_events(event)
    
    if menu.update():
        break
    default_manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    default_manager.draw_ui(window_surface)

    pygame.display.update()

default_manager.clear_and_reset()

path_level_modules = ["level_modules/level_module_1.json", "level_modules/level_module_2.json","level_modules/level_module_3.json"]

bg = Background()
bg.init_class(default_manager, path_level_modules)

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            bg.button_pressed(event)

        default_manager.process_events(event)

    default_manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    default_manager.draw_ui(window_surface)

    pygame.display.update()
