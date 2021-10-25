import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox, QLabel, QWidget,
                             QProgressBar)
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtMultimedia import QSound
import parametros
from Backend1 import Character, Moneda
from Backend2 import Tablero, Pieza
from Backend3 import Enemigo, Kamikaze
from Backend4 import TorreRacimo, TorreFranco
import random
import time
from Backend5 import Base, write_top
from parametros import GENERACION_1, GENERACION_2, COSTO_TORRE_R, \
    COSTO_TORRE_F, DINERO_INICIAL, SPRITE_MAPA, PERSONAJE_SPRITE, Dim_label,\
    RUTA_MAPA

sprite_mapa, personaje_sprite = SPRITE_MAPA, PERSONAJE_SPRITE
base = parametros.base
t_sprite = parametros.torres_sprite
objetos = parametros.objetos_sprite
kamikaze, enemigo = parametros.kamikaze, parametros.enemigo
tam = Dim_label


def crear_tablero_extra(self):
    mapa = self.tablero_back
    fila, columnas = len(mapa.piezas), len(mapa.piezas[0])
    posiciones = []
    for i in range(fila):
        for j in range(columnas):
            posiciones.append((j, i))
    for posicion in posiciones:
        i, j = posicion
        if mapa.pos(*posicion) == "X":
            label = QLabel(self)
            label.setGeometry(i * tam, j * tam, tam, tam)
            pixmap = QPixmap(sprite_mapa["obstaculo"]).scaled(tam, tam)
            label.setPixmap(pixmap)
            self.tab_front[posicion] = label
        elif mapa.pos(*posicion) == "C":
            label = QLabel(self)
            label.setGeometry(i * tam, j * tam, tam, tam)
            pixmap = QPixmap(sprite_mapa["camino"]).scaled(tam, tam)
            label.setPixmap(pixmap)
            self.tab_front[posicion] = label
        elif mapa.pos(*posicion) == "S":
            label = QLabel(self)
            label.setGeometry(i * tam, j * tam, tam, tam)
            pixmap = QPixmap(sprite_mapa["inicio"]).scaled(tam, tam)
            label.setPixmap(pixmap)
            self.tab_front[posicion] = label
        elif mapa.pos(*posicion) == "B":
            fondo = QLabel(self)
            fondo.setGeometry(i * tam, j * tam, tam, tam)
            pix = QPixmap(sprite_mapa["inicio"]).scaled(tam, tam)
            fondo.setPixmap(pix)
            if mapa.pos(i + 1, j) == "B" and mapa.pos(i, j + 1) == "B":
                label = QLabel(self)
                label.setGeometry(i * tam, j * tam, tam, tam)
                pixmap = QPixmap(base[f"{self.tipo}ar_iz"]).scaled(tam, tam)
                label.setPixmap(pixmap)
                self.tab_front[posicion] = label
            elif mapa.pos(i + 1, j) == "B" and mapa.pos(i, j - 1) == "B":
                label = QLabel(self)
                label.setGeometry(i * tam, j * tam, tam, tam)
                pixmap = QPixmap(base[f"{self.tipo}ab_iz"]).scaled(tam, tam)
                label.setPixmap(pixmap)
                self.tab_front[posicion] = label
                self.tablero_back.posicion_base = posicion
            elif mapa.pos(i - 1, j) == "B" and mapa.pos(i, j + 1) == "B":
                label = QLabel(self)
                label.setGeometry(i * tam, j * tam, tam, tam)
                pixmap = QPixmap(base[f"{self.tipo}ar_de"]).scaled(tam, tam)
                label.setPixmap(pixmap)
                self.tab_front[posicion] = label
            elif mapa.pos(i - 1, j) == "B" and mapa.pos(i, j - 1) == "B":
                label = QLabel(self)
                label.setGeometry(i * tam, j * tam, tam, tam)
                pixmap = QPixmap(base[f"{self.tipo}ab_de"]).scaled(tam, tam)
                label.setPixmap(pixmap)
                self.tab_front[posicion] = label
        else:
            label = QLabel(self)
            label.setGeometry(i * tam, j * tam, tam, tam)
            pixmap = QPixmap(sprite_mapa["libre"]).scaled(tam, tam)
            label.setPixmap(pixmap)
            self.tab_front[posicion] = label


def key_press_event_extra(self, e):
    if self.ronda_activa:
        self.frame += 1
        if e.key() == Qt.Key_D:
            if self.cheat_ronda == (True, True):
                self.acabar_ronda()
                self.cheat_ronda = (False, False)
            else:
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
        if e.key() == Qt.Key_E:
            self.cheat_ronda = (True, False)
        elif e.key() == Qt.Key_N:
            self.cheat_ronda = (True, True)
        else:
            self.cheat_ronda = (False, False)

    if e.key() == Qt.Key_L:
        self.acabar_ronda()
    if e.key() == Qt.Key_M:
        self.cheat_moenda = (True, False)
    elif e.key() == Qt.Key_O and self.cheat_moenda == (True, False):
        self.cheat_moenda = (True, True)
    elif e.key() == Qt.Key_N and self.cheat_moenda == (True, True):
        self.monedas_interfaz += parametros.DINERO_TRAMPA
        self.dinero_label.setText(f'{self.monedas_interfaz}')
        self.cheat_moenda = (False, False)
    else:
        self.cheat_moenda = (False, False)


def mouse_press_event_extra(self, event):
    tam2 = parametros.Dim_label_menu
    torre1, torre2 = parametros.torre1, parametros.torre2
    x, y = event.x()//tam2, event.y()//tam2
    if x == torre1[0] and y == torre1[1] and not self.ronda_activa:
        self.arrastrar, fram = True, 1
    elif x == torre2[0] and y == torre2[1] and not self.ronda_activa:
        self.arrastrar, fram = True, 2
    if self.arrastrar:
        label = QLabel(self)
        label.setGeometry(x*tam2, y*tam2, tam2, tam2)
        label.setPixmap(QPixmap(t_sprite[f"t_{fram}"]).scaled(tam2, tam2))
        label.show()
        self.objeto_arrastrable = (label, fram)
    if (x, y) in self.tablero_back.torres_construidas:
        self.eliminar_torre = (True, x, y)


def mouse_move_event_extra(self, event):
    tam2 = parametros.Dim_label_menu
    if self.arrastrar:
        self.objeto_arrastrable[0].move(event.x()-tam2/2, event.y()-tam2/2)


def mouse_release_event_extra(self, event):
    x, y = event.x()//tam, event.y()//tam
    if self.arrastrar and ((x, y) in self.tablero_back.posibles_torres):
        if self.objeto_arrastrable[1] == 1:
            costo = COSTO_TORRE_R
        else:
            costo = COSTO_TORRE_F
        if self.monedas_interfaz >= costo:
            self.monedas_interfaz -= costo
            self.dinero_label.setText(f'{self.monedas_interfaz}')
            self.objeto_arrastrable[0].move(x*tam, y*tam)
            self.tablero_back.torres_construidas.add((x, y))
            self.tablero_back.posibles_torres.remove((x, y))
            self.label_atacando = QLabel(self)
            self.label_atacando.setGeometry(tam*x, tam*y - 10, 60, 10)
            self.label_atacando.setText("Atacando")
            self.label_atacando.hide()
            label = self.objeto_arrastrable[0]
            if self.objeto_arrastrable[1] == 1:
                self.torres_front[(x, y)] = (label,
                                             TorreRacimo(self.enemigos, (x, y),
                                                         label,
                                                         self.label_atacando))
            elif self.objeto_arrastrable[1] == 2:
                self.torres_front[(x, y)] = (label,
                                             TorreFranco(self.enemigos, (x, y),
                                                         label,
                                                         self.label_atacando))
            self.torres_front[(x, y)][1].signal_label_ataque.connect(
                self.mostrar_label)
            self.torres_front[(x, y)][1].signal_atack.connect(
                self.atacar_enemigo)
            self.update_mapa_backend.emit((x, y, "A"))
            self.objeto_arrastrable, self.arrastrar = None, False
        else:
            self.objeto_arrastrable[0].deleteLater()
            self.objeto_arrastrable, self.arrastrar = None, False
    elif self.arrastrar:
        self.objeto_arrastrable[0].deleteLater()
        self.objeto_arrastrable, self.arrastrar = None, False
    if self.eliminar_torre[0]:
        if x == self.eliminar_torre[1] and y == self.eliminar_torre[2] and \
                self.ronda_activa:
            self.tablero_back.torres_construidas.remove((x, y))
            self.tablero_back.posibles_torres.add((x, y))
            label = self.torres_front[(x, y)][0]
            label.setPixmap(QPixmap(objetos["explosion"]).scaled(tam, tam))
            self.torres_front[(x, y)][1].viva = False
            del self.torres_front[(x, y)]
            self.eliminar_torre = (False, 0, 0)
            self.update_mapa_backend.emit((x, y, "E"))
        elif x == self.eliminar_torre[1] and y == self.eliminar_torre[2] \
                and not self.ronda_activa:
            self.tablero_back.torres_construidas.remove((x, y))
            self.tablero_back.posibles_torres.add((x, y))
            label = self.torres_front[(x, y)][0]
            label.hide()
            self.torres_front[(x, y)][1].viva = False
            del self.torres_front[(x, y)]
            self.eliminar_torre = (False, 0, 0)
            self.update_mapa_backend.emit((x, y, "E"))
        else:
            self.eliminar_torre = (False, 0, 0)
