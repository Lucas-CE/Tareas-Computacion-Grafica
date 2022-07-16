from libs.assets_path import getAssetPath
from libs.gpu_shape import GPUShape
import libs.easy_shaders as es
from OpenGL.GL import *


#Funcion que retorne el gpu de la figura CON TEXTURA
def createGPUShapeTexture(shape, pipeline, texture):

    nombre = shape
    gpuName = GPUShape().initBuffers()
    pipeline.setupVAO(gpuName)
    gpuName.fillBuffers(nombre.vertices, nombre.indices, GL_STATIC_DRAW)
    gpuName.texture = es.textureSimpleSetup(
        getAssetPath(texture), GL_REPEAT, GL_REPEAT, GL_LINEAR, GL_LINEAR)
    
    return gpuName


#Funcion que retorna la gpu de una figura SIN TEXTURA
def createGPUShapeColor(shape, pipeline):

    gpuShape = es.GPUShape().initBuffers()
    pipeline.setupVAO(gpuShape)
    gpuShape.fillBuffers(shape.vertices, shape.indices, GL_STATIC_DRAW)

    return gpuShape
