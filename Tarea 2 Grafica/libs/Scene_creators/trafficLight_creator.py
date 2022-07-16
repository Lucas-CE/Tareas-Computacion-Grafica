from libs.assets_path import getAssetPath
import libs.transformations as tr
from libs.gpu_generator import *
import libs.basic_shapes as bs
import libs.scene_graph as sg
from OpenGL.GL import *
import numpy as np

#Se crea una funcion que creara un nodo de un cartel
def createTrafficLight(pipeline):

    #Se crean las gpus del palo, la cabecera, y las luces del semaforo

    gpuBody = createGPUShapeTexture(bs.createTextureParallelepiped(0.05, 0.05, 0.6), pipeline, 
                 "black.jpg")

    gpuHead = createGPUShapeTexture(bs.createTextureParallelepiped(0.07, 0.15, 0.2), pipeline, 
                 "gris.jpg")

    gpuLight1 = createGPUShapeTexture(bs.createTextureParallelepiped(0.07, 0.0725, 0.06), pipeline, 
                 "verde.jpg")

    gpuLight2 = createGPUShapeTexture(bs.createTextureParallelepiped(0.07, 0.0725, 0.06), pipeline, 
                 "red.jpg")


    #Se crea un nodo que contendra el semaforo completo
    trafficLightNode = sg.SceneGraphNode('trafficLightNode')

    #Se crea un nodo que contendra el palo del semaforo 
    body = sg.SceneGraphNode('bodyTraffic')
    body.childs += [gpuBody]
    
    #Se crea un nodo que contendra la cabeza del semaforo
    head = sg.SceneGraphNode('headTraffic')
    head.childs += [gpuHead]
    head.transform = tr.translate(0, 0, 0.51)

    #Se crean 2 nodos que contendran las luces del semaforo
    light1 = sg.SceneGraphNode('light1Traffic')
    light1.childs += [gpuLight1]
    light1.transform = tr.translate(-0.001, 0, 0.54)

    light2 = sg.SceneGraphNode('light2Traffic')
    light2.childs += [gpuLight2]
    light2.transform = tr.translate(-0.001, 0, 0.62)

    #Se agregan todos los nodos de las partes del semaforo
    trafficLightNode.childs += [body]
    trafficLightNode.childs += [head] 
    trafficLightNode.childs += [light1]
    trafficLightNode.childs += [light2]
    
    #Se retorna el nodo con el semaforo completo
    return trafficLightNode
    
    
