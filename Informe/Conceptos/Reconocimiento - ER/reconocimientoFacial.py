import cv2
import face_recognition

def reconocimientoFacial(frame):
    as_image = face_recognition.load_image_file("asencio.jpg")
    as_face_encoding = face_recognition.face_encodings(as_image)[0]
    is_image = face_recognition.load_image_file("isco1.jpg")
    is_face_encoding = face_recognition.face_encodings(is_image)[0]
    me_image = face_recognition.load_image_file("messi.jpg")
    me_face_encoding = face_recognition.face_encodings(me_image)[0]
    pi_image = face_recognition.load_image_file("pique.jpg")
    pi_face_encoding = face_recognition.face_encodings(pi_image)[0]
    ro_image = face_recognition.load_image_file("ronaldo.jpg")
    ro_face_encoding = face_recognition.face_encodings(ro_image)[0]
    me2_image = face_recognition.load_image_file("messi2.jpg")
    me2_face_encoding = face_recognition.face_encodings(me2_image)[0]
    sua_image = face_recognition.load_image_file("suarez2.jpg")
    sua_face_encoding = face_recognition.face_encodings(sua_image)[0]
    dem_image = face_recognition.load_image_file("dembele.jpg")
    dem_face_encoding = face_recognition.face_encodings(dem_image)[0]
    jmsanchez_image = face_recognition.load_image_file("jmsanchez.jpg")
    jmsanchez_face_encoding = face_recognition.face_encodings(jmsanchez_image)[0]
    rak_image = face_recognition.load_image_file("rakitic.jpg")
    rak_face_encoding = face_recognition.face_encodings(rak_image)[0]

    known_faces = [
        as_face_encoding,
        is_face_encoding,
        me_face_encoding,
        pi_face_encoding,
        ro_face_encoding,
        me2_face_encoding,
        sua_face_encoding,
        dem_face_encoding,
        jmsanchez_face_encoding,
        rak_face_encoding
    ]
    face_locations = []
    face_encodings = []
    face_names = []
    # Cambio de imagen de BGR A RGB 
    rgb_frame = frame[:, :, ::-1]
    # Localiza rostros
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    face_names = []
    for face_encoding in face_encodings:
        # Coincidencia de rostro
        match = face_recognition.compare_faces(known_faces, face_encoding, tolerance=0.50)
        name = None
        if match[0]:
            name = "Asensio"
        elif match[1]:
            name = "Isco"
        elif match[2]:
            name = "Messi"
        elif match[3]:
            name = "Pique"
        elif match[4]:
            name = "Ronaldo"
        elif match[5]:
            name = "Messi"
        elif match[6]:
            name = "Suarez"
        elif match[7]:
            name = "Dembele"
        elif match[8]:
            name = "JM Sanchez"
        elif match[9]:
            name = "Rakitic"
        face_names.append(name)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        print(name)


prueba = cv2.imread('prueba.jpg') 

reconocimientoFacial(prueba)