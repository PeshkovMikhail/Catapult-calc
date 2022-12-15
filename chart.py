from PyQt6.QtWidgets import *
from PyQt6.QtCharts import QChart, QChartView, QLineSeries, QValueAxis
from PyQt6.QtCore import Qt, QRect
from math import pi, cos
from numpy import arange

class Chart(QWidget):
    def __init__(self, A, Vx, Vy, t, S, gamma, h1, l0, x):
        super().__init__()
        self.setWindowTitle("Результаты")

        self.Vx = Vx
        self.Vy = Vy
        self.h = h1
        self.gamma=gamma
        self.l0 = l0
        self.x_coord = x

        h_max = Vy**2/(2*9.81)
        y_axis = QValueAxis()
        y_axis.setRange(0, h_max*100 + 10)
        y_axis.setLabelFormat("%0.2f")
        y_axis.setTickCount(1)
        y_axis.setMinorTickCount(0)
        y_axis.setTitleText("Высота")

        x_axis = QValueAxis()
        x_axis.setRange(-10, S*100+ 10)
        x_axis.setLabelFormat("%0.2f")
        x_axis.setTickCount(1)
        x_axis.setMinorTickCount(0)
        x_axis.setTitleText("Расстояние")

        coord_series = QLineSeries()
        coord_series.setName("Траектория")
        
        for time in arange(0, t+0.01, 0.01):
            coord_series.append(self.x(time)*100, self.y(time)*100)
        
        chart = QChart()
        chart.legend().setVisible(True)
        chart.addSeries(coord_series)
        chart.addAxis(x_axis, Qt.AlignmentFlag.AlignBottom)
        chart.addAxis(y_axis, Qt.AlignmentFlag.AlignLeft)
        chartView = QChartView()
        chartView.setGeometry(QRect(100, 100, 680, 500))
        info = QLabel(f'''
        Конечный угол: {round(gamma*180/pi, 3)} градусов
        Расстояние: {round(S, 3)} м
        Время полета: {round(t, 3)} с
        Работа: {round(A, 3)} Дж
        ''')
        
        chartView.setChart(chart)
        

        main_layout = QHBoxLayout()
        main_layout.addWidget(chartView)
        main_layout.addWidget(info)

        self.setLayout(main_layout)

    def x(self, t):
        return self.Vx * t - cos(self.gamma)*self.l0-self.x_coord

    def y(self, t):
        return (self.h + self.Vy * t - 9.81*t**2/2)
