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

def actualizarCoordenadas(matriz, ruta):
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


def graficar(contador):
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
    
    actualizarCoordenadas(matriz, ruta)
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
    
    actualizarCoordenadas(matriz, ruta)
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
    
    actualizarCoordenadas(matriz, ruta)
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
    
    actualizarCoordenadas(matriz, ruta)
    return matriz


opcion=0
contador=0
Graficas=[]
Graficas.append(graficar(contador))
contador=int(contador)+1
while(opcion!=6):
    print("Ingresa lo que quieras hacer: ")
    print("1-Reflectar")
    print("2-Expandir")
    print("3-Cortar")
    print("4-Rotar con respecto al origen")
    print("5-Graficar")
    print("6-Salir")
    opcion=int(input())
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
        Graficas.append(graficar(contador))
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
        matriz=expandir(matriz, c, eje, ruta)
        Graficas.append(graficar(contador))
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
        Graficas.append(graficar(contador))
        contador=int(contador)+1
    elif(opcion==4):
        print("Ingresa el valor del ángulo para rotar")
        c=float(input())
        matriz=rotar(matriz, c, eje, ruta)
        Graficas.append(graficar(contador))
        contador=int(contador)+1
    elif(opcion==5):
        Graficas.append(graficar(contador))
        contador=int(contador)+1
    elif(opcion==6):
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