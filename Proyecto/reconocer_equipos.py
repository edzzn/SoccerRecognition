import cv2
import os
import numpy as np


def contadorMascara(jugador_img, player_hsv, lower_color, upper_color):
    # Equipo 1
    mascara1 = cv2.inRange(player_hsv, lower_color, upper_color)
    res1 = cv2.bitwise_and(jugador_img, jugador_img, mask=mascara1)
    res1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
    res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
    conteoNoZero = cv2.countNonZero(res1)
    return conteoNoZero


def reconocer_equipo(image):
    equipo = ""
    team_color = (255, 0, 0)

    lower_verde = np.array([40, 40, 40])
    upper_verde = np.array([70, 255, 255])

    lower_azul = np.array([92, 86, 61])
    upper_azul = np.array([179, 255, 255])

    lower_blanco = np.array([0, 4, 209])
    upper_blanco = np.array([179, 255, 255])

    lower_neon = np.array([0, 163, 163])
    upper_neon = np.array([179, 255, 255])
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_verde, upper_verde)
    res = cv2.bitwise_and(image, image, mask=mask)
    res_gray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # kernel para operaciones morfológicas en la imagen de umbral para una mejor salida
    kernel = np.ones((13, 13), np.uint8)
    thresh = cv2.threshold(
        res_gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    # Encuentra contorno en imagen de umbral
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # Criterios seleccion jugadores
        if(h >= (1.1)*w):
            if(w > 0.5 and h >= 0.5):
                jugador_img = image[y:y+h, x:x+w]
                player_hsv = cv2.cvtColor(jugador_img, cv2.COLOR_BGR2HSV)
                # Equipo 1
                conteoNoZero1 = contadorMascara(
                    jugador_img, player_hsv, lower_azul, upper_azul)
                # Equipo 2
                conteoNoZero = contadorMascara(
                    jugador_img, player_hsv, lower_blanco, upper_blanco)
                # Equipo 3
                conteoNoZero2 = contadorMascara(
                    jugador_img, player_hsv, lower_neon, upper_neon)
                orden = max(
                    sorted([conteoNoZero1, conteoNoZero, conteoNoZero2]))

                if(conteoNoZero1 >= 20 and orden == conteoNoZero1):
                    equipo = "Barca"
                    team_color = (72, 54, 176)
                if(conteoNoZero >= 20 and orden == conteoNoZero):
                    equipo = "Real Madrid"
                    team_color = (55, 175, 212)

                if(conteoNoZero2 >= 20 and orden == conteoNoZero2):
                    equipo = "Arbitro - Juez"
                    team_color = (0, 0, 255)

    label = 'Persona' if equipo == '' else equipo
    return (label, team_color)


if __name__ == "__main__":
    image = cv2.imread('./rm.png')
    equipo = reconocer_equipo(image)
    print(equipo)
