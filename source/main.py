import copy
import numpy as np
import pygame
import pygame_gui
from pygame_gui import UIManager, PackageResource
from pygame_gui.elements import UIButton
from pygame_gui.elements import UILabel
from pygame_gui.elements import UIPanel
from pygame_gui.elements import UITextBox

is_running = False

pygame.init()

pygame.display.set_caption('[Game Title]')

screen_length = 1366
screen_width = 768
window_surface = pygame.display.set_mode((screen_length, screen_width))


bg = pygame.Surface((screen_length, screen_width))
bg.fill(pygame.Color('#A5AAAF'))

manager = UIManager((screen_length, screen_width)) #, 'data/themes/quick_theme.json')

creation_button = UIButton(text= "Split Timeline", tool_tip_text = 'Copy the current timeline into two',
							relative_rect=pygame.Rect(300,500,200,50),
							manager = manager)

clock = pygame.time.Clock()
is_running = True

while is_running:
	time_delta = clock.tick(60)/1000.0
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			is_running = False

#		if event.type == pygame_gui.UI_BUTTON_PRESSED:
			#if event.ui_element == button_name:
             #   passpass

		manager.process_events(event)

	manager.update(time_delta)

	window_surface.blit(bg, (0, 0))
	manager.draw_ui(window_surface)

	pygame.display.update()
