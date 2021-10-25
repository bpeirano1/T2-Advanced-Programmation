import sys
from PyQt5 import uic
from PyQt5.QtWidgets import (QApplication, QMessageBox, QLabel, QWidget)
from Ventana_juego import GameWindow
window_name, base_class = uic.loadUiType("Primera Ventana.ui")


class StartWindow(window_name, base_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.ventana_juego = None
        self.usuario = ""
        self.BJugar.setEnabled(False)
        self.BJugar.clicked.connect(self.click_button)
        self.Biniciar_sesion.clicked.connect(self.click_biniciar)
        self.Bcerrar_sesion.clicked.connect(self.click_bcerrar)
        self.Bactualizar_top10.clicked.connect(self.top_10)
        # Aca activamos el top 10
        self.top_10()

    def click_button(self):
        if not self.radioButton1.isChecked() and not\
                self.radioButton2.isChecked():
            QMessageBox.warning(self, "Error seleccion equipo",
                                " No ha seleccionado un equipo")
        else:
            for rb_id in range(1, 3):
                if getattr(self, 'radioButton' + str(rb_id)).isChecked():
                    opcion = rb_id
            self.ventana_juego = GameWindow(self.usuario, opcion)
            self.ventana_juego.show()
            self.click_bcerrar()

    def click_biniciar(self):
        texto = self.nombre_usuario.text()
        if texto == "":
            QMessageBox.warning(self, "Error nombre", " No ha ingresado un "
                                                      "nombre de usuario")
        else:
            self.mensaje_sesion.setText(f'{texto} ha iniciado sesion')
            self.usuario = texto
            self.BJugar.setEnabled(True)
            self.Biniciar_sesion.setEnabled(False)
            self.Bcerrar_sesion.setEnabled(True)

    def click_bcerrar(self):
        self.nombre_usuario.setText("")
        self.mensaje_sesion.setText("")
        self.usuario = ""
        self.Biniciar_sesion.setEnabled(True)
        self.Bcerrar_sesion.setEnabled(False)
        self.BJugar.setEnabled(False)

    def top_10(self):
        with open("puntajes.txt", "r", encoding="utf-8") as file:
            lista = []
            for line in file:
                us, pts = line.strip().split(",")
                pts = int(pts)
                lista.append([us, pts])
            lista.sort(key=lambda x: x[1], reverse=True)
            while len(lista) < 10:
                lista.append([None, None])
            self.label_top1.setText(f'1) {lista[0][0]}: {lista[0][1]}')
            self.label_top2.setText(f'2) {lista[1][0]}: {lista[1][1]}')
            self.label_top3.setText(f'3) {lista[2][0]}: {lista[2][1]}')
            self.label_top4.setText(f'4) {lista[3][0]}: {lista[3][1]}')
            self.label_top5.setText(f'5) {lista[4][0]}: {lista[4][1]}')
            self.label_top6.setText(f'6) {lista[5][0]}: {lista[5][1]}')
            self.label_top7.setText(f'7) {lista[6][0]}: {lista[6][1]}')
            self.label_top8.setText(f'8) {lista[7][0]}: {lista[7][1]}')
            self.label_top9.setText(f'9) {lista[8][0]}: {lista[8][1]}')
            self.label_top10.setText(f'10) {lista[9][0]}: {lista[9][1]}')


if __name__ == '__main__':
    def hook(type, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook
    app = QApplication([])
    mi_juego = StartWindow()
    mi_juego.show()
    app.exec()
