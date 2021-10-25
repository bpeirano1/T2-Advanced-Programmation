from PyQt5.QtCore import QObject, pyqtSignal, QRect
from PyQt5.Qt import QTest


class Character(QObject):

    update_position_signal = pyqtSignal(dict)

    def __init__(self,  parent, x, y):
        super().__init__()
        self._x = x
        self._y = y

        # Se conecta la señal update_position con el metodo del parent (MainGame.update_position)
        self.update_position_signal.connect(parent.update_position)

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):

        if 0 < value < 400:
            self._y = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        """
        Chequea que la coordenada x se encuentre dentro de los parámetros y envía la señal
        update_position con las nuevas coordenadas.
        :param value: int
        :return: none
        """

        if 0 < value < 400:
            self._x = value
            self.update_position_signal.emit({'x': self.x, 'y': self.y})

    def move(self, event):

        ### esto lo saque del hint 7 del enunciado

        jug = QRect(self._x, self._y,1,1)
        obj = QRect(100, 100, 40, 40)

        if event == 'R':
            if QRect(self._x+10, self._y,10,10).intersects(obj):
                pass
            else:
                self.x += 10
        if event == 'L':
            if QRect(self._x-10, self._y,10,10).intersects(obj):
                pass
            else:
                self.x -= 10
        if event == 'Up':
            if QRect(self._x, self._y -10 ,10,10).intersects(obj):
                pass
            else:
                self.y -= 10
        if event == "Down":
            if QRect(self._x, self._y + 10,10,10).intersects(obj):
                pass
            else:
                self.y += 10

