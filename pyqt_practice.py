import sys
import numpy as np
import PyQt5
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas 

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class Canvas(FigureCanvas):
    def __init__(self, parent):
        self.fig_, self.ax_ = plt.subplots( dpi=50)
        super().__init__(self.fig_)
        self.setParent(parent)

        self.ax_.cla()
        self.ax_.grid()
        self.ax_.set(xlabel='time (s)', ylabel='units')
        plt.tight_layout()
        self.plot_sine(0, 0, 0)

    def plot_sine(self, a, b, c):
        self.ax_.cla()
        self.ax_.grid()
        self.ax_.set(xlabel='time (s)', ylabel='units')
        plt.tight_layout()
        t = np.arange(0.0, 10.0, 0.01)
        f = b * np.sin(a * t + c)
        self.ax_.plot(t, f)
        self.draw()


class PrimaryWorkspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)
        self.layout_ = PyQt5.QtWidgets.QVBoxLayout()
        
        # initialize tree menu
        self.tree_ = PyQt5.QtWidgets.QTreeWidget()
        self.tree_.setColumnCount(5)
        self.tree_.setHeaderLabels(['Type','Name','Attribute','Value','Unit'])

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
        self.tab1_.layout.addWidget(self.graph_,2)
        self.tab1_.layout.addWidget(self.tree_,1)
        self.graph_.plot_sine(0,0,0)


        # adding widgets to layout
        self.layout_.addWidget(self.tabs_, 1)
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

        # creating table items and setting rules
        item_a = PyQt5.QtWidgets.QTableWidgetItem('A')
        item_b = PyQt5.QtWidgets.QTableWidgetItem('B')
        item_c = PyQt5.QtWidgets.QTableWidgetItem('C')
        
        item_a.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable | PyQt5.QtCore.Qt.ItemIsEnabled)
        item_b.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable | PyQt5.QtCore.Qt.ItemIsEnabled)
        item_c.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable | PyQt5.QtCore.Qt.ItemIsEnabled)

        # adding parameters to table
        self.table_.setItem(0,0,item_a)
        self.table_.setItem(1,0,item_b)
        self.table_.setItem(2,0,item_c)

        # adding initial values to table
        self.table_.setItem(0,1,PyQt5.QtWidgets.QTableWidgetItem('1'))
        self.table_.setItem(1,1,PyQt5.QtWidgets.QTableWidgetItem('1'))
        self.table_.setItem(2,1,PyQt5.QtWidgets.QTableWidgetItem('0'))

        # adjusting table
        self.table_.setMinimumWidth(200)
        self.table_.setColumnWidth(0,100)
        self.table_.setColumnWidth(1,100)
        self.table_.verticalHeader().setVisible(False)

        # adding table to widget
        self.layout_.addWidget(self.table_)
        self.setLayout(self.layout_)

    def get_table_values(self):
        vals = []
        for i in range(3):
            item_text = self.table_.item(i, 1).text()
            if isfloat(item_text):
                vals.append(float(item_text))
            else:
                self.table_.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem('0'))
                vals.append(float(self.table_.item(i,1).text()))
        return vals


class Workspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)
        self.layout_ = PyQt5.QtWidgets.QHBoxLayout()
        self.primary_ = PrimaryWorkspace(self)
        self.secondary_ = SecondaryWorkspace(self)

        # adding sections to  workspace
        self.layout_.addWidget(self.primary_)
        self.layout_.addSpacing(100)
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
        self.menu_bar_ = self.menuBar()

        # handling menubar
        self.menu_bar_.setNativeMenuBar(False) # MacOS shows menubar at top of screen
        file_menu = self.menu_bar_.addMenu('&File')
        edit_menu = self.menu_bar_.addMenu('&Edit')
        help_menu = self.menu_bar_.addMenu('&Help')

        # create actions
        new_action = PyQt5.QtWidgets.QAction('&New',self)
        open_action = PyQt5.QtWidgets.QAction('&Open File...',self)
        save_action = PyQt5.QtWidgets.QAction('&Save',self)
        exit_action = PyQt5.QtWidgets.QAction('&Exit',self)
        undo_action = PyQt5.QtWidgets.QAction('&Undo',self)
        redo_action = PyQt5.QtWidgets.QAction('&Redo',self)
        doc_action = PyQt5.QtWidgets.QAction('&Documentation',self)

        # link actions
        file_menu.addAction(new_action)
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(exit_action)

        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        help_menu.addAction(doc_action)

        # preparing main window
        self.setWindowTitle(self.title_)
        self.setCentralWidget(self.main_)
        self.setMenuBar(self.menu_bar_)

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
