import matplotlib
import matplotlib.backends.backend_agg as agg
import pygame
import pylab
import yaml
from pygame_gui import UIManager
from pygame_gui.elements import UIImage, UIWindow

matplotlib.use("Agg")


class Information_Popup:
    def __init__(self, window_title: str, data: str, manager: UIManager) -> None:
        with open("config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)
        self.window_length = self.config["screen_length"]
        self.window_width = self.config["screen_width"]
        self.window_title = window_title
        self.data = data
        self.manager = manager

    def display_graph(self) -> None:
        # create the popup window
        window = UIWindow(
            pygame.Rect(
                self.window_length / 6,
                self.window_width / 10,
                (4 * self.window_length) / 6,
                (8 * self.window_width) / 10,
            ),
            manager=self.manager,
            window_display_title=self.window_title,
        )

        # create the graph
        fig = pylab.figure(
            figsize=[4, 4], dpi=100,  # Inches  # 100 dots per inch,
        )  # resulting buffer is 400x400 pixels
        ax = fig.gca()
        ax.plot([1, 2, 4])
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()

        # create the image element
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        image = UIImage(
            pygame.Rect(
                0, 0, (4 * self.window_length) / 6, ((8 * self.window_width) / 10) - 55
            ),
            surf,
            manager=self.manager,
            container=window,
        )