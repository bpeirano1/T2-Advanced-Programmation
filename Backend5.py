from PyQt5.QtCore import QObject
from parametros import HP_BASE, Dim_label
tam = Dim_label


class Base (QObject):
    def __init__(self, progressbar):
        super().__init__()
        self.hp = HP_BASE
        self.bar = progressbar
        self.bar.setMaximum(self.hp)
        self.bar.setValue(self.hp)


def write_top(usuario, puntaje):
    with open("puntajes.txt", "a", encoding="utf8") as file:
        file.write(f'\n{usuario},{puntaje}')
