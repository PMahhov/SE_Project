import pygame
import pygame_gui
import yaml
from background import Background
from information_popup import Information_Popup
from pygame_gui import UIManager

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]

is_running = False

pygame.init()

pygame.display.set_caption("[Game Title]")

window_surface = pygame.display.set_mode((screen_width, screen_height))


background = pygame.Surface((screen_width, screen_height))
background.fill(pygame.Color("#A5AAAF"))
default_manager = UIManager(
    (screen_width, screen_height)
)  # , 'data/themes/quick_theme.json')

bg = Background()
bg.init_class(default_manager)

#popup = Information_Popup("window", "data", default_manager)
#popup.display_graph()

clock = pygame.time.Clock()
is_running = True

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
