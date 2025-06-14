import cv2
import numpy as np
import face_recognition

# Cargar el clasificador HaarCascade
face_cascade = cv2.CascadeClassifier('assets/haarcascade_frontalface_default.xml')

def get_face_encoding(image):
    rgb_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    encodings = face_recognition.face_encodings(rgb_img)
    if encodings:
        return encodings[0]
    return None 