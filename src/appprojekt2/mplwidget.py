import numpy as np
import matplotlib

try:
    from PyQt5 import QtWidgets
except ModuleNotFoundError:
    from PyQt6 import QtWidgets

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
matplotlib.use('QtAgg')


# Matplotlib canvas class to create figure
class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi, tight_layout=True)
        self.ax = self.fig.add_subplot(111)
        super(MplCanvas, self).__init__(self.fig)


# Matplotlib widget
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)  # Inherit from QWidget
        # Create canvas object (the canvas to plot on)
        self.canvas = MplCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Set box for plotting (frame that holds tha canvas and the toolbar)
        self.vbl = QtWidgets.QVBoxLayout()
        # add the canvas to the plot box
        self.vbl.addWidget(self.canvas)
        # add the toolbar
        self.vbl.addWidget(self.toolbar)
        self.setLayout(self.vbl)

    def scatter_plot(self, x: np.ndarray, y: np.ndarray, x_label: str, y_label: str, title: str):
        """
        Plots the given data x over data y as scatter plot. The graph is set up accordingly.
        """
        self.canvas.ax.clear()
        # scatter x data over y data
        self.canvas.ax.scatter(x, y)

        # set title and axis labels
        self.canvas.ax.set_title(title, fontsize=25)
        self.canvas.ax.set_xlabel(x_label, fontsize=20)
        self.canvas.ax.set_ylabel(y_label, fontsize=20)

        # enable grid
        self.canvas.ax.grid(True)

        # show the plot (like plt.show())
        self.canvas.draw()

    def line_plot(self, x: np.ndarray, y: np.ndarray, x_label: str, y_label: str, title: str):
        """
        Plots the given data x over data y as line plot. The graph is set up accordingly.
        """
        self.canvas.ax.clear()
        # scatter x data over y data
        self.canvas.ax.plot(x, y)

        # set title and axis labels
        self.canvas.ax.set_title(title, fontsize=25)
        self.canvas.ax.set_xlabel(x_label, fontsize=20)
        self.canvas.ax.set_ylabel(y_label, fontsize=20)

        # enable grid
        self.canvas.ax.grid(True)

        # show the plot (like plt.show())
        self.canvas.draw()

    def clear(self):
        """
        Clears the plot canvas
        """
        self.canvas.ax.clear()
        # redrawing is required to apply the clearing
        self.canvas.draw()
