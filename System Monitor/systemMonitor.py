import sys
import platform
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime,
                          QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase,
                         QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *
from PyQt5 import uic
import psutil
from pyqtgraph import PlotWidget
import pyqtgraph as pg
from pathlib import Path
import numpy as np
from collections import deque

counter = 0
jumper = 10
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi("main2.ui", self)
        self.cpu_percent = 0
        self.ram_percent = 0
        self.traces = dict()
        self.timestamp = 0
        self.timeaxis = []
        self.cpuaxis = []
        self.ramaxis = []
        self.current_timer_graph = None
        self.graph_lim = 15
        self.deque_timestamp = deque([], maxlen=self.graph_lim + 20)
        self.deque_cpu = deque([], maxlen=self.graph_lim + 20)
        self.deque_ram = deque([], maxlen=self.graph_lim + 20)
        self.ui.label.setText(f"{platform.system()} {platform.machine()}")

        self.graphwidget1 = PlotWidget(title="CPU percent")
        x1_axis = self.graphwidget1.getAxis('bottom')
        x1_axis.setLabel(text='Time since start (s)')
        y1_axis = self.graphwidget1.getAxis('left')
        y1_axis.setLabel(text='Percent')

        self.graphwidget2 = PlotWidget(title="RAM percent")
        x2_axis = self.graphwidget2.getAxis('bottom')
        x2_axis.setLabel(text='Time since start (s)')
        y2_axis = self.graphwidget2.getAxis('left')
        y2_axis.setLabel(text='Percent')

        self.pushButton.clicked.connect(self.show_cpu_graph)
        self.pushButton_2.clicked.connect(self.show_ram_graph)
        self.ui.gridLayout.addWidget(self.graphwidget1, 0, 0, 1, 3)
        self.ui.gridLayout.addWidget(self.graphwidget2, 0, 0, 1, 3)

        self.current_timer_systemStat = QtCore.QTimer()
        self.current_timer_systemStat.timeout.connect(self.getsystemStatpercent)
        self.current_timer_systemStat.start(1000)
        self.show_cpu_graph()

    def getsystemStatpercent(self):
        self.cpu_percent = psutil.cpu_percent()
        self.ram_percent = psutil.virtual_memory().percent
        self.setValue(self.cpu_percent, self.ui.labelPercentageCPU, self.ui.circularProgressCPU, "rgba(252, 0, 8, 1)")
        self.setValue(self.ram_percent, self.ui.labelPercentageRAM, self.ui.circularProgressRAM,
                      "rgba(163, 77, 255, 1)")

    def start_cpu_graph(self):
        if self.current_timer_graph:
            self.current_timer_graph.stop()
            self.current_timer_graph.deleteLater()
            self.current_timer_graph = None
        self.current_timer_graph = QtCore.QTimer()
        self.current_timer_graph.timeout.connect(self.update_cpu)
        self.current_timer_graph.start(1000)

    def update_cpu(self):
        self.timestamp += 1
        self.deque_timestamp.append(self.timestamp)
        self.deque_cpu.append(self.cpu_percent)
        self.deque_ram.append(self.ram_percent)
        timeaxis_list = list(self.deque_timestamp)
        cpu_list = list(self.deque_cpu)

        if self.timestamp > self.graph_lim:
            self.graphwidget1.setRange(xRange=[self.timestamp - self.graph_lim + 1, self.timestamp],
                                       yRange=[min(cpu_list[-self.graph_lim:]), max(cpu_list[-self.graph_lim:])])
        self.set_plotdata(name="cpu", data_x=timeaxis_list, data_y=cpu_list)

    def start_ram_graph(self):
        if self.current_timer_graph:
            self.current_timer_graph.stop()
            self.current_timer_graph.deleteLater()
            self.current_timer_graph = None
        self.current_timer_graph = QtCore.QTimer()
        self.current_timer_graph.timeout.connect(self.update_ram)
        self.current_timer_graph.start(1000)

    def update_ram(self):
        self.timestamp += 1
        self.deque_timestamp.append(self.timestamp)
        self.deque_cpu.append(self.cpu_percent)
        self.deque_ram.append(self.ram_percent)
        timeaxis_list = list(self.deque_timestamp)
        ram_list = list(self.deque_ram)
        if self.timestamp > self.graph_lim:
            self.graphwidget2.setRange(xRange=[self.timestamp - self.graph_lim + 1, self.timestamp],
                                       yRange=[min(ram_list[-self.graph_lim:]), max(ram_list[-self.graph_lim:])])
        self.set_plotdata(name="ram", data_x=timeaxis_list, data_y=ram_list)

    def show_cpu_graph(self):
        self.graphwidget2.hide()
        self.graphwidget1.show()
        self.start_cpu_graph()
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(True)
        self.pushButton.setStyleSheet("QPushButton" "{" "background-color : lightblue;" "}")
        self.pushButton_2.setStyleSheet(
            "QPushButton"
            "{"
            "background-color : rgb(255, 44, 174);"
            "}"
            "QPushButton"
            "{"
            "color : white;"
            "}"
        )

    def show_ram_graph(self):
        self.graphwidget1.hide()
        self.graphwidget2.show()
        self.start_ram_graph()
        self.pushButton_2.setEnabled(False)
        self.pushButton.setEnabled(True)
        self.pushButton_2.setStyleSheet("QPushButton" "{" "background-color : lightblue;" "}")
        self.pushButton.setStyleSheet(
            "QPushButton"
            "{"
            "background-color : rgba(0, 136, 255, 1);"
            "}"
            "QPushButton"
            "{"
            "color : white;"
            "}"
        )

    def set_plotdata(self, name, data_x, data_y):
        if name in self.traces:
            self.traces[name].setData(data_x, data_y)
        else:
            if name == "cpu":
                self.traces[name] = self.graphwidget1.getPlotItem().plot(pen=pg.mkPen((255, 17, 0), width=3))
            elif name == "ram":
                self.traces[name] = self.graphwidget2.getPlotItem().plot(pen=pg.mkPen((200, 0, 255), width=3))

    def setValue(self, value, labelPercentage, progressBarName, color):
        sliderValue = value
        htmlText = """<p align="center"><span style=" font-size:43pt;">
        {VALUE}</span><span style=" font-size:20pt; vertical-align:super;">%</span></p>"""
        labelPercentage.setText(htmlText.replace("{VALUE}", f"{sliderValue:.1f}"))
        self.progressBarValue(sliderValue, progressBarName, color)

    def progressBarValue(self, value, widget, color):
        styleSheet = """
        QFrame{
        	border-radius: 110px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} {COLOR});
        }
        """
        progress = (100 - value) / 100.0
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)
        if value == 100:
            stop_1 = "1.000"
            stop_2 = "1.000"
        newStylesheet = styleSheet.replace("{STOP_1}", stop_1).replace("{STOP_2}", stop_2).replace("{COLOR}", color)
        widget.setStyleSheet(newStylesheet)


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = uic.loadUi("splash_screen.ui", self)
        self.progressBarValue(0)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 120))
        self.ui.circularBg.setGraphicsEffect(self.shadow)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.start(15)
        self.show()

    def progress(self):
        global counter
        global jumper
        value = counter
        htmlText = """<p><span style=" font-size:55pt;">
        {VALUE}</span><span style=" font-size:30pt; vertical-align:super;">%</span></p>"""
        newHtml = htmlText.replace("{VALUE}", str(jumper))
        if (value > jumper):
            self.ui.labelPercentage.setText(newHtml)
            jumper += 10
        if value >= 100:
            value = 1.000
        self.progressBarValue(value)
        if counter == 10:
            self.main = MainWindow()
        if counter > 100:
            self.timer.stop()
            self.main.show()
            self.close()
        counter += 0.5

    def progressBarValue(self, value):
        styleSheet = """
        QFrame{
        	border-radius: 150px;
        	background-color: qconicalgradient(cx:0.5, cy:0.5, angle:90, stop:{STOP_1} rgba(255, 0, 127, 0), stop:{STOP_2} rgba(85, 170, 255, 255));
        }
        """
        progress = (100 - value) / 100.0
        stop_1 = str(progress - 0.001)
        stop_2 = str(progress)
        newStylesheet = styleSheet.replace(
            "{STOP_1}", stop_1).replace("{STOP_2}", stop_2)
        self.ui.circularProgress.setStyleSheet(newStylesheet)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
