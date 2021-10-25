from PyQt5.QtCore import QThread, QMutex, QMutexLocker
import parametros
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QPixmap, QTransform
import time
from random import randint, choice
enemigo = parametros.enemigo
kamikaze = parametros.kamikaze
tam = parametros.Dim_label


class Enemigo(QThread):

    trigger = pyqtSignal(tuple)
    danar_base_signal = pyqtSignal(int)
    signal_dead = pyqtSignal()
    lock = QMutex()

    def __init__(self, parent, camino, label, bar, tipo):
        super().__init__()
        self.label = label
        self.camino = camino
        self.tipo = tipo
        self._hp = parametros.HP_ENEMIGOS
        inicio = self.camino.pop(0)
        self.ataque = parametros.ATK_NORMAL
        self.__position = inicio
        self.pos = self.__position
        # self.trigger.connect(parent.actualizar_enemigo)
        # self.danar_base_signal.connect(parent.atacar_base)
        # self.signal_dead.connect(parent.update_muertos)
        self._frame = 1
        self.bar = bar
        self.bar.setMaximum(self._hp)
        self.bar.setValue(self._hp)
        self.bar.setGeometry(inicio[0]*tam, inicio[1]*tam - 10, 60, 5)
        self.start()

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value >= 0:
            self.bar.setValue(value)

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.frame += 1
        x_inicial, y_inicial = self.__position
        x_final, y_final = value
        if x_final - x_inicial == 1:
            imagen = QPixmap(enemigo[f'{self.tipo}izq_{self._frame}'])
            imagen = imagen.transformed(QTransform().scale(-1, 1))
        elif x_final - x_inicial == -1:
            imagen = QPixmap(enemigo[f'{self.tipo}izq_{self._frame}'])
        elif y_final - y_inicial == 1:
            imagen = QPixmap(enemigo[f'{self.tipo}ab_{self._frame}'])
        elif y_final - y_inicial == -1:
            imagen = QPixmap(enemigo[f'{self.tipo}ar_{self._frame}'])
        else:
            eleccion = choice(list(enemigo))
            while True:
                if int(eleccion[0]) == self.tipo:
                    break
                else:
                    eleccion = choice(list(enemigo))
            imagen = QPixmap(enemigo[eleccion])
        self.label.setPixmap(imagen)
        self.__position = value
        self.bar.move(x_final*tam, y_final*tam - 10)
        self.trigger.emit(({"x": value[0], "y": value[1]}, self.label))

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def run(self):
        while self.hp > 0:
            time.sleep(1)
            if not self.camino:
                if self.hp == 0:
                    break
                else:
                    time.sleep(1/parametros.SPD_NORMAL)
                    with QMutexLocker(self.lock):
                        self.danar_base_signal.emit(self.ataque)
                self.position = self.__position
                self.pos = self.__position
            else:
                nueva_posicion = self.camino.pop(0)
                self.position = nueva_posicion
                self.pos = nueva_posicion
        self.label.hide()
        self.bar.hide()
        self.label.deleteLater()
        self.bar.deleteLater()
        self.signal_dead.emit()
        self.quit()
        self.deleteLater()


class Kamikaze(QThread):

    trigger = pyqtSignal(tuple)
    danar_base_signal = pyqtSignal(int)
    signal_dead = pyqtSignal()
    signal_tdestroy = pyqtSignal(tuple)
    lock = QMutex()

    def __init__(self, parent, camino, label, tab, bar, tipo):
        super().__init__()
        self.label = label
        self.camino = camino
        self.tipo = tipo
        self._hp = parametros.HP_ENEMIGOS
        inicio = self.camino.pop(0)
        self.ataque = parametros.ATK_KAMIKAZE
        self.__position = inicio
        self.pos = self.__position
        # self.trigger.connect(parent.actualizar_enemigo)
        # self.danar_base_signal.connect(parent.atacar_base)
        # self.signal_dead.connect(parent.update_muertos)
        self._frame = 1
        self.tab = tab
        # self.signal_tdestroy.connect(parent.destroy_tower)
        self.p_adyacente = set()
        self.bar = bar
        self.bar.setMaximum(self._hp)
        # self.bar.setValue(self._hp)
        self.bar.setGeometry(inicio[0] * tam, inicio[1] * tam - 10, 60, 5)
        self.start()

    @property
    def hp(self):
        return self._hp

    @hp.setter
    def hp(self, value):
        self._hp = value
        if value >= 0:
            # self.bar.setValue(value)
            pass

    @property
    def position(self):
        return self.__position

    @position.setter
    def position(self, value):
        self.frame += 1
        x_inicial, y_inicial = self.__position
        x_final, y_final = value
        if x_final - x_inicial == 1:
            imagen = QPixmap(kamikaze[f'{self.tipo}izq_{self._frame}'])
            imagen = imagen.transformed(QTransform().scale(-1, 1))
        elif x_final - x_inicial == -1:
            imagen = QPixmap(kamikaze[f'{self.tipo}izq_{self._frame}'])
        elif y_final - y_inicial == 1:
            imagen = QPixmap(kamikaze[f'{self.tipo}ab_{self._frame}'])
        elif y_final - y_inicial == -1:
            imagen = QPixmap(kamikaze[f'{self.tipo}ar_{self._frame}'])
        else:
            imagen = QPixmap(kamikaze[choice(list(enemigo))])
        self.label.setPixmap(imagen)
        self.__position = value
        self.bar.move(x_final * tam, y_final * tam - 10)
        self.trigger.emit(({"x": value[0], "y": value[1]}, self.label))

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def completar_p_adyacente(self):
        nuevo_set = set()
        x, y = self.__position
        for i in range(1, 2):
            if x - i >= 0:
                nuevo_set.add((x-i, y))
            if x + i <= 19:
                nuevo_set.add((x + i, y))
            if y - i >= 0:
                nuevo_set.add((x, y - i))
            if y + i <= 15:
                nuevo_set.add((x, y + i))
        self.p_adyacente = nuevo_set

    def run(self):
        while self.hp > 0:
            time.sleep(1)
            if self.p_adyacente & self.tab.torres_construidas:
                interseccion = self.p_adyacente & self.tab.torres_construidas
                for line in list(interseccion):
                    self.signal_tdestroy.emit(line)
                self.label.setPixmap(
                    QPixmap("missprite/explosion").scaled(40, 40))
                time.sleep(1)
                self.hp = 0
            elif not self.camino:
                if self.hp == 0:
                    break
                else:
                    with QMutexLocker(self.lock):
                        self.danar_base_signal.emit(self.ataque)
                        self.hp = 0
                        self.label.setPixmap(
                            QPixmap("missprite/explosion").scaled(40, 40))
                        time.sleep(1)
            else:
                nueva_posicion = self.camino.pop(0)
                self.position = nueva_posicion
                self.pos = nueva_posicion
                self.completar_p_adyacente()
        self.label.hide()
        self.bar.hide()
        self.label.deleteLater()
        self.bar.deleteLater()
        self.signal_dead.emit()
        self.quit()
        self.deleteLater()







