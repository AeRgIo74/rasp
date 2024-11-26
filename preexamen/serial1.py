
import serial
from time import sleep


ser = serial.Serial("/dev/rfcomm0",9600) #Se inicia la comunicacion serial con los parametros de:
#nombre del dispositivo serial, baud rate, tiempo para leer operaciones
ser.reset_input_buffer() # limpiar byte innecesario

# a=0


try:
    # Bucle principal para medir y reportar continuamente la distancia
    while True:
        a=int(input("ingrese 1 o 0  -   "))
        
        msg=str(a)
        msg=msg+"\n"
        data=ser.write(msg.encode())
        sleep(1)
        print(a,"\n")

except KeyboardInterrupt:
    #print('Interrupcion de teclado')# Manejar KeyboardInterrupt (Ctrl+C) para salir del bucle de manera ordenada
    print("Programa terminado por el usuario")
    ser.close()
    
