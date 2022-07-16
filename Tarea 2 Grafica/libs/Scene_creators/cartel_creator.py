from libs.assets_path import getAssetPath
import libs.transformations as tr
from libs.gpu_generator import *
import libs.basic_shapes as bs
import libs.scene_graph as sg
from OpenGL.GL import *
import numpy as np


#Se crea una funcion que creara un nodo de un cartel
def createCartel(pipeline):

    #Se crean las gpus de las patas del cartel y del cartel
    gpuCartel = createGPUShapeTexture(bs.createTextureParallelepiped(1.5, 0.2, 1), pipeline,
                 "inostroza.jpg")
                 
    gpuPatas = createGPUShapeTexture(bs.createTextureParallelepiped(0.15, 0.15, 0.2), pipeline, 
                 "texturaCASA3.jpg")

    #Se crea la primera pata del control
    pataCartel1 = sg.SceneGraphNode('pata1')
    pataCartel1.transform = tr.translate(0.5, 0.025, 0)
    pataCartel1.childs += [gpuPatas]

    #Se crea la segunda pata del control
    pataCartel2 = sg.SceneGraphNode('pata2')
    pataCartel2.transform = tr.translate(-0.5, 0.025, 0)
    pataCartel2.childs += [gpuPatas]

    #Se crea el cartel
    cartel = sg.SceneGraphNode('cartel')
    cartel.transform = tr.translate(0,0,0.2)
    cartel.childs += [gpuCartel]

    #Se crea un nodo que contendra el cartel y sus 2 patas
    cartelComplete = sg.SceneGraphNode('cartelComplete')
    cartelComplete.transform = tr.rotationZ(-30*np.pi/180)

    #Se agregan al nodo cartel completo el cartel y las patas
    cartelComplete.childs += [cartel]
    cartelComplete.childs += [pataCartel1]
    cartelComplete.childs += [pataCartel2]
    
    #Retorna el cartel con sus patas
    return cartelComplete
        