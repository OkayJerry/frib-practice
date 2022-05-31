import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton
from PyQt5 import QtCore

class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(1, 1), dpi=100)
        plt.tight_layout()
        super().__init__(fig)
        self.setParent(parent)

        self.ax.grid()
        self.ax.set(xlabel='time (s)', ylabel='units')

    def plot_sine(self):
        t = np.arange(0.0, 2.0, 0.01)
        s = np.sin(2 * np.pi * t)
        self.ax.plot(t, s)
        self.draw()

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('PyQt Practice')
        self.resize(750, 750)

        canvas = Canvas(self)
        run_button = QPushButton('Run')
        run_button.setFixedSize(QtCore.QSize(750, 50))
        run_button.clicked.connect(canvas.plot_sine)
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        layout.addWidget(run_button)
        self.setLayout(layout)

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec_())
