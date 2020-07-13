# Tracking de un partido de futbol-soccer
### Autores: 
- Abad Freddy, Reinozo Edisson, Santos David

##### Descripcion detallada: [Informe](www.google.com)

En el contexto del mundo globalizado actual, donde una persona de un lugar recóndito puede tener acceso a un amplio repertorio de campeonatos de fútbol, surge la necesidad de procesar estos juegos para generar conocimiento en base a la información existente. El procesamiento de video conforma una disciplina amplia basada en el procesamiento de imágenes. Procesar un partido de fútbol significa identificar a los *jugadores en campo, su número de camiseta, la ocurrencia de alguna falta de juego o la obtención de un gol*. 

Proponer este trabajo significa mantener un ambiente controlado permitiendo así ya sea a periodistas, aficionados o cuerpo directivo mejorar en la toma de decisiones que concluyan en una mejor estrategia de juego. Este procesamiento de video se implementa en distintas fases: *segmentación de la imagen, identificación de contornos, aproximación de objetos, rastreo a través de los frames de video, el dibujo de las secciones en movimiento y el análisis de faltas, goles, velocidad de jugador-balón*. 

Cada fase, prevé diversos problemas los cuales se abordan en este proyecto. Estos problemas no son nuevos, por lo que en la actualidad existen metodologías detalladas, modelos pre entrenados, los cuales fueron utilizados en este proyecto. Sin duda el campo de la visión por computadora, presenta muchas ventajas antes diversas situaciones en las cuales explorar.

Herramientas utilizadas: 
- OpenCV
- Face_recognition
- YOLO v3

Funciones y herramientas utilizadas en cada una
- Identificacion de Jugadores y Balon - YOLO v3.
- Reconocimiento facial en imágenes en primera camara- facial_recognition.
- Demarcacion de lineas del campo de juego y analisis de gol - OpenCV - HoughLines.
- Identificacion de Equipos en base al uniforme - Delimitacion de Colores usando el esquema de colores HSV (OpenCV).
- Traza del balon y calculo de velocidad - Uso de álgebra y geometría basica (Fórmula de Velocidad, Distancia).

### Resultado
<div style="width: 100%; height: 0px; position: relative; padding-bottom: 55.000%;"><iframe src="https://streamable.com/e/ins44d" frameborder="0" width="100%" height="100%" allowfullscreen style="width: 100%; height: 100%; position: absolute;"></iframe></div>
