import copy
import numpy as np
import pygame
import pygame_gui
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIButton, UILabel, UIPanel, UITextBox

from background import Background


is_running = False

pygame.init()

pygame.display.set_caption('[Game Title]')

screen_length = 1366
screen_width = 768
window_surface = pygame.display.set_mode((screen_length, screen_width))


bg = pygame.Surface((screen_length, screen_width))
bg.fill(pygame.Color('#A5AAAF'))
default_manager = UIManager((screen_length, screen_width)) #, 'data/themes/quick_theme.json')

background = Background(default_manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
	time_delta = clock.tick(60)/1000.0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			is_running = False

		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			if event.ui_element == background.creation_button:
			  print("i'm here")

		default_manager.process_events(event)

	default_manager.update(time_delta)

	window_surface.blit(bg, (0, 0))
	default_manager.draw_ui(window_surface)

	pygame.display.update()
