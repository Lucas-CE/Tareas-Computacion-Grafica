import numpy as np
from OpenGL.GL import *

SIZE_IN_BYTES = 4

class Shape:
    def __init__(self, vertexData, indexData):
        self.vertexData = vertexData
        self.indexData = indexData


#Crear un cuadrado de lado L
def createQuad(L, r, g, b):

    #Se define un vertexData donde cada 6 coordenadas, 3 indican la posicion de un vertice, y los siguientes
    #3 corresponden a los colores en r,g,b.
    vertexData = np.array([
    #   positions        colors
        -L/2, -L/2, 0.0,  r, g, b,
         L/2, -L/2, 0.0,  r, g, b,
         L/2,  L/2, 0.0,  r, g, b,
        -L/2,  L/2, 0.0,  r, g, b
        ], dtype = np.float32)

    #Se crea un arreglo que guarda los vertices guardados en vertexData
    #Cada 3 vertices se forma un triangulo
    indexData = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return Shape(vertexData, indexData)


#Crear un triangulo con vertices en los puntos (x1,y1), (x2,y2), (x3,y3)
def createTriangle(x1,y1,x2,y2,x3,y3,r,g,b):

    vertexData = np.array([
    #   positions        colors
         x1, y1, 0.0,  r, g, b,
         x2, y2, 0.0,  r, g, b,
         x3, y3, 0.0,  r, g, b
        ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2], dtype= np.uint32)

    return Shape(vertexData, indexData)


#Creamos un circulo con N vertices, de colores r,g,b, angulo recorrido ang y desfase desf
def createCircle(N, R, r, g, b, ang = 2 * np.pi, desf = 0):

    vertexData = [
        # posicion     # color
        0.0, 0.0, 0.0, r, g, b
    ]

    indexData = []

    dtheta = ang / N

    for i in range(N):

        theta = i * dtheta + desf

        x = R * np.cos(theta)
        y = R * np.sin(theta)
        z = 0

        vertexData += [
            # pos    # color
            x, y, z, r, g, b
        ]

        indexData += [0, i, i+1]

    indexData += [0, N, 1]

    return Shape(vertexData, indexData)

#Crea un triangulo volteado, con las proporciones deseadas para una letra V
def create_V_Triangle(L, r, g, b):

    vertexData = np.array([
    #   positions        colors
          0.0, 0.0, 0.0,  r, g, b,
          (L-7*L/10), L, 0.0,  r, g, b,
         -(L-7*L/10), L, 0.0,  r, g, b,
        ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2], dtype= np.uint32)

    return Shape(vertexData, indexData)


def createHalfEllipse(N, Rx, Ry, r, g, b, desf = 0):

    vertexData = [
        # posicion     # color
        0.0, 0.0, 0.0, r, g, b
    ]

    indexData = []

    dtheta = np.pi / N

    for i in range(N+1):
        
        theta = i * dtheta

        x = Rx * np.cos(theta + desf)
        y = Ry * np.sin(theta + desf)
        z = 0

        vertexData += [
            # pos    # color
            x, y, z, r, g, b
        ]

        indexData += [0, i, i+1]

    return Shape(vertexData, indexData)
    


def createEllipse(N, Rx, Ry, r, g, b):

    vertexData = [
        # posicion     # color
        0.0, 0.0, 0.0, r, g, b
    ]

    indexData = []

    dtheta = 2 * np.pi / N

    for i in range(N):
        theta = i * dtheta

        x = Rx * np.cos(theta)
        y = Ry * np.sin(theta)
        z = 0

        vertexData += [
            # pos    # color
            x, y, z, r, g, b
        ]

        indexData += [0, i, i+1]

    indexData += [0, N, 1]

    return Shape(vertexData, indexData)


def create_BartSimpson_hair(r, g, b):

    vertexData = [
    #   positions        colors
        -0.30, 0.0, 0.0,  r, g, b,
        -0.30, 0.05, 0.0,  r, g, b,
        -0.25, 0.0, 0.0,  r, g, b
        ]

    indexData = [0, 1, 2]

    i = 0

    while i<=8:

        change_factor = 0.1 * i / 2

        vertexData += [
            # pos    # color
            -0.2 + change_factor, 0.05, 0.0, r, g, b,
            -0.15 + change_factor, 0.0, 0.0, r, g, b
        ]

        indexData += [2+i, 3+i, 4+i]

        i = i+2

    vertexData += [

        0.25, 0.0, 0.0, r, g, b,
        0.30, 0.05, 0.0, r, g, b,
        0.30, 0.0, 0.0, r, g, b
    ]

    indexData += [3+i, 4+i, 5+i]

    return Shape(vertexData, indexData)


def create_Rectangle(Lx, Ly, r, g, b):

    vertexData = np.array([
    #   positions        colors
        -Lx/2, -Ly/2, 0.0,  r, g, b,
         Lx/2, -Ly/2, 0.0,  r, g, b,
         Lx/2,  Ly/2, 0.0,  r, g, b,
        -Lx/2,  Ly/2, 0.0,  r, g, b
        ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return Shape(vertexData, indexData)


def create_inclined_parallelogram(r, g, b):
    
    vertexData = np.array([
    #   positions        colors
        0.0, 0.0, 0.0,  r, g, b,
        0.0, 0.05, 0.0,  r, g, b,
        0.05, 0.0, 0.0,  r, g, b,
        0.05, -0.05, 0.0,  r, g, b
        ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return Shape(vertexData, indexData)


def create_front_Mouth_triangle(r, g, b):

    vertexData = np.array([
    #   positions        colors
         0.0,  0.0, 0.0,  r, g, b,
         0.0, 0.15, 0.0, r, g, b,
         0.05, 0.0, 0.0, r, g, b
        ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2], dtype= np.uint32)

    return Shape(vertexData, indexData)
