import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QSizePolicy
from PyQt5 import QtCore
import PyQt5
import matplotlib

class Canvas(matplotlib.backends.backend_qt5agg.FigureCanvasQTAgg):
    def __init__(self, parent):
        self.fig_, self.ax_ = matplotlib.pyplot.subplots(figsize=(5, 5), dpi=100)
        matplotlib.pyplot.tight_layout()
        super().__init__(self.fig_)
        self.setParent(parent)

        self.ax_.grid()
        self.ax_.set(xlabel='time (s)', ylabel='units')

    def plot_sine(self, a, b, c):
        self.ax_.cla()
        t = np.arange(0.0, 10.0, 0.01)
        f = b * np.sin(a * t + c)
        self.ax_.plot(t, f)
        self.draw()


class PrimaryWorkspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        
        # initialize tabs
        self.tabs_ = PyQt5.QtWidgets.QTabWidget()
        self.tab1_ = PyQt5.QtWidgets.QWidget()
        self.tab2_ = PyQt5.QtWidgets.QWidget()

        # adding tabs
        self.tabs_.addTab(self.tab1_,'Tab 1')
        self.tabs_.addTab(self.tab2_,'Tab 2')

        # creating first tab
        self.tab1_.layout = PyQt5.QtWidgets.QVBoxLayout(self.tab1_)
        self.graph_ = Canvas(self.tab1_)
        self.tab1_.layout.addWidget(self.graph_)

        # adding tabs to widget
        self.layout_.addWidget(self.tabs_)
        self.setLayout(self.layout_)

    def update(self, a, b, c):
        self.graph_.plot_sine(a, b, c)

class SecondaryWorkspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()

        # initializing table
        self.table_ = PyQt5.QtWidgets.QTableWidget()

        # formatting table
        self.table_.setRowCount(3)
        self.table_.setColumnCount(2)
        self.table_.setHorizontalHeaderItem(0,PyQt5.QtWidgets.QTableWidgetItem('Parameter'))
        self.table_.setHorizontalHeaderItem(1,PyQt5.QtWidgets.QTableWidgetItem('Value'))


        # adding parameters to table
        self.table_.setItem(0,0,PyQt5.QtWidgets.QTableWidgetItem('A'))
        self.table_.setItem(1,0,PyQt5.QtWidgets.QTableWidgetItem('B'))
        self.table_.setItem(2,0,PyQt5.QtWidgets.QTableWidgetItem('C'))

        # adding initial values to table
        self.table_.setItem(0,1,PyQt5.QtWidgets.QTableWidgetItem('1'))
        self.table_.setItem(1,1,PyQt5.QtWidgets.QTableWidgetItem('1'))
        self.table_.setItem(2,1,PyQt5.QtWidgets.QTableWidgetItem('0'))

        
        # adding table to widget
        self.layout_.addWidget(self.table_)
        self.setLayout(self.layout_)

    def get_table_values(self):
        vals = []
        for i in range(3):
            vals.append(float(self.table_.item(i, 1).text()))
        return vals


class Workspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)
        self.layout_ = PyQt5.QtWidgets.QHBoxLayout()
        self.primary_ = PrimaryWorkspace(self)
        self.secondary_ = SecondaryWorkspace(self)

        # adding sections to  workspace
        self.layout_.addWidget(self.primary_)
        self.layout_.addWidget(self.secondary_)
        self.setLayout(self.layout_)

    def update(self):
        a, b, c = self.secondary_.get_table_values()
        self.primary_.update(a, b, c)


class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.title_ = 'PyQt Practice'
        self.main_ = PyQt5.QtWidgets.QWidget()
        
        self.setWindowTitle(self.title_)
        self.setCentralWidget(self.main_)

        # setting layout
        workspace = Workspace(self.main_)
        button1 = PyQt5.QtWidgets.QPushButton('Run')
        button1.clicked.connect(workspace.update)
        layout = PyQt5.QtWidgets.QVBoxLayout(self.main_)
        layout.addWidget(workspace)
        layout.addWidget(button1)
        

if __name__ == '__main__':
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()
	app.exec_()
