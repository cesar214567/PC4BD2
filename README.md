#  Base de datos Multimedia, PC4 


## Integrantes
|  **#** | **Código** | **Apellidos, Nombre** | **% Trabajo** |
| :---: | :---: | :---: | :---: |
|  1 | 201810142 |Madera Garces, Cesar Antonio | 100% |
|  2 | 201810245 |Sobrados Burgos, Enrique Francisco | 100% |
|  3 | 201810614 |Villegas Suárez, Ariana Mirella | 100% |

## Ejecución del proyecto: 

- sudo apt install python3-rtree

- pip3 install imutils 

- cd web/

- python3 server.py

- Ingresar a localhost:8081

## Experimentos

### Experimento 1

**Foto de prueba: Abdullah Gul**
|  **Precisión** | **ED** | **MD** | **ED_tiempo** | **MD_tiempo** |
| :---: | :---: | :---: | :---: | :---: |
| K = 4 | 1 | 1 | 0.134s | 0.142s |
| K = 8 | 1 | 1 | 0.145s | 0.138s |
| K = 16 | 0.94 | 0.94 | 0.131s | 0.146s |

### Explicación experimento 1
Como se puede observar en los resultados,  se obtuvo un tiempo muy parecido en ambos casos debido a que la manera en la que se están calculando, se necesita iterar por toda la data almacenada. Sin embargo, el método euclidiano en la experimentación tenía resultados más precisos que el Manhattan, lo cual se observa en el orden de los resultados.



### Experimento 2

**K = 20**

**Foto de prueba: Abdullah Gul**

 **KNN-Secuencial métrica: Manhattan**

|  **N** | **KNN-RTree** | **KNN-Secuencial** |
| :---: | :---: | :---: | 
|  100 | 0.860ms | 1.489ms |
|  200 | 1.041ms | 2.507ms |
|  400 | 1.433ms | 5.041ms |
|  800 | 2.035ms | 8.576ms |
|  1600 | 3.551ms | 16.667ms |
|  3200 | 6.593ms | 39.126ms |
|  6400 | 13.643ms | 69.158ms |
|  12800 | 41.005ms | 130.523ms  |

### Explicación Experimento 2
En este experimento, observamos que el tiempo del KNN-R-Tree es sustancialmente menor al del KNN-Secuencial, esto se debe a que el KNN-Secuencial recorre toda la colección en busca de las K imágenes más cercanas al query. En cambio, el KNN-R-Tree solo recorre algunos nodos, los cuales se pueden representar como cuadrantes, que podrían contener el punto (la imagen) que se está buscando.

## Backend

### Extraer features

En base a la referencia dada en el enunciado del proyecto construimos dos funciones:

- getFeatures() para extraer el vector característico de 128 dimensiones con el modelo cnn de la librería face_recognition y la lectura de la imagen se realizó con la librería cv2(computer vision). 
- extract() para extraer los vectores característicos de las imágenes de n directorio específico y almacenarlos en un archivo (pickle) como un diccionario de nombres y vectores.

El módulo pickle implementa protocolos binarios para serializar y deserializar una estructura de objeto Python.

### KNN - Search

Se utilizaron las librerías scipy para las distancias (métricas) y heapq para mantener una cola de prioridades.

La función de KNN search básicamente recorre todos los vectores en la colección y calcula su distancia con el vector de la imagen del query de acuerdo a la métrica seleccionada (Euclidiana o Manhattan). Luego evalúa si la cola de prioridades está llena o no, si no está llena inserta el vector junto con la distancia, caso contrario, compara la mayor distancia de la cola de prioridades con la del vector de la imagen actual en la colección, y coloca en la cola de prioridades el menor y continúa con el siguiente vector en la colección.

### RTREE-Search

Se utilizo la libreria “rtree” para poder crear la estructura. Para ello se utilizó las siguientes configuraciones:

p = index.Property()
p.dimension = 128
p.buffering_capacity = 128
p.dat_extension = 'data'
p.idx_extension = 'index'
rtree = index.Index('128d_index',properties=p,interleaved = False)  #interleaved se setea a falso para mayor comodidad a la hora de insertar tuplas

- Inserción

rtree.insert(id = i,coordinates = Tupla, obj = {“nombre”:nombre}) #Tupla contiene elementos del tipo (a1,a1,a2,a2… a128,a128) 

- Búsqueda

lres = list(rtree.nearest(coordinates=tuple(list_carac), num_results=int(K), objects = "raw"))

### Consulta

Para obtener los resultados de la consulta por imagen se siguen los siguientes pasos:

Cargar el diccionario que contienen los vectores característicos y los nombres de las imágenes procesadas.
Construir el Rtree.
Ingresar la imagen
Procesar la imagen enviada 
Obtener los K nombres de las imágenes junto con sus pesos (depende de la consulta)
Enviarlos como formato Json al frontend
Cargar las imágenes desde el frontend.

## Frontend

Aparecerá la pantalla del index, y se ingresa a “get started” o a la opción “queries” para ingresar a la pantalla de visualización de queries.

Dentro de la pantalla de query, se le da al usuario 2 opciones: 
Subir una foto y buscar los personajes parecidos a quien esté en la imagen usando KNN-Secuencial . Como resultado aparecerán en la tabla inferior las tuplas conteniendo la imagen, el nombre de la imagen y su distancia con la imagen ingresada.
Subir una foto y buscar los personajes parecidos a quien esté en la imagen usando Rtree-Secuencial . Como resultado aparecerán en la tabla inferior las tuplas conteniendo la imagen y el nombre de la imagen. La distancia no se está tomando en cuenta ya que no se sabe cual es la función de distancia que se está utilizando internamente.


Las imágenes subidas pueden estar en formato jpg, jpeg y png y se podrán visualizar los resultados en sus tablas ya predefinidas por sección: una sección únicamente para las consultas por R-Tree y la otra para las consultas por KNN-Secuencial.

Para pasar la información de frontend a backend se está utilizando json y jquery. 



## Servidor: 

Cada opción está llamando a una ruta diferente en el servidor: 
- POST: /KNN/<method>/<K> llama a la función que hace la busqueda por KNN y utiliza K como parámetro para retornar lo K mas parecidos, el method determina si va a hacer manhattan o euclidiano. 

- POST: /RTREE/<K>: llama a la función que va a insertar la imagen al R-Tree y recibe K como parámetro para retornar los K mas parecidos.
