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
from Frontend2 import crear_tablero_extra, key_press_event_extra, \
    mouse_press_event_extra, mouse_release_event_extra, mouse_move_event_extra
import random
import time
from Backend5 import Base, write_top
from parametros import GENERACION_1, GENERACION_2, COSTO_TORRE_R,\
    COSTO_TORRE_F, DINERO_INICIAL, SPRITE_MAPA, PERSONAJE_SPRITE, Dim_label,\
    RUTA_MAPA, COSTO_MEJORA_ALCANCE, COSTO_MEJORA_ATAQUE, TIEMPO_ENEMIGO

sprite_mapa, personaje_sprite = SPRITE_MAPA, PERSONAJE_SPRITE
base = parametros.base
t_sprite = parametros.torres_sprite
objetos = parametros.objetos_sprite
kamikaze, enemigo = parametros.kamikaze, parametros.enemigo
tam = Dim_label

window_name2, base_class2 = uic.loadUiType("ventana_juego.ui")


class GameWindow(window_name2, base_class2, QWidget):

    move_character_signal = pyqtSignal(str)
    update_mapa_backend = pyqtSignal(tuple)
    monedas_interfaz = DINERO_INICIAL
    monedas_ronda = 0
    ronda_activa = False
    n_muertos = 0
    n_ronda = 1
    arrastrar = False
    objeto_arrastrable = None
    eliminar_torre = (False, 0, 0)
    cheat_moenda = (False, False)
    cheat_ronda = (False, False)
    points = 0
    tdestroy_ronda = 0
    edestroy_ronda = 0
    mejoras = [False, False]

    def __init__(self, nombre, tipo, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.setupUi(self)
        self.setFixedSize(1000, 600)
        self.usuario = nombre
        self.tipo = tipo
        QSound.play("furelise.wav")
        # Intancio Tablero Backend
        self.tablero_back = Tablero(RUTA_MAPA)
        self.tablero_back.crear_tablero()
        self.camino_corto = self.tablero_back.ruta_corta()
        self.caminos = self.tablero_back.caminos()
        # se crea un diccionario del tablero del frontend
        self.tab_front = dict()
        self.crear_tablero_front()
        # se crea las opciones del lado
        self.nombre.setText(f"Usuario: {nombre}")
        self.dinero.setPixmap(QPixmap(objetos['moneda']).scaled(tam, tam))
        self.dinero_label.setText(f'{self.monedas_interfaz}')
        self.torre1.setPixmap(QPixmap(t_sprite["t_1"]).scaled(tam, tam))
        self.torre2.setPixmap(QPixmap(t_sprite["t_2"]).scaled(tam, tam))
        # Conecto el boton
        self.Bempezar_ronda.clicked.connect(self.ronda)
        # para no hacer atributos dinamicos
        self._frame, self.backend_character = 0, None
        self.front_character = None
        self.contador, self.regulador = 0, 1
        self.timer, self.timer2 = None, None
        self.pbar_enem = None
        self.imagen = None
        # enemeigos
        self.enemigo, self.enemigos, self.label_enemigo = None, [], None
        # base
        self.progressbar_base = QProgressBar(self)
        self.progressbar_base.setGeometry(self.tablero_back.posicion_base[0] *
                                          tam,
                                          self.tablero_back.posicion_base[1] *
                                          tam + tam, 120, 5)
        self.base = Base(self.progressbar_base)
        # torres
        self.label_torre1.setText(f'Racimo: ${COSTO_TORRE_R}')
        self.label_torre2.setText(f'Francotiradora: ${COSTO_TORRE_F}')
        self.torres_front, self.torres_destruidas = {}, []
        # Mejoras
        self.Bmejora_alcance.setText(f'Mejora $ {COSTO_MEJORA_ALCANCE}')
        self.Bmejora_ataque.setText(f'Mejora $ {COSTO_MEJORA_ATAQUE}')
        # monedas threads
        self.monedas = []
        # conectando señales
        self.update_mapa_backend.connect(self.tablero_back.actualizar_torre)
        self.Bcerrar_sesion.clicked.connect(self.cerrar_sesion)
        self.Bmejora_alcance.clicked.connect(self.mejora_1)
        self.Bmejora_ataque.clicked.connect(self.mejora_2)
        self.c_top10 = 0
        # Ronda
        self.n_enemigos = ((self.n_ronda - 1) * GENERACION_1) + GENERACION_2
        self.enemigos_proximos.setText(f"Enemigos Proximos: {self.n_enemigos}")

# properties que usa la clase Character del Backend1, se instancia en el metodo,
    # crear_personaje()

    @property
    def frame(self):
        return self._frame

    @frame.setter
    def frame(self, value):
        if value > 3:
            self._frame = 1
        else:
            self._frame = value

    def keyPressEvent(self, e):
        key_press_event_extra(self, e)

    def mousePressEvent(self, event):
        mouse_press_event_extra(self, event)

    def mouseMoveEvent(self, event):
        mouse_move_event_extra(self, event)

    def mouseReleaseEvent(self, event):
        mouse_release_event_extra(self, event)

    def crear_tablero_front(self):
        crear_tablero_extra(self)

    def ronda(self):
        self.Bmejora_alcance.setEnabled(False)
        self.Bmejora_ataque.setEnabled(False)
        self.enemigos_proximos.setText(f"Enemigos Proximos: ")
        self.label_ronda.setText(f'{self.n_ronda}')
        self.Bempezar_ronda.setEnabled(False)
        for i in range(len(self.enemigos)):
            obj = self.enemigos.pop(0)
            del obj
        self.progressBar.show()
        self.ronda_activa = True
        self.n_enemigos = ((self.n_ronda - 1)*GENERACION_1) + GENERACION_2
        self.progressBar.setMaximum(self.n_enemigos)
        self.progressBar.setValue(0)
        self.crear_personaje()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.crear_monedas)
        self.timer.start(parametros.TIEMPO_MONEDA*1000)
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.crear_enemigo)
        self.contador, self.regulador = 0, 1
        self.timer2.start(1000 * TIEMPO_ENEMIGO)

    def acabar_ronda(self):
        muertos = self.n_muertos
        self.contador = self.n_enemigos + 1
        for line, label in self.enemigos:
            line.hp = 0
        self.n_muertos = self.n_muertos + 1
        self.update_muertos()

    def crear_enemigo(self):
        self.contador += 1
        if self.contador > self.n_enemigos:
            self.timer2.stop()
            return
        camino, lista = random.choice(self.caminos), []
        for line in camino:
            lista.append(line)
        x, y = lista[0]
        self.label_enemigo, self.pbar_enem = QLabel(self), QProgressBar(self)
        self.label_enemigo.setGeometry(x * tam + 10, y * tam + 10, 25, 25)
        if self.regulador > 3:
            self.regulador = 1
            self.enemigo = Kamikaze(self, lista, self.label_enemigo,
                                    self.tablero_back, self.pbar_enem,
                                    self.tipo)
            self.imagen = QPixmap(kamikaze[f"{self.tipo}ab_1"])
            self.enemigo.signal_tdestroy.connect(self.destroy_tower)
        else:
            self.enemigo = Enemigo(self, lista, self.label_enemigo,
                                   self.pbar_enem, self.tipo)
            self.imagen = QPixmap(enemigo[f"{self.tipo}ab_1"])
        self.label_enemigo.setPixmap(self.imagen)
        self.regulador += 1
        self.label_enemigo.show()
        self.pbar_enem.show()
        self.enemigo.trigger.connect(self.actualizar_enemigo)
        self.enemigo.danar_base_signal.connect(self.atacar_base)
        self.enemigo.signal_dead.connect(self.update_muertos)
        self.enemigos.append((self.enemigo, self.label_enemigo))

    def crear_personaje(self):
        self._frame = 1
        self.backend_character = Character(500, 500, self.tablero_back)
        self.backend_character.update_position_signal.connect(
            self.update_position)
        self.backend_character.update_money_signal.connect(self.update_money)
        self.move_character_signal.connect(self.backend_character.move)
        # Se crea el personaje en el frontend.
        self.front_character = QLabel(self)
        self.front_character.setGeometry(500, 500, 20, 20)
        self.front_character.setPixmap(QPixmap(personaje_sprite["ab_1"]))
        self.front_character.show()

    def crear_monedas(self):
        if not self.ronda_activa:
            self.timer.stop()
        label = QLabel(self)
        label.setPixmap(QPixmap(objetos["moneda"]).scaled(40, 40))
        label.show()
        moneda = Moneda(label, self.tablero_back)
        if not self.ronda_activa:
            label.hide()
        self.monedas.append(moneda)

    def update_position(self, event):
        self.front_character.move(event['x'], event['y'])

    def update_money(self):
        self.monedas_interfaz += 1
        self.monedas_ronda += 1
        self.dinero_label.setText(f'{self.monedas_interfaz}')

    def update_muertos(self):
        self.n_muertos += 1
        self.progressBar.setValue(self.n_muertos)
        if self.n_muertos == self.n_enemigos:
            self.edestroy_ronda = self.n_muertos
            self.actualizar_points()
            self.n_muertos, self.ronda_activa = 0, False
            self.Bempezar_ronda.setEnabled(True)
            self.n_ronda += 1
            self.regulador = 1
            self.n_enemigos = ((self.n_ronda - 1) * GENERACION_1) + GENERACION_2
            self.enemigos_proximos.setText(
                f"Enemigos Proximos: {self.n_enemigos}")
            if not self.mejoras[0]:
                self.Bmejora_alcance.setEnabled(True)
            if not self.mejoras[1]:
                self.Bmejora_ataque.setEnabled(True)
            for coin in self.monedas:
                coin.label.hide()
            if self.n_ronda > 1:
                self.front_character.deleteLater()
                self.backend_character.deleteLater()
            i = 0
            largo = len(self.monedas)
            while i < largo:
                print(self.monedas[0].isFinished())
                if self.monedas[0].isFinished():
                    objeto = self.monedas.pop(0)
                    objeto.deleteLater()
                i += 1
            print(self.monedas)

    def actualizar_enemigo(self, tupla):
        event, label = tupla
        label.move(event["x"] * tam + tam//4, event["y"] * tam + tam//4)

    def actualizar_points(self):
        puntos = ((self.monedas_ronda * self.base.hp) //
                  (self.tdestroy_ronda + 1)) + self.edestroy_ronda
        self.points += puntos
        self.puntos.setText(f'Puntos: {self.points}')
        print(self.monedas_ronda)
        print(self.base.hp)
        print(self.tdestroy_ronda)
        print(self.edestroy_ronda)
        msg = QMessageBox(self)
        msg.setText(f"Datos Ronda:\n\nMonedas de la ronda: {self.monedas_ronda}"
                    f"\nTorres Destruidas: {self.tdestroy_ronda} "
                    f"\nEnemigos Destruidos: {self.edestroy_ronda} "
                    f"\nPuntos de la ronda: {puntos} "
                    f"\nPuntos Totales: {self.points}")
        msg.exec()
        self.monedas_ronda, self.tdestroy_ronda, self.edestroy_ronda = 0, 0, 0

    def destroy_tower(self, tupla):
        self.tdestroy_ronda += 1
        self.torres_front[tupla][1].viva = False
        self.tablero_back.torres_construidas.remove(tupla)
        self.tablero_back.posibles_torres.add(tupla)
        self.update_mapa_backend.emit((tupla[0], tupla[1], "E"))
        self.torres_destruidas.append(self.torres_front[tupla])
        del self.torres_front[tupla]

    def atacar_base(self, event):
        if self.base.hp > 0:
            self.base.hp -= event
            self.base.bar.setValue(self.base.hp)
        else:
            self.c_top10 += 1
            if self.c_top10 == 1:
                self.points += self.n_muertos
                msg = QMessageBox(self)
                msg.setText(f" HAS PERDIDO EL JUEGO\n\nDatos Ultima Ronda:"
                            f"\n\nMonedas de la ronda: {self.monedas_ronda}"
                            f"\nTorres Destruidas: {self.tdestroy_ronda} "
                            f"\nEnemigos Destruidos: {self.n_muertos} "
                            f"\nPuntos de la ronda: {self.n_muertos} "
                            f"\nPuntos Totales: {self.points}")
                msg.exec()
                write_top(self.usuario, self.points)
                self.close()

    def atacar_enemigo(self, event):
        enemy, dano = event
        if enemy.hp > 0:
            enemy.hp -= dano

    def cerrar_sesion(self):
        msg = QMessageBox(self)
        msg.setText(f"HAS CERRADO LA SESION, NO OBTIENES PUNTOS POR LA "
                    f"ULTIMA RONDA\n\nPuntos Totales: {self.points}")
        msg.exec()
        write_top(self.usuario, self.points)
        self.close()

    def mejora_1(self):
        if self.monedas_interfaz >= COSTO_MEJORA_ALCANCE:
            self.monedas_interfaz -= COSTO_MEJORA_ALCANCE
            self.mejoras[0] = True
            self.Bmejora_alcance.setEnabled(False)
            self.dinero_label.setText(f'{self.monedas_interfaz}')
            for label, torre in self.torres_front.values():
                torre.f_aumento_alcance()
        else:
            QMessageBox.warning(self, "", "No le alcanza el dinero para mejora"
                                          " de alcance")

    def mejora_2(self):
        if self.monedas_interfaz >= COSTO_MEJORA_ATAQUE:
            self.mejoras[1] = True
            self.Bmejora_ataque.setEnabled(False)
            self.monedas_interfaz -= COSTO_MEJORA_ATAQUE
            self.dinero_label.setText(f'{self.monedas_interfaz}')
            for label, torre in self.torres_front.values():
                torre.f_aumento_ataque()
        else:
            QMessageBox.warning(self, "", "No le alcanza el dinero para mejora"
                                          " de ataque")

    def mostrar_label(self, event):
        label, tipo = event
        if tipo == "E":
            label.hide()
        if tipo == "M":
            label.show()
