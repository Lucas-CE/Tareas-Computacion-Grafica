# coding=utf-8
"""A convenience class container to reference a shape on GPU memory"""

#import OpenGL.GL as ogl
from OpenGL.GL import *
import numpy as np
import archives.constant as C

__author__ = "Daniel Calderon"
__license__ = "MIT"

#Se usan la cantidad de bytes definidos en constant
SIZE_IN_BYTES = C.SIZE_IN_BYTES

#Se crea la clase 
class GPUShape:

    #Se definen los objetos de vao vbo ebo textura y tamano como None inicialmente,
    #luego se cambiaran
    def __init__(self):
        """VAO, VBO, EBO and texture handlers to GPU memory"""
        
        self.vao = None
        self.vbo = None
        self.ebo = None
        self.texture = None
        self.size = None

    #Funcion que define los objetos de la clase vao vbo y ebo con los generadores de buffers y arrays
    #de openGL
    def initBuffers(self):
        """Convenience function for initialization of OpenGL buffers.
        It returns itself to enable the convenience call:
        gpuShape = GPUShape().initBuffers()

        Note: this is not the default constructor as you may want
        to use some already existing buffers.
        """
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        return self

    #Funcin encargada de retornar los objetos de la clase como strings
    def __str__(self):
        return "vao=" + str(self.vao) +\
            "  vbo=" + str(self.vbo) +\
            "  ebo=" + str(self.ebo) +\
            "  tex=" + str(self.texture)

    #Encargado guardar en los buffers los datos respectivos de las figuras o cuerpos que se usan
    def fillBuffers(self, vertices, indices, usage):

        vertexData = np.array(vertices, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        self.size = len(indices)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, len(vertexData) * SIZE_IN_BYTES, vertexData, usage)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, len(indices) * SIZE_IN_BYTES, indices, usage)

    #Funcion que se encarga de limpiar los gpus de la memoria
    def clear(self):
        """Freeing GPU memory"""

        if self.texture != None:
            glDeleteTextures(1, [self.texture])
        
        if self.ebo != None:
            glDeleteBuffers(1, [self.ebo])

        if self.vbo != None:
            glDeleteBuffers(1, [self.vbo])

        if self.vao != None:
            glDeleteVertexArrays(1, [self.vao])
        