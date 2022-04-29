import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
import pygame
import pylab
import yaml
import numpy as np
from pygame_gui import UIManager
from pygame_gui.elements import UIImage, UIWindow
from typing import List

matplotlib.use("Agg")

class Information_Popup:
    def __init__(self, window_title: str, data: any, initial_number_of_historical_data: int, x_label: int, y_label: int, manager: UIManager) -> None:
        with open("config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)
        self.window_width = self.config["screen_width"]
        self.window_height = self.config["screen_height"]
        self.window_title = window_title
        self.data = np.array(data, dtype=object)
        self.initial_number_of_historical_data = initial_number_of_historical_data
        self.x_label = x_label
        self.y_label = y_label
        self.manager = manager

    def display_graph(self) -> None:
        # create the popup window
        self.window = UIWindow(
            pygame.Rect(
                ((self.window_width - (2.5 * self.window_width/6)) / 2) ,
                self.window_height / 8,
                (2.5 * self.window_width) / 6,
                (6 * self.window_height + 50) / 10,
            ),
            manager=self.manager,
            window_display_title= "Historical Information",
        )
       
        # create the graph
        fig = pylab.figure(
            figsize=[4, 4], dpi=300,  # Inches  # 100 dots per inch,
        )  # resulting buffer is 400x400 pixels
        ax = fig.gca()
        
        x_values = []
        for i in range(self.initial_number_of_historical_data):
            x_values.append(i - self.initial_number_of_historical_data + 1)
        for i in range(len(self.data) - self.initial_number_of_historical_data):
            x_values.append(i + 1)
        ax.plot(x_values, self.data)
        
        # set graph parameters
        ax.set_title(self.window_title, fontsize = 12, pad = 10)
        ax.set_xlabel(self.x_label, labelpad=3, fontsize = 10)
        ax.set_ylabel(self.y_label, labelpad=0, fontsize = 10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        y_max = np.amax(self.data) + 0.2 * (np.amax(self.data) - np.amin(self.data))
        y_min = np.amin(self.data) - 0.2 * (np.amax(self.data) - np.amin(self.data))
        ax.set_ylim(y_min, y_max)

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()

        # create the image element
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        image = UIImage(
            pygame.Rect(
                0, 0, (2.5 * self.window_width) / 6,((self.window_width - (2.5 * self.window_width/6)) / 2 +8)
            ),
            surf,
            manager=self.manager,
            container=self.window,
        )

    def kill(self):
        self.window.kill()
        