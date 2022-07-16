from OpenGL.GL import *
from matplotlib.pyplot import draw
from archives.gpu_shape import GPUShape
import archives.transformations as tr
import numpy as np
import archives.basic_shapes as bs
import archives.constant as C
import math

#Se crea una funcion donde recibe los vertices e indices de una figura o cuerpo y el shader a usar
#y retorna la gpu al crear la figura
def create_GPUFigure(figure, pipeline):

    nombre = figure
    gpuName = GPUShape().initBuffers()
    pipeline.setupVAO(gpuName)
    gpuName.fillBuffers(nombre.vertexData, nombre.indexData, GL_STATIC_DRAW)
    return gpuName


#Creamos la clase aristas del cubo
class CubeEdges:

    def __init__(self, pipeline):

        #Se define la variable pipeline como el shader que se usara
        self.pipeline = pipeline
        
        #Creamos el gpu de la arista
        gpuEDGE = create_GPUFigure(bs.create_RectangleParallelepiped(C.EDGE_THICKNESS,C.EDGE_LARGE, 1, 0, 0), pipeline)
        
        #Se define la variable gpuEDGE donde se guarda la gpu de la arista
        self.gpuEDGE = gpuEDGE

    
    #Creamos la funcion encargada de dibujar las aristas del cubo
    def draw_CubeEdges(self):

        pipeline = self.pipeline

        #Creamos la figura que dibujar las aristas segun sus posiciones y angulos de rotacion
        def draw_figure(gpu, x, y, z, alpha, beta):

            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "model"), 1, GL_TRUE, 
            tr.matmul([tr.rotationX(alpha), tr.rotationY(beta), tr.translate(x, y, z)]))

            pipeline.drawCall(gpu)

        #Guardamos en variables el valor de pi, y de el largo de las aristas
        pi = math.pi
        L = C.EDGE_LARGE

        #Dibujamos las 4 aristas paradas en 
        draw_figure(self.gpuEDGE, L/2, L/2, 0, 0, 0)
        draw_figure(self.gpuEDGE, -L/2, L/2, 0, 0, 0)
        draw_figure(self.gpuEDGE, L/2, -L/2, 0, 0, 0)
        draw_figure(self.gpuEDGE, -L/2, -L/2, 0, 0, 0)

        #Dibujamos las aristas paralelas de una direccion
        draw_figure(self.gpuEDGE, L/2, L/2, 0, pi/2, 0)
        draw_figure(self.gpuEDGE, -L/2, L/2, 0, pi/2, 0)
        draw_figure(self.gpuEDGE, L/2, -L/2, 0, pi/2, 0)
        draw_figure(self.gpuEDGE, -L/2, -L/2, 0, pi/2, 0)

        #Dibujamos las aristas restantes que unen los dos cuadrados que qudaron
        draw_figure(self.gpuEDGE, L/2, L/2, 0, pi/2, pi/2)
        draw_figure(self.gpuEDGE, -L/2, L/2, 0, pi/2, pi/2)
        draw_figure(self.gpuEDGE, L/2, -L/2, 0, pi/2, pi/2)
        draw_figure(self.gpuEDGE, -L/2, -L/2, 0, pi/2, pi/2)



        