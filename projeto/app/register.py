# -*- coding: latin-1 -*-

import cv2
import os
import threading

from PIL import Image
photos_limit = 450

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

pictures_confirm = True

new_user = raw_input("Insira o nome do usuário a ser cadastrado: ")

confirmation = raw_input("Esse é o nome desejado? " + new_user + "\n(digite sim ou nao) ")
confirmation = confirmation.lower()

while confirmation[0] is 'n' or confirmation[0] is not 's':
    new_user = raw_input("Insira o nome do usuário a ser cadastrado: ")
    confirmation = raw_input("Esse é o nome desejado? " + new_user + "\n(digite sim ou nao) ")
    confirmation = confirmation.replace(" ", "").lower()

images_directory = os.getcwd()
print(images_directory)

images_directory = images_directory + "/Images/" + new_user
print(images_directory)


try:
    os.makedirs(images_directory)
except OSError:
    print("Ocorreu um erro ao criar usuário. Verifique se o nome já está sendo, se há caracteres inválidos no nome usado ou se não há espaço suficiente. O programa será abortado.")
    exit(1)
else:
    print("O usuario de nome", new_user, "foi cadastrado com sucesso!")    


print("O programa irá retirar algumas fotos do usuário para o reconhecimento facial. O usuário precisa se posicionar em frente a câmera.")
raw_input("Pressione ENTER para continuar...")

capture = cv2.VideoCapture(0)

photos_taken = 0
while(pictures_confirm):
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for(x, y, w, h) in faces:
        region_of_interest_colored = frame[y:y+h, x:x+w]
        rectangle_thickness = 2
        rectangle_color = (0, 255, 0)
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), rectangle_color, rectangle_thickness)

    cv2.imshow('Novo usuário', frame)
    save_image = "image" + str(photos_taken) + ".png"
    
    if cv2.waitKey(20) & 0xFF == ord('q') | photos_taken == photos_limit:
        break

capture.release()
cv2.destroyAllWindows()
raw_input("O programa terminou. Pressione ENTER para sair...")




