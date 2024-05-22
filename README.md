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
Al realizar todo el proceso, los resultados demuestran el recuento y la confianza, de lo contrario da estadísticas en blanco, lo que significa que no encontró nada. 
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
Y luego debe de ejecutar esta lista de comandos
```cd
git clone https://github.com/Joshy14Y/OS_Object_Detection.git
```
```cd
git clone https://github.com/Joshy14Y/OS_Object_Detection.git
```
```cd
git clone https://github.com/Joshy14Y/OS_Object_Detection.git
```
```cd
git clone https://github.com/Joshy14Y/OS_Object_Detection.git
```

