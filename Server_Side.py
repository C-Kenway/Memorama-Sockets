
import socket
import random
import time
HOST = "127.0.0.1"
#HOST = "192.168.90.165"  # The server's hostname or IP address
PORT = 5000  # Puerto usado por el servidor
buffer_size = 1024

#HOST = str(input('Ingrese el la direccion del host para el server: '))
#PORT = int(input('Ingrese el Puerto: '))
# Crear un objeto socket para el servidor
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignar una dirección IP y un número de puerto al socket
servidor.bind((HOST, PORT))

# Configurar el socket para escuchar conexiones entrantes
servidor.listen(1)
print('El servidor está escuchando en {}:{}'.format(HOST, PORT))

# Aceptar una conexión entrante
cliente, direccion = servidor.accept()
print('Se ha establecido una conexión desde {}:{}'.format(direccion[0], direccion[1]))

#Espera la decicion de la dificultad
#respuesta = cliente.recv(buffer_size).decode()
dificultad = str(cliente.recv(buffer_size).decode())
print('Respuesta del servidor:', dificultad)
if 'Principiante' in dificultad:
   # Inicializar el tablero del juego para Principiante
   palabras = ['gato', 'perro', 'oso', 'conejo']
   tablero = random.sample(palabras * 2, k=8)
   random.shuffle(tablero)
   tablero_oculto = ['X'] * 8
   print(tablero)
   lim_sup = 7

if 'Avanzado' in dificultad:
   # Inicializar el tablero del juego para Avanzado
   palabras = ['gato', 'perro', 'oso', 'conejo','pez','lobo','jirafa','canario','iguana']
   tablero = random.sample(palabras * 2, k=18)
   random.shuffle(tablero)
   tablero_oculto = ['X'] * 18
   print(tablero)
   lim_sup = 17

puntaje=0
# Enviar el tablero oculto al cliente
cliente.send(str(tablero_oculto).encode())
start_time = time.time()
# Iniciar el bucle del juego
Intento=0
tiro_previo = " "
while True:

    # Recibir una selección del cliente
    seleccion = int(cliente.recv(buffer_size).decode())
    # Verificar si la selección es válida
    if seleccion < 0 or seleccion > lim_sup:
        respuesta = 'La selección no es válida '
        cliente.send(str(tablero_oculto).encode())
        # Enviar la respuesta al cliente
        cliente.send(respuesta.encode())
        Intento = 0
    elif tablero_oculto[seleccion] != 'X':

        respuesta = 'La carta ya fue seleccionada'
        # Mostrar la carta seleccionada al cliente
        cliente.send(str(tablero_oculto).encode())
        # Enviar la respuesta al cliente
        cliente.send(respuesta.encode())
        Intento=0
    else:
        if Intento == 2:
            # Verificar si se formó una pareja
            if tiro_previo == tablero[seleccion]:
                respuesta = '\n¡Felicidades! Ha formado una pareja'
                # Mostrar la carta seleccionada al cliente
                tablero_oculto[seleccion] = tablero[seleccion]
                cliente.send(str(tablero_oculto).encode())
                Intento=0
                tiro_previo=""
                if 'X' not in tablero_oculto:
                    cliente.send('\n ¡Felicidades! Ha ganado el juego'.encode())
                    break
                else:
                    # Enviar la respuesta al cliente
                    cliente.send(respuesta.encode())
                    puntaje = puntaje + 1
            else:
                respuesta = 'No fue pareja. Sige Jugando'
                # Mostrar la carta seleccionada al cliente
                tablero_oculto[seleccion] = tablero[seleccion]
                cliente.send(str(tablero_oculto).encode())
                #Volvemos a cubrir todas las cartas
                tablero_oculto = ['X'] * 8
                # Enviar la respuesta al cliente
                cliente.send(respuesta.encode())
                tiro_previo =" "
                Intento = 0
                if puntaje!=0:
                    puntaje = puntaje-1
                else:
                    puntaje = puntaje
        else:
            Intento = 1
            if Intento == 1:
                respuesta = 'Siguiente Tiro'
                # Mostrar la carta seleccionada al cliente
                tablero_oculto[seleccion] = tablero[seleccion]
                cliente.send(str(tablero_oculto).encode())
                # Enviar la respuesta al cliente
                cliente.send(respuesta.encode())
                # Guardamos la posicion del tiro previo para comparar si es pareja mas adelante
                tiro_previo = tablero[seleccion]
                Intento = Intento + 1




end_time = time.time()
elapsed_time = end_time-start_time
tiempoP = f'\n Tiempo transcurrido: {elapsed_time:.2f} segundos'
cliente.send(str(tiempoP).encode())
puntaje2 = f'\nPuntaje Final: {puntaje}'
cliente.send(str(puntaje2).encode())
# Cerrar la conexión con el cliente
cliente.close()

# Cerrar el socket del servidor
servidor.close()

