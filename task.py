from math import (cos, sin, atan, pi, sqrt)
from PyQt6.QtWidgets import *
from PyQt6.QtCore import Qt

g = 9.80655
dB = 0.00001


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Catapult calculator")
        container = QWidget()

        self.mainLayout = QVBoxLayout()

        self.spoon_len = self.newOption("Длина ложки (см)", 0.15)
        self.spring_len = self.newOption("Длина пружины (см)", 0.0837)
        self.spoon_mass = self.newOption("Масса ложки (г)", 0.06)
        self.bullet_mass = self.newOption("Масса снаряда (г)", 0.06)
        self.k = self.newOption("Жесткость пружины (Н/м)", 358.0)
        self.x = self.newOption("Отступ по горизонтали (см)", 0.0571)
        self.h = self.newOption("Высота крепления пружины (см)", 0.0785)
        self.mount = self.newOption("Расстояние от оси до крепления к ложке (см)", 0.0949)
        self.alpha = self.newOption("Начальный угол (градус)", 34.0)

        self.mainLayout.addItem(QSpacerItem(0, 10, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))
        calc_button = QPushButton("Расчет")
        calc_button.clicked.connect(self.calc)
        self.mainLayout.addWidget(calc_button)

        container.setLayout(self.mainLayout)
        self.setCentralWidget(container)

        self.setMinimumSize(300, 300)

    def calc(self):
        ms = self.bullet_mass.value()
        ml = self.spoon_mass.value()
        x = self.x.value()
        lx = self.h.value()
        l_fr = self.mount.value()
        lp = self.spring_len.value()
        l0 = self.spoon_len.value()
        k = self.k.value()
        alpha = self.alpha.value()
        gamma = 90
        A = 0
        


        Fm=ms*g

        Fl=ml*g
        alpha = alpha*pi/180
        gamma = gamma*pi/180
        i=alpha
        while i<gamma:
            l1 = x+cos(i)*l_fr
            l2 = lx-sin(i)*l_fr
            lpu = sqrt(l1*l1+l2*l2)

            dx = lpu-lp
            Fy=k*dx
            u = atan(l2/l1)
            omega = pi/2-i-u
            Fyx = cos(omega)*Fy

            Fmx=Fm*cos(i)
            Flx=Fl*cos(i)
            F0=Fyx*l_fr/l0-Fmx-Flx
            dl=dB*l0




            #print(F0,dx)
            if (F0<0):
                print("конечный угол= ",i*180/pi)
                gamma = i
                break
            A+=F0*dl
            i+=dB

        print("====================")
        print(A)
        
        m0=ms/2+ml/3
        A/=m0


        h1 = sin(gamma)*l0+0.01435



        V0= sqrt(A)


        Vy = cos(gamma)*V0
        Vx = sin(gamma)*V0


        D = Vy*Vy+2*h1*g

        t =(sqrt(D)+ Vy)/(g)

        print(t)
        S = t*Vx-cos(gamma)*l0-x

        msg = QMessageBox()
        msg.setWindowTitle("Результат")
        msg.setText(f'''
        Конечный угол: {round(gamma*180/pi, 3)} градусов
        Расстояние: {round(S, 3)} м
        Время полета: {round(t, 3)} с
        Работа: {round(A, 3)} Дж
        ''')
        msg.exec()
    
    def newOption(self, name, default = 0):
        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignmentFlag.AlignTop)
        w = QDoubleSpinBox()
        
        w.setDecimals(4)
        w.setMinimum(0)
        w.setMaximum(1000)
        w.setValue(default)
        w.setFixedSize(70, 20)
        w.setAlignment(Qt.AlignmentFlag.AlignRight)
        lab = QLabel(name)
        lay.addWidget(lab)
        lay.addWidget(w)
        self.mainLayout.addLayout(lay)
        return w

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
