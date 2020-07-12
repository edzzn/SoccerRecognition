try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import cv2
import time
import random


def reconocer_numero(image):
    t1 = time.time()
    numero = random.randint(2, 30)
    # numero = ''
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # image = Image.fromarray(image)

    # texto = pytesseract.image_to_string(image)
    # if (texto != ''):
    #     numero = ''.join(c for c in texto if c.isdigit())

    # t2 = time.time()
    # print('rec num', str(t2-t1))
    return numero
