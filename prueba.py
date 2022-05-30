from csv import writer
import os
from os import remove


#Ruta del archivo
ruta = "Programa poligonos/poligono.txt"
remove(ruta)

file = open(ruta, "w")
file.write("x y\n")
file.close()

print("Hola, ingresa la cantidad de puntos que quieras agregar")
#Cantidad de lados
n=int(input())
#Ciclo para obtener las coordenadas
for i in range(0, n):
    print("Ingresa x del vector "+str(i))
    #coordenada en x
    x=int(input())
    print("Ingresa y del vector "+str(i))
    #coordenada en y
    y=int(input())
    #cadena para agregar a un archivo de texto del cual se leerá la coordenada
    cadena=str(x)+" "+str(y)
    #se abre el archivo en a para append(añadir)
    with open(ruta, 'a') as f:
        #se inserta la cadena al archivo
        f.write(cadena+"\r")
        f.close()
