from libs.Scene_creators.trafficLight_creator import *
from libs.Scene_creators.lamppost_creator import *
from libs.Scene_creators.cartel_creator import *
from libs.Scene_creators.base_creator import *
from libs.Scene_creators.houses_creator import *
import random


#Se define una funcion encargada de crear un nodo con la escena a montar
def createScene(pipeline):

    #Se crean los nodos que contienen a las casas, al cartel, y al piso
    houses = createHouse(pipeline)
    base = createBase(pipeline)
    cartel = createCartel(pipeline)
    lampposts = createLamppost(pipeline)
    trafficLight = createTrafficLight(pipeline)

    #Se definen como houseTi, a las casas i entre 0,1,2 dentro de los hijos de el nodo houses
    houseT1 = houses.childs[0]
    houseT2 = houses.childs[1]
    houseT3 = houses.childs[2]

    #Se definen como lamppostTi, a los postes tipo i, con i = 1 o 2.
    lamppostT1 = lampposts.childs[0]
    lamppostT2 = lampposts.childs[1]

    #Se crea un nodo que contendra toda la escena
    scene = sg.SceneGraphNode('system')

    #Se agrega la transformacion del nodo escena como la traslacion en -4.5,4,0
    #esto porque la escena despues de ser montada, inicia en 0,0,0 pero no está centrada en este punto
    scene.transform = tr.translate(-4.5, -4, 0)

    #Se crea el nodo que contendra a las casas en sus posiciones correspondientes
    houses_in_position = sg.SceneGraphNode('houses_in_pos')

    #Se itera en el rango de 6
    for i in range(6):

        #Si es que i es menor a 4, las casas a poner en el eje x seran 8
        if i < 4: number_houses_Xaxis = 8
        #Si el i es menor que 4, las casas a poner en el eje x son solo 4
        #esto corresponde a la parte del barrio que tiene un pedazo de cesped despues de las casas
        else: number_houses_Xaxis = 4

        #Se itera en el rango del numero de casas a poner en el eje x
        for j in range(number_houses_Xaxis):

            #Se crea una variable r que contendra un numero aleatorio entre 1 y 3 para elegir el
            #el tipo de casa
            r = random.randint(1,3)

            #Definimos como c a la distancia extra que debe trasladarse las casas por las calles
            c = (i//2)*0.5

            #Si estamos poniendo las casas de una fila en x par, entonces la orientacion es la original
            if i%2 == 0: orientation = 0
            #Si estamos poniendo una casa en una fila en x impar, entonces la casa debe orientarse en el
            #sentido opuesto
            else: orientation = (np.pi)

            #Se define la variable casa como el tipo de casa que corresponda segun el numero r
            if r == 1: casa = houseT1
            elif r == 2: casa = houseT2
            elif r == 3: casa = houseT3

            #Se crea el nodo houseF que contiene la casa segun el tipo elegido, y en la posicion que
            #corresponda segun el i,j. Luego se agrega esta al nodo de casas en posicion
            houseF = sg.SceneGraphNode('house('+str(i)+','+str(j)+')')
            houseF.transform = tr.matmul([tr.translate(j, i + c, 0),tr.translate(1, 1, 0),
                                            tr.rotationZ(orientation)])
            houseF.childs += [casa]
            houses_in_position.childs += [houseF]

    #Se crea el nodo que contendra el cartel y se traslada a su posicion en el cesped
    cartelNode = sg.SceneGraphNode('cartelNode')
    cartelNode.transform = tr.translate(6.4,6.4,0)
    cartelNode.childs += [cartel]

    #Se crea el nodo que contendra a los postes de luz en sus posiciones correspondientes
    lamppost_in_position = sg.SceneGraphNode('houses_in_pos')

    #Seteamos los postes en sus posiciones
    #Ponemos 2 faros por cada eje paralelo al x
    for j in range(2):

        #Determinamos la rotacion respecto a que punto de x esta
        if j == 0: rot = 3*np.pi/4
        else: rot = -3*np.pi/4
        
        #Ponemos 3 faros por eje para lelo al eje y
        for i in range(3):

            #Determinamos un ajuste hecho para el poste del pasto triangular
            if j == 1 and i == 2: ajust = -0.5
            else: ajust = 0

            #Se crea el nodo post que contiene un poste de tipo 2, y en la posicion que
            #corresponda segun el i,j. Luego se agrega este al nodo de postes de luz en posicion
            post = sg.SceneGraphNode('post(' +str(j)+','+str(i)+ ')')
            post.transform = tr.matmul([tr.translate(0.5 + j * (8 + ajust), 0.5 + 2.5 * i, 0),
                                        tr.rotationZ(rot)])
            post.childs += [lamppostT2]
            lamppost_in_position.childs += [post]

    #Se crean nodos con los postes y las transformaciones que los ponen en sus posiciones
    #Luego se agregan como nodos hijos de el nodo con los postes en sus posiciones
    post = sg.SceneGraphNode('post(2)')
    post.transform = tr.matmul([tr.translate(5.3,6.7,0), tr.rotationZ(-120*np.pi/180)])
    post.childs += [lamppostT1]
    lamppost_in_position.childs += [post]

    post = sg.SceneGraphNode('post(3)')
    post.transform = tr.matmul([tr.translate(7.2,5.6,0), tr.rotationZ(60*np.pi/180)])
    post.childs += [lamppostT1]
    lamppost_in_position.childs += [post]

    #Se crea un nodo con el semaforo y luego se posiciona
    trafficLightF = sg.SceneGraphNode('trafficLight')
    trafficLightF.childs += [trafficLight]
    trafficLight.transform = tr.translate(4.5, 2.51, 0)

    #Se agregan base, casas y el cartel en posicion a los hijos del nodo que contiene toda la escena
    scene.childs += [base]
    scene.childs += [houses_in_position]
    scene.childs += [cartelNode]
    scene.childs += [lamppost_in_position]
    scene.childs += [trafficLightF]

    #Se retorna al nodo que contiene toda la escena
    return scene
