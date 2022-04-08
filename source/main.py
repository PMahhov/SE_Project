import pygame
import pygame_gui
import yaml
from background import Background
from information_popup import Information_Popup
from pygame_gui import UIManager

with open("config.yaml") as config_file:
    config = yaml.safe_load(config_file)
screen_length = config["screen_length"]
screen_width = config["screen_width"]
is_running = False

pygame.init()

pygame.display.set_caption("[Game Title]")

window_surface = pygame.display.set_mode((screen_length, screen_width))


background = pygame.Surface((screen_length, screen_width))
background.fill(pygame.Color("#A5AAAF"))
default_manager = UIManager(
    (screen_length, screen_width)
)  # , 'data/themes/quick_theme.json')

bg = Background()
bg.init_class(default_manager)

# pop up window
import matplotlib

matplotlib.use("Agg")


# # create the popup window
# examplewindow = UIWindow(pygame.Rect(screen_length/6 , screen_width/10, (4*screen_length)/6, (8*screen_width)/10), manager = default_manager, window_display_title="test_window")

# # create the graph
# fig = pylab.figure(figsize=[4, 4], # Inches
#                    dpi=100,        # 100 dots per inch, so the resulting buffer is 400x400 pixels
#                    )
# ax = fig.gca()
# ax.plot([1, 2, 4])
# canvas = agg.FigureCanvasAgg(fig)
# canvas.draw()

# # create the image element
# renderer = canvas.get_renderer()
# raw_data = renderer.tostring_rgb()
# size = canvas.get_width_height()
# surf = pygame.image.fromstring(raw_data, size, "RGB")
# image = UIImage(pygame.Rect(0, 0, (4*screen_length)/6, ((8*screen_width)/10)-55), surf, manager = default_manager, container=examplewindow)
popup = Information_Popup("window", "data", default_manager)
popup.display_graph()

clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == bg.creation_button:
                print("i'm here")

        default_manager.process_events(event)

    default_manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    default_manager.draw_ui(window_surface)

    pygame.display.update()
