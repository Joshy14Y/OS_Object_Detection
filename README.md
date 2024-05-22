# Sistema de Reconocimiento Facial y de Objetos en Vídeos con Arquitectura en la Nube y Multiprocesamiento
Estudiantes
- Joshua Sancho Burgos
- Kristel Salas Villegas 
- Samantha Acuña Montero

## Descripción General del Proyecto

El proyecto consiste en desarrollar un sistema integral y eficiente para analizar archivos de vídeo, especialmente películas, 
con el propósito de identificar y cuantificar la presencia de personas y objetos específicos, como autos y armas. Este sistema utilizará 
tecnologías avanzadas de reconocimiento facial y de objetos y se basará en una arquitectura de procesamiento distribuido en la nube. 
Esto permitirá manejar grandes volúmenes de datos visuales, garantizando un análisis rápido y preciso.

## Multiprocesamiento

El proyecto se centra en procesar grandes videos dividiéndolos en partes más pequeñas para facilitar el análisis. Para mejorar la eficiencia y reducir el tiempo de procesamiento, se emplea el multiprocesamiento, donde varias partes del video se procesan simultáneamente en diferentes hilos.

Primero, el video grande se divide en segmentos más pequeños. Luego, cada uno de estos segmentos es asignado a un hilo separado para realizar la detección de objetos. Cada hilo trabaja en paralelo, procesando su segmento del video de manera independiente, identificando y clasificando objetos en cada cuadro del video.

Los resultados de todos los hilos se recogen y consolidan en un archivo JSON. Finalmente, los datos recolectados se analizan y se visualizan en forma de gráficos, mostrando estadísticas como el número de objetos detectados y la confianza media en cada detección. Este enfoque de multiprocesamiento no solo mejora la eficiencia del sistema, sino que también permite manejar grandes volúmenes de datos de manera más efectiva.

## Arquitectura 
La arquitectura del sistema se puede describir como una arquitectura monolítica que integra múltiples funcionalidades relacionadas con la división de videos, detección de objetos y visualización de estadísticas. 
### División de Video 
La primera etapa del sistema implica la división de un video grande en varias partes más pequeñas. Esta tarea es manejada por un componente que abre el 
video original, calcula el número de cuadros que debe contener cada parte y crea archivos de video temporales donde se almacenan estos cuadros.
### Detección de Objetos 
Un componente de detección de objetos utiliza el modelo YOLOv8 para procesar cada parte del video, cuadro por cuadro. Este componente identifica y clasifica objetos presentes en 
cada cuadro, anotando las detecciones con sus respectivas confianzas. Para mejorar la eficiencia y acelerar el procesamiento, esta tarea se ejecuta en múltiples hilos. 
Cada hilo procesa una parte del video de manera simultánea.Finalmente, las detecciones realizadas se almacenan en una estructura de datos centralizada (un archivo JSON) que reúne 
los resultados de todos los hilos.
### Análisis y Visualización
Una vez que los datos de detección están almacenados, otro componente los analiza para calcular estadísticas por clase y generar gráficos visuales. Este componente crea gráficos de barras que muestran el número de detecciones y la confianza media para cada clase de objeto detectado. Los gráficos generados se guardan como archivos de imagen, proporcionando una visualización clara y comprensible de los resultados de detección.

<div align="center">
  <img src="https://res.cloudinary.com/dgm059qwp/image/upload/v1716334936/SO/appn4x0zvvpgsf6oe2q6.png" alt="Diagrama" width="300" height="600">
</div>

## Implementación
La implementación del proyecto se basa en tres archivos.py, los cuales son:
### Process_video.py
Define la función thread_safe_predict que carga el modelo YOLO, lee los cuadros de un video, realiza predicciones sobre cada cuadro y guarda los resultados en una estructura de datos, además de guardar imágenes de los cuadros con las detecciones anotadas. Luego, define la función process_videos_with_threading, que utiliza hilos para procesar múltiples videos de manera concurrente, almacenando los resultados de cada video en un diccionario y guardándolos en un archivo JSON. 
### Frame_divider.py
Primero divide un video en varias partes iguales y guarda cada parte en un archivo temporal. Primero, abre el video y obtiene el número total de cuadros. Luego, calcula cuántos cuadros debe contener cada parte y crea archivos de video temporales para cada una. A través de un bucle, lee los cuadros del video original y los escribe en los archivos temporales correspondientes, cambiando de archivo cuando se alcanza el número de cuadros por parte. Al finalizar, libera los recursos utilizados y retorna las rutas de los archivos de video temporales. Este proceso divide vídeos grandes en partes más pequeñas y manejables, para que sea más fácil. 
### Plot_data.py
Carga datos de detección de objetos desde un archivo JSON, calcula estadísticas por clase y generales, y genera gráficos que muestran la cantidad de detecciones y la confianza media por clase. La función plot_general_stats toma las clases, los conteos y las medias de confianza, y guarda un gráfico de barras que muestra estas estadísticas. Además, crea directorios para guardar estos gráficos si no existen. La función plot_class_and_general_stats procesa el JSON para calcular estas estadísticas para cada video y para todos los videos en conjunto, llamando a plot_general_stats para generar y guardar los gráficos correspondientes.

## Resultados 
Al realizar todo el proceso de la detección de actores:
- Brad Pitt
- Henry Cavill
- Keanu Reeves
- Ryan Gosling
- Kim Chaewon

Y objetos como: 
- Armas de Fuego
- Teléfonos 

Los resultados demuestran el recuento de objetos detectados y la confianza media en cada detección, de lo contrario da estadísticas en blanco, lo que significa que no encontró nada. 
| Resultado 1 | Resultado 2 | Resultado 3 |
|----------|----------|----------|
| ![Imagen 1](https://res.cloudinary.com/dgm059qwp/image/upload/f_auto,q_auto/v1/SO/zt0f11cyuhnjppz8aeyf) | ![Imagen 2](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334937/SO/kcjvkmoqrb9egtsotyi5.jpg) | ![Imagen 3](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334937/SO/ipebmzxkita8ts6knvqq.jpg) |

| Resultado 4 | Resultado 5 | Resultado 6 |
|----------|----------|----------|
| ![Imagen 4](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334933/SO/krmjq2a0c4sqw2prhik4.jpg) | ![Imagen 5](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334935/SO/eieandyxj9fig9byrsze.jpg) | ![Imagen 6](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334936/SO/fbaqmct0holzfkh09nns.jpg) |

| Resultado 7 | Resultado 8 | Resultado 9 |
|----------|----------|----------|
| ![Imagen 7](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334933/SO/lcsah93ntdsqua31hsyb.jpg) | ![Imagen 8](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334933/SO/jpzwia5slfekdunflsps.jpg)| ![Imagen 9](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334934/SO/tp50lmenssnmd5tqvliv.jpg) |

| Resultado 10 | Resultado 11 | Resultado 12 |
|----------|----------|----------|
| ![Imagen 10](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334936/SO/cb6qkfmfqmiyd28qs4kf.jpg) | ![Imagen 11](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334934/SO/cczpl8golifjzwmnctab.jpg)| ![Imagen 12](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334935/SO/mb8kwgw2b4uvxyhfumpz.jpg) |

| Resultado 13 | Resultado 14 | Resultado 15 |
|----------|----------|----------|
| ![Imagen 13](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334935/SO/fgtczvcqefw2kxeropgs.jpg) | ![Imagen 14](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334936/SO/jldvskxquieh7v6uilsz.jpg)| ![Imagen 15](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334934/SO/z0imswj3j0tep9qav6tk.jpg) |

| Resultado 16 | Resultados Generales |
|----------|----------|
| ![Imagen 16](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334935/SO/ukzeuxe2aboj9216vkiw.jpg) | ![Imagen Results](https://res.cloudinary.com/dgm059qwp/image/upload/v1716334937/SO/xnwyooun0u1ooxg5j3mi.jpg)|

## Instrucciones de Instalación
1) Primeramente debe de instalar Anaconda: 
  <a href="https://www.anaconda.com/download">Descargar Anaconda</a>

2) Luego de haber instalado Anaconda, debe de crear un entorno, busca Anaconda Navigator y lo abre. 
<div align="center">
  <img src="https://res.cloudinary.com/dgm059qwp/image/upload/v1716337685/SO/nx1h6v76c0tvkjegjcva.png" alt="Imagen1" width="800" height="400">
</div>
<div align="center">
  <img src="https://res.cloudinary.com/dgm059qwp/image/upload/v1716338295/SO/ayu61ncxyo3zsfcj9xnb.png" alt="Imagen2" width="800" height="400">
</div>
<div align="center">
  <img src="https://res.cloudinary.com/dgm059qwp/image/upload/v1716338295/SO/v7fumzrgabtarrj3gsmr.png" alt="Imagen2" width="400" height="250">
</div>

## Guía de Uso

1) Clonar este repositorio
```git
git clone https://github.com/Joshy14Y/OS_Object_Detection.git
```
2) Crear un entorno de Conda con Python 3.11 e instalar las siguientes dependencias:

Package                   Version
------------------------- --------------------
aiosignal                 1.3.1
albumentations            1.4.7
annotated-types           0.6.0
anyio                     4.2.0
argon2-cffi               21.3.0
argon2-cffi-bindings      21.2.0
asttokens                 2.0.5
async-lru                 2.0.4
attrs                     23.1.0
Babel                     2.11.0
beautifulsoup4            4.12.2
bleach                    4.1.0
Brotli                    1.0.9
certifi                   2023.7.22
cffi                      1.16.0
chardet                   4.0.0
charset-normalizer        2.0.4
click                     8.1.7
colorama                  0.4.6
comm                      0.2.1
contourpy                 1.2.1
cycler                    0.10.0
debugpy                   1.6.7
decorator                 5.1.1
defusedxml                0.7.1
exceptiongroup            1.2.0
executing                 0.8.3
fastjsonschema            2.16.2
filelock                  3.13.1
fonttools                 4.51.0
frozenlist                1.4.1
fsspec                    2024.2.0
idna                      2.10
imageio                   2.34.1
intel-openmp              2021.4.0
ipykernel                 6.28.0
ipython                   8.20.0
ipywidgets                8.1.2
jedi                      0.18.1
Jinja2                    3.1.3
joblib                    1.4.2
json5                     0.9.6
jsonschema                4.19.2
jsonschema-specifications 2023.7.1
jupyter                   1.0.0
jupyter_client            8.6.0
jupyter-console           6.6.3
jupyter_core              5.5.0
jupyter-events            0.8.0
jupyter-lsp               2.2.0
jupyter_server            2.10.0
jupyter_server_terminals  0.4.4
jupyterlab                4.0.11
jupyterlab-pygments       0.1.2
jupyterlab_server         2.25.1
jupyterlab-widgets        3.0.10
kiwisolver                1.4.5
lazy_loader               0.4
MarkupSafe                2.1.3
matplotlib                3.8.4
matplotlib-inline         0.1.6
mistune                   2.0.4
mkl                       2021.4.0
mpmath                    1.3.0
msgpack                   1.0.8
nbclient                  0.8.0
nbconvert                 7.10.0
nbformat                  5.9.2
nest-asyncio              1.6.0
networkx                  3.2.1
notebook                  7.0.8
notebook_shim             0.2.3
numpy                     1.26.3
opencv-python             4.9.0.80
opencv-python-headless    4.9.0.80
overrides                 7.4.0
packaging                 23.2
pandas                    2.2.2
pandocfilters             1.5.0
parso                     0.8.3
pillow                    10.2.0
pip                       23.3.1
platformdirs              3.10.0
ply                       3.11
prometheus-client         0.14.1
prompt-toolkit            3.0.43
protobuf                  5.26.1
psutil                    5.9.0
pure-eval                 0.2.2
py-cpuinfo                9.0.0
pycparser                 2.21
pydantic                  2.7.1
pydantic_core             2.18.2
Pygments                  2.15.1
pyparsing                 3.1.2
PyQt5                     5.15.10
PyQt5-sip                 12.13.0
PySocks                   1.7.1
python-dateutil           2.8.2
python-dotenv             1.0.1
python-json-logger        2.0.7
python-magic              0.4.27
pytz                      2024.1
pywin32                   305.1
pywinpty                  2.0.10
PyYAML                    6.0.1
pyzmq                     25.1.2
qtconsole                 5.5.1
QtPy                      2.4.1
ray                       2.10.0
referencing               0.30.2
requests                  2.31.0
requests-toolbelt         1.0.0
rfc3339-validator         0.1.4
rfc3986-validator         0.1.1
roboflow                  1.1.28
rpds-py                   0.10.6
scikit-image              0.23.2
scikit-learn              1.4.2
scipy                     1.13.0
seaborn                   0.13.2
Send2Trash                1.8.2
setuptools                68.2.2
sip                       6.7.12
six                       1.16.0
sniffio                   1.3.0
soupsieve                 2.5
stack-data                0.2.0
sympy                     1.12
tbb                       2021.11.0
terminado                 0.17.1
thop                      0.1.1.post2209072238
threadpoolctl             3.5.0
tifffile                  2024.5.10
tinycss2                  1.2.1
tomli                     2.0.1
torch                     2.3.0+cu121
torchaudio                2.3.0+cu121
torchvision               0.18.0+cu121
tornado                   6.3.3
tqdm                      4.66.2
traitlets                 5.7.1
typing_extensions         4.9.0
tzdata                    2024.1
ultralytics               8.2.4
urllib3                   2.1.0
wcwidth                   0.2.5
webencodings              0.5.1
websocket-client          0.58.0
wheel                     0.41.2
widgetsnbextension        4.0.10
win-inet-pton             1.1.0

3) Ejecutar el archivo main.py en el entorno conda creado.