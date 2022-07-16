import libs.transformations as tr
from libs.gpu_generator import *
from libs.basic_shapes import *
import libs.scene_graph as sg
from OpenGL.GL import *
import numpy as np

#Definimos createLamppost como la funcion que creara la base con todos los objetos combinados
def createLamppost(pipeline):

    #Creamos las gpus de las partes de los postes

    #Creamos gpu de el cuerpo del poste
    GPUbody = createGPUShapeTexture(createTextureParallelepiped(0.05, 0.05, 0.8), pipeline, "gris.jpg")

    #Creamos gpu de el brazo del poste
    GPUarm = createGPUShapeTexture(createTextureParallelepiped(0.05, 0.05, 0.5), pipeline, "gris.jpg")

    #Creamos gpu de la cabeza de el poste
    GPUhead = createGPUShapeTexture(createTextureParallelepiped(0.1, 0.2, 0.05), pipeline, "gris.jpg")


    #Creamos el nodo que contendra a los postes
    lamppost = sg.SceneGraphNode('lamppost')
    
    #Creamos los nodos que contendran los postes tipo 1 y 2
    lamppost_1 = sg.SceneGraphNode('lamppost_1')
    lamppost_2 = sg.SceneGraphNode('lamppost_2')

    #Creamos el nodo del cuerpo del poste tipo 1
    bodyNode_1 = sg.SceneGraphNode('body_1')
    bodyNode_1.childs += [GPUbody]
    bodyNode_1.transform = tr.scale(1, 1, 1/0.8)
    lamppost_1.childs += [bodyNode_1]

    #Creamos el nodo del cuerpo del poste tipo 2
    bodyNode_2 = sg.SceneGraphNode('body_2')
    bodyNode_2.childs += [GPUbody]
    lamppost_2.childs += [bodyNode_2]

    #Creamos el nodo del brazo del poste tipo 1
    armNode = sg.SceneGraphNode('arm_1')
    armNode.transform = tr.matmul([tr.translate(0,0.015,0.9),tr.rotationX(-2*np.pi/8)])
    armNode.childs += [GPUarm]
    lamppost_1.childs += [armNode]

    #Creamos el nodo de la cabeza del poste tipo 1
    headNode_1 = sg.SceneGraphNode('head_1')
    headNode_1.transform = tr.translate(0,0.42,1.24)
    headNode_1.childs += [GPUhead]
    lamppost_1.childs += [headNode_1]

    #Creamos el nodo de la cabeza del poste tipo 2
    headNode_2 = sg.SceneGraphNode('head_2')
    headNode_2.transform = tr.matmul([tr.translate(0,0.05,0.8),tr.rotationX(np.pi/8)])
    headNode_2.childs += [GPUhead]
    lamppost_2.childs += [headNode_2]

    #Agregamos los postes al nodo que contiene todos los tipos de postes
    lamppost.childs += [lamppost_1, lamppost_2]

    return lamppost

