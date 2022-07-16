import libs.transformations as tr
from libs.gpu_generator import *
from libs.basic_shapes import *
import libs.scene_graph as sg
from OpenGL.GL import *
import numpy as np


#Definimos createBase como la funcion que creara la base con todos los objetos combinados
def createBase(pipeline):

    #Creamos las partes del piso

    #Creamos la base
    gpuBase = createGPUShapeTexture(create_base(9,8), pipeline, "grass.jpg")

    #Creamos los tipos de calles, tendremos 3 tipos de calle (segun el largo)
    #Creamos la calle tipo 1
    gpuST1 = createGPUShapeTexture(create_RectangleXY(8,0.5), pipeline, "street.jpg")

    #Creamos la calle tipo 2
    gpuST2 = createGPUShapeTexture(create_RectangleXY(5,0.5), pipeline, "street.jpg")

    #Creamos la calle tipo 3
    gpuST3 = createGPUShapeTexture(create_RectangleXY(2.5/np.sin(np.pi*0.25),0.5), pipeline, "street.jpg")

    #Creamos una base larga que ira por debajo de la base principal
    gpuUnderBase = createGPUShapeTexture(createTextureParallelepiped(20,20,0.2), pipeline, 'grass.jpg')

    #Creamos el piso del escenario
    floor = sg.SceneGraphNode('floor')

    #Creamos la base y lo agregamos como nodo hijo a floor
    base = sg.SceneGraphNode('base')
    base.childs += [gpuBase]
    floor.childs += [base]

    #Creamos la base secundaria y se agrega como nodo al nodo de floor
    underBase = sg.SceneGraphNode('underBase')
    underBase.transform = tr.matmul([tr.translate(5,5,-0.3)])
    underBase.childs += [gpuUnderBase]
    floor.childs += [underBase]


    #Creamos las calles
    streets = sg.SceneGraphNode('streets')

    #Agregamos las calles en las posiciones que deben quedar al nodo streets
    
    #Agregamos las calles tipo 1
    #Calles paralelas al eje x
    for i in range(3):
        streetsT1 = sg.SceneGraphNode('streetT1('+str(i)+')')
        streetsT1.transform = tr.matmul([tr.translate(0.0, 2.5 * i, 0.0),
                                       tr.translate(0.5 + 4, 0.25, 0.001)])
        streetsT1.childs += [gpuST1]
        streets.childs += [streetsT1]

    #Calle paralela al eje y (recordar tipo 1)
    streetsT1 = sg.SceneGraphNode('streetT1(3)')
    streetsT1.transform = tr.matmul([tr.translate(0.25, 4, 0.001),
                                   tr.rotationZ(np.pi/2)])
    streetsT1.childs += [gpuST1]
    streets.childs += [streetsT1]

    #Agregamos las calles tipo 2
    streetsT2 = sg.SceneGraphNode('streetT2(0)')
    streetsT2.transform = tr.matmul([tr.translate(0.5 + 2.5, 0.25 + 7.5, 0.001), tr.scale(1.2,1,1)])
    streetsT2.childs += [gpuST2]
    streets.childs += [streetsT2]

    streetsT2 = sg.SceneGraphNode('streetT2(1)')
    streetsT2.transform = tr.matmul([tr.translate(0.25 + 8.5, 2.5, 0.001),
                                   tr.rotationZ(np.pi/2), tr.scale(1,1,1)])
    streetsT2.childs += [gpuST2]
    streets.childs += [streetsT2]

    #Agregamos la calle tipo 3
    streetsT3 = sg.SceneGraphNode('streetT3(0)')
    streetsT3.transform = tr.matmul([tr.translate(7.5, 6.5, 0.001), tr.rotationZ(-np.pi*0.25)])
    streetsT3.childs += [gpuST3]
    streets.childs += [streetsT3]


    #Con el nodo streets ya completo, lo agregamos como nodo hijo al nodo floor
    floor.childs += [streets]

    #Se retorna el nodo que contiene el piso
    return floor
