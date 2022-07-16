from libs.assets_path import getAssetPath
import libs.transformations as tr
from libs.gpu_generator import *
import libs.basic_shapes as bs
import libs.scene_graph as sg
from OpenGL.GL import *
import numpy as np

#Aqui se creara la casa con nodos
def createHouse(pipeline):

    #Creamos las partes de la casa

    #Creamos los cuerpos de las paredes
    #Sera representada por un paralelepipedo de 1 x 0.001 x 0.8
    gpuWBT1 = createGPUShapeTexture(bs.createTextureParallelepiped(1, 0.001, 0.8), pipeline, "texturaCASA1.jpg")
    gpuWBT2 = createGPUShapeTexture(bs.createTextureParallelepiped(1, 0.001, 0.8), pipeline, "texturaCASA2.jpg")
    gpuWBT3 = createGPUShapeTexture(bs.createTextureParallelepiped(1, 0.001, 0.8), pipeline, "texturaCASA3.jpg")

    #Creamos el techo
    gpuRoofT1 = createGPUShapeTexture(bs.create_triangleXYZ(1, 1, 0.2), pipeline, "roof1.jpg")
    gpuRoofT2 = createGPUShapeTexture(bs.create_triangleXYZ(1, 1, 0.2), pipeline, "roof2.jpg")
    gpuRoofT3 = createGPUShapeTexture(bs.createTextureParallelepiped(1,1,0.001), pipeline, "texturaCASA3.jpg")

    #Creamos una puerta
    gpuDOOR = createGPUShapeTexture(bs.createTextureParallelepiped(0.2,0.01,0.4), pipeline, "door.jpg")

    #Creamos una ventana
    gpuWindow = createGPUShapeTexture(bs.createTextureParallelepiped(0.2, 0.01, 0.3), pipeline, "glass.jpg")


    #Iniciamos la construccion de los nodos

    #Creamos el nodo de las casas de todos los tipos
    houses = sg.SceneGraphNode('houses')

    #Creamos el nodo de las casas tipo 1 y 2
    houseT1 = sg.SceneGraphNode('houseT1')
    houseT2 = sg.SceneGraphNode('houseT2')
    houseT3 = sg.SceneGraphNode('houseT3')
    
    #Movemos las casas a la posicion de la primera casa
    houseT1.transform = tr.matmul([tr.scale(0.9, 0.8, 1)])
    houseT2.transform = tr.matmul([tr.scale(0.9, 0.8, 1)])
    houseT3.transform = tr.matmul([tr.scale(0.9, 0.8, 1)])


    #Creamos las partes que se usaran en todos los modelos de casa

    #Creamos el nodo que contendra las ventanas
    windws = sg.SceneGraphNode('windowNode')

    #Creamos las 2 ventanas que iran en la entrada
    for i in range(2):
        windw = sg.SceneGraphNode('window('+str(i)+')')
        windw.transform = tr.matmul([tr.translate(-0.3 + 0.6*i, -0.001, 0.4)])
        windw.childs += [gpuWindow]
        windws.childs += [windw]


    #Creamos el nodo de la puerta
    door = sg.SceneGraphNode('door')
    door.transform = tr.matmul([tr.translate(0, -0.001, 0)])
    door.childs += [gpuDOOR]

    
    #Creamos el nodo que contiene el techo de la casa tipo 1
    roofT1 = sg.SceneGraphNode('roofT1')
    roofT1.transform = tr.matmul([tr.translate(0, 0, 0.8)])
    roofT1.childs += [gpuRoofT1]

    #Creamos el nodo que contiene el techo de la casa tipo 2
    roofT2 = sg.SceneGraphNode('roofT2')
    roofT2.transform = tr.matmul([tr.translate(0, 0, 1.6)])
    roofT2.childs += [gpuRoofT2]

    #Creamos el nodo que contiene el techo de la casa tipo 3
    roofT3 = sg.SceneGraphNode('roofT3')
    roofT3.transform = tr.matmul([tr.translate(0, 0, 0.8)])
    roofT3.childs += [gpuRoofT3]


    #Creamos distintos tipos de paredes (crearemos distintos tipos)

    #Creamos las paredes de las casas tipo 1

    #Pared de cuerpo principal (solo un cuadrado que será la pared)
    wall_body_pT1 = sg.SceneGraphNode('wall_body_pT1')
    wall_body_pT1.childs += [gpuWBT1]

    #Pared de cuerpo secundario tipo 1 (lateral)
    wall_body_sT1 = sg.SceneGraphNode('wall_body_sT1')
    wall_body_sT1.transform = tr.matmul([tr.rotationZ(-np.pi/2)])
    wall_body_sT1.childs += [gpuWBT1]

    #Creamos el nodo con la pared de enfrente (tiene la pared, ventanas, y una puerta)
    wall_frontT1 = sg.SceneGraphNode('wall_frontT1')
    wall_frontT1.childs += [wall_body_pT1]#wall_with_headT1]
    wall_frontT1.childs += [door]
    wall_frontT1.childs += [windws]


    #Creamos las paredes de las casas tipo 2

    #Pared de cuerpo principal casa T1 (solo un cuadrado que será la pared)
    wall_body_pT2 = sg.SceneGraphNode('wall_body_pT2')
    wall_body_pT2.childs += [gpuWBT2]

    #Pared de cuerpo secundario tipo 2 (lateral)
    wall_body_sT2 = sg.SceneGraphNode('wall_body_sT2')
    wall_body_sT2.transform = tr.matmul([tr.rotationZ(-np.pi/2)])
    wall_body_sT2.childs += [gpuWBT2]

    #Pared principal solo con ventanas
    wall_with_window = sg.SceneGraphNode('wall_with_window')
    wall_with_window.childs += [wall_body_pT2]
    wall_with_window.childs += [windws]

    #Pared del frente casa tipo 2
    wall_frontT2 = sg.SceneGraphNode('wall_frontT2')
    wall_frontT2.childs += [wall_with_window]
    wall_frontT2.childs += [door]


    #Creamos las paredes de las casas tipo 3

    #Pared de cuerpo principal (solo un cuadrado que será la pared)
    wall_body_pT3 = sg.SceneGraphNode('wall_body_pT3')
    wall_body_pT3.childs += [gpuWBT3]

    #Pared de cuerpo secundario tipo 1 (lateral)
    wall_body_sT3 = sg.SceneGraphNode('wall_body_sT3')
    wall_body_sT3.transform = tr.matmul([tr.rotationZ(-np.pi/2)])
    wall_body_sT3.childs += [gpuWBT3]

    #Creamos el nodo con la pared de enfrente (tiene la pared con cabecera, ventanas, y una puerta)
    wall_frontT3 = sg.SceneGraphNode('wall_frontT2')
    wall_frontT3.childs += [wall_body_pT3]
    wall_frontT3.childs += [door]
    wall_frontT3.childs += [windws]



    #Creamos los nodos que contienen las 4 paredes de la casas 1, 2 y 3
    wallsT1 = sg.SceneGraphNode('wallsT1')
    wallsT2 = sg.SceneGraphNode('wallsT2')
    wallsT3 = sg.SceneGraphNode('wallsT3')


    #Creamos la casa tipo 1
    #Creamos los nodos de las 4 paredes donde usamos las paredes y elementos antes creados
    #Añadimos las paredes delantera y trasera
    wallT1 = sg.SceneGraphNode('wallT1(0)')
    wallT1.transform = tr.matmul([tr.translate(0, -0.5, 0)])
    wallT1.childs += [wall_frontT1]
    wallsT1.childs += [wallT1]

    wallT1 = sg.SceneGraphNode('wallT1(1)')
    wallT1.transform = tr.matmul([tr.translate(0, 0.5, 0)])
    wallT1.childs += [wall_body_pT1]
    wallsT1.childs += [wallT1]

    #Añadimos las paredes laterales
    for i in range(2):
        wallT1 = sg.SceneGraphNode('wallT1('+str(i+2)+')')
        wallT1.transform = tr.matmul([tr.translate(0.5 - i, 0, 0)])
        wallT1.childs += [wall_body_sT1]
        wallsT1.childs += [wallT1]

    #Agregamos los nodos de las paredes y del techo como nodos hijo de el nodo de la casa tipo 1
    houseT1.childs += [wallsT1]
    houseT1.childs += [roofT1]

    #Agregamos el nodo houseT1 como nodo hijo del nodo houses
    houses.childs += [houseT1]


    #Creamos la casa tipo 2
    #La casa tendra 2 pisos, por lo que creamos 2 sets de paredes

    #Set 1 de paredes, piso 1
    #Añadimos las paredes delantera y trasera
    wallT2 = sg.SceneGraphNode('wallT2p1(0)')
    wallT2.transform = tr.matmul([tr.translate(0, -0.5, 0)])
    wallT2.childs += [wall_frontT2]
    wallsT2.childs += [wallT2]

    wallT2 = sg.SceneGraphNode('wallT2p1(1)')
    wallT2.transform = tr.matmul([tr.translate(0, 0.5, 0)])
    wallT2.childs += [wall_body_pT2]
    wallsT2.childs += [wallT2]

    #Añadimos las paredes laterales
    for i in range(2):
        wallT2 = sg.SceneGraphNode('wallT2p1('+str(i+2)+')')
        wallT2.transform = tr.matmul([tr.translate(0.5 - i, 0, 0)])
        wallT2.childs += [wall_body_sT2]
        wallsT2.childs += [wallT2]

    #Set 2 de paredes, piso 2
    #Añadimos las paredes delantera y trasera
    wallT2 = sg.SceneGraphNode('wallT2p2(0)')
    wallT2.transform = tr.matmul([tr.translate(0, -0.5, 0.8)])
    wallT2.childs += [wall_with_window]
    wallsT2.childs += [wallT2]

    wallT2 = sg.SceneGraphNode('wallT2p2(1)')
    wallT2.transform = tr.matmul([tr.translate(0, 0.5, 0.8)])
    wallT2.childs += [wall_with_window]
    wallsT2.childs += [wallT2]

    #Añadimos las paredes laterales
    for i in range(2):
        wallT2 = sg.SceneGraphNode('wallT2p2('+str(i+2)+')')
        wallT2.transform = tr.matmul([tr.translate(0.5 - i, 0, 0.8)])
        wallT2.childs += [wall_body_sT2]
        wallsT2.childs += [wallT2]

    #Agregamos los nodos de las paredes y del techo como nodos hijo de el nodo de la casa tipo 1
    houseT2.childs += [wallsT2]
    houseT2.childs += [roofT2]

    #Agregamos el nodo houseT2 como nodo hijo del nodo houses
    houses.childs += [houseT2]


    #Creamos la casa tipo 3
    #Creamos los nodos de las 4 paredes donde usamos las paredes y elementos antes creados
    #Añadimos las paredes delantera y trasera
    wallT3 = sg.SceneGraphNode('wallT3(0)')
    wallT3.transform = tr.matmul([tr.translate(0, -0.5, 0)])
    wallT3.childs += [wall_frontT3]
    wallsT3.childs += [wallT3]

    wallT3 = sg.SceneGraphNode('wallT3(1)')
    wallT3.transform = tr.matmul([tr.translate(0, 0.5, 0)])
    wallT3.childs += [wall_body_pT3]
    wallsT3.childs += [wallT3]

    #Añadimos las paredes laterales
    for i in range(2):
        wallT3 = sg.SceneGraphNode('wallT3('+str(i+2)+')')
        wallT3.transform = tr.matmul([tr.translate(0.5 - i, 0, 0)])
        wallT3.childs += [wall_body_sT3]
        wallsT3.childs += [wallT3]

    #Agregamos los nodos de las paredes y del techo como nodos hijo de el nodo de la casa tipo 3
    houseT3.childs += [wallsT3]
    houseT3.childs += [roofT3]

    #Agregamos el nodo houseT3 como nodo hijo del nodo houses
    houses.childs += [houseT3]

    #Se retorna el nodo que contiene los 3 tipos de casas
    return houses
