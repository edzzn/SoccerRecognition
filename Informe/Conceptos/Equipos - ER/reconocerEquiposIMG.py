import cv2
import os
import numpy as np
class searchEquipo:
    def __init__(self, image):
        self.image=image
        self.lower_verde = np.array([40,40, 40])
        self.upper_verde = np.array([70, 255, 255])

        self.lower_azul = np.array([92,86,61])
        self.upper_azul = np.array([179,255,255])

        self.lower_blanco = np.array([0,4,209])
        self.upper_blanco = np.array([179,255,255])

        self.lower_neon = np.array([0,163,163])
        self.upper_neon = np.array([179,255,255])
        self.font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    def contadorMascara(self,jugador_img,player_hsv,lower_color,upper_color):
        # Equipo 1
        mascara1 = cv2.inRange(player_hsv, lower_color,upper_color)
        res1 = cv2.bitwise_and(jugador_img, jugador_img, mask=mascara1)
        res1 = cv2.cvtColor(res1,cv2.COLOR_HSV2BGR)
        res1 = cv2.cvtColor(res1,cv2.COLOR_BGR2GRAY)
        conteoNoZero = cv2.countNonZero(res1)
        return conteoNoZero
    def detectarEquipo(self):
        hsv = cv2.cvtColor(self.image,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_verde, self.upper_verde)
        res = cv2.bitwise_and(self.image, self.image, mask=mask)
        res_gray = cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
        # kernel para operaciones morfológicas en la imagen de umbral para una mejor salida
        kernel = np.ones((13,13),np.uint8)
        thresh = cv2.threshold(res_gray,127,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        #Encuentra contorno en imagen de umbral    
        _,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            #Criterios seleccion jugadores
            if(h>=(1.1)*w):
                if(w>0.5 and h>= 0.5):
                    jugador_img = self.image[y:y+h,x:x+w]
                    player_hsv = cv2.cvtColor(jugador_img,cv2.COLOR_BGR2HSV)
                    # Equipo 1
                    conteoNoZero1=self.contadorMascara(jugador_img,player_hsv,self.lower_azul,self.upper_azul)
                    # Equipo 2
                    conteoNoZero=self.contadorMascara(jugador_img,player_hsv,self.lower_blanco,self.upper_blanco)
                    # Equipo 3
                    conteoNoZero2=self.contadorMascara(jugador_img,player_hsv,self.lower_neon,self.upper_neon)
                    orden=max(sorted([conteoNoZero1,conteoNoZero,conteoNoZero2]))
                    equipo=""
                    colores=(255,255,255)
                    if(conteoNoZero1 >= 20 and orden==conteoNoZero1):
                        equipo="Barca"
                        colores=(0,0,255)
                    else:
                        pass
                    if(conteoNoZero>=20 and  orden==conteoNoZero):
                        equipo="Real Madrid"
                        colores=(255,255,255)
                    else:
                        pass
                    if(conteoNoZero2>=20 and orden==conteoNoZero2):
                        equipo="Arbitro - Juez"
                        colores=(252, 231, 159)
                    else:
                        pass
                    print("Equipo> ",equipo)
                    cv2.putText(self.image, equipo, (x-2, y-2), self.font, 0.8, colores, 2, cv2.LINE_AA)
                    cv2.rectangle(self.image,(x,y),(x+w,y+h),colores,3)

        self.image =cv2.resize(self.image, (760, 540))
        cv2.imshow("Reconocimiento de Equipos",self.image)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()


image = cv2.imread('C:/Users/Fredd/Desktop/Equipos - ER/player-1058.jpg') 
imagenEquipo=searchEquipo(image)
imagenEquipo.detectarEquipo()

# image = cv2.imread('C:/Users/Fredd/Desktop/Equipos - ER/player-1059.jpg') 
# imagenEquipo=searchEquipo(image)
# imagenEquipo.detectarEquipo()

# image = cv2.imread('C:/Users/Fredd/Desktop/Equipos - ER/player-1060.jpg') 
# imagenEquipo=searchEquipo(image)
# imagenEquipo.detectarEquipo()

# image = cv2.imread('C:/Users/Fredd/Desktop/Equipos - ER/rm.png') 
# imagenEquipo=searchEquipo(image)
# imagenEquipo.detectarEquipo()