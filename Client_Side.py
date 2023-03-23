#!/usr/bin/env python3
import socket
import os
HOST = "127.0.0.1"  # Nombre del host o direccion ip
#HOST = "192.168.254.223"  # Nombre del host o direccion ip
PORT = 5000  # Puerto usado por el servidor
buffer_size = 1024

#HOST = str(input('Ingrese el la direccion del host para el server: '))
#PORT = int(input('Ingrese el Puerto: '))
# Crear un objeto socket para el cliente
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar el socket a un servidor remoto en el puerto 5000
cliente.connect((HOST, PORT))
print('Se ha establecido una conexión con el servidor remoto.')

#Selecciona Dificultad del juego
while True:
    print("Dificultad: 1)Principiante 2)Avanzado \n Ingrese numero:")
    eleccion = input()
    int_eleccion = int(eleccion)
    if int_eleccion == 1:
        cliente.send('Principiante'.encode())
        break
    elif int_eleccion== 2:
        cliente.send('Avanzado'.encode())
        break
    else:
        print("Digite una opcion valida")
# Recibir el tablero oculto del servidor
tablero_oculto = eval(cliente.recv(buffer_size).decode())
print('Tablero para tu partida:\n', tablero_oculto)

# Iniciar el bucle del juego
while True:
    os.system("cls")
    # Solicitar al usuario que seleccione una carta
    seleccion = int(input('\nIngrese el número de la carta que desea voltear (0-7): '))

    # Enviar la selección al servidor
    cliente.send(str(seleccion).encode())

    carta_volteada=eval(cliente.recv(buffer_size).decode())
    print("")
    print('Tu Tablero:', carta_volteada)

    # Recibir la respuesta del servidor
    respuesta = cliente.recv(buffer_size).decode()
    print('Respuesta del servidor:', respuesta)

    # Verificar si el juego ha terminado
    if '\n ¡Felicidades! Ha ganado el juego' in respuesta:
        break

tiempoP = cliente.recv(buffer_size).decode()
print(tiempoP)
puntaje = cliente.recv(buffer_size).decode()
print(puntaje)
# Cerrar la conexión con el servidor
cliente.close()
