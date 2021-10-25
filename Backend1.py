from Backend2 import Tablero, Pieza
from PyQt5.QtCore import QObject, pyqtSignal, QRect, QThread
from PyQt5.Qt import QTest
from PyQt5.QtGui import QPixmap
import parametros
from random import choice
import time

objetos = parametros.objetos_sprite
tam = parametros.Dim_label


class Character(QThread):

    update_position_signal = pyqtSignal(dict)
    update_money_signal = pyqtSignal()

    def __init__(self, x, y, tab):
        super().__init__()
        self._x = x
        self._y = y
        self.tablero = tab

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):

        if 0 < value < 600:
            self._y = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})
            print(self._x, self._y)

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):

        if 0 < value < 790:
            self._x = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})
            print(self._x, self._y)

    def move(self, event):

        if event == 'R':
            if not self.hay_obtaculo("R"):
                self.x += parametros.SPEED_PLAYER
        if event == 'L':
            if not self.hay_obtaculo("L"):
                self.x -= parametros.SPEED_PLAYER
        if event == 'Up':
            if not self.hay_obtaculo("Up"):
                self.y -= parametros.SPEED_PLAYER
        if event == "Down":
            if not self.hay_obtaculo("Down"):
                self.y += parametros.SPEED_PLAYER
        if self.tablero.hay_moneda(self._x//tam, self._y//tam, "Read"):
            print("HolaBart")
            self.tablero.hay_moneda(self._x//tam, self._y//tam, "Change")
            self.update_money_signal.emit()

    def hay_obtaculo(self, event):
        tablero = self.tablero
        if event == "R":
            x = self._x + 10
            y = self._y
            x = x // parametros.Dim_label
            y = y // parametros.Dim_label
            if tablero.pos(x, y) == "X" or tablero.pos(x, y) == "B" or \
                    tablero.pos(x, y) == "T":
                jug = QRect(self._x+10, self._y, 20, 20)
                obj = QRect(x*tam, y*tam, tam, tam)
                print(jug.intersects(obj))
                return jug.intersects(obj)
            else:
                return False

        elif event == "L":
            x = self._x - 10
            y = self._y
            x = x // parametros.Dim_label
            y = y // parametros.Dim_label
            if tablero.pos(x, y) == "X" or tablero.pos(x, y) == "B" or \
                    tablero.pos(x, y) == "T":
                jug = QRect(self._x-10, self._y, 20, 20)
                obj = QRect(x*tam, y*tam, tam, tam)
                print(jug.intersects(obj))
                return jug.intersects(obj)
            else:
                return False

        elif event == "Up":
            x = self._x
            y = self._y-10
            x = x // parametros.Dim_label
            y = y // parametros.Dim_label
            if tablero.pos(x, y) == "X" or tablero.pos(x, y) == "B" or \
                    tablero.pos(x, y) == "T":
                jug = QRect(self._x, self._y-10, 20, 20)
                obj = QRect(x*tam, y*tam, tam, tam)
                print(jug.intersects(obj))
                return jug.intersects(obj)
            else:
                return False

        elif event == "Down":
            x = self._x
            y = self._y + 10
            x = x // parametros.Dim_label
            y = y // parametros.Dim_label
            if tablero.pos(x, y) == "X" or tablero.pos(x, y) == "B" or \
                    tablero.pos(x, y) == "T":
                jug = QRect(self._x, self._y + 10, 20, 20)
                obj = QRect(x*tam, y*tam, tam, tam)
                print(jug.intersects(obj))
                return jug.intersects(obj)
            else:
                return False


class Moneda(QThread):
    def __init__(self, label, tablero):
        super().__init__()
        self.duracion = parametros.DURACION_MONEDA
        self.__position = (0, 0)
        self.label = label
        self.tablero = tablero
        self.libre = self.tablero.posiciones_libre
        self.torres = self.tablero.torres_construidas
        self.start()

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.__position = value
        x, y = value
        self.label.move(x*tam, y*tam)
        self.label.show()

    def run(self):
        variable = True
        eleccion = None
        while variable:
            eleccion = choice(list(self.libre))
            if eleccion not in self.torres:
                variable = False
        self.libre.remove(eleccion)
        self.tablero.piezas[eleccion[1]][eleccion[0]].moneda = True
        self.tablero.piezas[eleccion[1]][eleccion[0]].label = self.label
        self.position = eleccion
        time.sleep(self.duracion)
        self.libre.add(eleccion)
        self.tablero.piezas[eleccion[1]][eleccion[0]].moneda = False
        self.label.hide()
