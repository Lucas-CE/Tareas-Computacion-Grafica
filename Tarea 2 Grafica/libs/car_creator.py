import sys
from libs.assets_path import getAssetPath
import libs.transformations as tr
from libs.objFunctions import *
import libs.easy_shaders as es
import libs.scene_graph as sg
from OpenGL.GL import *
import numpy as np
from libs.gpu_generator import createGPUShapeColor


#Funcion que retorna el nodo del auto posicionado en su estado inicial
def createCar(colorPipeline):

    #Se crea la forma del auto
    shapeCar = readOBJ(getAssetPath('car.obj'), (128/255, 128/255, 128/255))
    
    #Se crea la gpu del auto
    gpuCar = createGPUShapeColor(shapeCar, colorPipeline)

    #Se crea un nodo que contendra al auto con sus transformaciones ya realizadas
    systemCar = sg.SceneGraphNode('system-car')

    #Se crea un nodo que contendra el gpu del auto y las transformaciones para dejarlo en su estado
    #inicial
    car = sg.SceneGraphNode('system-carNew')
    car.childs += [gpuCar]
    car.transform = tr.matmul([tr.uniformScale(0.10), tr.rotationZ(np.pi), tr.rotationX(np.pi/2)])

    #Se agrega el nodo del auto y sus transformaciones al nodo systemcar
    systemCar.childs += [car]

    return systemCar