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
- Identificacion de Jugadores (Uniforme y Numero) y Balon - YOLO v3 e Identificacion de Equipos en base al uniforme - Delimitacion de Colores usando el esquema de colores HSV (OpenCV).

  ![HSV](https://user-images.githubusercontent.com/38579765/87358132-cbfee780-c52a-11ea-9a74-dce5b913afec.png)
  ![EQUIPO1](https://user-images.githubusercontent.com/38579765/87358199-f05ac400-c52a-11ea-8890-c687a965468d.png)
  ![EQUIPO3](https://user-images.githubusercontent.com/38579765/87358214-f51f7800-c52a-11ea-9eaf-809124471ad9.png)
  ![EQUIPO2](https://user-images.githubusercontent.com/38579765/87358215-f650a500-c52a-11ea-9bb5-b2bcdfe90319.png)
  ![OCR](https://user-images.githubusercontent.com/38579765/87358316-28620700-c52b-11ea-90be-c45b26372893.png)
  
- Reconocimiento facial en imágenes en primera camara- facial_recognition.
  
  ![RECONOCIMIENTO](https://user-images.githubusercontent.com/38579765/87358309-239d5300-c52b-11ea-9c8a-83171ff81d4e.png)
  
- Reconocimiento de Gol
  
  ![GOL](https://user-images.githubusercontent.com/38579765/87358288-1a13eb00-c52b-11ea-89b7-e27e204bbcb9.png)

- Demarcacion de lineas del campo de juego y analisis de gol - OpenCV - HoughLines.
  
  ![LINEA](https://user-images.githubusercontent.com/38579765/87358300-1ed89f00-c52b-11ea-9da3-43533d03f347.png)

- Traza del balon y calculo de velocidad - Uso de álgebra y geometría basica (Fórmula de Velocidad, Distancia).
  
  ![TRAZA](https://user-images.githubusercontent.com/38579765/87358313-26984380-c52b-11ea-931a-15782ba8ba12.png)
  ![TRAZA2](https://user-images.githubusercontent.com/38579765/87358521-9d354100-c52b-11ea-9b44-0ee3bf5fc3cb.png)

### Resultado
[Video](https://streamable.com/e/ins44d)
