RUTA_MAPA = "mapas/mapa_1.txt"
# ENEMIGO
ATK_NORMAL = 10
SPD_NORMAL = 5
MOV_NORMAL = 1
HP_ENEMIGOS = 60
Dim_enemigo = 20
ATK_KAMIKAZE = 15
TIEMPO_ENEMIGO = 1
# BASE
HP_BASE = 200
# DINERO
DINERO_INICIAL = 200
TIEMPO_MONEDA = 2
DURACION_MONEDA = 5
CANTIDAD_MONEDA = 0
PROBABILIDAD_ENEMIGO_MONEDA = 0
DINERO_TRAMPA = 100
# Torres
SPD_FRANCOTIRADORA = 5
ATK_FRANCOTIRADORA = 25
ATK_RACIMO = 15
SPD_RACIMO = 5
COSTO_TORRE_R = 50
COSTO_TORRE_F = 60
# MEJORAS TORRES
MEJORA_ATAQUE = 10
COSTO_MEJORA_ATAQUE = 10
MEJORA_ALCANCE = 2
COSTO_MEJORA_ALCANCE = 20
TIEMPO_VIDA_PERDIDA = 1
TIEMPO_ATAQUE_TORRE = 1
TIEMPO_INUTILIZABLE = 0

SPEED_PLAYER = 10
Dim_label = 40
Dim_personaje = 40

# MENU
Dim_label_menu = 40
torre1 = (21, 4)
torre2 = (21, 5)

# Ronda
GENERACION_1 = 1
GENERACION_2 = 4

# otras
CONSTANTE_DESTRUCCION = 1


# SPRITES
SPRITE_MAPA = {"libre": "sprites/mapa/towerDefense_tile024.png",
               "camino": "sprites/mapa/towerDefense_tile093.png",
               "obstaculo": "sprites/mapa/towerDefense_tile128.png",
               "inicio": "sprites/mapa/towerDefense_tile113.png",
               "base": "sprites/mapa/towerDefense_tile084.png"}

PERSONAJE_SPRITE = {"ab_1": "sprites/personaje/m/m_01.png",
                    "ab_2": "sprites/personaje/m/m_02.png",
                    "ab_3": "sprites/personaje/m/m_03.png",
                    "ar_1": "sprites/personaje/m/m_04.png",
                    "ar_2": "sprites/personaje/m/m_05.png",
                    "ar_3": "sprites/personaje/m/m_06.png",
                    "izq_1": "sprites/personaje/m/m_07.png",
                    "izq_2": "sprites/personaje/m/m_08.png",
                    "izq_3": "sprites/personaje/m/m_09.png"}

base = {"1ar_iz": "missprite/base_gato/base_cuadrada1.png",
        "1ar_de": "missprite/base_gato/base_cuadrada2.png",
        "1ab_iz": "missprite/base_gato/base_cuadrada3.png",
        "1ab_de": "missprite/base_gato/base_cuadrada4.png",
        "2ar_iz": "missprite/base_ping/base_cuadrada1.png",
        "2ar_de": "missprite/base_ping/base_cuadrada2.png",
        "2ab_iz": "missprite/base_ping/base_cuadrada3.png",
        "2ab_de": "missprite/base_ping/base_cuadrada4.png"}

enemigo = {"1ab_1": "sprites/pinguino/normal/normal_01.png",
           "1ab_2": "sprites/pinguino/normal/normal_02.png",
           "1ab_3": "sprites/pinguino/normal/normal_03.png",
           "1ar_1": "sprites/pinguino/normal/normal_35.png",
           "1ar_2": "sprites/pinguino/normal/normal_36.png",
           "1ar_3": "sprites/pinguino/normal/normal_37.png",
           "1izq_1": "sprites/pinguino/normal/normal_18.png",
           "1izq_2": "sprites/pinguino/normal/normal_19.png",
           "1izq_3": "sprites/pinguino/normal/normal_20.png",
           "2ab_1": "sprites/gato/normal/normal_01.png",
           "2ab_2": "sprites/gato/normal/normal_02.png",
           "2ab_3": "sprites/gato/normal/normal_03.png",
           "2ar_1": "sprites/gato/normal/normal_27.png",
           "2ar_2": "sprites/gato/normal/normal_28.png",
           "2ar_3": "sprites/gato/normal/normal_29.png",
           "2izq_1": "sprites/gato/normal/normal_13.png",
           "2izq_2": "sprites/gato/normal/normal_19.png",
           "2izq_3": "sprites/gato/normal/normal_18.png"}

kamikaze = {"1ab_1": "sprites/pinguino/kamikaze/kamikaze_01.png",
            "1ab_2": "sprites/pinguino/kamikaze/kamikaze_02.png",
            "1ab_3": "sprites/pinguino/kamikaze/kamikaze_03.png",
            "1ar_1": "sprites/pinguino/kamikaze/kamikaze_32.png",
            "1ar_2": "sprites/pinguino/kamikaze/kamikaze_33.png",
            "1ar_3": "sprites/pinguino/kamikaze/kamikaze_34.png",
            "1izq_1": "sprites/pinguino/kamikaze/kamikaze_17.png",
            "1izq_2": "sprites/pinguino/kamikaze/kamikaze_18.png",
            "1izq_3": "sprites/pinguino/kamikaze/kamikaze_19.png",
            "2ab_1": "sprites/gato/kamikaze/kamikaze_02.png",
            "2ab_2": "sprites/gato/kamikaze/kamikaze_03.png",
            "2ab_3": "sprites/gato/kamikaze/kamikaze_04.png",
            "2ar_1": "sprites/gato/kamikaze/kamikaze_38.png",
            "2ar_2": "sprites/gato/kamikaze/kamikaze_39.png",
            "2ar_3": "sprites/gato/kamikaze/kamikaze_41.png",
            "2izq_1": "sprites/gato/kamikaze/kamikaze_18.png",
            "2izq_2": "sprites/gato/kamikaze/kamikaze_20.png",
            "2izq_3": "sprites/gato/kamikaze/kamikaze_22.png"}

torres_sprite = {"t_1": "sprites/mapa/towerDefense_tile250.png",
                 "t_2": "sprites/mapa/towerDefense_tile249.png"}

objetos_sprite = {'moneda': "sprites/mapa/towerDefense_tile287",
                  'explosion': "sprites/mapa/towerDefense_tile021"}
