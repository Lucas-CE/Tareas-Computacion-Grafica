import libs.constant as C
import numpy as np

#Creamos el controlador de las camaras
#Se dividen en IN, para la camara recorriendo el mapa, y OUT para la camara fuera del mapa
class camController:
    
    def __init__(self):

        #Define si la cama es la que mira desde arriba o la que recorre el lugar
        self.camOUT = True

        #Definimos un angulo desde donde mira la camara en la vista ortho
        self.ThetaAngle = np.pi/4
        self.AlphaAngle = -np.pi/4
        self.velAngleOut = np.pi/100

        #Definimos atributos para cuando la camara recorre el lugar
        self.pos = [0, -1.25, 1]
        self.vel = 0.05
        self.PhiAngle = np.pi
        self.BetaAngle = np.pi/2
        self.velAngleIN = np.pi/100

    #Se define la funcion move que mueve la camara IN en los factores x e y
    def move(self, x, y):

        if 4.5 > self.pos[0] + x > -4.5:
            self.pos[0] += x

        if 4 > self.pos[1] + y > -4:
            self.pos[1] += y

    #Se define la funcion change_beta que modifica el angulo beta segun la velocidad
    #definida en la clase como velAngleIN, con el signo entregado sign (+ o -)
    def change_beta(self, sign):

        if 0 < self.BetaAngle + sign * self.velAngleIN < np.pi*0.95:
            self.BetaAngle += sign * self.velAngleIN

    #Se define la funcion change_theta que modifica el angulo theta segun la velocidad
    #definida en la clase como velAngleIN, con el signo entregado sign (+ o -)
    def change_theta(self, sign):

        if 0 < self.ThetaAngle + sign * self.velAngleIN < np.pi*0.48:
            self.ThetaAngle += sign * self.velAngleIN


#Se define la clase del controlador de el sol y la luna
class SunMoonController:

    def __init__(self):

        #Se define la posicion inicial del sol en polares (la de la luna depende de la del sol)
        self.pos = [15,np.pi/2]

        #Se define la velocidad del sol segun cuanto queremos que se demore en tiempo real el sol
        #en dar una vuelta
        self.vel = [0, 2 * np.pi / C.SUN_PERIOD]

    #Funcion que cambia el angulo de la posicion
    def move(self,theta):
        self.pos[1] += theta

    #Funcion que actualiza el estado de la posicion segun un dt de tiempo
    def update(self,dt):
        self.move(dt*self.vel[1])

    #Funcion que devuelve una lista con las posiciones del sol y la luna en cartesianas
    def XYZpos(self):
        xSun = self.pos[0]*np.cos(self.pos[1])
        xMoon = self.pos[0]*np.cos(self.pos[1] + np.pi)
        zSun = self.pos[0]*np.sin(self.pos[1])
        zMoon = self.pos[0]*np.sin(self.pos[1] + np.pi)
        y = 0

        return [[xSun,y,zSun],[xMoon,y,zMoon]]


#Clase del controlador de las luces del auto
class carLights:

    def __init__(self):

        #Se define la posicion relativa al auto de las luces
        self.posL9 = [-0.05, -0.4, 0]
        self.posL10 = [0.05, -0.4, 0]

        #Se define la direccion hacia donde apuntan las luces
        self.directL9 = [0, 1, 0]
        self.directL10 = [0, 1, 0]

    #Funcion que cambia las posiciones de las luces
    def moveLights(self, newPosL9, newPosL10):

        self.posL9 = newPosL9
        self.posL10 = newPosL10

    #Funcion que cambia a la direccion de las luces
    def changeDirection(self, newDirec):

        self.directL9 = newDirec
        self.directL10 = newDirec


#Clase del controlador de la luz del semaforo
class controller_TrafficLight:

    def __init__(self):
        #Variable que maneja si la luz esta encendida
        self.greenON = 0

    #Funcion que cambia el estado de la luz
    def change_state(self):

        if self.greenON == 0: self.greenON = 1
    
        else: self.greenON = 0