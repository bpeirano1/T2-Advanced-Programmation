from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from parametros import ATK_RACIMO, SPD_RACIMO, MEJORA_ALCANCE, MEJORA_ATAQUE, \
    ATK_FRANCOTIRADORA, SPD_FRANCOTIRADORA, TIEMPO_ATAQUE_TORRE, Dim_label
import time
from PyQt5.QtGui import QPixmap

tam = Dim_label


class TorreFranco(QThread):
    signal_atack = pyqtSignal(tuple)
    signal_label_ataque = pyqtSignal(tuple)

    def __init__(self, enemigos, posicion, label, label_ataque):
        super().__init__()
        self.viva = True
        self.label = label
        self.mejora_alcance = False
        self.mejora_ataque = False
        self.posicion = posicion
        self.ataque = ATK_FRANCOTIRADORA
        self.enemigos = enemigos
        self.alcance = 3
        self.posiciones_alcance = set()
        self.completar_posiciones_alcance()
        # self.signal_atack.connect(parent.atacar_enemigo)
        self.hay_enemigo = False
        self.enemigo_a_atacar = None
        self.label_atacando = label_ataque
        self.start()

    def completar_posiciones_alcance(self):
        radio = self.alcance // 2
        x, y = self.posicion
        for i in range(1, radio + 1):
            if x - i >= 0:
                self.posiciones_alcance.add((x - i, y))
            if x + i <= 19:
                self.posiciones_alcance.add((x + i, y))
            if y - i >= 0:
                self.posiciones_alcance.add((x, y - i))
            if y + i <= 15:
                self.posiciones_alcance.add((x, y + i))
            if x - i >= 0 and y - i >= 0:
                self.posiciones_alcance.add((x - i, y - i))
            if x - i >= 0 and y + i <= 15:
                self.posiciones_alcance.add((x - i, y + i))
            if x + i <= 19 and y - i >= 0:
                self.posiciones_alcance.add((x + i, y - i))
            if x + i <= 19 and y + i <= 15:
                self.posiciones_alcance.add((x + i, y + i))

    def f_aumento_alcance(self):
        if not self.mejora_alcance:
            self.mejora_alcance = True
            self.alcance += MEJORA_ALCANCE
            self.completar_posiciones_alcance()

    def f_aumento_ataque(self):
        if not self.mejora_ataque:
            self.mejora_ataque = True
            self.ataque += MEJORA_ATAQUE

    def time_out_aviso_ataque(self):
        self.label_atacando.hide()

    def run(self):
        while self.viva:
            time.sleep(1/SPD_FRANCOTIRADORA)
            if self.hay_enemigo and self.enemigo_a_atacar.pos in \
                    self.posiciones_alcance:
                if self.enemigo_a_atacar.hp > 0:

                    print(f' antes de ataque el hp es '
                          f'{self.enemigo_a_atacar.hp}')
                    self.signal_label_ataque.emit((self.label_atacando, "M"))
                    self.signal_atack.emit((self.enemigo_a_atacar, self.ataque))
                    print(f' despues ataque el hp {self.enemigo_a_atacar.hp}')
                    time.sleep(TIEMPO_ATAQUE_TORRE)
                    self.signal_label_ataque.emit((self.label_atacando, "E"))
                else:
                    self.enemigo_a_atacar = None
                    self.hay_enemigo = False
            else:
                for enemigo, label in self.enemigos:
                    if enemigo.pos in self.posiciones_alcance:
                        if enemigo.hp > 0:
                            if not self.hay_enemigo:
                                self.hay_enemigo = True
                                self.enemigo_a_atacar = enemigo
                                print(
                                    f' antes de ataque el hp es '
                                    f'{self.enemigo_a_atacar.hp}')
                                self.signal_label_ataque.emit(
                                    (self.label_atacando, "M"))
                                self.signal_atack.emit(
                                    (self.enemigo_a_atacar, self.ataque))
                                time.sleep(TIEMPO_ATAQUE_TORRE)
                                self.signal_label_ataque.emit(
                                    (self.label_atacando, "E"))
                                print(
                                    f' despues ataque el hp '
                                    f'{self.enemigo_a_atacar.hp}')
        self.label.setPixmap(
            QPixmap("missprite/explosion").scaled(40, 40))
        time.sleep(1)
        self.label.hide()
        self.label.deleteLater()
        self.quit()
        self.deleteLater()


class TorreRacimo(QThread):
    signal_atack = pyqtSignal(tuple)
    signal_label_ataque = pyqtSignal(tuple)

    def __init__(self, enemigos, posicion, label, label_ataque):
        super().__init__()
        self.viva = True
        self.label = label
        self.mejora_alcance = False
        self.mejora_ataque = False
        self.posicion = posicion
        self.ataque = ATK_RACIMO
        self.enemigos = enemigos
        self.alcance = 3
        self.posiciones_alcance = set()
        self.completar_posiciones_alcance()
        self.label_atacando = label_ataque
        # self.signal_atack.connect(parent.atacar_enemigo)
        self.start()

    def completar_posiciones_alcance(self):
        radio = self.alcance//2
        x, y = self.posicion
        for i in range(1, radio + 1):
            if x - i >= 0:
                self.posiciones_alcance.add((x-i, y))
            if x + i <= 19:
                self.posiciones_alcance.add((x + i, y))
            if y - i >= 0:
                self.posiciones_alcance.add((x, y - i))
            if y + i <= 15:
                self.posiciones_alcance.add((x, y + i))
            if x - i >= 0 and y - i >= 0:
                self.posiciones_alcance.add((x - i, y - i))
            if x - i >= 0 and y + i <= 15:
                self.posiciones_alcance.add((x - i, y + i))
            if x + i <= 19 and y - i >= 0:
                self.posiciones_alcance.add((x + i, y - i))
            if x + i <= 19 and y + i <= 15:
                self.posiciones_alcance.add((x + i, y + i))

    def f_aumento_alcance(self):
        if not self.mejora_alcance:
            self.mejora_alcance = True
            self.alcance += MEJORA_ALCANCE
            self.completar_posiciones_alcance()

    def f_aumento_ataque(self):
        if not self.mejora_ataque:
            self.mejora_ataque = True
            self.ataque += MEJORA_ATAQUE

    def run(self):
        while self.viva:
            time.sleep(1/SPD_RACIMO)
            for enemigo, label in self.enemigos:
                if enemigo.pos in self.posiciones_alcance:
                    if enemigo.hp > 0:
                        print(f' antes de ataque el hp es {enemigo.hp}')
                        print(enemigo)
                        self.signal_label_ataque.emit(
                            (self.label_atacando, "M"))
                        self.signal_atack.emit((enemigo, self.ataque))
                        time.sleep(TIEMPO_ATAQUE_TORRE)
                        self.signal_label_ataque.emit(
                            (self.label_atacando, "E"))
                        print(f' despues ataque el hp {enemigo.hp}')
                        print(enemigo)
        self.label.setPixmap(
            QPixmap("missprite/explosion").scaled(40, 40))
        time.sleep(1)
        self.label.deleteLater()
        self.quit()
        self.deleteLater()
