import numpy as np

#Clase que guarda las propiedades de una luz puntual
class puntualLight:
    def __init__(self):
        self.La = np.array([0, 0, 0])
        self.Ld = np.array([0, 0, 0])
        self.Ls = np.array([0, 0, 0])
        self.Ka = np.array([0, 0, 0])
        self.Kd = np.array([0, 0, 0])
        self.Ks = np.array([0, 0, 0])
        self.position = np.array([0, 0, 0])
        self.shininess = np.array([0, 0, 0])
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032

#Clase que guarda las propiedades de una luz spotlight
class Spotlight:
    def __init__(self):
        self.ambient = np.array([0 ,0, 0])
        self.diffuse = np.array([0, 0, 0])
        self.specular = np.array([0, 0, 0])
        self.constant = 1.0
        self.linear = 0.09
        self.quadratic = 0.032
        self.position = np.array([0, 0, 0])
        self.direction = np.array([0, 0, 0])
        self.cutOff = 0
        self.outerCutOff = 0