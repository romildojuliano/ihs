# -*- coding: latin-1 -*-

import cv2
import os
import threading

from PIL import Image
photos_limit = 300

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml')

new_user = raw_input("Insira o nome do usuário a ser cadastrado: ")

confirmation = raw_input("Esse é o nome desejado? " + new_user + "\n(digite sim ou nao) ")
confirmation = confirmation.lower()

while confirmation[0] is 'n' or confirmation[0] is not 's':
    new_user = raw_input("Insira o nome do usuário a ser cadastrado: ")
    confirmation = raw_input("Esse é o nome desejado? " + new_user + "\n(digite sim ou nao) ")
    confirmation = confirmation.replace(" ", "").lower()

images_directory = os.getcwd()
print(images_directory)

images_directory = images_directory + "/Images/" + str(new_user) + '/'
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
while(True):
    ret, frame = capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
    for(x, y, w, h) in faces:
        region_of_interest = frame[y:y+h, x:x+w]
        rectangle_thickness = 2
        rectangle_color = (0, 255, 0)
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), rectangle_color, rectangle_thickness)
        save_image = "image" + str(photos_taken) + ".png"
        print(save_image)
        cv2.imwrite("Images/" + new_user + "/" + save_image, frame)
        photos_taken += 1

    cv2.imshow('Novo usuario', frame)
    if cv2.waitKey(20) & 0xFF == ord('q') or photos_taken == photos_limit:
        break

capture.release()
cv2.destroyAllWindows()
print("Leitura completa! O usuário " + new_user + " foi cadastrado com sucesso!")
raw_input("Agora o programa irá realizar a atualização do banco de dados. Pressione ENTER para continuar...")
os.system('python faces_train.py')
raw_input("A atualização terminou. Pressione ENTER para sair...")




