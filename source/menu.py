import pygame
from pygame_gui import UIManager
from pygame_gui.elements import UIButton, UILabel   #, UIWindow, UIPanel
from pygame_gui.windows import UIMessageWindow
import yaml

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_height = config["screen_height"]
screen_width = config["screen_width"]
about_text = config["about_section"]

class Menu:
    def __init__(self, manager: UIManager, background: any) -> None:
        self.manager = manager
        self.box_width = screen_width / 3
        self.box_height = 50
        self.background = background
        self.stop = False


        self.start_button = UIButton(
            text="Start",
            tool_tip_text="Start the first scenario",
            relative_rect=pygame.Rect(
                (screen_width / 2) - self.box_width / 3,
                1.3*screen_height/3,
                2*self.box_width/3,
                self.box_height,
            ),
            manager=self.manager,
            visible=True,
        )

        self.about_button = UIButton(
            text="About",
            relative_rect=pygame.Rect(
                (screen_width / 2) - self.box_width / 3,
                1.7*screen_height/3,
                2*self.box_width/3,
                self.box_height,
            ),
            manager=self.manager,
            visible=True,
        )

    def button_pressed(self, event) -> None:
        if event.ui_element == self.start_button:
            self.start_scenario()
        if event.ui_element == self.about_button:
            self.display_about_window()

    def update(self) -> bool:
        if not self.stop:
            font_title = pygame.font.SysFont(None, 80)
            title = font_title.render('Welcome to Simulex!', True, (60, 60, 60))

            font_subtitle = pygame.font.SysFont(None, 40)
            subtitle = font_subtitle.render("The simulation exercise of executive simultaneous exchange", True, (80, 80, 80))

            self.background.blit(title, (0.29*screen_width, 150))
            self.background.blit(subtitle, (0.2*screen_width, 250))

        return self.stop

    def start_scenario(self) -> None:
        self.stop = True
        self.background.fill(pygame.Color("#A5AAAF"))

    def display_about_window(self) -> None:
        try: 
            self.about_window.kill()
        except:
            pass
        finally:
            self.about_window = UIMessageWindow(
                pygame.Rect(
                    (2 * screen_width / 8),
                    (2 * screen_height / 12),
                    (1.5 * self.box_width),
                    (8 * self.box_height),
                ),
                manager=self.manager,
                window_title= "About",
                html_message=about_text
            )


