from collections import deque


class Pieza:
    def __init__(self, tipo):
        self.tipo = tipo
        self.moneda = False
        self.label = None


class Tablero:

    def __init__(self, archivo):
        self.piezas = []
        self.archivo = archivo
        self.posiciones = []
        self.posibles_torres = set()
        self.torres_construidas = set()
        # Son O y C para las monedas las posiciones libre
        self.posiciones_libre = set()
        self.posicion_base = (0, 0)

    def crear_tablero(self):
        with open(self.archivo, "r", encoding="utf-8") as file:
            for line in file:
                lista = []
                linea = line.replace("\n", "").strip().split()
                for line2 in linea:
                    lista.append(Pieza(line2))
                self.piezas.append(lista)
        for i in range(len(self.piezas)):
            for j in range(len(self.piezas[0])):
                self.posiciones.append((j, i))

        self.completar_posibles_torres()
        self.completar_libre()

    def imprimir_tablero(self):
        for line in self.piezas:
            lista = []
            for line2 in line:
                lista.append(line2.tipo)
            print('-'.join(lista))

    def hay_moneda(self, x, y, elemento):
        if elemento == "Read":
            return self.piezas[y][x].moneda
        elif elemento == "Change":
            self.piezas[y][x].moneda = False
            self.piezas[y][x].label.hide()
            self.piezas[y][x].label = None

    def pos(self, x, y):
        return self.piezas[y][x].tipo

    def cambiar_elemento_pos(self, x, y, elemento):
        self.piezas[y][x].tipo = elemento

    def encontrar_s(self):
        lista = []
        for elementos in self.posiciones:
            if self.pos(*elementos) == "S":
                lista.append(elementos)
        return lista

    def grafo(self):
        dict = {}
        largox = len(self.piezas[0])
        largoy = len(self.piezas)
        for i in range(largox):
            for j in range(largoy):
                punto = (i, j)
                hijos = []
                if 0 <= i-1:
                    hijos.append((i-1, j))
                if i+1 < largox:
                    hijos.append((i+1, j))
                if 0 <= j-1:
                    hijos.append((i, j-1))
                if j+1 < largoy:
                    hijos.append((i, j+1))
                dict[punto] = hijos
        return dict

# Aqui empeiza el camino mas corto""""""""""

    # para el siguiente bfs me base en una duda de stackoverflow
    # aqui va el link
# https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth
    # -first-search
    def bfs(self, start):
        queue = [[start]]
        visited = set()
        grafo = self.grafo()

        while queue:

            path = queue.pop(0)
            new_path = None

            vertex = path[-1]

            if self.pos(*vertex) == "B":
                return path

            elif vertex not in visited:
                for current_neighbour in grafo.get(vertex, []):
                    if self.pos(*current_neighbour) == "C":
                        new_path = list(path)
                        new_path.append(current_neighbour)
                        queue.append(new_path)
                    if self.pos(*current_neighbour) == "B":
                        new_path.pop(-1)
                        return new_path

                # Mark the vertex as visited
                visited.add(vertex)
# RUTA CORTA

    def ruta_corta(self):
        inicios = self.encontrar_s()
        camino_corto = []
        for inicio in inicios:
            lista = self.bfs(inicio)
            if len(camino_corto) == 0:
                camino_corto = lista
            elif len(lista) < len(camino_corto):
                camino_corto = lista
        return camino_corto

    def caminos(self):
        inicios = self.encontrar_s()
        caminos = []
        for inicio in inicios:
            lista = self.bfs(inicio)
            caminos.append(lista)
        return caminos

    def completar_posibles_torres(self):
        for posicion in self.posiciones:
            if self.pos(*posicion) == "O":
                i, j = posicion
                if self.pos(i+1, j) == "C":
                    self.posibles_torres.add(posicion)
                if self.pos(i-1, j) == "C":
                    self.posibles_torres.add(posicion)
                if self.pos(i, j+1) == "C":
                    self.posibles_torres.add(posicion)
                if self.pos(i, j-1) == "C":
                    self.posibles_torres.add(posicion)

    def actualizar_torre(self, tupla):
        i, j, tipo = tupla
        if tipo == "A":
            self.piezas[j][i].tipo = "T"
        elif tipo == "E":
            self.piezas[j][i].tipo = "O"

    def completar_libre(self):
        for posicion in self.posiciones:
            if self.pos(*posicion) == "O" or self.pos(*posicion) == "C":
                self.posiciones_libre.add(posicion)
