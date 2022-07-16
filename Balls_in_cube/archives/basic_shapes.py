import numpy as np
from OpenGL.GL import *
import archives.constant as C
import math

SIZE_IN_BYTES = C.SIZE_IN_BYTES

#Se crea una clase Shape
class Shape:
    def __init__(self, vertexData, indexData):

        #Se crea un objeto donde se guardaran los vertices
        self.vertexData = vertexData

        #Se crea un objeto donde se guardaran los indices
        self.indexData = indexData
 

#Creamos un paralelepipedo rectangular
#Se usa como inspiracion la funcion de creacion del cubo del aux 5 pero modificando las posiciones
def create_RectangleParallelepiped(thickness, height, r, g, b):

    t = thickness
    h = height/2

    vertexData = np.array([
        #positions #texture
        -t, -t,  h,  r, g, b,
         t, -t,  h,  r, g, b,
         t,  t,  h,  r, g, b,
        -t,  t,  h,  r, g, b,

        -t, -t, -h,  r, g, b,
         t, -t, -h,  r, g, b,
         t,  t, -h,  r, g, b,
        -t,  t, -h,  r, g, b   
        ], dtype=np.float32)

    indexData = np.array([
        0, 1, 2, 2, 3, 0,
        4, 5, 6, 6, 7, 4,
        4, 5, 1, 1, 0, 4,
        6, 7, 3, 3, 2, 6,
        5, 6, 2, 2, 1, 5,
        7, 4, 0, 0, 3, 7
    ])

    return Shape(vertexData, indexData)


#Creamos una esfera
#La parametrizacion de la esfera fue extraida y basada del siguiente link
#http://www.songho.ca/opengl/gl_sphere.html#sphere
def create_Sphere(radius,n,m):

    sectorCount = n
    stackCount = m

    sectorStep = 2*math.pi/sectorCount
    stackStep = math.pi/stackCount

    pStep = 1/sectorCount
    qStep = 1/stackCount

    indexData = []

    vertexData = []

    for i in range(stackCount+1):

        stackAngle = math.pi/2 - i * stackStep
        p = pStep * i

        xy = radius * math.cos(stackAngle)
        z = radius * math.sin(stackAngle)

        for j in range(sectorCount+1):

            sectorAngle = j * sectorStep
            q = qStep * j

            x = xy * math.cos(sectorAngle)
            y = xy * math.sin(sectorAngle)
            
            vertexData += [
            # pos    # texture
            x, y, z, p, q
            ]


    i=0
    while i < stackCount:

        k1 = i * (sectorCount + 1)
        k2 = k1 + sectorCount + 1

        j = 0
        while j < sectorCount:

            if i != 0:
                indexData += [k1, k2, k1+1]

            if i != (stackCount-1):
                indexData += [k1+1, k2, k2+1]

            j += 1
            k1 += 1
            k2 += 1

        i += 1


    return Shape(vertexData, indexData)

