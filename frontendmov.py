import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout
from PyQt5.QtGui import (QPixmap, QTransform)
from PyQt5.QtCore import QObject, pyqtSignal, Qt
from backendmov import Character

#### me base en la ayudantia del semestre pasado para los movimientos#####
#### es la ayudantia de mario

personaje_sprite = {"ab_1":"sprites/personaje/m/m_01.png",
                    "ab_2":"sprites/personaje/m/m_02.png",
                    "ab_3":"sprites/personaje/m/m_03.png",
                    "ar_1":"sprites/personaje/m/m_04.png",
                    "ar_2":"sprites/personaje/m/m_05.png",
                    "ar_3":"sprites/personaje/m/m_06.png",
                    "izq_1":"sprites/personaje/m/m_07.png",
                    "izq_2": "sprites/personaje/m/m_08.png",
                    "izq_3": "sprites/personaje/m/m_09.png"}

sprite_mapa ={"libre": "sprites/mapa/towerDefense_tile024.png",
              "camino": "sprites/mapa/towerDefense_tile093.png",
              "obstaculo": "sprites/mapa/towerDefense_tile128.png",
              "inicio":"sprites/mapa/towerDefense_tile113.png",
              "base": "sprites/mapa/towerDefense_tile084.png"}

class MainWindow(QWidget):

    move_character_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 400, 400)
        self._frame = 1
        self.rellenar_espacio_horizontal()
        self.agregar_obstaculo(100, 100)


        # Se instancia el personaje del backend y se conecta move_character_signal con la función
        # move de Character.
        self.backend_character = Character(self, 30, 30)
        self.move_character_signal.connect(self.backend_character.move)

        # Se crea el personaje en el frontend.
        self.front_character = QLabel(self)
        self.front_character.setPixmap(QPixmap(personaje_sprite["ab_1"]))
        self.front_character.move(30, 30)

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def rellenar_espacio_horizontal(self):

        for i in range(0,10):
            valor = 0
            while valor != 400:
                label = QLabel(self)
                label.setGeometry(valor,i*40, 40, 40)
                label.setPixmap(QPixmap(sprite_mapa["libre"]))
                label.setScaledContents(True)
                label.setVisible(True)
                valor += 40

    def agregar_obstaculo(self,i,j):
        label = QLabel(self)
        label.setGeometry(i, j , 40, 40)
        label.setPixmap(QPixmap(sprite_mapa["obstaculo"]))
        label.setScaledContents(True)
        label.setVisible(True)





    def keyPressEvent(self, e):
        self.frame += 1
        if e.key() == Qt.Key_D:
            imagen = QPixmap(personaje_sprite[f"izq_{self.frame}"])
            imagen = imagen.transformed(QTransform().scale(-1, 1))
            self.front_character.setPixmap(imagen)
            self.move_character_signal.emit('R')
        if e.key() == Qt.Key_A:
            self.front_character.setPixmap(
                QPixmap(personaje_sprite[f"izq_{self.frame}"]))
            self.move_character_signal.emit('L')
        if e.key() == Qt.Key_W:
            self.front_character.setPixmap(QPixmap(
                personaje_sprite[f"ar_{self.frame}"]))
            self.move_character_signal.emit('Up')
        if e.key() == Qt.Key_S:
            self.front_character.setPixmap(QPixmap(
                personaje_sprite[f"ab_{self.frame}"]))
            self.move_character_signal.emit("Down")


    def update_position(self, event):

        self.front_character.move(event['x'], event['y'])



if __name__ == '__main__':
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())


