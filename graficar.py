import itertools
import io
from string import ascii_uppercase
from matplotlib.transforms import TransformNode
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import os
from os import remove
import math
import webbrowser

from sympy import expand, matrix2numpy

def labels_gen():
    size = 1
    while True:
        for s in itertools.product(ascii_uppercase, repeat=size):
            yield "".join(s)
        size +=1

ruta = "Programa poligonos/poligono.txt"
remove(ruta)

file = open(ruta, "w")
file.write("x y\n")
file.close()
n=0
op=0
print("Hola, quieres ingresar los puntos (1) o elegir una figura predeterminada (2)?")
op=int(input())
if(op==2):
    opcion=6
else:
    

    print("Hola, ingresa la cantidad de puntos que quieras agregar")
    #Cantidad de lados
    n=int(input())

    matriz = [[0] * 2 for i in range(n)]

    #Ciclo para obtener las coordenadas
    for i in range(0, n):
        print("Ingresa x del punto "+str(i+1))
        #coordenada en x
        x=float(input())
        matriz[i][0]=x
        print("Ingresa y del punto "+str(i+1))
        #coordenada en y
        y=float(input())
        matriz[i][1]=y
        #cadena para agregar a un archivo de texto del cual se leerá la coordenada
        cadena=str(x)+" "+str(y)
        #se abre el archivo en a para append(añadir)
        with open(ruta, 'a') as f:
            #se inserta la cadena al archivo
            f.write(cadena+"\r")
            f.close()

    print(matriz)



def graficar(contador, ruta):
    # Cargamos el csv
    data=pd.read_csv(ruta ,header=0,delim_whitespace=True)

    # Cálculo del centroide
    centroide = np.mean(data, axis=0)

    # Cáculo del ángulo polar
    aux = data - centroide
    polar_angles = np.arctan2(aux.y, aux.x)

    # Obtenemos un nuevo DataFrame con los vértices ordenados
    data = data.reindex(polar_angles.argsort())


    ax = plt.subplot(111)

    # Creamos el polígono
    plygon = plt.Polygon(data, fill=True, facecolor="#ffb3b3", edgecolor='#ff0000', alpha=1, zorder=1)
    ax.add_patch(plygon)

    # Creamos los vértices
    ax.scatter(data.x, data.y, c='b', zorder=2)

    # Etiquetas para cada vértice y arista
    etiquetas = labels_gen()
    for i, vertice in enumerate(data.values):
        lb = next(etiquetas)
        ax.annotate(str(lb), xy=vertice + 0.1)
        punto_medio = (vertice +  data.values[(i + 1) % (data.shape[0])]) / 2
        ax.annotate(str(lb.lower()), xy=punto_medio)

    # Mostramos los ejes centrados en el origen
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Configuramos la rejilla
    ax.grid(color='gray', linestyle='dashed', linewidth=1, alpha=0.4)

    # Escalamos la gráfica
    ax.autoscale_view()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))

    
    #Guardamos la gráfica
    nombreGrafica="grafica"+str(contador)+".png"
    plt.savefig(nombreGrafica)
    
    # Mostramos la gráfica
    plt.show()
    #return nombreGrafica

def actualizarCoordenadas(matriz, ruta, n):
    file = open(ruta, "w")
    file.write("x y\n")
    file.close()

    #Ciclo para obtener las coordenadas
    for i in range(0, n):
        #coordenada en x
        x=matriz[i][0]
        #coordenada en y
        y= matriz[i][1]
        #cadena para agregar a un archivo de texto del cual se leerá la coordenada
        cadena=str(x)+" "+str(y)
        #se abre el archivo en a para append(añadir)
        with open(ruta, 'a') as f:
            #se inserta la cadena al archivo
            f.write(cadena+"\r")
            f.close()


def multiplicarMatrices(matriz, matriz2):

    multiplicacion = [[0] * 2 for i in range(len(matriz))]
    for i in range(len(multiplicacion)):
        for j in range(len(multiplicacion[i])):
            for k in range(len(matriz2)):
                multiplicacion [i][j] = multiplicacion [i][j] + matriz[i][k]*matriz2[k][j]
    print(multiplicacion)

    return multiplicacion


def reflexion(matriz, eje, ruta):
    if(eje=="X" or eje=="x"):
        transformacion = [[0] * 2 for i in range(2)]
        transformacion[0][0]=-1
        transformacion[0][1]=0
        transformacion[1][0]=0
        transformacion[1][1]=1
        print(transformacion)
        matriz=multiplicarMatrices(matriz, transformacion)
        print(matriz)
    elif(eje=="Y" or eje=="y"):
        transformacion = [[0] * 2 for i in range(2)]
        transformacion[0][0]=1
        transformacion[0][1]=0
        transformacion[1][0]=0
        transformacion[1][1]=-1
        print(transformacion)
        matriz=multiplicarMatrices(matriz, transformacion)
    
    actualizarCoordenadas(matriz, ruta, n)
    return matriz

def expandir(matriz, c, eje, ruta):
    if(eje=="X" or eje=="x"):
        transformacion = [[0] * 2 for i in range(2)]
        transformacion[0][0]=c
        transformacion[0][1]=0
        transformacion[1][0]=0
        transformacion[1][1]=1
        print(transformacion)
        matriz=multiplicarMatrices(matriz, transformacion)
        print(matriz)
    elif(eje=="Y" or eje=="y"):
        transformacion = [[0] * 2 for i in range(2)]
        transformacion[0][0]=1
        transformacion[0][1]=0
        transformacion[1][0]=0
        transformacion[1][1]=c
        print(transformacion)
        matriz=multiplicarMatrices(matriz, transformacion)
    
    actualizarCoordenadas(matriz, ruta, n)
    return matriz

def cortar(matriz, c, eje, ruta):
    if(eje=="X" or eje=="x"):
        transformacion = [[0] * 2 for i in range(2)]
        transformacion[0][0]=1
        transformacion[0][1]=0
        transformacion[1][0]=c
        transformacion[1][1]=1
        print(transformacion)
        matriz=multiplicarMatrices(matriz, transformacion)
        print(matriz)
    elif(eje=="Y" or eje=="y"):
        transformacion = [[0] * 2 for i in range(2)]
        transformacion[0][0]=1
        transformacion[0][1]=c
        transformacion[1][0]=0
        transformacion[1][1]=1
        print(transformacion)
        matriz=multiplicarMatrices(matriz, transformacion)
    
    actualizarCoordenadas(matriz, ruta, n)
    return matriz

def rotar(matriz, c, eje, ruta):
    
    transformacion = [[0] * 2 for i in range(2)]
    transformacion[0][0]=math.cos(math.radians(c))
    transformacion[0][1]=math.sin(math.radians(c))
    transformacion[1][0]=math.sin(math.radians(c))*(-1)
    transformacion[1][1]=math.cos(math.radians(c))
    print(transformacion)
    matriz=multiplicarMatrices(matriz, transformacion)
    print(matriz)
    
    actualizarCoordenadas(matriz, ruta, n)
    return matriz

ruta1="Programa poligonos/poligono1.txt"
file = open(ruta1, "w")
file.write("x y\n")
file.close()
with open(ruta1, 'a') as f:
    #se inserta la cadena al archivo
    f.write("2 2"+"\r")
    f.write("2 -2"+"\r")
    f.write("-2 2"+"\r")
    f.write("-2 -2"+"\r")
    f.close()

ruta2="Programa poligonos/poligono2.txt"
file = open(ruta2, "w")
file.write("x y\n")
file.close()
with open(ruta2, 'a') as f:
    #se inserta la cadena al archivo
    f.write("0 1"+"\r")
    f.write("3 3"+"\r")
    f.write("-3 3"+"\r")
    f.write("-2 4"+"\r")
    f.write("2 4"+"\r")
    f.write("0 3.5"+"\r")
    f.close()


ruta3="Programa poligonos/poligono3.txt"
file = open(ruta3, "w")
file.write("x y\n")
file.close()
with open(ruta3, 'a') as f:
    #se inserta la cadena al archivo
    f.write("0 9"+"\r")
    f.write("2 2"+"\r")
    f.write("-8 2"+"\r")
    f.write("8 2"+"\r")
    f.write("-2 2"+"\r")
    f.write("3 -2"+"\r")
    f.write("-3 -2"+"\r")
    f.write("0 -5"+"\r")
    f.write("5 -9"+"\r")
    f.write("-5 -9"+"\r")

    f.close()


ruta4="Programa poligonos/poligono4.txt"
file = open(ruta4, "w")
file.write("x y\n")
file.close()
with open(ruta4, 'a') as f:
    #se inserta la cadena al archivo
    f.write("0 0"+"\r")
    f.write("0 8"+"\r")
    f.write("6 8"+"\r")
    f.write("6 6"+"\r")
    f.write("2 6"+"\r")
    f.write("2 4"+"\r")
    f.write("4 4"+"\r")
    f.write("4 2"+"\r")
    f.write("2 2"+"\r")
    f.write("2 0"+"\r")

    f.close()

ruta5="Programa poligonos/poligono5.txt"
file = open(ruta5, "w")
file.write("x y\n")
file.close()
with open(ruta5, 'a') as f:
    #se inserta la cadena al archivo
    f.write("6 7"+"\r")
    f.write("2 7"+"\r")
    f.write("1 8"+"\r")
    
    f.close()


"""ruta5="Programa poligonos/poligono5.txt"
file = open(ruta5, "w")
file.write("x y\n")
file.close()
with open(ruta5, 'a') as f:
    #se inserta la cadena al archivo
    f.write("-10 1"+"\r")
    f.write("-9 2"+"\r")
    f.write("-7 3"+"\r")
    f.write("-5 3"+"\r")
    f.write("-3 6"+"\r")
    f.write("0 4"+"\r")
    f.write("4 3"+"\r")
    f.write("6 1"+"\r")
    f.write("8 7"+"\r")
    f.write("11 0"+"\r")
    f.write("12 -2"+"\r")
    f.write("10 -1"+"\r")
    f.write("6 -3"+"\r")
    f.write("5 -5"+"\r")
    f.write("2 -4"+"\r")
    f.write("-5 -4"+"\r")
    f.write("-7 -2"+"\r")
    f.write("-7 -6"+"\r")
    f.write("-8 -4"+"\r")
    f.write("-9 -2"+"\r")
    f.write("-9 -1"+"\r")
    f.write("-7 0"+"\r")
    

    f.close()
"""
#call it what you want



opcion=0
contador=0
Graficas=[]
if(op!=2):
    Graficas.append(graficar(contador, ruta))
contador=int(contador)+1
opcion2=0
ej1="ej1"
ej2="ej2"
ej3="ej3"
ej4="ej4"
ej5="ej5"
while(opcion!=7):
    if(op!=2):
        print("Ingresa lo que quieras hacer: ")
        print("1-Reflectar")
        print("2-Expandir")
        print("3-Cortar")
        print("4-Rotar con respecto al origen")
        print("5-Graficar")
        print("6-Mostrar ejemplos predeterminados")
        print("7-Salir")
        opcion=int(input())
    else:
        opcion=6
        op=1
    eje=""
    v=True
    c=0
    if(opcion==1):
        while(v):
            if(eje=="Y" or eje=="X" or eje=="y" or eje=="x"):
                v=False
            else:
                print("Ingresa el eje: ")
                eje=input()
        matriz=reflexion(matriz, eje, ruta)
        Graficas.append(graficar(contador, ruta))
        contador=int(contador)+1
    elif(opcion==2):
        while(v):
            if(eje=="Y" or eje=="X" or eje=="y" or eje=="x"):
                v=False
            else:
                print("Ingresa el eje: ")
                eje=input()
        print("Ingresa el valor de la constante para expandir")
        c=float(input())
        aux=c
        print("La constante es: "+str(aux))
        matriz=expandir(matriz, c, eje, ruta)
        Graficas.append(graficar(contador, ruta))
        contador=int(contador)+1
    elif(opcion==3):
        while(v):
            if(eje=="Y" or eje=="X" or eje=="y" or eje=="x"):
                v=False
            else:
                print("Ingresa el eje: ")
                eje=input()
        print("Ingresa el valor de la constante para cortar")
        c=float(input())
        matriz=cortar(matriz, c, eje, ruta)
        Graficas.append(graficar(contador, ruta))
        contador=int(contador)+1
    elif(opcion==4):
        print("Ingresa el valor del ángulo para rotar")
        c=float(input())
        matriz=rotar(matriz, c, eje, ruta)
        Graficas.append(graficar(contador, ruta))
        contador=int(contador)+1
    elif(opcion==5):
        Graficas.append(graficar(contador, ruta))
        contador=int(contador)+1
    elif(opcion==6):
        opcion=0
        print("Opcion 1")
        print("Opcion 2")
        print("Opcion 3")
        print("Opcion 4")
        print("Opcion 5")
        opcion2=int(input())
        if(opcion2==1):
            graficar(ej1, ruta1)
            
            

            with open(ruta1) as coordenadas:
                listaAux = coordenadas.readlines()
            coordenadas.close()
            print(listaAux)
            for i in range(len(listaAux)):
                listaAux[i]=listaAux[i].rstrip("\n")
            #print(listaAux)
            n=len(listaAux)-1
            matriz = [[0] * 2 for i in range(n)]
            for i in range(len(matriz)):
                matriz[i]=listaAux[i+1].split(" ")
            for i in range(len(matriz)):
                for j in range(len(matriz[i])):
                    matriz[i][j]=float(matriz[i][j])
            print(len(listaAux))
            actualizarCoordenadas(matriz, ruta, n)

        elif(opcion2==2):
            graficar(ej2, ruta2)

            with open(ruta2) as coordenadas:
                listaAux = coordenadas.readlines()
            coordenadas.close()
            print(listaAux)
            for i in range(len(listaAux)):
                listaAux[i]=listaAux[i].rstrip("\n")
            #print(listaAux)
            n=len(listaAux)-1
            matriz = [[0] * 2 for i in range(n)]
            for i in range(len(matriz)):
                matriz[i]=listaAux[i+1].split(" ")
            for i in range(len(matriz)):
                for j in range(len(matriz[i])):
                    matriz[i][j]=float(matriz[i][j])
            print(len(listaAux))
            actualizarCoordenadas(matriz, ruta, n)
        elif(opcion2==3):
            graficar(ej3, ruta3)

            with open(ruta3) as coordenadas:
                listaAux = coordenadas.readlines()
            coordenadas.close()
            print(listaAux)
            for i in range(len(listaAux)):
                listaAux[i]=listaAux[i].rstrip("\n")
            #print(listaAux)
            n=len(listaAux)-1
            matriz = [[0] * 2 for i in range(n)]
            for i in range(len(matriz)):
                matriz[i]=listaAux[i+1].split(" ")
            for i in range(len(matriz)):
                for j in range(len(matriz[i])):
                    matriz[i][j]=float(matriz[i][j])
            print(len(listaAux))
            actualizarCoordenadas(matriz, ruta, n)

        elif(opcion2==4):
            graficar(ej4, ruta4)

            with open(ruta4) as coordenadas:
                listaAux = coordenadas.readlines()
            coordenadas.close()
            print(listaAux)
            for i in range(len(listaAux)):
                listaAux[i]=listaAux[i].rstrip("\n")
            #print(listaAux)
            n=len(listaAux)-1
            matriz = [[0] * 2 for i in range(n)]
            for i in range(len(matriz)):
                matriz[i]=listaAux[i+1].split(" ")
            for i in range(len(matriz)):
                for j in range(len(matriz[i])):
                    matriz[i][j]=float(matriz[i][j])
            print(len(listaAux))
            actualizarCoordenadas(matriz, ruta, n)

        elif(opcion2==5):
            graficar(ej5, ruta5)

            with open(ruta5) as coordenadas:
                listaAux = coordenadas.readlines()
            coordenadas.close()
            print(listaAux)
            for i in range(len(listaAux)):
                listaAux[i]=listaAux[i].rstrip("\n")
            #print(listaAux)
            n=len(listaAux)-1
            matriz = [[0] * 2 for i in range(n)]
            for i in range(len(matriz)):
                matriz[i]=listaAux[i+1].split(" ")
            for i in range(len(matriz)):
                for j in range(len(matriz[i])):
                    matriz[i][j]=float(matriz[i][j])
            print(len(listaAux))
            actualizarCoordenadas(matriz, ruta, n)
        else:
            print("opcion no valida")
        
    elif(opcion==7):
        print("Bai")
    else:
        print("Opcion invalida")


"""
f = open('index.html','w')

mensaje = <html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Geometría de las T.L.</title>
</head>
<body>
    <header>
        <br>
        <h1>Geometría de las T.L.</h1>
        
    </header>
    
        <div>
            <br>
            <h2>Algoritmo Bayesiano</h2>
            <br>
            <p>Con ayuda de este algoritmo nos daremos cuenta la probabilidad que hay en que un estudiante 
            apruebe tomando en cuenta las calificaciones de las encuesta.</p>
             <img src='Bayesiano_calificaciones.png'>
        </div>
    <br><br>
    
</body>
</html>


f.write(mensaje)
f.close()

webbrowser.open_new_tab('index.html')
"""

"""
contador=0
Graficas=[]
Graficas.append(graficar(contador))
contador=int(contador)+1
eje="Y"

matriz=reflexion(matriz, eje, ruta)
Graficas.append(graficar(contador))

c=2
matriz=expandir(matriz, c, eje, ruta)

Graficas.append(graficar(contador))
contador=int(contador)+1

c=3
matriz=cortar(matriz, c, eje, ruta)

Graficas.append(graficar(contador))
contador=int(contador)+1

c=270
matriz=rotar(matriz, c, eje, ruta)

Graficas.append(graficar(contador))
contador=int(contador)+1

print(matriz)
"""

"""
Ingresa x del punto 1
2
Ingresa y del punto 1
2
Ingresa x del punto 2
1
Ingresa y del punto 2
1
Ingresa x del punto 3
-1
Ingresa y del punto 3
1
Ingresa x del punto 4
-2
Ingresa y del punto 4
2
Ingresa x del punto 5
-1
Ingresa y del punto 5
-1
Ingresa x del punto 6
-2
Ingresa y del punto 6
-2
Ingresa x del punto 7
1
Ingresa y del punto 7
-1
Ingresa x del punto 8
2
Ingresa y del punto 8
-2
"""