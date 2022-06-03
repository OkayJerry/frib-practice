import sys
import numpy as np
import PyQt5
from matplotlib.backends.qt_compat import QtWidgets
from matplotlib.backends.backend_qtagg import FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

def isfloat(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

class PrimaryWorkspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)

        # initialize
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self._create_tree()
        self._create_graph()
        self._create_tabs()

        # add widgets to layout
        self.layout.addWidget(self.tabs, 1)
        self.setLayout(self.layout)

    def _create_tabs(self):
        # initialize
        self.tabs = PyQt5.QtWidgets.QTabWidget()
        tab1 = PyQt5.QtWidgets.QWidget()
        tab2 = PyQt5.QtWidgets.QWidget()

        # link
        self.tabs.addTab(tab1,'Tab 1')
        self.tabs.addTab(tab2,'Tab 2')

        # first tab
        tab1.layout = PyQt5.QtWidgets.QVBoxLayout(tab1)
        tab1.layout.addWidget(self.graph,2)
        tab1.layout.addWidget(self.toolbar)
        tab1.layout.addWidget(self.tree,1)


    def _create_graph(self):
        # initialize
        self.fig = Figure(figsize=(5,3))
        self.graph = FigureCanvas(self.fig)
        self.ax = self.graph.figure.subplots()
        self.toolbar = NavigationToolbar(self.graph,self)

        # set
        self.ax.set_title('B * sin(A * x + C)')
        self.ax.set_xlabel('x')
        self.ax.set_ylabel('y')
        self.ax.autoscale()
        t = np.linspace(0,10,101)
        self.fig.subplots_adjust(wspace=100,hspace=100)
        self.fig.tight_layout()

        # initial plot
        self.line, = self.ax.plot(t,np.sin(t))

    def update_graph(self,a,b,c):
        t = np.linspace(0,10,101)
        self.line.set_data(t,b*np.sin(a*t+c))
        self.line.figure.canvas.draw()
        
    def _create_tree(self):
        # initialize
        self.tree = PyQt5.QtWidgets.QTreeWidget()

        # format
        self.tree.setColumnCount(5)
        self.tree.setHeaderLabels(['Type','Name','Attribute','Value','Unit'])
        self.tree.header().setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.Stretch)

       

class SecondaryWorkspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)

        # initialize
        self.layout = PyQt5.QtWidgets.QVBoxLayout()
        self._create_table()

        # add table to widget
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)

    def _create_table(self):
        # initialize
        self.table = PyQt5.QtWidgets.QTableWidget()

        # format
        self.table.setRowCount(3)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderItem(0,PyQt5.QtWidgets.QTableWidgetItem('Parameter'))
        self.table.setHorizontalHeaderItem(1,PyQt5.QtWidgets.QTableWidgetItem('Value'))
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(PyQt5.QtWidgets.QHeaderView.Stretch)

        # set custom vertical headers
        item_a = PyQt5.QtWidgets.QTableWidgetItem('A')
        item_b = PyQt5.QtWidgets.QTableWidgetItem('B')
        item_c = PyQt5.QtWidgets.QTableWidgetItem('C')
        item_a.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable | PyQt5.QtCore.Qt.ItemIsEnabled)
        item_b.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable | PyQt5.QtCore.Qt.ItemIsEnabled)
        item_c.setFlags(PyQt5.QtCore.Qt.ItemIsSelectable | PyQt5.QtCore.Qt.ItemIsEnabled)
        item_a.setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)
        item_b.setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)
        item_c.setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.table.setItem(0,0,item_a)
        self.table.setItem(1,0,item_b)
        self.table.setItem(2,0,item_c)

        # set initial values
        item_1 = PyQt5.QtWidgets.QTableWidgetItem('1')
        item_2 = PyQt5.QtWidgets.QTableWidgetItem('1')
        item_3 = PyQt5.QtWidgets.QTableWidgetItem('0')
        item_1.setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)
        item_2.setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)
        item_3.setTextAlignment(PyQt5.QtCore.Qt.AlignCenter)
        self.table.setItem(0,1,item_1)
        self.table.setItem(1,1,item_2)
        self.table.setItem(2,1,item_3)


    def get_table_values(self):
        vals = []
        for i in range(3):
            item_text = self.table.item(i, 1).text()
            if isfloat(item_text):
                vals.append(float(item_text))
            else:
                self.table.setItem(i,1,PyQt5.QtWidgets.QTableWidgetItem('0'))
                vals.append(float(self.table.item(i,1).text()))
        return vals


class Workspace(PyQt5.QtWidgets.QWidget):
    def __init__(self, parent):
        super(PyQt5.QtWidgets.QWidget, self).__init__(parent)

        # initialize
        self.layout = PyQt5.QtWidgets.QHBoxLayout()
        self.primary = PrimaryWorkspace(self)
        self.secondary = SecondaryWorkspace(self)

        # add sections to workspace
        self.layout.addWidget(self.primary,2)
        self.layout.addSpacing(50)
        self.layout.addWidget(self.secondary,1)
    
        self.setLayout(self.layout)

    def update(self):
        # graph
        a,b,c = self.secondary.get_table_values()
        self.primary.update_graph(a,b,c)

class Window(PyQt5.QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        # initialize
        self.main = PyQt5.QtWidgets.QWidget()
        workspace = Workspace(self.main)
        self._create_menu_bar()

        # set
        self.setWindowTitle('PyQt Practice')
        self.setCentralWidget(self.main)
        self.setMenuBar(self.menu_bar)
        button1 = PyQt5.QtWidgets.QPushButton('Run')
        button1.clicked.connect(workspace.update)
        layout = PyQt5.QtWidgets.QVBoxLayout(self.main)
        layout.addWidget(workspace)
        layout.addWidget(button1)
        
    def _create_menu_bar(self):
        # initialize
        self.menu_bar = self.menuBar()

        # format
        self.menu_bar.setNativeMenuBar(False) # MacOS shows menubar at top of screen
        file_menu = self.menu_bar.addMenu('&File')
        edit_menu = self.menu_bar.addMenu('&Edit')
        help_menu = self.menu_bar.addMenu('&Help')

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


if __name__ == '__main__':
	app = PyQt5.QtWidgets.QApplication(sys.argv)
	window = Window()
	window.show()
	app.exec_()
