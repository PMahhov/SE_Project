import matplotlib
import matplotlib.backends.backend_agg as agg
from matplotlib.ticker import MaxNLocator
import numpy as np
import pygame
import pylab
import yaml
from pygame_gui import UIManager
from pygame_gui.elements import UIImage, UIWindow

matplotlib.use("Agg")


class Information_Popup:
    
    """
    A class that displays a graph with historical information for stocks (stock prices) or for a loan (interest rates)

    ...
    ATTRIBUTES
    ----------
    screen_width: int
    screen_height: int
    window_title: str
    data: np.array(int) or np.array(float)
        Data to be plotted on a graph. Contains historical prices (for stocks) or historical interest rates (for loans). 
        Is appended to after each time interval
    initial number of historical data: int
        Initial number of data points for historical prices (stocks) or interest rates (loan)
    x_label: str
        Label for x-axis
    y_label: str
        Label for y-axis
    manager: UIManager
        Manager for the Graphical User Interface
    
    METHODS
    -------
    display_graph():
        Creates and displays the graph with Matplotlib and add it to the pop-up window
    
    kill():
        Kills the information pop-up window
    """
    
    def __init__(self, window_title: str, data: any, initial_number_of_historical_data: int, x_label: int, y_label: int, manager: UIManager) -> None:
        with open("config.yaml") as config_file:
            self.config = yaml.safe_load(config_file)
        self.screen_width = self.config["screen_width"]
        self.screen_height = self.config["screen_height"]
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
                ((self.screen_width - (2.5 * self.screen_width/6)) / 2) ,
                self.screen_height / 8,
                (2.5 * self.screen_width) / 6,
                (6 * self.screen_height + 50) / 10,
            ),
            manager=self.manager,
            window_display_title="Historical Information",
        )

        # create the graph
        fig = pylab.figure(
            figsize=[4, 4],
            dpi=300,  # Inches  # 100 dots per inch,
        )  # resulting buffer is 400x400 pixels
        ax = fig.gca()

        x_values = []
        for i in range(self.initial_number_of_historical_data):
            x_values.append(i - self.initial_number_of_historical_data + 1)
        for i in range(len(self.data) - self.initial_number_of_historical_data):
            x_values.append(i + 1)
        ax.plot(x_values, self.data)

        # set graph parameters
        ax.set_title(self.window_title, fontsize = 11, pad = 10)
        ax.set_xlabel(self.x_label, labelpad=3, fontsize = 9)
        ax.set_ylabel(self.y_label, labelpad=0, fontsize = 9)
        ax.tick_params(axis='both', which='major', labelsize=8)
        y_max = np.amax(self.data) + 0.2 * (np.amax(self.data) - np.amin(self.data))
        y_min = np.amin(self.data) - 0.2 * (np.amax(self.data) - np.amin(self.data))
        if self.y_label == "stock price":
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
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
                0, 0, (2.5 * self.screen_width) / 6,((self.screen_width - (2.5 * self.screen_width/6)) / 2 +8)
            ),
            surf,
            manager=self.manager,
            container=self.window,
        )

    def kill(self):
        self.window.kill()
