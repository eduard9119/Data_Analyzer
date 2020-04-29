#Let's add a different widget, a common slider...
from PySide2.QtCore import Qt
from PySide2.QtWidgets import *
from PySide2.QtGui import QIcon # Get the package to add an icon
from PySide2.QtCore import Slot

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import pandas as pd

import sys

separator = ';'

app = QApplication([])
window = QWidget()
window.setWindowTitle('Data Analyzer')
window.setWindowIcon(QIcon('icon.png'))

tab1 = QWidget()
tab2 = QWidget()
layout = QVBoxLayout()
layout_tab1 = QVBoxLayout()
layout_tab2 = QVBoxLayout()

# Define slider widget, note the orientation argument:
slider = QSlider(Qt.Horizontal)


def loadFile():
    fname = QFileDialog.getOpenFileName(btn_load, "Open File",'c:\\',"Data files (*.csv *.xls *.xlsx)")[0]

    if fname.endswith('.csv'):
      df = pd.read_csv(fname, sep=separator)
    elif fname.endswith('.xls') or fname.endswith('.xlsx'):
      df = pd.read_excel(fname)
    print(df.head())
    label_file.setText(fname)
    print("Separator: "+separator)

    table_prev.header = df.columns
    table_prev.size = [ 75, 375, 85, 600 ]
    table_prev.setColumnCount(len(table_prev.header))
    table_prev.setHorizontalHeaderLabels(table_prev.header)
    table_prev.setSelectionMode(QTableView.ExtendedSelection)
    table_prev.setSelectionBehavior(QTableView.SelectRows)
    table_prev.setAlternatingRowColors(True)
    table_prev.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
    print(df.shape[0])
    row_count = 0
    if df.shape[0] > 50:
        row_count = 50
    else:
        row_count = df.shape[0]
    table_prev.setRowCount(row_count)
    for row in range(0, row_count):
        #print(row, ", ")
        print("--------------------")
        for col in range(0, df.shape[1]):
            table_prev.setItem(row, col, QTableWidgetItem(str(df.iloc[row, col])))
            print(row, col, df.iloc[row, col])

    table_prev.resizeColumnsToContents()

tabWidget = QTabWidget()
tabWidget.addTab(tab1,'Load Dataset')
tabWidget.addTab(tab2,'Tab 2')
layout.addWidget(tabWidget)

label_separator = QLabel('Choose a column separator')
layout_tab1.addWidget(label_separator)
radioBtn_semicolon = QRadioButton(";")
radioBtn_semicolon.setChecked(True)
radioBtn_semicolon.toggled.connect(lambda:btnstate(radioBtn_semicolon))
radioBtn_comma = QRadioButton(",")#.setChecked(True
radioBtn_comma.toggled.connect(lambda:btnstate(radioBtn_comma))
radioBtn_pipe = QRadioButton("|")
radioBtn_pipe.toggled.connect(lambda:btnstate(radioBtn_pipe))
layout_radioBtn_separator = QHBoxLayout()
layout_radioBtn_separator.addWidget(radioBtn_comma)
layout_radioBtn_separator.addWidget(radioBtn_semicolon)
layout_radioBtn_separator.addWidget(radioBtn_pipe)
layout_tab1.addLayout(layout_radioBtn_separator)
btn_load = QPushButton('Open Dataset...')
layout_tab1.addWidget(btn_load)
btn_load.clicked.connect(loadFile) # clicked signal

def btnstate(b):
    if b.isChecked() == True:
        separator = b.text()
        print("Separator: "+separator)

label_file = QLabel('')
layout_tab1.addWidget(label_file)

table_prev = QTableWidget()
layout_tab1.addWidget(table_prev)

'''fileDialog = QFileDialog()
fig = Figure(figsize=(600,600), dpi=72, facecolor=(1,1,1), edgecolor=(0,0,0))
ax = fig.add_subplot(111)
# Add data:
ax.plot([0,1])
# generate the canvas to display the plot
canvas = FigureCanvas(fig)
layout_tab2.addWidget(canvas)
layout_tab1.addWidget(fileDialog)'''

layout_tab2.addWidget(slider) #Add the slider

window.setLayout(layout)
tab1.setLayout(layout_tab1)
tab2.setLayout(layout_tab2)

window.show()
app.exec_()
