import numpy as np
from OpenGL.GL import *
import libs.constant as C
import math

SIZE_IN_BYTES = C.SIZE_IN_BYTES

#Se crea una clase Shape
class Shape:
    def __init__(self, vertices, indices):

        #Se crea un objeto donde se guardaran los vertices
        self.vertices = vertices

        #Se crea un objeto donde se guardaran los indices
        self.indices = indices

    def __str__(self):
        return "vertices: " + str(self.vertices) + "\n"\
            "indices: " + str(self.indices)
 
 
#Creamos un rectangulo en el plano XY
def create_RectangleXY(x, y):

    vertexData = np.array([
    #   positions      texture  normals
        -x/2, -y/2, 0,   0, 1,   0,0,1, 
         x/2, -y/2, 0,   1, 1,   0,0,1, 
         x/2,  y/2, 0,   1, 0,   0,0,1, 
        -x/2,  y/2, 0,   0, 0,   0,0,1
         ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return Shape(vertexData, indexData)


#Creamos un rectangulo en el plano XZ
def create_RectangleXZ(x, z):

    vertexData = np.array([
    #    positions   texture normals
        -x/2, 0, z,   0, 0,   0,1,0,
         x/2, 0, z,   1, 0,   0,1,0,
         x/2, 0, 0,   1, 1,   0,1,0,
        -x/2, 0, 0,   0, 1,   0,1,0
        ], dtype = np.float32)

    indexData = np.array(
        [0, 1, 2,
         2, 3, 0], dtype= np.uint32)

    return Shape(vertexData, indexData)


#Creamos un paralelepipedo rectangular
#Se usa como inspiracion la funcion de creacion del cubo del aux 5 pero modificando las posiciones
def createTextureParallelepiped(Lx, Ly, Lz):

    Lx = Lx/2
    Ly = Ly/2

    # Defining locations and texture coordinates for each vertex of the shape
    vertices = [
        #  positions   texture   normals
        # Z+
        -Lx, -Ly,  Lz,    0, 1,    0,0,1,
         Lx, -Ly,  Lz,    1, 1,    0,0,1,
         Lx,  Ly,  Lz,    1, 0,    0,0,1,
        -Lx,  Ly,  Lz,    0, 0,    0,0,1,

        # Z-
        -Lx, -Ly,   0,    0, 1,    0,0,-1,
         Lx, -Ly,   0,    1, 1,    0,0,-1,
         Lx,  Ly,   0,    1, 0,    0,0,-1,
        -Lx,  Ly,   0,    0, 0,    0,0,-1,

        # X+
        Lx, -Ly,   0,     0, 1,    1,0,0,
        Lx,  Ly,   0,     1, 1,    1,0,0,
        Lx,  Ly,  Lz,     1, 0,    1,0,0,
        Lx, -Ly,  Lz,     0, 0,    1,0,0,

        # X-
        -Lx, -Ly,   0,    0, 1,    -1,0,0,
        -Lx,  Ly,   0,    1, 1,    -1,0,0,
        -Lx,  Ly,  Lz,    1, 0,    -1,0,0,
        -Lx, -Ly,  Lz,    0, 0,    -1,0,0,

        # Y+
        -Lx,  Ly,   0,    1, 1,     0,1,0,
         Lx,  Ly,   0,    0, 1,     0,1,0,
         Lx,  Ly,  Lz,    0, 0,     0,1,0,
        -Lx,  Ly,  Lz,    1, 0,     0,1,0,

        # Y-
        -Lx, -Ly,   0,    0, 1,     0,-1,0,
         Lx, -Ly,   0,    1, 1,     0,-1,0,
         Lx, -Ly,  Lz,    1, 0,     0,-1,0,
        -Lx, -Ly,  Lz,    0, 0,     0,-1,0
    ]

    # Defining connections among vertices
    # We have a triangle every 3 indices specified
    indices = [
        0, 1, 2, 2, 3, 0,  # Z+
        7, 6, 5, 5, 4, 7,  # Z-
        8, 9, 10, 10, 11, 8,  # X+
        15, 14, 13, 13, 12, 15,  # X-
        19, 18, 17, 17, 16, 19,  # Y+
        20, 21, 22, 22, 23, 20]  # Y-

    return Shape(vertices, indices)


#Creamos un triangulo con ancho en Y
def create_triangleXYZ(Lx, Ly, Lz):

    Lx = Lx/2
    Ly = Ly/2

    #Este angulo se calculo especificamente para este caso
    alp = 78.69*np.pi/180

    vertexData = np.array([
        #positions #texture
        #Y+
        -Lx, Ly, 0,    0,   1,   0,1,0,
          0, Ly,Lz,  1/2, 2/3,   0,1,0,
         Lx, Ly, 0,    1,   1,   0,1,0,

        #Y-
        -Lx, -Ly, 0,    0,   1,  0,-1,0,
          0, -Ly,Lz,  1/2, 2/3,  0,-1,0,
         Lx, -Ly, 0,    1,   1,  0,-1,0,

        #C1
        -Lx,  Ly, 0, 0, 1, 0, 0, -1,
         Lx,  Ly, 0, 1, 1, 0, 0, -1,
        -Lx, -Ly, 0, 0, 1, 0, 0, -1,
         Lx, -Ly, 0, 1, 1, 0, 0, -1,

        #C2
          0,  Ly, Lz,  0, 0, np.cos(alp),0,np.sin(alp),
         Lx,  Ly,  0,  0, 1, np.cos(alp),0,np.sin(alp),
          0, -Ly, Lz,  1, 0, np.cos(alp),0,np.sin(alp),
         Lx, -Ly,  0,  1, 1, np.cos(alp),0,np.sin(alp),

        #C3
        -Lx,  Ly,  0,  1, 1, -np.cos(alp),0,np.sin(alp),
          0,  Ly, Lz,  1, 0, -np.cos(alp),0,np.sin(alp),
        -Lx, -Ly,  0,  0, 1, -np.cos(alp),0,np.sin(alp),
          0, -Ly, Lz,  0, 0, -np.cos(alp),0,np.sin(alp)
         
        ], dtype=np.float32)

    indexData = np.array([
        0, 1, 2, 3, 4, 5,
        6, 7, 8, 7, 8, 9,
        10, 11, 12, 11, 12, 13,
        14, 15, 16, 15, 16, 17
        ])

    return Shape(vertexData, indexData)


#Creamos la base de la ciudad
#Esta tiene forma de 5 lados
def create_base(length, width):

    l = length
    w = width
    g = 0.2
    m = 10 #multiplicador de textura

    vertexData = np.array([
        #positions           #texture     #normals
        #Z+
              0,       0, 0,      0,    1*m,  0,0,1,
              0,       w, 0,      0,      0,  0,0,1,
        13*l/18,       w, 0, 5*m/18,      0,  0,0,1,
              l, 11*w/16, 0,    1*m, 5/16*m,  0,0,1,
              l,       0, 0,    1*m,    1*m,  0,0,1,

        #Z-
              0,       0, -g,      0,    1*m,  0,0,-1,
              0,       w, -g,      0,      0,  0,0,-1,
        13*l/18,       w, -g, 5*m/18,      0,  0,0,-1,
              l, 11*w/16, -g,    1*m, 5/16*m,  0,0,-1,
              l,       0, -g,    1*m,    1*m,  0,0,-1,

        #X+
        l, 11*w/16,    0, 1*m, 5/16*m,  1,0,0,
        l,       0,    0, 1*m,    1*m,  1,0,0,
        l, 11*w/16, -g, 1*m, 5/16*m,  1,0,0,
        l,       0, -g, 1*m,    1*m,  1,0,0,

        #X-
        0, 0,    0, 0,    1*m,  -1,0,0,
        0, w,    0, 0,      0,  -1,0,0,
        0, 0, -g, 0,    1*m,  -1,0,0,
        0, w, -g, 0,      0,  -1,0,0,

        #Y+
        0,       w,    0,      0, 0,  0,1,0,
        13*l/18, w,    0, 5*m/18, 0,  0,1,0,
        0,       w, -g,      0, 0,  0,1,0,
        13*l/18, w, -g, 5*m/18, 0,  0,1,0,

        #Y-
        0, 0,    0,   0, 1*m, 0,-1,0,
        l, 0,    0, 1*m, 1*m, 0,-1,0,
        0, 0, -g,   0, 1*m, 0,-1,0,
        l, 0, -g, 1*m, 1*m, 0,-1,0,

        #Cara diagonal
        13*l/18,       w,    0, 5*m/18,      0,  np.cos(np.pi/4),np.cos(np.pi/4),0,
              l, 11*w/16,    0,    1*m, 5/16*m,  np.cos(np.pi/4),np.cos(np.pi/4),0,
        13*l/18,       w, -g, 5*m/18,      0,  np.cos(np.pi/4),np.cos(np.pi/4),0,
              l, 11*w/16, -g,    1*m, 5/16*m,  np.cos(np.pi/4),np.cos(np.pi/4),0

        ], dtype=np.float32)

    indexData = np.array([
        0, 1, 2, 0, 2, 3,
        0, 3, 4,
        5, 6, 7, 5, 7, 8,
        5, 8, 9,
        10, 11, 12, 11, 12, 13,
        14, 15, 16, 15, 16, 17,
        18, 19, 20, 19, 20, 21,
        22, 23, 24, 23, 24, 25,
        26, 27, 28, 27, 28, 29

    ])

    return Shape(vertexData, indexData)

