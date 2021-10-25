# Tarea 2: DCCivil War :school_satchel:



## Consideraciones generales :octocat:

A modo general hay que tener en cosnideración que mi programa se cae o crashea debes en cuando en el transcurso de las ronda (generalmente esto ocurre despues de la ronda 3 y tambien cuando se ponen muchas torres en el mapa), esta caida no se debe a un error puntual sino que sale "Process finished with exit code -1073741515 (0xC0000135)", por lo que estuve leyendo, creo que esto se puede deber a la cantidad de threads corriendo y también por temas de setear la Qprogressbar.
Además se puede ver en el codigo que imprime la interfaz de pyCharm, que cuando se termina una ronda aparece el siguiente error "QObject::setParent: Cannot set parent, new parent is in a different thread", el cual se relaciona con la funcionalidad de detener las monedas cuando se acaba la ronda, esto solo afecta en que cuando se acaba una ronda, todas las monedas que estaban en el mapa desaparecen, pero luego aparece solo una nueva moneda por el tiempo definido de su creación.


Otro punto importante es que mi programa puede estar un poco desordeando, asi que trataré de dejar explicadas las cosas lo mejor posible en este readme, es por esto que en muchas partes de esta lectura se nombran muchas de las lineas y archivos en que estan las cosas, ya que no hice muchos comentarios en mis codigos.


Otros aspectos a tener en consideración y que se detallan mejor adelante es que, no se puede poner pausa en el juego, no aparecen las monedas cuando un enemigo es eliminado, los comandos de los cheat-codes estan implementados pero algunas de sus funcionalidades fallan, para actualizar la lista de top 10 despues de una partida hay que presionar el respectivo boton, el juego solo tiene musica de fondo, entre otras.


Mi frontend esta dividido en 3 partes, "Ventana_inicio.py", "Ventana_juego.py", "Frontend2.py"
Tambien se calcula el camino mas corto como un BFS

Tambier destacar que mi tarea su utiliza paths relativos pero que no utilicé os para crear los paths asi que sistemas operativos distintos al de windows podrian tener problemas para leer los archivos.


Recomendación, si es que mi programa se cae mucho, recomiendo desactivarle el setvalue de los enemigos normales, ya que eso podria estar ayudando a causar esos problemas y que dehecho ya hice con los kamikazes para disminuir el numero de crasheos (esto se especifica mejor en la parte de enemigos de las cosas implementadas y no implementadas)


Por último para revisar donde se conectan las principales señales de mi juego, es mas facil encontrarlas si es que te ubicas en las funciones en donde se instancias las diferentes clases( estan detalladas mas adelante las lineas y archivos en que se instancian), ya que generalmente conectaba las señales justo despues o un par de lineas despues de instanciar alguna clase. 


### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 3.Parametros: Esta parte esta hecha completa en el sentido de que estan escritas las Diferentes Constantes pedias en el enunciado, pero de las cuales algunas no se utilizan en el desarrollo del juego. concretamente las que no se ocuapan son: PROBABILIDAD_ENEMIGO_MONEDA, TIEMPO_INUTILIZABLE y CONSTANTE_DESTRUCCION.

Los parametros extra que creé son "Dim_label", el cual representa la dimension cuadrdada de los labels instanciados con imagenes, los paramtros que estan bajo el comentario " # Menu" y los diccionearios que estan abajo del cometnario " # Sprites".


* Parte 5. Entidades:En esta Part hice todas las entidades.
    * Parte 5.1 Enemigos: Hecha completa, se pueden revisar lass dos clases de enemigo en el archivo "Backend3.py" y estas se instancian en "Ventana_juego.py", especificamente el kamikaze en al linea 182 y el enemigo normal en la linea 188. Los dos tipos de enemigo cumplen con sus respectivas funciones de movimiento por casilla, los dos atacan correctamente y también el enemigo kamikaze explota cuando corresponde. Por último, agregar que estos siguen el camino mas corto hacia la base. Ojo que cuando instancio a los dos tipos de enemigos estos reciben como atributo al parent(self), porfavor eliminar esa parte cuando se instacia y eliminar del init de las clases también a "parent", esto en verdad no afecta nada en mi codigo ya que elimine la modelacion circular por lo que el parent del init no se utiliza en la clase (dehecho aparece en griz pq no se esta llamando).
    * Parte 5.2 Personaje: Hecha completa, se puede revisar en la clase Character del archivo "Backend1.py" y esta se instancia en "Ventana_juego.py", especificamente en la funcion crear_personaje que empieza en la linea 200. El personaje cumple con el movimiento continuo, desaparece cuando se acaba una ronda, choca con los obstaculos y torres, y agarra monedas.
    * Parte 5.3 Base: Hecha completa, se puede revisar la clase Base en el archivo "Backend5" y esta se instancia en "Ventana_juego.py" en la linea 89.
    * Parte 5.4 Torres: Hecha casi completa, se puede revisar las clases de las torres en el archivo "Backend4" y estas se instancias en el archivo "frontend2.py"(este archivo contiene funciones auxilaires que se llaman en "Ventana_juego.py", se explica mejor abajo en librerias propias) en la linea 181(Torre Racimo) y en la linea 186(Torre Francotiradora). El problema que tiene es que las torres francotiradoras despues de matar a un enemigo no atacan al enemigo con menor vida sino al primero que encuentran.


* Parte 6. Monedas: Hecha casi completa, se crean correctamente las monedas respetando el tiempo de entre apariciones y la duracion de cada una de ellas. No se implemento que aparecieran monedas cuando mueren los enemigos y tambien hay un problema al tratar de parar la creacion de las monedas cuando se acaba la ronda, ya que cuando termina una ronda desaparecen todas las monedas pero derepente aparece una sola moneda, la cual despues de que termina su duración esta desaparece y no aparece ninguna moneda más, este hecho arroja el error que se nombra en las consideraciones generales ("QObject::setParent: Cannot set parent, new parent is in a different thread") pero el cual no afecta posteriormente en el funcionamiento del juego ni el de agarrar las monedas por el personaje. La clase moneda se encuentra en el archivo "Backend1.py" y se instancia en el archivo "Ventana_juego.py" en la linea 219 (en el metodo crear_moneda()). Por último, agregar que el label de las monedas en el juego es la imagen del signo "$".
   
   
* Parte 7. Mejoras: Hecha completa, estas se pueden ver en los metodos mejora_1() y mejora_2() del archivo "Ventana_juego.py" en las lineas 327 y 339 respectivamente. Ambos metodos estan asociados correctamente a los botones de la interfaz del juego. El unico problema que se puede tener es que si se compran las dos mejoras seguidas en una ronda, el programa a veces se cierra y no arroja ningun error como tal, sino que Process Finished.... (como el mensaje que se explico en las consideraciones generales).

    
* Parte 8. Mapa: hecha casi completa, los tres mapas se cargan correctamente en el juego, la eleccion del mapa a jugar se hace cambiando el nombre del mapa en el archivo "parametros.py" especificamente RUTA_MAPA, para cambiar el nombre no se debe alterar el path relativo del parametro, es decir, la forma correcta es RUTA_MAPA = "mapas/mapa_X.txt", donde X puede ser 1, 2 o bonus. el unico problema que tiene esta parte es que el progrmaa no puede cargar mapas que tengan diferente tamaño a 15*20 (tamaño de los tres mapas dados).


* Parte 9. Puntaje: Hecha completa, el puntaje se calcula correctamente, esto se puede ver cuando se acaba una ronda en el juego, y el codigo del calculo se puede apreciar en el archivo "Ventana_juego.py" en el metodo actualizar_points() en la linea 268 especificamente.

  
* Parte 10. Interfaz: Hecha incompleta
    * Parte 10.2 Ventana de inicio: Hecha completa 
    
    * Parte 10.3 Ventana de juego: 
     * Parte 10.3.1 Preparando ronda: Hecha completa
     * Parte 10.3.2 Ronda: Hecha incompleta, como detallé en la seccion de monedas hay problemas con una moneda al final de la ronda, la pausa no esta implementada en el juego, por lo que el boton de pausa y la tecla "p" no sirven. Por último detallar que la barra de mi kamikaze no la seteo, ya que me di cuenta que asi el programa se caia menos. para activar el seteo de esta barra se tiene que ir al archivo "Backend3.py" y quitarle los "#" a las lineas 144 y 156.
     * Parte 10.3.3 Movimiento: Hecho completo
     * Parte 10.3.4 Fin de la ronda: Hecha completa pero ojo que cuando el usuario gana una una ronda, solo sale un cartel diciendo los datos de la ronda(pero no dice victoria explicitamente), en cambio cuando pierde sale en el mensaje que a perdido explicitamente y dps se muestran los datos de la ronda.
    
    
* Parte 11. Funcionalidades extras: Hecha incompleta, es decir todos los cheat codes funcionan bien llamandolos, es decir, apretando las teclas necesarias o haciendo click, pero no todas las funcionalidades estan correctas. 
    * El cheat para aumentar el dinero funciona correctamente. 
    
    * El cheat de avanzar de ronda funciona mas o menos, ya que acaba la ronda correctamente, solo en el caso en que se hayan creado todos los enemigos de la ronda y estos no hayan sido atacados por torres. Si algun enemigo es atacado por las torres entonces este cheat code no funciona. En el caso de que se active el cheat code y no todos los enemigos han sido creados, la ronda se acaba y se elimian los enemigos correspondientes, pero el problema que se tiene es que no se deja iniciar la siguiente ronda. 
    
    *  El cheat de la destruccion de torres, solo muestra la explosión de la torre cuando se hace click sobre ella y además la ronda se encuentra activa, pero esto no deshabilita a las otras torre, ni  tampoco daña a los enemigos. Cabe destacar que cuando se hace click en una torre, en la que la ronda no esta activada entonces esta no explota (pero si desaparece), con esto quiero mostrar que si diferencie ambos casos de la destruccion de las torres.
    
En el codigo se puede ver implementacion de los cheat codes dentro de las funciones key_press_event_extra(), mouse_press_event_extra() y mouse_release_event_extra()

    
* Parte 12. Sprites: Hecha completa, se utilizan las sprites dadas y además se usan algunas propias guardadas en la carpeta "missprites.
    
     
* Parte 13. GitIgnore: Hecha completa


* Parte 14. Avance de la Tarea: Hecha completa y entregada dentro del plazo, dehecho son los archivos "frontendmov.py" y "backendmov.py que aparecen en mi repositorio.


* Parte 15. Bonus: Hecho completo el bonus del camino mas corto el cual esta dado por un BFS, el cual se calcula a partir de un grafo hecho con las piezas del mapa. La creacion del grafo se puede ver a partir del metodo grafo() y el bfs a partir del metodo bfs() del archivo "Backend2.py" , lineas 66 y 89 respectivamente.

En el caso del bonus de musica, no lo hice completo, solo se puede poner musica de fondo en la linea 57 del archivo "Vantana_juego.py".

    ...


## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```Ventana_inicio.py```


## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```time```-> ```sleep()```
2. ```Random```-> ```randint(), choice()```
3. ```PyQT5```-> ```uic```
4. ```PyQt5.QtWidgets```-> ```QApplication(), QMessageBox(), QLabel(), QProgressBar()``` 
5. ```PyQt5.QtGui```-> ```QPixmap(), QTransform()``` 
6. ```PyQt5.QtCore```-> ```pyqtSignal(), QTimer(), QRect(), QThread(), QMutex(), QObject(), QMutexLocker()``` 
7. ```PyQt5.QtMultimedia```-> ```QSound()``` 
8. ```collections```-> ```deque()``` 
9. ```sys```-> ```sys.__excepthook__``` 

Cabe destacar que la librería Pyqt5 se tiene que instalar.



...

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```Backend1```-> Contine a la ```Clase Character```, la cual representa al personaje que recolecta monedas en el backend y la ```Clase Moneda```, la cual hereda de Qthread y cada una de sus instancias es una moneda del juego.
2. ```Backend2```-> Contine a ```Clase Pieza```, la cual cada instancia representa un elemento del mapa (Libre, Camino, obtaculo, etc...) y la ```Clase Tablero```, la cual agrupa las diferentes instancias de Pieza y las ordena segun su posicion en el mapa, en resumen, la instancia de Tablero es el Backend del mapa.
3. ```Backend3```-> Contine a la ```Clase Enemigo```, la cual hereda de Qthread y cada elemento instanciado es un enemigo normal del juego y la ```Clase Kamikaze``` la cual también hereda de Qthread y cada elemento instanciado es un Enemigo Kamikaze.
4. ```Backend4```-> Contine a la ```Clase TorreFranco```, la cual hereda de Qthread y cada elemento instanciado es un Torre Francotiradora del juego y la ```Clase TorreRacimo``` la cual también hereda de Qthread y cada elemento instanciado es un Torre Racimo del juego.
5. ```Backend5```-> Contine a la ```Clase Base```, la cual hereda de QObject y representa el backend de la base del juego que hay que defender y además contine a la ```Funcion write_top```, la que se encarga de guardar el usuario con su respectivo puntaje de la partida en el archivo "puntajes.txt"
6. ```parametros```-> Contiene todas las constantes del juego, lo que permite manipular los datos del juego de manera mas fácil.
2. ```Ventana_inicio```-> Contine a la ```Clase StartWindow```, la cual cuando se instancia aparece la ventana de inicio del juego (Nombre usuario, elegir equipo, ver el top 10, etc...), esta clase hereda de "Primera_ventana.ui", ya que la ventana fue diseñada en QT Designer. Este archivo es parte del Fronted.
2. ```Ventana_juego```-> Contine a la ```Clase GameWindow```, la cual cuando se instancia (esto ocurre en la Ventana_inicio.py) aparece la ventana del juego (poner torres, aparcen los enemigos, etc), esta clase hereda de "ventana_juego.ui", ya que la ventana fue diseñanda en QT Designer. Este archivo es parte del Frontend.
2. ```Frontend2```-> Este archivo contiene funciones auxliares hechas para acortar el largo del codigo de la "Ventana_juego.py", estas incluye  ```crear_tablero_extra()```, ```key_press_event_extra()```, ```mouse_press_event_extra()```, ``` mouse_move_event_extra()``` y ``` mouse_release_event_extra()```. Estas funciones son llamadas en la "Ventana_juego.py" en funciones con el mismo nombre solo que cortandole la parte "extra"

...


## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. (https://stackoverflow.com/questions/8922060/how-to-trace-the-path-in-a-breadth-first-search): este codigo trata de un bfs y me base en esto para encontrar el camino mas corto, para ello cree un grafo del tablero para poder recorrerlo. Esto está implementado en el archivo Backend2.py en las líneas 91 a la 114.
2. (Ayudantia de Interfaz Grafica 2°Semestre 2018, ayudantia de Mario): este codigo lo utilicé para crear el movimiento inicial de mi personaje. Lo podemos encontrar en el archivo Backend1.py en el esqueleto de mi clase Character y  en el archivo Ventana_juego.py en las lineas de la 112 a la 121 y en la linea 200 a la 211


